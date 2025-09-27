from rest_framework import generics, permissions, status, filters as drf_filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Ticket, TicketComment
from .serializers import TicketSerializer, TicketCommentSerializer
from .permissions import IsTicketOwnerOrAdminOrAgent
from .filters import TicketFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from .tasks import send_escalation_email

User = get_user_model()

class TicketCreateView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = TicketFilter
    search_fields = ['title', 'description']

    def get_queryset(self):
        user = self.request.user
        qs = Ticket.objects.all()
        if user.role == 'ADMIN':
            return qs
        if user.role == 'AGENT':
            return qs.filter(assigned_to=user)
        return qs.filter(created_by=user)

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTicketOwnerOrAdminOrAgent]

    def perform_update(self, serializer):
        serializer.save()

class AssignTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        if user.role != 'ADMIN':
            return Response({'detail': 'Only admins can assign tickets.'}, status=status.HTTP_403_FORBIDDEN)
        ticket = get_object_or_404(Ticket, pk=pk)
        agent_id = request.data.get('agent_id')
        agent = get_object_or_404(User, pk=agent_id)
        if agent.role != 'AGENT':
            return Response({'detail': 'User is not an agent.'}, status=status.HTTP_400_BAD_REQUEST)
        ticket.assigned_to = agent
        ticket.save()
        return Response(TicketSerializer(ticket).data)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('pk')
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        # permission check
        if not (self.request.user.role == 'ADMIN' or ticket.created_by == self.request.user or (ticket.assigned_to and ticket.assigned_to == self.request.user)):
            raise permissions.PermissionDenied("You cannot comment on this ticket.")
        serializer.save(author=self.request.user, ticket=ticket)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def manual_escalate(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    # only admin or assigned agent or owner can escalate manually
    if not (request.user.role == 'ADMIN' or ticket.assigned_to == request.user or ticket.created_by == request.user):
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    ticket.status = Ticket.STATUS_ESCALATED
    ticket.save()
    send_escalation_email.delay(ticket.id)
    return Response({'detail': 'Ticket escalated'}, status=status.HTTP_200_OK)

class ReportingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response({'detail': 'Only admin can view reports.'}, status=403)
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        opened = Ticket.objects.filter(created_at__gte=week_ago).count()
        resolved = Ticket.objects.filter(status=Ticket.STATUS_RESOLVED, updated_at__gte=week_ago).count()
        escalated = Ticket.objects.filter(status=Ticket.STATUS_ESCALATED, updated_at__gte=week_ago).count()
        return Response({'opened_last_7_days': opened, 'resolved_last_7_days': resolved, 'escalated_last_7_days': escalated})
