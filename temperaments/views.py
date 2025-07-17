# temperaments/views.py - CACHE OPTİMİZE EDİLMİŞ VERSİYON

from django.shortcuts import render
from django.db.models import Count, Q
from django.core.cache import cache  # ← YENİ: Cache import
from django.views.decorators.cache import cache_page  # ← YENİ: Cache decorator

from profiles.models import RecommendedContent, UserContentInteraction
from testing_algorithm.models import TestResult

@cache_page(60 * 15)  # ← YENİ: 15 dakika cache (statik sayfa)
def temperaments(request):
    """Mizaçlar ana sayfası - CACHE'Lİ"""
    return render(request, 'temperaments/temperaments.html')

def air_more(request):
    """Hava mizacı detay sayfası - CACHE'Lİ VERSİYON"""
    
    # Anonymous kullanıcılar için cache
    if not request.user.is_authenticated:
        cache_key = 'air_more_anonymous'
        cached_data = cache.get(cache_key)
        if cached_data:
            print("✅ Cache HIT: Air page (anonymous)")
            return render(request, 'temperaments/air_more.html', cached_data)
    
    print(f"❌ Cache MISS: Air page - {request.user.username if request.user.is_authenticated else 'anonymous'}")
    
    # Element suggestions'ı cache'den al
    suggestions_cache_key = 'air_element_suggestions'
    element_suggestions = cache.get(suggestions_cache_key)
    
    if not element_suggestions:
        element_suggestions = RecommendedContent.objects.select_related('category').filter(
            related_element_name='Hava',
            is_active=True,
            show_on_temperament_page=True
        ).annotate(
            like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
        ).order_by('order', '-created_at')[:3]
        
        # Cache'e kaydet (10 dakika)
        cache.set(suggestions_cache_key, list(element_suggestions), 600)
        print("💾 Cache SET: Air element suggestions")
    else:
        print("✅ Cache HIT: Air element suggestions")
    
    # Kullanıcı etkileşimleri (cache'lenmez - kullanıcıya özel)
    if request.user.is_authenticated:
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        for content in element_suggestions:
            if content.id in interactions_dict:
                interaction = interactions_dict[content.id]
                content.is_liked = interaction.liked
                content.is_saved = interaction.saved
                content.is_viewed = interaction.viewed
            else:
                content.is_liked = False
                content.is_saved = False
                content.is_viewed = False
    
    context = {
        'element_name': 'Hava',
        'element_suggestions': element_suggestions,
    }
    
    # Test result kontrol (cache'li)
    if request.user.is_authenticated:
        test_cache_key = f'user_test_result_{request.user.id}'
        test_result = cache.get(test_cache_key)
        
        if test_result is None:
            test_result = TestResult.objects.select_related('dominant_element').filter(
                user=request.user
            ).order_by('-date_taken').first()
            # Cache'e kaydet (30 dakika)
            cache.set(test_cache_key, test_result, 1800)
            print(f"💾 Cache SET: User test result - {request.user.username}")
        else:
            print(f"✅ Cache HIT: User test result - {request.user.username}")
        
        if test_result:
            is_users_element = test_result.dominant_element.name == "Hava"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
    
    # Anonymous için cache'le
    if not request.user.is_authenticated:
        cache.set('air_more_anonymous', context, 900)  # 15 dakika
        print("💾 Cache SET: Air page (anonymous)")
    
    return render(request, 'temperaments/air_more.html', context)

def fire_more(request):
    """Ateş mizacı detay sayfası - CACHE'Lİ VERSİYON"""
    
    # Anonymous kullanıcılar için cache
    if not request.user.is_authenticated:
        cache_key = 'fire_more_anonymous'
        cached_data = cache.get(cache_key)
        if cached_data:
            print("✅ Cache HIT: Fire page (anonymous)")
            return render(request, 'temperaments/fire_more.html', cached_data)
    
    print(f"❌ Cache MISS: Fire page - {request.user.username if request.user.is_authenticated else 'anonymous'}")
    
    # Element suggestions'ı cache'den al
    suggestions_cache_key = 'fire_element_suggestions'
    element_suggestions = cache.get(suggestions_cache_key)
    
    if not element_suggestions:
        element_suggestions = RecommendedContent.objects.select_related('category').filter(
            related_element_name='Ateş',
            is_active=True,
            show_on_temperament_page=True
        ).annotate(
            like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
        ).order_by('order', '-created_at')[:3]
        
        # Cache'e kaydet (10 dakika)
        cache.set(suggestions_cache_key, list(element_suggestions), 600)
        print("💾 Cache SET: Fire element suggestions")
    else:
        print("✅ Cache HIT: Fire element suggestions")
    
    # Kullanıcı etkileşim bilgilerini ekle
    if request.user.is_authenticated:
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        for content in element_suggestions:
            if content.id in interactions_dict:
                interaction = interactions_dict[content.id]
                content.is_liked = interaction.liked
                content.is_saved = interaction.saved
                content.is_viewed = interaction.viewed
            else:
                content.is_liked = False
                content.is_saved = False
                content.is_viewed = False
    
    context = {
        'element_name': 'Ateş',
        'element_suggestions': element_suggestions,
    }
    
    # Test result kontrol (cache'li)
    if request.user.is_authenticated:
        test_cache_key = f'user_test_result_{request.user.id}'
        test_result = cache.get(test_cache_key)
        
        if test_result is None:
            test_result = TestResult.objects.select_related('dominant_element').filter(
                user=request.user
            ).order_by('-date_taken').first()
            cache.set(test_cache_key, test_result, 1800)
            print(f"💾 Cache SET: User test result - {request.user.username}")
        else:
            print(f"✅ Cache HIT: User test result - {request.user.username}")
        
        if test_result:
            is_users_element = test_result.dominant_element.name == "Ateş"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
    
    # Anonymous için cache'le
    if not request.user.is_authenticated:
        cache.set('fire_more_anonymous', context, 900)
        print("💾 Cache SET: Fire page (anonymous)")
    
    return render(request, 'temperaments/fire_more.html', context)

