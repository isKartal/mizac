from django.db import models
from django.contrib.auth.models import User

class SocialAccount(models.Model):
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        # İleride başka provider'lar eklenebilir
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    uid = models.CharField(max_length=255, help_text="Provider'dan gelen unique ID")
    email = models.EmailField()
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('provider', 'uid')
        verbose_name = 'Sosyal Hesap'
        verbose_name_plural = 'Sosyal Hesaplar'
    
    def __str__(self):
        return f"{self.user.username} - {self.provider}"