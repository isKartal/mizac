# profiles/views.py - CACHE OPTİMİZE EDİLMİŞ VERSİYON

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.core.cache import cache  # ← YENİ: Cache import
from django.views.decorators.cache import cache_page  # ← YENİ: Cache decorator
import hashlib  # ← YENİ: Cache key için

from testing_algorithm.models import TestResult
from .models import RecommendedContent, UserContentInteraction, ContentCategory

@login_required
def profiles(request):
    """ Profil ana sayfasını gösterir - CACHE'Lİ """
    
    # Cache key (kullanıcıya özel)
    cache_key = f'user_profile_stats_{request.user.id}'
    cached_stats = cache.get(cache_key)
    
    if cached_stats:
        print(f"✅ Cache HIT: Profile stats - {request.user.username}")
        return render(request, 'profiles/profiles.html', cached_stats)
    
    print(f"❌ Cache MISS: Profile stats - {request.user.username}")
    
    # Etkileşim istatistiklerini hesapla (Optimized query)
    user_interactions = UserContentInteraction.objects.filter(user=request.user)
    
    viewed_count = user_interactions.filter(viewed=True).count()
    liked_count = user_interactions.filter(liked=True).count()
    saved_count = user_interactions.filter(saved=True).count()
    
    context = {
        'viewed_count': viewed_count,
        'liked_count': liked_count,
        'saved_count': saved_count
    }
    
    # Cache'e kaydet (10 dakika)
    cache.set(cache_key, context, 600)
    print(f"💾 Cache SET: Profile stats - {request.user.username}")
    
    return render(request, 'profiles/profiles.html', context)

@login_required
def my_temperament(request):
    """Kullanıcının mizaç sonucunu kontrol eder ve ilgili mizaç sayfasına yönlendirir - CACHE'Lİ"""
    
    # Cache key
    cache_key = f'user_temperament_{request.user.id}'
    cached_result = cache.get(cache_key)
    
    if cached_result:
        print(f"✅ Cache HIT: Temperament redirect - {request.user.username}")
        return redirect(cached_result)
    
    print(f"❌ Cache MISS: Temperament redirect - {request.user.username}")
    
    # Optimized query
    test_result = TestResult.objects.select_related('dominant_element').filter(
        user=request.user
    ).order_by('-date_taken').first()
    
    if test_result:
        # Element bilgisini al
        dominant_element = test_result.dominant_element
        
        # Element adına göre uygun mizaç sayfasına yönlendir
        redirect_url = None
        if dominant_element.name == "Ateş":
            redirect_url = 'fire_more'
        elif dominant_element.name == "Hava":
            redirect_url = 'air_more'
        elif dominant_element.name == "Su":
            redirect_url = 'water_more'
        elif dominant_element.name == "Toprak":
            redirect_url = 'earth_more'
        else:
            redirect_url = 'temperaments'
        
        # Cache'e kaydet (30 dakika - test sonucu değişmez genelde)
        cache.set(cache_key, redirect_url, 1800)
        print(f"💾 Cache SET: Temperament redirect - {redirect_url}")
        
        return redirect(redirect_url)
    else:
        # Eğer test sonucu yoksa, kullanıcıya bilgi mesajı göster ve test sayfasına yönlendir
        messages.info(request, "Mizaç sonucunuzu görmek için önce mizaç testini çözmelisiniz.")
        return redirect('test_list')