def water_more(request):
    """Su mizacı detay sayfası - CACHE'Lİ VERSİYON"""
    
    # Anonymous kullanıcılar için cache
    if not request.user.is_authenticated:
        cache_key = 'water_more_anonymous'
        cached_data = cache.get(cache_key)
        if cached_data:
            print("✅ Cache HIT: Water page (anonymous)")
            return render(request, 'temperaments/water_more.html', cached_data)
    
    print(f"❌ Cache MISS: Water page - {request.user.username if request.user.is_authenticated else 'anonymous'}")
    
    # Element suggestions'ı cache'den al
    suggestions_cache_key = 'water_element_suggestions'
    element_suggestions = cache.get(suggestions_cache_key)
    
    if not element_suggestions:
        element_suggestions = RecommendedContent.objects.select_related('category').filter(
            related_element_name='Su',
            is_active=True,
            show_on_temperament_page=True
        ).annotate(
            like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
        ).order_by('order', '-created_at')[:3]
        
        # Cache'e kaydet (10 dakika)
        cache.set(suggestions_cache_key, list(element_suggestions), 600)
        print("💾 Cache SET: Water element suggestions")
    else:
        print("✅ Cache HIT: Water element suggestions")
    
    # Kullanıcı etkileşim bilgilerini ekle
    if request.user.is_authenticated:
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        for content in element_suggestions:
            if content.id in interactions_dict:
                interaction = interactions_dict[content.id]
                content.is_liked = interaction.liked
                content.is_saved = interaction.saved
                content.is_viewed = interaction.viewed
            else:
                content.is_liked = False
                content.is_saved = False
                content.is_viewed = False
    
    context = {
        'element_name': 'Su',
        'element_suggestions': element_suggestions,
    }
    
    # Test result kontrol (cache'li)
    if request.user.is_authenticated:
        test_cache_key = f'user_test_result_{request.user.id}'
        test_result = cache.get(test_cache_key)
        
        if test_result is None:
            test_result = TestResult.objects.select_related('dominant_element').filter(
                user=request.user
            ).order_by('-date_taken').first()
            cache.set(test_cache_key, test_result, 1800)
            print(f"💾 Cache SET: User test result - {request.user.username}")
        else:
            print(f"✅ Cache HIT: User test result - {request.user.username}")
        
        if test_result:
            is_users_element = test_result.dominant_element.name == "Su"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
    
    # Anonymous için cache'le
    if not request.user.is_authenticated:
        cache.set('water_more_anonymous', context, 900)
        print("💾 Cache SET: Water page (anonymous)")
    
    return render(request, 'temperaments/water_more.html', context)

def earth_more(request):
    """Toprak mizacı detay sayfası - CACHE'Lİ VERSİYON"""
    
    # Anonymous kullanıcılar için cache
    if not request.user.is_authenticated:
        cache_key = 'earth_more_anonymous'
        cached_data = cache.get(cache_key)
        if cached_data:
            print("✅ Cache HIT: Earth page (anonymous)")
            return render(request, 'temperaments/earth_more.html', cached_data)
    
    print(f"❌ Cache MISS: Earth page - {request.user.username if request.user.is_authenticated else 'anonymous'}")
    
    # Element suggestions'ı cache'den al
    suggestions_cache_key = 'earth_element_suggestions'
    element_suggestions = cache.get(suggestions_cache_key)
    
    if not element_suggestions:
        element_suggestions = RecommendedContent.objects.select_related('category').filter(
            related_element_name='Toprak',
            is_active=True,
            show_on_temperament_page=True
        ).annotate(
            like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
        ).order_by('order', '-created_at')[:3]
        
        # Cache'e kaydet (10 dakika)
        cache.set(suggestions_cache_key, list(element_suggestions), 600)
        print("💾 Cache SET: Earth element suggestions")
    else:
        print("✅ Cache HIT: Earth element suggestions")
    
    # Kullanıcı etkileşim bilgilerini ekle
    if request.user.is_authenticated:
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        for content in element_suggestions:
            if content.id in interactions_dict:
                interaction = interactions_dict[content.id]
                content.is_liked = interaction.liked
                content.is_saved = interaction.saved
                content.is_viewed = interaction.viewed
            else:
                content.is_liked = False
                content.is_saved = False
                content.is_viewed = False
    
    context = {
        'element_name': 'Toprak',
        'element_suggestions': element_suggestions,
    }
    
    # Test result kontrol (cache'li)
    if request.user.is_authenticated:
        test_cache_key = f'user_test_result_{request.user.id}'
        test_result = cache.get(test_cache_key)
        
        if test_result is None:
            test_result = TestResult.objects.select_related('dominant_element').filter(
                user=request.user
            ).order_by('-date_taken').first()
            cache.set(test_cache_key, test_result, 1800)
            print(f"💾 Cache SET: User test result - {request.user.username}")
        else:
            print(f"✅ Cache HIT: User test result - {request.user.username}")
        
        if test_result:
            is_users_element = test_result.dominant_element.name == "Toprak"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
    
    # Anonymous için cache'le
    if not request.user.is_authenticated:
        cache.set('earth_more_anonymous', context, 900)
        print("💾 Cache SET: Earth page (anonymous)")
    
    return render(request, 'temperaments/earth_more.html', context)