from django.db import models

class PDF(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to='pdfs/')  # Saves PDF in the 'pdfs/' directory

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)  # Correct field name is 'phone', not 'phone_no'
    first_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
