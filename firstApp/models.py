from django.db import models

class UserInfo(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} ({self.email})"

from django.db import models

class ChatMessage(models.Model):
    message = models.TextField()
    reply = models.TextField()
    received_time = models.DateTimeField()
    reply_time = models.DateTimeField()
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE, default=1)  # Set default value here (e.g., default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message: {self.message[:50]}... | Received: {self.received_time}"



