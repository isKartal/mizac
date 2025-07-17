# test_cache.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mizac.settings')
django.setup()

from django.core.cache import cache
import time

def test_cache():
    print("🧪 Cache sistemi test ediliyor...")
    
    # Test 1: Basit cache
    cache.set('test_key', 'Mizaç cache çalışıyor!', 30)
    value = cache.get('test_key')
    
    if value == 'Mizaç cache çalışıyor!':
        print("✅ Basit cache testi BAŞARILI")
    else:
        print("❌ Basit cache testi BAŞARISIZ")
        return
    
    # Test 2: Performance test
    print("⏱️ Performance test başlıyor...")
    
    # Cache'siz simülasyon
    start_time = time.time()
    for i in range(100):
        data = f"test_data_{i}" * 50
    no_cache_time = time.time() - start_time
    
    # Cache'li test
    cache.set('bulk_data', [f"test_data_{i}" * 50 for i in range(100)], 60)
    start_time = time.time()
    cached_data = cache.get('bulk_data')
    cache_time = time.time() - start_time
    
    print(f"   📊 Cache'siz: {no_cache_time:.4f}s")
    print(f"   📊 Cache'li: {cache_time:.4f}s")
    if cache_time > 0:
        print(f"   🚀 Hız artışı: {no_cache_time/cache_time:.1f}x")
    
    # Test 3: Django cache framework test
    print("🔧 Django cache framework test...")
    cache.set('django_test', {'message': 'Django cache aktif!'}, 60)
    django_result = cache.get('django_test')
    
    if django_result and django_result.get('message') == 'Django cache aktif!':
        print("✅ Django cache framework ÇALIŞIYOR!")
    else:
        print("❌ Django cache framework SORUNLU")
    
    print("\n🎉 Cache sistemi hazır! Django views'ları test edebilirsiniz.")

if __name__ == "__main__":
    test_cache()