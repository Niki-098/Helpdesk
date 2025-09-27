from celery import shared_task
from django.utils.timezone import now
from .models import Ticket
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_escalation_email(ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        return

    subject = f"Ticket {ticket.id} escalated: {ticket.title}"
    message = f"Ticket {ticket.id} has been escalated.\nTitle: {ticket.title}\nStatus: {ticket.status}\nPriority: {ticket.priority}\n"
    recipients = list(User.objects.filter(role='ADMIN').values_list('email', flat=True))
    if ticket.created_by and ticket.created_by.email:
        recipients.append(ticket.created_by.email)
    recipients = [r for r in recipients if r]
    if recipients:
        send_mail(subject, message, None, recipients)

@shared_task
def check_ticket_escalations():
    # thresholds in hours
    thresholds = {'HIGH': 1, 'MEDIUM': 4, 'LOW': 24}
    now_time = now()
    tickets = Ticket.objects.filter(status__in=[Ticket.STATUS_OPEN, Ticket.STATUS_IN_PROGRESS])
    for t in tickets:
        elapsed_hours = (now_time - t.created_at).total_seconds() / 3600.0
        if thresholds.get(t.priority, 24) <= elapsed_hours:
            t.status = Ticket.STATUS_ESCALATED
            t.save()
            send_escalation_email.delay(t.id)
