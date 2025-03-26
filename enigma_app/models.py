from django.db import models

# Create your models here.


class EncryptionHistory(models.Model):
    message = models.TextField()
    encrypted_message = models.TextField()
    rotor_settings = models.JSONField()
    plugboard_settings = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encrypted at {self.timestamp}"
