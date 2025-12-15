from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

# 2. Model Skripsi/Tugas Akhir
class Skripsi(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Menunggu Persetujuan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    )

    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='skripsi_student')
    lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='skripsi_lecturer')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.judul} - {self.student.username}"

# 3. Model ChatMessage (HARUS DI LUAR Class Skripsi)
class ChatMessage(models.Model):
    # Perhatikan huruf 'S' besar pada 'Skripsi' di bawah ini
    skripsi = models.ForeignKey(Skripsi, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"