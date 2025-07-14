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
            user_element = test_result.dominant_element
            
            # Kullanıcının mizacına uygun önerileri getir (maksimum 3 tane)
            # İşlem yapılırken beğeni sayısına göre en popüler içerikler ilk 3'te olacak
            user_suggestions = RecommendedContent.objects.filter(
                related_element_name=user_element.name,
                is_active=True
            ).annotate(
                like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
            ).order_by('order', '-created_at')[:3]
            
            # Kullanıcının etkileşimlerini al
            user_interactions = UserContentInteraction.objects.filter(user=request.user)
            interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
            
            # İçerikler için etkileşim bilgilerini hazırla
            for content in user_suggestions:
                if content.id in interactions_dict:
                    # Kullanıcının bu içerikle etkileşimi varsa, özelliklerini kopyalayalım
                    interaction = interactions_dict[content.id]
                    content.is_liked = interaction.liked
                    content.is_saved = interaction.saved
                    content.is_viewed = interaction.viewed
                else:
                    # Etkileşim yoksa, varsayılan değerleri ayarla
                    content.is_liked = False
                    content.is_saved = False
                    content.is_viewed = False
            
            context = {
                'user_element': user_element,
                'user_suggestions': user_suggestions,
                'has_test_result': True
            }
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