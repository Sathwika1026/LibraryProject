from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    USER_STUDENT = 'student'
    USER_FACULTY = 'faculty'
    USER_ADMIN = 'admin'

    USER_TYPES = [
        (USER_STUDENT, 'Student'),
        (USER_FACULTY, 'Faculty'),
        (USER_ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
