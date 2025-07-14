from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from testing_algorithm.models import TestResult
from profiles.models import RecommendedContent, UserContentInteraction
from django.db.models import Count, Q

def index(request):
    context = {}
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucunu da gönderelim
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Test sonucundan kullanıcının elementini al
            dominant_element_name = test_result.dominant_element  # String olarak al
            
            # Kullanıcının mizacına uygun önerileri getir (sınırsız - [:3] kaldırıldı)
            user_suggestions = RecommendedContent.objects.filter(
                related_element_name=dominant_element_name,  # String kullan
                is_active=True
            ).annotate(
                like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
            ).order_by('order', '-created_at')
            
            # Kullanıcının etkileşimlerini al
            user_interactions = UserContentInteraction.objects.filter(user=request.user)
            interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
            
            # İçerikler için etkileşim bilgilerini hazırla
            for content in user_suggestions:
                if content.id in interactions_dict:
                    interaction = interactions_dict[content.id]
                    content.is_liked = interaction.liked
                    content.is_saved = interaction.saved
                    content.is_viewed = interaction.viewed
                else:
                    content.is_liked = False
                    content.is_saved = False
                    content.is_viewed = False
                    
                    # Yeni etkileşim oluştur
                    UserContentInteraction.objects.create(
                        user=request.user,
                        content=content,
                        liked=False,
                        saved=False,
                        viewed=False
                    )
            
            # Template'in beklediği yapıda gönder
            context = {
                'user_element': {
                    'name': dominant_element_name,      # Template: {{ user_element.name }}
                    'contents': user_suggestions,       # Template: {{ user_element.contents }}
                },
                'has_test_result': True
            }
            
            # Debug için
            print(f"DEBUG - Element: {dominant_element_name}")
            print(f"DEBUG - İçerik sayısı: {user_suggestions.count()}")
            
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
    
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')

from django.http import JsonResponse

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f"Yeni Mesaj: {name}"
        message_body = f"Mesaj: {message}\nGönderen: {email}"
        send_mail(subject, message_body, settings.EMAIL_HOST_USER, ['4mizacinfo@gmail.com'])
        return JsonResponse({'success': 'Mesajınız başarıyla gönderilmiştir.'})
    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)

def temperament(request):
    return render(request, 'main/temperament.html')

def privacypolicy(request):
    return render(request, 'main/privacypolicy.html')