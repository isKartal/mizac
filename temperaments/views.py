# temperaments/views.py

from django.shortcuts import render
from django.db.models import Count, Q
from profiles.models import RecommendedContent, UserContentInteraction
from testing_algorithm.models import TestResult

def temperaments(request):
    """Mizaçlar ana sayfası"""
    return render(request, 'temperaments/temperaments.html')

def air_more(request):
    """Hava mizacı detay sayfası"""
    
    # Hava mizacı için mizaç sayfasında gösterilmek üzere işaretlenmiş içerikleri getir
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Hava',
        is_active=True,
        show_on_temperament_page=True  # Yeni alan ile filtreleme
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')[:3]  # En fazla 3 adet
    
    # Kullanıcının giriş yapmış olması durumunda, beğeni bilgilerini ekle
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
    
    # Kullanıcının mizacı ile karşılaştırma
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
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
        
    return render(request, 'temperaments/air_more.html', context)

def earth_more(request):
    """Toprak mizacı detay sayfası"""
    
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Toprak',
        is_active=True,
        show_on_temperament_page=True  # Yeni alan ile filtreleme
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')[:3]
    
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
    
    # Kullanıcının mizacı ile karşılaştırma
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
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
        
    return render(request, 'temperaments/earth_more.html', context)

def fire_more(request):
    """Ateş mizacı detay sayfası"""
    
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Ateş',
        is_active=True,
        show_on_temperament_page=True  # Yeni alan ile filtreleme
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')[:3]
    
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
    
    # Kullanıcının mizacı ile karşılaştırma
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
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
        
    return render(request, 'temperaments/fire_more.html', context)

def water_more(request):
    """Su mizacı detay sayfası"""
    
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Su',
        is_active=True,
        show_on_temperament_page=True  # Yeni alan ile filtreleme
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')[:3]
    
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
    
    # Kullanıcının mizacı ile karşılaştırma
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
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
        
    return render(request, 'temperaments/water_more.html', context)