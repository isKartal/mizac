# profiles/utils.py
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class WebPConverter:
    """WebP dönüştürme ve optimizasyon sınıfı"""
    
    @staticmethod
    def convert_to_webp(image_field, quality=85, max_width=1500, max_height=750):
        """
        Yüklenen görseli WebP formatına dönüştürür
        
        Args:
            image_field: Django ImageField
            quality: WebP kalitesi (0-100)
            max_width: Maksimum genişlik
            max_height: Maksimum yükseklik
        
        Returns:
            WebP formatında InMemoryUploadedFile
        """
        try:
            # Görseli aç
            image = Image.open(image_field)
            
            # EXIF verilerini koru ve döndür
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
    
    @staticmethod
    def create_responsive_versions(image_field, base_name):
        """
        Farklı cihazlar için çoklu boyut oluşturur
        
        Returns:
            dict: {'desktop': file, 'tablet': file, 'mobile': file}
        """
        sizes = {
            'desktop': (1500, 750),
            'tablet': (1200, 600),
            'mobile': (800, 400),
            'thumbnail': (400, 200)
        }
        
        responsive_images = {}
        
        for size_name, (width, height) in sizes.items():
            try:
                webp_file = WebPConverter.convert_to_webp(
                    image_field, 
                    quality=85 if size_name == 'desktop' else 80,
                    max_width=width, 
                    max_height=height
                )
                responsive_images[size_name] = webp_file
            except Exception as e:
                print(f"{size_name} boyutu oluşturulamadı: {e}")
                
        return responsive_images

def optimize_existing_images():
    """
    Mevcut PNG dosyalarını WebP'ye dönüştürme scripti
    """
    from .models import RecommendedContent
    
    contents = RecommendedContent.objects.filter(image__isnull=False)
    converted_count = 0
    
    for content in contents:
        if content.image and content.image.name.endswith(('.webp', '.webp', '.jpeg')):
            try:
                # WebP'ye dönüştür
                webp_file = WebPConverter.convert_to_webp(content.image)
                
                # Yeni dosyayı kaydet
                content.image.save(
                    webp_file.name,
                    webp_file,
                    save=True
                )
                
                converted_count += 1
                print(f"✅ Dönüştürüldü: {content.title}")
                
            except Exception as e:
                print(f"❌ Hata: {content.title} - {e}")
    
    print(f"\n🎉 Toplam {converted_count} görsel WebP'ye dönüştürüldü!")