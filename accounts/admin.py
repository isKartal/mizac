from django.contrib import admin
from .models import SocialAccount

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'email', 'created_at')
    list_filter = ('provider', 'created_at')
    search_fields = ('user__username', 'email', 'uid')
    readonly_fields = ('created_at', 'updated_at')