@login_required
def my_suggestions(request):
    """ Kullanıcıya önerilen içerikleri görüntüler - CACHE'Lİ VERSİYON """
    
    # Debug bilgisi ekle
    print("Session bilgileri:", dict(request.session))
    print("test_completed session var mı:", 'test_completed' in request.session)
    
    # Cache key (kullanıcıya özel)
    cache_key = f'user_suggestions_{request.user.id}'
    cached_data = cache.get(cache_key)
    
    if cached_data and 'test_completed' not in request.session:
        print(f"✅ Cache HIT: User suggestions - {request.user.username}")
        return render(request, 'profiles/my_suggestions.html', cached_data)
    
    print(f"❌ Cache MISS: User suggestions - {request.user.username}")
    
    # Kullanıcının test sonucunu al (Optimized query)
    test_result = TestResult.objects.select_related('dominant_element').filter(
        user=request.user
    ).order_by('-date_taken').first()
    
    # Eğer kullanıcı henüz testi çözmemişse test sayfasına yönlendir
    if not test_result:
        messages.warning(request, "Önerileri görmek için önce mizaç testini çözmelisiniz.")
        return redirect('test_list')
    
    # Test sonucundan dominant element ismini al
    dominant_element_name = test_result.dominant_element.name
    element_characteristics = test_result.dominant_element.characteristics
    
    # Kullanıcının etkileşimlerini önceden sorgula (Optimized)
    user_interactions = UserContentInteraction.objects.filter(
        user=request.user
    ).select_related('content')
    interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
    
    # SADECE kullanıcının baskın elementine göre içerik önerilerini al (Optimized query)
    recommended_contents = RecommendedContent.objects.select_related('category').filter(
        is_active=True, 
        related_element_name=dominant_element_name
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')
    
    # İçerikler için etkileşim bilgilerini hazırla
    for content in recommended_contents:
        # Etkileşim bilgisini geçici bir özellik olarak ekle
        if content.id in interactions_dict:
            interaction = interactions_dict[content.id]
            content.is_liked = interaction.liked
            content.is_saved = interaction.saved
            content.is_viewed = interaction.viewed
        else:
            # Etkileşim yoksa, varsayılan değerleri ayarla
            content.is_liked = False
            content.is_saved = False
            content.is_viewed = False
            
            # Yeni etkileşim oluştur ve kaydet
            interaction = UserContentInteraction(
                user=request.user,
                content=content,
                liked=False,
                saved=False,
                viewed=False
            )
            interaction.save()
            interactions_dict[content.id] = interaction
    
    # Kategorileri cache'den al
    categories_cache_key = 'content_categories_all'
    categories = cache.get(categories_cache_key)
    
    if not categories:
        categories = list(ContentCategory.objects.all())
        cache.set(categories_cache_key, categories, 3600)  # 1 saat cache
        print("💾 Cache SET: Content categories")
    
    # Yeni eklenen bilgiler
    recently_completed_test = False
    if 'test_completed' in request.session:
        recently_completed_test = True
        print("Test tamamlandı bayrağı bulundu, kaldırılıyor")
        del request.session['test_completed']
        request.session.modified = True
    
    context = {
        'contents': list(recommended_contents),  # QuerySet'i listeye çevir
        'categories': categories,
        'dominant_element': dominant_element_name,
        'element_characteristics': element_characteristics,
        'recently_completed_test': recently_completed_test,
    }
    
    # Cache'e kaydet (5 dakika - kullanıcı etkileşimleri değişebilir)
    if not recently_completed_test:  # Yeni test tamamlanmadıysa cache'le
        cache.set(cache_key, context, 300)
        print(f"💾 Cache SET: User suggestions - {request.user.username}")
    
    return render(request, 'profiles/my_suggestions.html', context)

@login_required
def api_all_contents(request):
    """Tüm mizaç tipleri için öneri içeriklerini dönen API - CACHE'Lİ"""
    
    # Cache key (kullanıcıya özel)
    cache_key = f'api_all_contents_{request.user.id}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print(f"✅ Cache HIT: API all contents - {request.user.username}")
        return JsonResponse(cached_data)
    
    print(f"❌ Cache MISS: API all contents - {request.user.username}")
    
    # Kullanıcının etkileşimlerini al (Optimized)
    user_interactions = UserContentInteraction.objects.filter(
        user=request.user
    ).select_related('content')
    interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
    
    # Tüm aktif içerikleri al (Optimized query)
    all_contents = RecommendedContent.objects.select_related('category').filter(
        is_active=True
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')
    
    # İçerik listesini hazırla
    contents_list = []
    
    for content in all_contents:
        # Etkileşim bilgisini sözlükten al veya varsayılanları kullan
        if content.id in interactions_dict:
            interaction = interactions_dict[content.id]
            is_liked = interaction.liked
            is_saved = interaction.saved
            is_viewed = interaction.viewed
        else:
            is_liked = False
            is_saved = False
            is_viewed = False
            
            # Yeni etkileşim oluştur ve kaydet
            interaction = UserContentInteraction(
                user=request.user,
                content=content,
                liked=False,
                saved=False,
                viewed=False
            )
            interaction.save()
        
        # İçerik bilgilerini sözlüğe çevir
        content_dict = {
            'id': content.id,
            'title': content.title,
            'short_description': content.short_description,
            'image': content.image.url if content.image else None,
            'category_id': content.category.id,
            'category_name': content.category.name,
            'related_element_name': content.related_element_name,
            'like_count': content.like_count,
            'order': content.order,
            'created_at': content.created_at.isoformat(),
            'is_liked': is_liked,
            'is_saved': is_saved,
            'is_viewed': is_viewed,
        }
        
        contents_list.append(content_dict)
    
    # Response data
    response_data = {'contents': contents_list}
    
    # Cache'e kaydet (3 dakika - API için kısa cache)
    cache.set(cache_key, response_data, 180)
    print(f"💾 Cache SET: API all contents - {request.user.username}")
    
    return JsonResponse(response_data)

@login_required
def api_saved_contents(request):
    """Kullanıcının kaydedilmiş içeriklerini dönen API - CACHE'Lİ"""
    
    # Cache key
    cache_key = f'api_saved_contents_{request.user.id}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print(f"✅ Cache HIT: API saved contents - {request.user.username}")
        return JsonResponse(cached_data)
    
    print(f"❌ Cache MISS: API saved contents - {request.user.username}")
    
    # Kullanıcının kaydedilmiş içeriklerini al (Optimized query)
    saved_interactions = UserContentInteraction.objects.filter(
        user=request.user,
        saved=True,
        content__is_active=True
    ).select_related('content', 'content__category').annotate(
        like_count=Count('content__user_interactions', filter=Q(content__user_interactions__liked=True))
    ).order_by('-id')
    
    # İçerik listesini hazırla
    contents_list = []
    
    for interaction in saved_interactions:
        content = interaction.content
        
        # İçerik bilgilerini sözlüğe çevir
        content_dict = {
            'id': content.id,
            'title': content.title,
            'short_description': content.short_description,
            'image': content.image.url if content.image else None,
            'category_name': content.category.name,
            'category_id': content.category.id,
            'related_element_name': content.related_element_name,
            'like_count': interaction.like_count,
            'order': content.order,
            'created_at': content.created_at.isoformat(),
            'is_liked': interaction.liked,
            'is_saved': True,
            'is_viewed': interaction.viewed,
        }
        
        contents_list.append(content_dict)
    
    # Response data
    response_data = {
        'success': True,
        'contents': contents_list,
        'count': len(contents_list)
    }
    
    # Cache'e kaydet (2 dakika - saved content sık değişebilir)
    cache.set(cache_key, response_data, 120)
    print(f"💾 Cache SET: API saved contents - {request.user.username}")
    
    return JsonResponse(response_data)

def content_detail(request, content_id):
    """ İçerik detaylarını AJAX ile dönen view - CACHE'Lİ """
    
    # Cache key (kullanıcıya özel)
    if request.user.is_authenticated:
        cache_key = f'content_detail_{content_id}_{request.user.id}'
    else:
        cache_key = f'content_detail_{content_id}_anonymous'
    
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print(f"✅ Cache HIT: Content detail - {content_id}")
        return JsonResponse(cached_data)
    
    print(f"❌ Cache MISS: Content detail - {content_id}")
    
    content = get_object_or_404(RecommendedContent, id=content_id, is_active=True)
    
    # Kullanıcı giriş yapmışsa etkileşim bilgilerini güncelle
    if request.user.is_authenticated:
        interaction, created = UserContentInteraction.objects.get_or_create(
            user=request.user,
            content=content
        )
        
        if not interaction.viewed:
            interaction.viewed = True
            interaction.viewed_at = timezone.now()
            interaction.save()
            
            # Viewed durumu değiştiğinde cache'i temizle
            cache.delete(f'user_suggestions_{request.user.id}')
            cache.delete(f'api_all_contents_{request.user.id}')
        
        # Beğeni sayısını hesapla
        like_count = UserContentInteraction.objects.filter(content=content, liked=True).count()
        
        # JSON formatında içerik detaylarını döndür
        data = {
            'id': content.id,
            'title': content.title,
            'content': content.content,
            'image': content.image.url if content.image else None,
            'category': content.category.name,
            'category_id': content.category.id,
            'related_element': content.related_element_name,
            'like_count': like_count,
            'liked': interaction.liked,
            'saved': interaction.saved,
        }
        
        # Cache'e kaydet (10 dakika - content detail sık değişmez)
        cache.set(cache_key, data, 600)
        
    else:
        # Giriş yapmayan kullanıcılar için
        like_count = UserContentInteraction.objects.filter(content=content, liked=True).count()
        
        data = {
            'id': content.id,
            'title': content.title,
            'content': content.content,
            'image': content.image.url if content.image else None,
            'category': content.category.name,
            'category_id': content.category.id,
            'related_element': content.related_element_name,
            'like_count': like_count,
            'liked': False,
            'saved': False,
        }
        
        # Anonymous için uzun cache (30 dakika)
        cache.set(cache_key, data, 1800)
    
    print(f"💾 Cache SET: Content detail - {content_id}")
    return JsonResponse(data)

@login_required
def toggle_like_content(request, content_id):
    """ İçeriği beğenme/beğenmeme durumunu değiştiren view - CACHE TEMİZLEME """
    if request.method == 'POST':
        content = get_object_or_404(RecommendedContent, id=content_id, is_active=True)
        interaction, created = UserContentInteraction.objects.get_or_create(
            user=request.user,
            content=content
        )
        
        # Beğenme durumunu değiştir
        interaction.liked = not interaction.liked
        interaction.save()
        
        # İlgili cache'leri temizle
        cache.delete(f'user_suggestions_{request.user.id}')
        cache.delete(f'api_all_contents_{request.user.id}')
        cache.delete(f'api_saved_contents_{request.user.id}')
        cache.delete(f'content_detail_{content_id}_{request.user.id}')
        cache.delete(f'user_profile_stats_{request.user.id}')
        print(f"🗑️ Cache CLEARED: Like toggled for content {content_id}")
        
        # Beğeni sayısını hesapla
        like_count = UserContentInteraction.objects.filter(content=content, liked=True).count()
        
        return JsonResponse({
            'success': True, 
            'liked': interaction.liked,
            'like_count': like_count
        })
    
    return JsonResponse({'success': False}, status=400)

@login_required
def toggle_save_content(request, content_id):
    """ İçeriği kaydetme/kaydetmeme durumunu değiştiren view - CACHE TEMİZLEME """
    if request.method == 'POST':
        content = get_object_or_404(RecommendedContent, id=content_id, is_active=True)
        interaction, created = UserContentInteraction.objects.get_or_create(
            user=request.user,
            content=content
        )
        
        # Kaydetme durumunu değiştir
        interaction.saved = not interaction.saved
        interaction.save()
        
        # İlgili cache'leri temizle
        cache.delete(f'user_suggestions_{request.user.id}')
        cache.delete(f'api_all_contents_{request.user.id}')
        cache.delete(f'api_saved_contents_{request.user.id}')
        cache.delete(f'content_detail_{content_id}_{request.user.id}')
        cache.delete(f'user_profile_stats_{request.user.id}')
        print(f"🗑️ Cache CLEARED: Save toggled for content {content_id}")
        
        return JsonResponse({'success': True, 'saved': interaction.saved})
    
    return JsonResponse({'success': False}, status=400)

@login_required
def restart_test(request):
    """Kullanıcının test sonuçlarını siler ve test listesi sayfasına yönlendirir - CACHE TEMİZLEME"""
    # Kullanıcının tüm test sonuçlarını sil
    TestResult.objects.filter(user=request.user).delete()
    
    # Test oturumundaki verileri temizle
    for key in ['test_phase', 'warm_score', 'cold_score', 'moist_score', 'dry_score', 'test_answers']:
        if key in request.session:
            del request.session[key]
    
    # Kullanıcının tüm cache'lerini temizle
    cache_keys_to_delete = [
        f'user_suggestions_{request.user.id}',
        f'user_temperament_{request.user.id}',
        f'user_profile_stats_{request.user.id}',
        f'api_all_contents_{request.user.id}',
        f'api_saved_contents_{request.user.id}',
    ]
    
    for cache_key in cache_keys_to_delete:
        cache.delete(cache_key)
    
    print(f"🗑️ Cache CLEARED: Test restart for user {request.user.username}")
    
    # Başarılı mesajı ekle
    messages.success(request, "Test sonuçlarınız silindi. Şimdi testi yeniden çözebilirsiniz.")
    
    # Test listesi sayfasına yönlendir
    return redirect('test_list')