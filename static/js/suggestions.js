document.addEventListener('DOMContentLoaded', function() {
  // ----- DEĞİŞKENLER -----
  let allContents = []; // Tüm içerikler
  let filteredContents = []; // Filtrelenmiş içerikler
  
  // Sayfalama değişkenleri - kişisel içerikler
  const itemsPerPage = 6;
  let currentPage = 1;
  let totalPages = 1;
  
  // Sayfalama değişkenleri - tüm mizaçlar
  let allItemsPerPage = 6;
  let allCurrentPage = 1;
  let allTotalPages = 1;
  
  // Filtre değişkenleri
  let activeCategory = 'all';
  let activeSort = 'newest';
  let activeElement = 'all';
  
  // DOM elementleri
  const contentSlider = document.getElementById('contentSlider');
  const allElementsContents = document.getElementById('allElementsContents');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const contentModal = document.getElementById('contentModal');
  const filterContainer = document.getElementById('filterContainer');
  const secondaryFilterContainer = document.getElementById('secondaryFilterContainer');
  
  // Slider kontrol butonları
  const prevSlideButton = document.getElementById('prevSlideButton');
  const nextSlideButton = document.getElementById('nextSlideButton');
  
  // ----- FİLTRE YAPIŞKAN DAVRANIŞI -----
  window.addEventListener('scroll', function() {
    if (filterContainer) {
      if (window.scrollY > 300) {
        filterContainer.classList.add('scrolled');
      } else {
        filterContainer.classList.remove('scrolled');
      }
    }
    
    if (secondaryFilterContainer) {
      if (window.scrollY > 700) {
        secondaryFilterContainer.classList.add('scrolled');
      } else {
        secondaryFilterContainer.classList.remove('scrolled');
      }
    }
  });
  
  // ----- KAYDIRMALI SLIDER FONKSİYONLARI -----
  // Slider kaydırma işlemi
  function scrollSlider(direction) {
    if (contentSlider) {
      const scrollAmount = direction === 'left' ? -300 : 300;
      contentSlider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  }
  
  // Slider butonlarına olay ekle
  if (prevSlideButton) {
    prevSlideButton.addEventListener('click', function() {
      scrollSlider('left');
    });
  }
  
  if (nextSlideButton) {
    nextSlideButton.addEventListener('click', function() {
      scrollSlider('right');
    });
  }
  
  // Slider içeriklerini kaydırma olayını dinle ve butonları güncelle
  if (contentSlider) {
    contentSlider.addEventListener('scroll', function() {
      // Kaydırma pozisyonlarını kontrol et
      const scrollLeft = contentSlider.scrollLeft;
      const maxScrollLeft = contentSlider.scrollWidth - contentSlider.clientWidth;
      
      // Sol butonu güncelle
      if (prevSlideButton) {
        prevSlideButton.style.opacity = scrollLeft <= 10 ? "0.5" : "1";
        prevSlideButton.style.pointerEvents = scrollLeft <= 10 ? "none" : "all";
      }
      
      // Sağ butonu güncelle
      if (nextSlideButton) {
        nextSlideButton.style.opacity = scrollLeft >= maxScrollLeft - 10 ? "0.5" : "1";
        nextSlideButton.style.pointerEvents = scrollLeft >= maxScrollLeft - 10 ? "none" : "all";
      }
    });
    
    // Sayfa yüklendiğinde butonları güncelle
    setTimeout(function() {
      // Kaydırma olayını manuel tetikle
      contentSlider.dispatchEvent(new Event('scroll'));
    }, 100);
  }
  
  // ----- FİLTRE BUTONLARI İÇİN OLAY DİNLEYİCİLERİ -----
  // Kategori filtreleme
  const categoryButtons = document.querySelectorAll('#categoryFilter .filter-option');
  categoryButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Aktif butonu değiştir
      categoryButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      
      // Filtreleme uygula
      activeCategory = this.dataset.category;
      filterPersonalizedContents();
      
      // Animasyon efekti ekle
      if (contentSlider) {
        contentSlider.style.opacity = '0';
        contentSlider.style.transform = 'translateY(15px)';
        
        setTimeout(() => {
          contentSlider.style.opacity = '1';
          contentSlider.style.transform = 'translateY(0)';
        }, 200);
      }
    });
  });
  
  // Sıralama
  const sortButtons = document.querySelectorAll('#sortFilter .filter-option');
  sortButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Aktif butonu değiştir
      sortButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      
      // Sıralama uygula
      activeSort = this.dataset.sort;
      filterPersonalizedContents();
      
      // Animasyon efekti ekle
      if (contentSlider) {
        contentSlider.style.opacity = '0';
        contentSlider.style.transform = 'translateY(15px)';
        
        setTimeout(() => {
          contentSlider.style.opacity = '1';
          contentSlider.style.transform = 'translateY(0)';
        }, 200);
      }
    });
  });
  
  // Element sekmesi filtreleme
  const elementTabs = document.querySelectorAll('#elementTabs .filter-option');
  elementTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      // Aktif sekmeyi değiştir
      elementTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      
      // Element filtresini uygula
      activeElement = this.dataset.element;
      filterAllContents();
      
      // Animasyon efekti ekle
      if (allElementsContents) {
        allElementsContents.style.opacity = '0';
        allElementsContents.style.transform = 'translateY(15px)';
        
        setTimeout(() => {
          allElementsContents.style.opacity = '1';
          allElementsContents.style.transform = 'translateY(0)';
        }, 200);
      }
    });
  });
  
  // ----- KİŞİSEL İÇERİKLERİ FİLTRELEME FONKSİYONU -----
  function filterPersonalizedContents() {
    if (!contentSlider) return;
    
    // Tüm kartları alın (NodeList)
    const allCards = contentSlider.querySelectorAll('.slider-card');
    
    // İçerikleri filtrele
    let filtered = Array.from(allCards);
    
    // Kategori filtreleme
    if (activeCategory !== 'all') {
      filtered = filtered.filter(card => card.dataset.category === activeCategory);
    }
    
    // Sıralama
    if (activeSort === 'popular') {
      // Beğeni butonu kaldırıldığı için sıralama özelliği kaldırıldı
      // Kartlar doğal sıralarında kalacak
    }
    
    // Tüm kartları gizle
    allCards.forEach(card => {
      card.style.display = 'none';
    });
    
    // Filtrelenmiş kartları göster
    filtered.forEach(card => {
      card.style.display = '';
      contentSlider.appendChild(card); // Sıralamayı uygulamak için DOM'a tekrar ekle
    });
    
    // Eğer hiç kart gösterilmiyorsa "İçerik bulunamadı" mesajı göster
    if (filtered.length === 0) {
      const emptyMessage = document.createElement('div');
      emptyMessage.className = 'empty-slider-message';
      emptyMessage.innerHTML = `
        <div class="empty-icon"><i class="fas fa-search"></i></div>
        <p class="empty-text">Bu filtrelere uygun içerik bulunamadı.</p>
      `;
      contentSlider.appendChild(emptyMessage);
    }
    
    // Slider'ı başa sıfırla
    contentSlider.scrollLeft = 0;
    
    // Butonları güncelle
    if (prevSlideButton && nextSlideButton) {
      contentSlider.dispatchEvent(new Event('scroll'));
    }
  }
  
  // ----- TÜM MİZAÇLAR İÇİN İÇERİKLERİ FİLTRELEME -----
  function filterAllContents() {
    // Sayfalamayı sıfırla
    allCurrentPage = 1;
    
    // Element filtreleme
    if (activeElement === 'all') {
      filteredContents = [...allContents];
    } else {
      filteredContents = allContents.filter(content => 
        content.related_element_name === activeElement
      );
    }
    
    // Toplam sayfa sayısını hesapla
    allTotalPages = Math.ceil(filteredContents.length / allItemsPerPage);
    
    // Filtrelenmiş içerikleri göster
    renderAllContents();
    
    // Sayfa numaralarını güncelle
    updateAllPageNumbers();
    
    // Sayfalama butonlarını güncelle
    updateAllPaginationButtons();
    
    // Sayfalama kontrollerini göster veya gizle
    const allContentsPagination = document.getElementById('allContentsPagination');
    if (allContentsPagination) {
      if (filteredContents.length > allItemsPerPage) {
        allContentsPagination.style.display = 'flex';
      } else {
        allContentsPagination.style.display = 'none';
      }
    }
  }
  
  // ----- SAYFALAMA FONKSİYONLARI -----
  // Sayfa numaralarını güncelle
  function updateAllPageNumbers() {
    const pageNumbers = document.getElementById('allPageNumbers');
    if (!pageNumbers) return;
    
    pageNumbers.innerHTML = '';
    
    // Maksimum gösterilecek sayfa sayısı
    const maxVisiblePages = 5;
    
    // Görünür sayfa aralığını hesapla
    let startPage = Math.max(1, allCurrentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(allTotalPages, startPage + maxVisiblePages - 1);
    
    // Görünür sayfa sayısını ayarla
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    // İlk sayfa bağlantısı ekle
    if (startPage > 1) {
      const firstPageButton = document.createElement('button');
      firstPageButton.className = 'page-button';
      firstPageButton.textContent = '1';
      firstPageButton.addEventListener('click', () => {
        gotoAllPage(1);
      });
      pageNumbers.appendChild(firstPageButton);
      
      // Arada çok fazla sayfa varsa ... ekle
      if (startPage > 2) {
        const ellipsis = document.createElement('span');
        ellipsis.className = 'page-ellipsis';
        ellipsis.textContent = '...';
        pageNumbers.appendChild(ellipsis);
      }
    }
    
    // Sayfa numaralarını oluştur
    for (let i = startPage; i <= endPage; i++) {
      const pageButton = document.createElement('button');
      pageButton.className = 'page-button' + (i === allCurrentPage ? ' active' : '');
      pageButton.textContent = i;
      pageButton.addEventListener('click', () => {
        gotoAllPage(i);
      });
      pageNumbers.appendChild(pageButton);
    }
    
    // Son sayfa bağlantısı ekle
    if (endPage < allTotalPages) {
      // Arada çok fazla sayfa varsa ... ekle
      if (endPage < allTotalPages - 1) {
        const ellipsis = document.createElement('span');
        ellipsis.className = 'page-ellipsis';
        ellipsis.textContent = '...';
        pageNumbers.appendChild(ellipsis);
      }
      
      const lastPageButton = document.createElement('button');
      lastPageButton.className = 'page-button';
      lastPageButton.textContent = allTotalPages;
      lastPageButton.addEventListener('click', () => {
        gotoAllPage(allTotalPages);
      });
      pageNumbers.appendChild(lastPageButton);
    }
  }
  
  // Sayfalama butonlarını güncelle
  function updateAllPaginationButtons() {
    const prevPageBtn = document.getElementById('allPrevPage');
    const nextPageBtn = document.getElementById('allNextPage');
    
    if (prevPageBtn) {
      prevPageBtn.disabled = allCurrentPage === 1;
    }
    
    if (nextPageBtn) {
      nextPageBtn.disabled = allCurrentPage === allTotalPages;
    }
  }
  
  // Tüm içerikler için belirli bir sayfaya git
  function gotoAllPage(page) {
    if (page < 1 || page > allTotalPages) return;
    
    allCurrentPage = page;
    
    // İçerikleri göster
    renderAllContents();
    
    // Sayfa numaralarını güncelle
    updateAllPageNumbers();
    
    // Sayfalama butonlarını güncelle
    updateAllPaginationButtons();
    
    // Sayfa başına kaydır
    if (allElementsContents) {
      // Scroll to the top of the content area
      allElementsContents.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
  
  // ----- SAYFALAMA BUTONLARINA OLAY EKLE -----
  const allPrevPageBtn = document.getElementById('allPrevPage');
  const allNextPageBtn = document.getElementById('allNextPage');
  
  if (allPrevPageBtn) {
    allPrevPageBtn.addEventListener('click', function() {
      gotoAllPage(allCurrentPage - 1);
    });
  }
  
  if (allNextPageBtn) {
    allNextPageBtn.addEventListener('click', function() {
      gotoAllPage(allCurrentPage + 1);
    });
  }
  
  // ----- AJAX İLE TÜM İÇERİKLERİ AL -----
  function fetchAllContents() {
    // Yükleniyor göstergesini göster
    loadingIndicator.style.display = 'flex';
    allElementsContents.style.display = 'none';
    
    // AJAX isteği ile tüm içerikleri al
    fetch('/profiles/api/all_contents/')
      .then(response => {
        if (!response.ok) {
          throw new Error('İçerikler alınırken hata oluştu');
        }
        return response.json();
      })
      .then(data => {
        // Yükleniyor göstergesini gizle
        loadingIndicator.style.display = 'none';
        allElementsContents.style.display = 'grid';
        document.getElementById('allContentsPagination').style.display = 'flex';
        
        // Tüm içerikleri diziye aktar
        allContents = data.contents;
        
        // Filtreleme yap ve içerikleri göster
        filterAllContents();
      })
      .catch(error => {
        console.error('Hata:', error);
        loadingIndicator.style.display = 'none';
        
        // Hata mesajı göster
        allElementsContents.innerHTML = `
          <div class="empty-state">
            <div class="empty-icon"><i class="fas fa-exclamation-circle"></i></div>
            <p class="empty-text">İçerikler yüklenirken bir hata oluştu. Lütfen sayfayı yenileyip tekrar deneyin.</p>
          </div>`;
        allElementsContents.style.display = 'block';
      });
  }
  
  // ----- TÜM MİZAÇLAR İÇİN İÇERİKLERİ GÖSTER -----
  function renderAllContents() {
    allElementsContents.innerHTML = '';
    
    if (filteredContents.length === 0) {
      allElementsContents.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon"><i class="fas fa-search"></i></div>
          <p class="empty-text">Bu mizaç tipi için henüz içerik bulunmamaktadır.</p>
        </div>`;
      return;
    }
    
    // Sayfalama için içerikleri filtrele
    const start = (allCurrentPage - 1) * allItemsPerPage;
    const end = start + allItemsPerPage;
    const pageContents = filteredContents.slice(start, end);
    
    // Kartları oluştur ve ekle
    pageContents.forEach((content, index) => {
      const card = document.createElement('div');
      card.className = 'content-card animated';
      card.dataset.contentId = content.id;
      card.dataset.category = content.category_id;
      
      // Element sınıfını belirle
      const elementClass = content.related_element_name.toLowerCase();
      
      card.innerHTML = `
        <div class="content-image ${content.image ? '' : 'placeholder-image'}" 
             ${content.image ? `style="background-image: url('${content.image}')"` : ''}>
          ${content.image ? '' : '<i class="fas fa-book-open"></i>'}
          <div class="content-element ${elementClass}">${content.related_element_name}</div>
          <div class="content-category">${content.category_name}</div>
        </div>
        <h3 class="content-title">${content.title}</h3>
        <div class="content-actions">
          <button class="action-button save-button ${content.is_saved ? 'saved' : ''}" 
                  data-content-id="${content.id}">
            <i class="${content.is_saved ? 'fas' : 'far'} fa-bookmark"></i>
            <span class="save-text">${content.is_saved ? 'Kaydedildi' : 'Kaydet'}</span>
          </button>
        </div>
      `;
      
      // Karta tıklama olayı ekle
      card.addEventListener('click', function(e) {
        if (!e.target.closest('.action-button')) {
          openContentModal(content.id);
        }
      });
      
      // Kaydetme butonuna olay ekle
      card.querySelector('.save-button').addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(content.id, this);
      });
      
      allElementsContents.appendChild(card);
      
      // Animasyon için sınıf ekle
      setTimeout(() => {
        card.classList.add('visible');
      }, 50 * (index + 1));
    });
  }
  
  // ----- İÇERİK DETAY MODALI -----
  let currentModalContentId = null;
  
  // Modal aç
  function openContentModal(contentId) {
    currentModalContentId = contentId;
    
    // İçeriği AJAX ile çek
    fetch(`/profiles/content/${contentId}/detail/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('İçerik yüklenirken hata oluştu');
        }
        return response.json();
      })
      .then(data => {
        // Modal başlığını ayarla
        document.getElementById('modalTitle').textContent = data.title;
        
        // Kategori bilgisini göster
        document.getElementById('modalCategory').textContent = data.category;
        
        // İçeriği göster
        document.getElementById('modalContent').innerHTML = data.content;
        
        // Kaydetme durumunu güncelle
        const saveBtn = document.getElementById('modalSaveBtn');
        saveBtn.dataset.contentId = contentId;
        saveBtn.className = `modal-action-btn${data.saved ? ' saved' : ''}`;
        saveBtn.innerHTML = data.saved ? 
          '<i class="fas fa-bookmark"></i> Kaydedildi' : 
          '<i class="far fa-bookmark"></i> Kaydet';
        
        // Modalı göster
        contentModal.classList.add('active');
        document.body.style.overflow = 'hidden';
      })
      .catch(error => {
        console.error('Hata:', error);
        alert('İçerik yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.');
      });
  }
  
  // Modal kapat
  document.getElementById('closeModal').addEventListener('click', function() {
    contentModal.classList.remove('active');
    document.body.style.overflow = '';
  });
  
  // Modal dışına tıklama ile kapatma
  contentModal.addEventListener('click', function(e) {
    if (e.target === contentModal) {
      contentModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
  
  // ESC tuşu ile modalı kapatma
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && contentModal.classList.contains('active')) {
      contentModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
  
  // Modal butonlarına olay ekle
  document.getElementById('modalSaveBtn').addEventListener('click', function() {
    toggleSave(this.dataset.contentId, this);
  });
  
  // ----- KAYDETME FONKSİYONLARI -----
  // Kaydetme işlevi
  function toggleSave(contentId, button) {
    fetch(`/profiles/content/${contentId}/toggle_save/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Kaydetme durumunu güncelle
        updateSaveStatus(contentId, data.saved);
      }
    })
    .catch(error => console.error('Hata:', error));
  }
  
  // Kaydetme durumunu güncelle
  function updateSaveStatus(contentId, isSaved) {
    // Kart butonlarını güncelle
    const saveButtons = document.querySelectorAll(`.save-button[data-content-id="${contentId}"]`);
    saveButtons.forEach(btn => {
      btn.classList.toggle('saved', isSaved);
      const icon = btn.querySelector('i');
      icon.className = isSaved ? 'fas fa-bookmark' : 'far fa-bookmark';
      
      const textSpan = btn.querySelector('.save-text');
      if (textSpan) {
        textSpan.textContent = isSaved ? 'Kaydedildi' : 'Kaydet';
      }
    });
    
    // Modal butonunu güncelle
    const modalSaveBtn = document.getElementById('modalSaveBtn');
    if (modalSaveBtn && modalSaveBtn.dataset.contentId === contentId) {
      modalSaveBtn.classList.toggle('saved', isSaved);
      modalSaveBtn.innerHTML = isSaved ? 
        '<i class="fas fa-bookmark"></i> Kaydedildi' : 
        '<i class="far fa-bookmark"></i> Kaydet';
    }
    
    // Tüm içerikler dizisinde ilgili içeriği güncelle
    const contentIndex = allContents.findIndex(c => c.id == contentId);
    if (contentIndex !== -1) {
      allContents[contentIndex].is_saved = isSaved;
    }
  }
  
  // ----- YARDIMCI FONKSİYONLAR -----
  // CSRF token'ı almak için yardımcı fonksiyon
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  // ----- SAYFA YÜKLEME OLAYLARI -----
  // Sayfayı hazırla
  function initPage() {
    // Kişisel içerik kartlarına olay ekle
    if (contentSlider) {
      // Kartlara tıklama olayı ekle
      const sliderCards = contentSlider.querySelectorAll('.slider-card');
      sliderCards.forEach(card => {
        card.addEventListener('click', function(e) {
          if (!e.target.closest('.action-button')) {
            openContentModal(this.dataset.contentId);
          }
        });
      });
      
      // Kaydetme butonlarına olay ekle
      contentSlider.querySelectorAll('.save-button').forEach(button => {
        button.addEventListener('click', function(e) {
          e.stopPropagation();
          toggleSave(this.dataset.contentId, this);
        });
      });
      
      // Slider'ı başa sıfırla
      contentSlider.scrollLeft = 0;
      
      // Butonları güncelle
      if (prevSlideButton && nextSlideButton) {
        setTimeout(() => {
          contentSlider.dispatchEvent(new Event('scroll'));
        }, 100);
      }
    }
    
    // Tüm içerikleri getir ve göster
    if (allElementsContents && loadingIndicator) {
      fetchAllContents();
    }
    
    // Animasyon için gözlemci ekle
    addAnimationObserver();
  }
  
  // Otomatik görünürlük animasyonları için gözlemci ekle
  function addAnimationObserver() {
    // IntersectionObserver desteğini kontrol et
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // Bir kez göründükten sonra gözlemlemeyi bırak
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });
      
      // Tüm animasyonlu kartları gözlemle
      document.querySelectorAll('.animated').forEach(card => {
        observer.observe(card);
      });
    } else {
      // IntersectionObserver desteklenmiyor - hepsini direkt göster
      document.querySelectorAll('.animated').forEach(card => {
        card.classList.add('visible');
      });
    }
  }
  
  // Mobil cihazlar için kart boyutlarını ayarlama
  function adjustCardSizes() {
    if (!contentSlider) return;
    
    const cards = contentSlider.querySelectorAll('.premium-card');
    if (!cards.length) return;
    
    // Ekran genişliğine göre kart genişliklerini ayarla
    if (window.innerWidth <= 768) {
      // Mobil görünüm: Her satırda 1 kart
      cards.forEach(card => {
        card.style.width = `calc(100% - 30px)`;
        card.style.maxWidth = '400px';
      });
    } else {
      // Tablet ve masaüstü görünüm: Her satırda 2 kart
      cards.forEach(card => {
        card.style.width = `calc(50% - 30px)`;
        card.style.maxWidth = '350px';
      });
    }
    
    // Kaydırma olayını tetikle
    contentSlider.dispatchEvent(new Event('scroll'));
  }
  
  // Pencere boyutu değiştiğinde kart boyutlarını ayarla
  window.addEventListener('resize', adjustCardSizes);
  
  // Sayfa yüklendiğinde tüm işlemleri başlat
  initPage();
  
  // Sayfa yüklendiğinde kart boyutlarını ayarla
  window.addEventListener('load', adjustCardSizes);
});