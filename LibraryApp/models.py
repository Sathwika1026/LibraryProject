from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    category = models.CharField(max_length=100)  # NEW
    author = models.CharField(max_length=255)
    copies = models.PositiveIntegerField(default=1)  # NEW
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_available(self):
        return self.copies > 0

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"