from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from testing_algorithm.models import TestResult
from profiles.models import RecommendedContent, UserContentInteraction
from django.db.models import Count, Q
import urllib.parse
import requests
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User

def google_login(request):
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)
def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Kod alınamadı.", status=400)

    # Token almak için istek
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return HttpResponse("Access token alınamadı.", status=400)

    # Kullanıcı bilgilerini al
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        return HttpResponse("Kullanıcı bilgileri alınamadı.", status=400)

    # Kullanıcıyı oluştur veya getir
    user, created = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": name})
    login(request, user)

    return redirect("index")  # anasayfaya yönlendir, URL ismi değişebilir
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