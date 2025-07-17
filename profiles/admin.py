# profiles/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.forms import Select
from .models import ContentCategory, RecommendedContent, UserContentInteraction


@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(RecommendedContent)
class RecommendedContentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'category', 
        'related_element_name',
        'image_preview',  # Görsel önizleme
        'image_info',     # Format ve boyut bilgisi
        'optimization_status',  # Optimizasyon durumu
        'is_active',
        'show_on_temperament_page',
        'order',
        'created_at'
    )
    
    list_filter = (
        'is_active', 
        'show_on_temperament_page',
        'category', 
        'related_element_name',
        'created_at'
    )
    
    search_fields = ('title', 'short_description', 'content')
    
    list_editable = (
        'is_active', 
        'show_on_temperament_page',
        'order'
    )
    
    date_hierarchy = 'created_at'
    ordering = ['related_element_name', 'order', '-created_at']
    
    readonly_fields = (
        'image_preview', 
        'image_info', 
        'optimization_status',
        'created_at', 
        'updated_at'
    )
    
    # Mizaç elementi için sabit değerler
    ELEMENT_CHOICES = [
        ('Ateş', 'Ateş'),
        ('Hava', 'Hava'), 
        ('Su', 'Su'),
        ('Toprak', 'Toprak'),
    ]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'short_description', 'content', 'image')
        }),
        ('Kategorizasyon', {
            'fields': ('category', 'related_element_name')
        }),
        ('Görüntüleme Ayarları', {
            'fields': ('is_active', 'show_on_temperament_page', 'order')
        }),
        ('Görsel Bilgileri', {
            'fields': ('image_preview', 'image_info', 'optimization_status'),
            'classes': ('collapse',)
        }),
        ('Tarih Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """Mizaç elementi için açılır liste göster"""
        if db_field.name == 'related_element_name':
            from django import forms
            form_field = forms.CharField(
                help_text='Aşağıdaki değerlerden birini seçin: Ateş, Hava, Su, Toprak',
                widget=Select(choices=self.ELEMENT_CHOICES)
            )
            return form_field
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def image_preview(self, obj):
        """Admin panelde görsel önizleme"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 120px; max-width: 180px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999; font-style: italic;">Görsel yok</span>')
    image_preview.short_description = "Önizleme"
    
    def image_info(self, obj):
        """Görsel format ve boyut bilgisi"""
        if obj.image:
            format_info = obj.get_image_format()
            size_info = obj.get_file_size()
            
            if format_info == 'WEBP':
                format_badge = f'<span style="background: #4CAF50; color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; font-weight: bold;">✅ {format_info}</span>'
            else:
                format_badge = f'<span style="background: #FF9800; color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; font-weight: bold;">⚠️ {format_info}</span>'
            
            size_badge = f'<span style="background: #2196F3; color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; margin-left: 4px;">{size_info}</span>'
            
            return format_html(f'{format_badge}{size_badge}')
        return format_html('<span style="color: #999;">-</span>')
    image_info.short_description = "Format & Boyut"
    
    def optimization_status(self, obj):
        """Optimizasyon durumu"""
        if obj.image:
            if obj.is_webp():
                return format_html(
                    '<span style="color: #4CAF50; font-weight: bold;">🚀 Optimize Edilmiş</span><br>'
                    '<small style="color: #666;">WebP formatında, hızlı yükleme</small>'
                )
            else:
                return format_html(
                    '<span style="color: #FF5722; font-weight: bold;">⚡ Optimize Edilebilir</span><br>'
                    '<small style="color: #666;">WebP\'ye dönüştürülebilir</small>'
                )
        return format_html('<span style="color: #999;">Görsel yok</span>')
    optimization_status.short_description = "Optimizasyon"
    
    def get_queryset(self, request):
        """Performans için select_related kullan"""
        return super().get_queryset(request).select_related('category')
    
    # Admin panele özel actions
    actions = ['mark_as_active', 'mark_as_inactive', 'add_to_temperament_page']
    
    def mark_as_active(self, request, queryset):
        """Seçili içerikleri aktif yap"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} adet içerik aktif yapıldı.')
    mark_as_active.short_description = "Seçili içerikleri aktif yap"
    
    def mark_as_inactive(self, request, queryset):
        """Seçili içerikleri pasif yap"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} adet içerik pasif yapıldı.')
    mark_as_inactive.short_description = "Seçili içerikleri pasif yap"
    
    def add_to_temperament_page(self, request, queryset):
        """Seçili içerikleri mizaç sayfasına ekle"""
        updated = queryset.update(show_on_temperament_page=True)
        self.message_user(request, f'{updated} adet içerik mizaç sayfasına eklendi.')
    add_to_temperament_page.short_description = "Mizaç sayfasına ekle"


@admin.register(UserContentInteraction)
class UserContentInteractionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'content', 
        'viewed', 
        'liked', 
        'saved', 
        'viewed_at'
    )
    list_filter = ('viewed', 'liked', 'saved', 'viewed_at')
    search_fields = ('user__username', 'content__title')
    readonly_fields = ('viewed_at',)
    
    def get_queryset(self, request):
        """Performans için select_related kullan"""
        return super().get_queryset(request).select_related('user', 'content')