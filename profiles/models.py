# profiles/models.py
from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


class WebPConverter:
    """WebP dönüştürme sınıfı"""
    
    @staticmethod
    def convert_to_webp(image_field, quality=85, max_width=1500, max_height=750):
        """
        Yüklenen görseli WebP formatına dönüştürür
        """
        try:
            # Görseli aç
            image = Image.open(image_field)
            
            # EXIF verilerini kontrol et ve döndür
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif is not None:
                    for tag, value in exif.items():
                        if tag == 274:  # Orientation tag
                            if value == 3:
                                image = image.rotate(180, expand=True)
                            elif value == 6:
                                image = image.rotate(270, expand=True)
                            elif value == 8:
                                image = image.rotate(90, expand=True)
            
            # RGBA'yı RGB'ye çevir (WebP için gerekli)
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Boyutları optimize et
            original_width, original_height = image.size
            
            if original_width > max_width or original_height > max_height:
                # Oranı koru
                ratio = min(max_width/original_width, max_height/original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # WebP formatına çevir
            output = BytesIO()
            image.save(
                output,
                format='WebP',
                quality=quality,
                optimize=True,
                method=6  # En iyi sıkıştırma
            )
            output.seek(0)
            
            # Dosya adını değiştir
            original_name = image_field.name
            name_without_ext = os.path.splitext(original_name)[0]
            webp_name = f"{name_without_ext}.webp"
            
            # InMemoryUploadedFile oluştur
            webp_file = InMemoryUploadedFile(
                output,
                'ImageField',
                webp_name,
                'image/webp',
                output.tell(),
                None
            )
            
            return webp_file
            
        except Exception as e:
            print(f"WebP dönüşüm hatası: {e}")
            return image_field


class ContentCategory(models.Model):
    """İçerik kategorileri için model"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    
    class Meta:
        verbose_name = "İçerik Kategorisi"
        verbose_name_plural = "İçerik Kategorileri"
    
    def __str__(self):
        return self.name


class RecommendedContent(models.Model):
    """Önerilen içerikler için model"""
    ELEMENT_CHOICES = [
        ('Ateş', 'Ateş'),
        ('Hava', 'Hava'),
        ('Su', 'Su'),
        ('Toprak', 'Toprak'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Başlık")
    short_description = models.TextField(verbose_name="Kısa Açıklama")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(
        upload_to='content_images/', 
        blank=True, 
        null=True, 
        verbose_name="Görsel",
        help_text="PNG, JPG veya WebP formatında yükleyebilirsiniz. Otomatik olarak WebP'ye dönüştürülecek ve optimize edilecek."
    )
    category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE, related_name="contents", verbose_name="Kategori")
    related_element_name = models.CharField(
        max_length=50, 
        verbose_name="İlgili Mizaç Elementi", 
        choices=ELEMENT_CHOICES,
        help_text="Ateş, Hava, Su veya Toprak değerlerinden birini seçin"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    
    # YENİ ALAN - Mizaç sayfasında gösterim için
    show_on_temperament_page = models.BooleanField(
        default=False, 
        verbose_name="Mizaç Sayfasında Göster",
        help_text="Bu içerik ilgili mizaç detay sayfasında (örn: air_more.html) özel öneriler bölümünde gösterilsin mi? Her mizaç için en fazla 3 adet seçmeniz önerilir."
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Önerilen İçerik"
        verbose_name_plural = "Önerilen İçerikler"
        ordering = ['order', '-created_at']
    
    def save(self, *args, **kwargs):
        """Kaydetme sırasında görseli WebP'ye dönüştür ve optimize et"""
        
        # Eğer yeni bir görsel yükleniyorsa ve WebP değilse
        if self.image and hasattr(self.image, 'file'):
            # Dosya uzantısını kontrol et
            if hasattr(self.image, 'name') and self.image.name:
                file_extension = self.image.name.lower().split('.')[-1]
                
                # PNG, JPG, JPEG ise WebP'ye dönüştür
                if file_extension in ['png', 'jpg', 'jpeg']:
                    try:
                        print(f"🔄 WebP'ye dönüştürülüyor: {self.image.name}")
                        webp_file = WebPConverter.convert_to_webp(self.image)
                        self.image = webp_file
                        print(f"✅ WebP dönüşümü başarılı: {webp_file.name}")
                    except Exception as e:
                        print(f"❌ WebP dönüşüm hatası: {e}")
                        # Hata durumunda orijinal dosyayı koru
                        pass
        
        # Modeli kaydet
        super().save(*args, **kwargs)
    
    def get_image_url(self):
        """Görsel URL'sini güvenli şekilde döndür"""
        if self.image:
            return self.image.url
        return '/static/images/default-placeholder.webp'
    
    def get_image_format(self):
        """Görsel formatını döndür"""
        if self.image and self.image.name:
            return self.image.name.split('.')[-1].upper()
        return "N/A"
    
    def is_webp(self):
        """Görselin WebP formatında olup olmadığını kontrol et"""
        return self.get_image_format() == 'WEBP'
    
    def get_file_size(self):
        """Dosya boyutunu human-readable format'ta döndür"""
        if self.image:
            try:
                size = self.image.size
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        return f"{size:.1f} {unit}"
                    size /= 1024.0
                return f"{size:.1f} TB"
            except:
                return "Bilinmiyor"
        return "Görsel yok"
    
    def __str__(self):
        return self.title


class UserContentInteraction(models.Model):
    """Kullanıcı içerik etkileşimleri için model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="content_interactions", verbose_name="Kullanıcı")
    content = models.ForeignKey(RecommendedContent, on_delete=models.CASCADE, related_name="user_interactions", verbose_name="İçerik")
    viewed = models.BooleanField(default=False, verbose_name="Görüntülendi mi?")
    liked = models.BooleanField(default=False, verbose_name="Beğenildi mi?")
    saved = models.BooleanField(default=False, verbose_name="Kaydedildi mi?")
    viewed_at = models.DateTimeField(blank=True, null=True, verbose_name="Görüntülenme Tarihi")
    
    class Meta:
        verbose_name = "Kullanıcı İçerik Etkileşimi"
        verbose_name_plural = "Kullanıcı İçerik Etkileşimleri"
        unique_together = ['user', 'content']
    
    def __str__(self):
        return f"{self.user.username} - {self.content.title}"