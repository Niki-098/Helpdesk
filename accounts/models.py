from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_USER = 'USER'
    ROLE_AGENT = 'AGENT'
    ROLE_ADMIN = 'ADMIN'
    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_AGENT, 'Agent'),
        (ROLE_ADMIN, 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    def nameEmail(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
