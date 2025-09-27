from django.urls import path
from .views import (
    TicketCreateView, TicketListView, TicketDetailView,
    AssignTicketView, CommentCreateView, manual_escalate, ReportingView
)

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/assign/', AssignTicketView.as_view(), name='ticket-assign'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='ticket-comment'),
    path('<int:pk>/escalate/', manual_escalate, name='ticket-escalate'),
    path('reporting/', ReportingView.as_view(), name='ticket-reporting'),
]
