from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from .google_oauth import get_google_auth_flow, get_user_info
from django.contrib.auth.decorators import login_required

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu kullanıcı adı zaten kullanılıyor.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Bu e-posta adresi zaten kullanılıyor.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Kullanıcıyı authenticate ederek backend bilgisini ekliyoruz
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Hesabınız başarıyla oluşturuldu!")
                    return redirect('index')
                else:
                    messages.error(request, "Kullanıcı doğrulaması yapılamadı.")
        else:
            messages.error(request, "Şifreler uyuşmuyor.")
    
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Kullanıcı adı veya şifre yanlış.")

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

def google_login(request):
    """Google ile giriş başlatma"""
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    # State'i session'a kaydet (CSRF koruması için)
    request.session['oauth_state'] = state
    
    return redirect(authorization_url)


def google_callback(request):
    """Google OAuth callback"""
    # State kontrolü
    state = request.session.get('oauth_state')
    flow = get_google_auth_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    # Kullanıcı bilgilerini al
    try:
        credentials = flow.credentials
        user_info = get_user_info(credentials)
        
        # Google'dan gelen bilgiler
        email = user_info.get('email')
        google_uid = user_info.get('sub')  # Google unique user ID
        username = email.split('@')[0]  # Email'in @ öncesi kısmı
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        
        from .models import SocialAccount
        
        # Sosyal hesap kontrolü
        social_account = SocialAccount.objects.filter(provider='google', uid=google_uid).first()
        
        # Giriş yapmış kullanıcı varsa ve hesap bağlama modundaysa
        if request.user.is_authenticated:
            if social_account:
                if social_account.user == request.user:
                    messages.info(request, "Bu Google hesabı zaten profilinize bağlı.")
                else:
                    messages.error(request, "Bu Google hesabı başka bir kullanıcıya bağlı.")
            else:
                # Hesabı mevcut kullanıcıya bağla
                SocialAccount.objects.create(
                    user=request.user,
                    provider='google',
                    uid=google_uid,
                    email=email,
                    extra_data=user_info
                )
                messages.success(request, "Google hesabınız başarıyla bağlandı.")
            return redirect('social_accounts')
        
        # Normal giriş/kayıt akışı
        if social_account:
            # Daha önce bu sosyal hesapla giriş yapılmış
            user = social_account.user
            login(request, user)
            messages.success(request, f"Hoş geldiniz, {user.username}!")
        else:
            # İlk kez giriş yapılıyor, önce email kontrolü yap
            user = User.objects.filter(email=email).first()
            
            if user:
                # Bu email'e sahip kullanıcı var, sosyal hesabı bağla
                SocialAccount.objects.create(
                    user=user,
                    provider='google',
                    uid=google_uid,
                    email=email,
                    extra_data=user_info
                )
                login(request, user)
                messages.success(request, f"Google hesabınız mevcut profilinize bağlandı. Hoş geldiniz, {user.username}!")
            else:
                # Yeni kullanıcı oluştur
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_unusable_password()  # Google ile giriş yaptığı için şifre yok
                user.save()
                
                # Sosyal hesabı bağla
                SocialAccount.objects.create(
                    user=user,
                    provider='google',
                    uid=google_uid,
                    email=email,
                    extra_data=user_info
                )
                
                login(request, user)
                messages.success(request, f"Hesabınız Google ile başarıyla oluşturuldu. Hoş geldiniz, {username}!")
                messages.info(request, "İsterseniz daha sonra profil ayarlarından normal şifre de belirleyebilirsiniz.")
        
        # Test sonucu kontrolü
        from testing_algorithm.models import TestResult
        if TestResult.objects.filter(user=user).exists():
            return redirect('profiles')
        else:
            # Test sonucu yoksa test sayfasına yönlendir
            return redirect('test_list')
    
    except Exception as e:
        messages.error(request, f"Google ile giriş yapılırken hata oluştu: {str(e)}")
        return redirect('login')
    
@login_required
def social_accounts(request):
    """Kullanıcının sosyal hesaplarını yönetme sayfası"""
    from .models import SocialAccount
    social_accounts = SocialAccount.objects.filter(user=request.user)
    
    # Google hesabı bağlı mı kontrol et
    has_google = social_accounts.filter(provider='google').exists()
    
    return render(request, 'accounts/social_accounts.html', {
        'social_accounts': social_accounts,
        'has_google': has_google
    })

@login_required
def connect_google(request):
    """Mevcut hesaba Google bağlama"""
    # Google OAuth flow'u başlat ama connect modunda
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    # State'i session'a kaydet
    request.session['oauth_state'] = state
    request.session['connecting_social'] = True  # Bağlama modunda olduğumuzu işaretle
    
    return redirect(authorization_url)

@login_required
def disconnect_social(request, provider):
    """Sosyal hesap bağlantısını kaldır"""
    from .models import SocialAccount
    
    # Kullanıcının en az bir giriş yöntemi olmalı
    if not request.user.has_usable_password() and request.user.social_accounts.count() == 1:
        messages.error(request, "Son giriş yönteminizi kaldıramazsınız. Önce bir şifre belirleyin.")
        return redirect('social_accounts')
    
    try:
        social_account = SocialAccount.objects.get(user=request.user, provider=provider)
        social_account.delete()
        messages.success(request, f"{provider.title()} hesap bağlantınız kaldırıldı.")
    except SocialAccount.DoesNotExist:
        messages.error(request, "Bu hesap bulunamadı.")
    
    return redirect('social_accounts')

@login_required
def set_password(request):
    """Sosyal hesapla giriş yapmış kullanıcılar için şifre belirleme"""
    if request.user.has_usable_password():
        messages.info(request, "Zaten bir şifreniz var.")
        return redirect('social_accounts')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            request.user.set_password(password)
            request.user.save()
            # Şifre değiştiğinde oturumu güncelle
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            messages.success(request, "Şifreniz başarıyla belirlendi.")
            return redirect('social_accounts')
        else:
            messages.error(request, "Şifreler uyuşmuyor.")
    
    return render(request, 'accounts/set_password.html')