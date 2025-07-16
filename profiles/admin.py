# profiles/admin.py

from django.contrib import admin
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
        'is_active', 
        'show_on_temperament_page',  # Model alanını direkt kullan
        'order',
        'created_at'
    )
    list_filter = (
        'is_active', 
        'show_on_temperament_page',  # Model alanı
        'category', 
        'related_element_name'
    )
    search_fields = ('title', 'short_description', 'content')
    list_editable = (
        'is_active', 
        'show_on_temperament_page',  # Model alanı - hızlı düzenleme
        'order'
    )
    date_hierarchy = 'created_at'
    ordering = ['related_element_name', 'order', '-created_at']
    
    # Mizaç elementi için sabit değerler
    ELEMENT_CHOICES = [
        ('Ateş', 'Ateş'),
        ('Hava', 'Hava'), 
        ('Su', 'Su'),
        ('Toprak', 'Toprak'),
    ]
    
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
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'short_description', 'content', 'image')
        }),
        ('Kategorizasyon', {
            'fields': ('category', 'related_element_name')
        }),
        ('Görünürlük ve Sıralama Ayarları', {
            'fields': ('is_active', 'show_on_temperament_page', 'order'),
            'description': '''
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h4 style="color: #495057; margin-top: 0;">📋 Görünürlük Ayarları:</h4>
                <ul style="margin: 0; color: #6c757d;">
                    <li><strong>Aktif mi:</strong> İçeriğin sitede görünür olup olmadığını belirler</li>
                    <li><strong>Mizaç Sayfasında Göster:</strong> Bu içerik seçili mizaç detay sayfasında "Özel Öneriler" bölümünde gösterilir</li>
                    <li><strong>Sıralama:</strong> Küçük sayı = Önce gösterilir (0 = En üstte, 1 = İkinci sırada...)</li>
                </ul>
                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>💡 Önemli:</strong> Her mizaç için en fazla 3 içerik seçmeniz önerilir. 
                    Fazla seçildiğinde ilk 3'ü (sıralama değerine göre) gösterilir.
                </div>
            </div>
            '''
        }),
    )
    
    def get_queryset(self, request):
        """Admin listesinde daha iyi sıralama"""
        qs = super().get_queryset(request)
        return qs.order_by('related_element_name', 'show_on_temperament_page', 'order', '-created_at')

@admin.register(UserContentInteraction)
class UserContentInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'viewed', 'liked', 'saved', 'viewed_at')
    list_filter = ('viewed', 'liked', 'saved')
    search_fields = ('user__username', 'content__title')
    date_hierarchy = 'viewed_at'
    readonly_fields = ('viewed_at',)