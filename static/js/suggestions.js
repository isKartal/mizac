// ==========================================================================
// SAYFA YÜKLENDİĞİNDE ÇALIŞACAK ANA FONKSİYON - DÜZELTME
// ==========================================================================

document.addEventListener('DOMContentLoaded', function() {
  // ========================================================================
  // DEĞİŞKEN TANIMLAMALARI
  // ========================================================================
  
  // ---- İçerik Verileri ----
  let allContents = [];          // Tüm içerikler
  let filteredContents = [];     // Filtrelenmiş içerikler
  
  // ---- Sayfalama Değişkenleri - Kişisel İçerikler ----
  const itemsPerPage = 6;
  let currentPage = 1;
  let totalPages = 1;
  
  // ---- Sayfalama Değişkenleri - Tüm Mizaçlar ----
  let allItemsPerPage = 6;
  let allCurrentPage = 1;
  let allTotalPages = 1;
  
  // ---- Filtre Değişkenleri ----
  let activeCategory = 'all';    // Aktif kategori filtresi
  let activeSort = 'newest';     // Aktif sıralama türü
  let activeElement = 'all';     // Aktif element filtresi
  
  // ---- DOM Elementleri ----
  const contentSlider = document.getElementById('contentSlider');
  const allElementsContents = document.getElementById('allElementsContents');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const contentModal = document.getElementById('contentModal');
  const filterContainer = document.getElementById('filterContainer');
  const secondaryFilterContainer = document.getElementById('secondaryFilterContainer');
  
  // ---- Slider Kontrol Butonları ----
  const prevSlideButton = document.getElementById('prevSlideButton');
  const nextSlideButton = document.getElementById('nextSlideButton');
  
  // ---- YENİ: Dropdown Elementleri ----
  const dropdownBtn = document.getElementById('categoryDropdownBtn');
  const dropdown = document.getElementById('categoryDropdown');
  const categoryOptions = document.querySelectorAll('.category-option');
  const selectedCategorySpan = dropdownBtn?.querySelector('.selected-category');
  
  // ========================================================================
  // YENİ: DROPDOWN KATEGORİ FİLTRE SİSTEMİ
  // ========================================================================
  
  /**
   * Dropdown kategori filtresini başlatır
   */
  function initDropdownFilter() {
    if (!dropdownBtn || !dropdown) return;
    
    console.log('Dropdown filtre sistemi başlatılıyor...');
    
    // Çekmece açma/kapama
    dropdownBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      dropdown.classList.toggle('open');
      dropdownBtn.classList.toggle('active');
    });
    
    // Dışarı tıklayınca kapat
    document.addEventListener('click', function() {
      dropdown.classList.remove('open');
      dropdownBtn.classList.remove('active');
    });
    
    // Kategori seçimi
    categoryOptions.forEach(option => {
      option.addEventListener('click', function(e) {
        e.stopPropagation();
        
        // Aktif durumu güncelle
        categoryOptions.forEach(opt => opt.classList.remove('active'));
        this.classList.add('active');
        
        // Global değişkeni güncelle
        activeCategory = this.dataset.category;
        
        // Buton metnini güncelle
        if (selectedCategorySpan) {
          selectedCategorySpan.textContent = this.querySelector('span').textContent;
        }
        
        // Çekmeceyi kapat
        dropdown.classList.remove('open');
        dropdownBtn.classList.remove('active');
        
        // Ana filtreleme fonksiyonunu çağır
        filterPersonalizedContents();
        
        console.log('Kategori değiştirildi:', activeCategory);
      });
    });
    
    // ESC tuşu ile kapat
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && dropdown.classList.contains('open')) {
        dropdown.classList.remove('open');
        dropdownBtn.classList.remove('active');
      }
    });
    
    // Keyboard navigation
    dropdown.addEventListener('keydown', function(e) {
      const options = dropdown.querySelectorAll('.category-option');
      const currentIndex = Array.from(options).findIndex(opt => opt === document.activeElement);
      
      switch(e.key) {
        case 'ArrowDown':
          e.preventDefault();
          const nextIndex = currentIndex < options.length - 1 ? currentIndex + 1 : 0;
          options[nextIndex].focus();
          break;
        case 'ArrowUp':
          e.preventDefault();
          const prevIndex = currentIndex > 0 ? currentIndex - 1 : options.length - 1;
          options[prevIndex].focus();
          break;
        case 'Enter':
          e.preventDefault();
          document.activeElement.click();
          break;
      }
    });
  }
  
  // ========================================================================
  // KAYDIRMALI SLIDER FONKSİYONLARI
  // ========================================================================
  
  /**
   * Slider'ı belirtilen yönde kaydırır
   * @param {string} direction - Kaydırma yönü ('left' veya 'right')
   */
  function scrollSlider(direction) {
    if (!contentSlider) return;
    
    const scrollAmount = direction === 'left' ? -300 : 300;
    contentSlider.scrollBy({ 
      left: scrollAmount, 
      behavior: 'smooth' 
    });
  }
  
  /**
   * Slider butonlarına olay dinleyicilerini ekler
   */
  function initSliderButtons() {
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
  }
  
  /**
   * Slider pozisyonuna göre butonların durumunu günceller
   */
  function updateSliderButtons() {
    if (!contentSlider) return;
    
    const scrollLeft = contentSlider.scrollLeft;
    const maxScrollLeft = contentSlider.scrollWidth - contentSlider.clientWidth;
    
    if (prevSlideButton) {
      const isAtStart = scrollLeft <= 10;
      prevSlideButton.style.opacity = isAtStart ? "0.5" : "1";
      prevSlideButton.style.pointerEvents = isAtStart ? "none" : "all";
    }
    
    if (nextSlideButton) {
      const isAtEnd = scrollLeft >= maxScrollLeft - 10;
      nextSlideButton.style.opacity = isAtEnd ? "0.5" : "1";
      nextSlideButton.style.pointerEvents = isAtEnd ? "none" : "all";
    }
  }
  
  /**
   * Slider kaydırma olayını dinler ve butonları günceller
   */
  function initSliderScrollListener() {
    if (!contentSlider) return;
    
    contentSlider.addEventListener('scroll', updateSliderButtons);
    
    setTimeout(function() {
      updateSliderButtons();
    }, 100);
  }
  
  // ========================================================================
  // ELEMENT FİLTRE SİSTEMİ (Diğer Mizaçlar İçin)
  // ========================================================================
  
  /**
   * Element sekmesi filtre butonlarına olay dinleyicilerini ekler
   */
function initElementFilters() {
  const elementTabs = document.querySelectorAll('#elementTabs .filter-option');
  
  elementTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      elementTabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      this.classList.add('active');
      this.setAttribute('aria-selected', 'true');
      
      activeElement = this.dataset.element;
      
      // ✅ YENİ: Her sekme değişiminde önce tüm durumları temizle
      clearAllStates();
      
      // YENİ: Kaydedilmiş içerikler sekmesi kontrolü
      if (activeElement === 'saved') {
        loadSavedContents();
      } else {
        filterAllContents();
      }
      
      addContentAnimation();
    });
  });
}
function clearAllStates() {
  const contentGrid = document.getElementById('allElementsContents');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const savedEmptyState = document.getElementById('savedEmptyState');
  const pagination = document.getElementById('allContentsPagination');
  
  // Tüm durumları sıfırla
  if (contentGrid) {
    contentGrid.innerHTML = '';
    contentGrid.style.display = 'none';
  }
  
  if (loadingIndicator) {
    loadingIndicator.style.display = 'none';
    loadingIndicator.classList.remove('active');
  }
  
  if (savedEmptyState) {
    savedEmptyState.style.display = 'none';
  }
  
  if (pagination) {
    pagination.style.display = 'none';
  }
}

function loadSavedContents() {
  showLoadingIndicator();
  
  fetch('/profiles/api/saved_contents/')
    .then(response => response.json())
    .then(data => {
      hideLoadingIndicator();
      if (data.success && data.contents.length > 0) {
        displaySavedContents(data.contents);
      } else {
        showSavedEmptyState();
      }
    })
    .catch(error => {
      console.error('Kaydedilmiş içerikler yüklenirken hata:', error);
      hideLoadingIndicator();
      showSavedEmptyState();
    });
}
// YENİ FONKSIYON: Kaydedilmiş içerikleri görüntüle
function displaySavedContents(contents) {
  const contentGrid = document.getElementById('allElementsContents');
  const pagination = document.getElementById('allContentsPagination');
  
  // Grid'i temizle ve göster
  contentGrid.innerHTML = '';
  contentGrid.style.display = 'grid';
  
  // Sayfalama'yı gizle (kaydedilmiş içeriklerde sayfalama yok)
  if (pagination) {
    pagination.style.display = 'none';
  }
  
  contents.forEach(content => {
    const contentCard = createSavedContentCard(content);
    contentGrid.appendChild(contentCard);
  });
  
  // Event listener'ları yeniden ekle
  addSavedContentEventListeners();
}



// YENİ FONKSIYON: Kaydedilmiş içerik kartı oluştur
// YENİ FONKSIYON: Kaydedilmiş içerik kartı oluştur - createContentCard ile aynı görünüm
function createSavedContentCard(content) {
  const contentCard = document.createElement('div');
  contentCard.className = 'content-card animated-card';
  contentCard.setAttribute('data-content-id', content.id);
  contentCard.setAttribute('data-element', content.related_element_name);
  
  // ✅ createContentCard ile aynı element sınıfı sistemi
  const elementClass = content.related_element_name.toLowerCase();
  
  // ✅ createContentCard ile AYNI HTML yapısı
  contentCard.innerHTML = `
    <div class="content-image ${content.image ? '' : 'placeholder-image'}" 
         ${content.image ? `style="background-image: url('${content.image}')"` : ''}>
      ${content.image ? '' : '<i class="fas fa-book-open"></i>'}
      <div class="content-element ${elementClass}">
        ${content.related_element_name}
      </div>
      <div class="content-category">
        ${content.category_name}
      </div>
    </div>
    
    <div class="content-header">
      <h3 class="content-title">${content.title}</h3>
      <button class="save-button-header saved" 
              data-content-id="${content.id}"
              type="button"
              title="Kaydedildi - Kaldırmak için tıklayın"
              aria-label="İçerik kaydedildi, kaldırmak için tıklayın">
        <i class="fas fa-bookmark" aria-hidden="true"></i>
      </button>
    </div>
  `;
  
  return contentCard;
}
// YENİ FONKSIYON: Element sınıfı belirle
function getElementClass(elementName) {
  const elementMap = {
    'Ateş': 'element-ates',
    'Hava': 'element-hava', 
    'Su': 'element-su',
    'Toprak': 'element-toprak'
  };
  return elementMap[elementName] || '';
}
// YENİ FONKSIYON: Kaydedilmiş içerikler için event listener'ları ekle
function addSavedContentEventListeners() {
  // İçerik kartlarına tıklama olayı
  document.querySelectorAll('#allElementsContents .content-card').forEach(card => {
    card.addEventListener('click', function(e) {
      if (!e.target.closest('.save-button-header')) {
        const contentId = this.dataset.contentId;
        openContentModal(contentId);
      }
    });
  });
  
  // Kaydet butonlarına olay (kaydedilmiş içeriklerde kaldırma işlemi)
  document.querySelectorAll('#allElementsContents .save-button-header').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const contentId = this.dataset.contentId;
      toggleSaveFromSavedList(contentId, this);
    });
  });
}

// YENİ FONKSIYON: Kaydedilmiş listeden içerik kaldırma
function toggleSaveFromSavedList(contentId, button) {
  // Onay dialogu göster
  if (confirm('Bu içeriği kaydedilmiş listesinden kaldırmak istediğinizden emin misiniz?')) {
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
      if (data.success && !data.saved) {
        // İçeriği listeden kaldır
        const card = button.closest('.content-card');
        if (card) {
          // Animasyonlu kaldırma
          card.style.transition = 'all 0.3s ease';
          card.style.opacity = '0';
          card.style.transform = 'translateY(-20px)';
          
          setTimeout(() => {
            card.remove();
            
            // Eğer hiç içerik kalmadıysa boş durum göster
            const remainingCards = document.querySelectorAll('#allElementsContents .content-card');
            if (remainingCards.length === 0) {
              showSavedEmptyState();
            }
          }, 300);
        }
      } else if (data.success && data.saved) {
        // Beklenmedik durum - tekrar kaydedildi
        updateSaveStatus(contentId, true);
      }
    })
    .catch(error => {
      console.error('Kaydetme işlemi hatası:', error);
      alert('İşlem sırasında bir hata oluştu. Lütfen tekrar deneyin.');
    });
  }
}

function showSavedEmptyState() {
  const contentGrid = document.getElementById('allElementsContents');
  let savedEmptyState = document.getElementById('savedEmptyState');
  
  // Grid'i gizle
  contentGrid.style.display = 'none';
  contentGrid.innerHTML = '';
  
  // Eğer savedEmptyState yoksa oluştur
  if (!savedEmptyState) {
    savedEmptyState = document.createElement('div');
    savedEmptyState.id = 'savedEmptyState';
    savedEmptyState.className = 'empty-state';
    savedEmptyState.setAttribute('role', 'status');
    savedEmptyState.innerHTML = `
      <div class="empty-icon">
        <i class="fas fa-bookmark" aria-hidden="true"></i>
      </div>
      <p class="empty-text">Henüz kaydedilmiş içeriğiniz bulunmuyor.</p>
      <p class="empty-subtext">İlginizi çeken içerikleri kaydetmek için <i class="far fa-bookmark"></i> simgesine tıklayın.</p>
    `;
    
    // Grid'den sonra ekle
    contentGrid.parentNode.insertBefore(savedEmptyState, contentGrid.nextSibling);
  }
  
  // Boş durumu göster
  savedEmptyState.style.display = 'block';
}
  /**
   * Slider için animasyon efekti ekler
   */
  function addSliderAnimation() {
    if (!contentSlider) return;
    
    contentSlider.style.opacity = '0';
    contentSlider.style.transform = 'translateY(15px)';
    
    setTimeout(() => {
      contentSlider.style.opacity = '1';
      contentSlider.style.transform = 'translateY(0)';
    }, 200);
  }
  
  /**
   * İçerik için animasyon efekti ekler
   */
  function addContentAnimation() {
    if (!allElementsContents) return;
    
    allElementsContents.style.opacity = '0';
    allElementsContents.style.transform = 'translateY(15px)';
    
    setTimeout(() => {
      allElementsContents.style.opacity = '1';
      allElementsContents.style.transform = 'translateY(0)';
    }, 200);
  }
  
  // ========================================================================
  // DÜZELTME: KİŞİSEL İÇERİKLERİ FİLTRELEME FONKSİYONU
  // ========================================================================
  
  /**
   * Kişisel içerikleri filtreler ve gösterir (DÜZELTME)
   */
  function filterPersonalizedContents() {
    if (!contentSlider) return;
    
    console.log('=== KİŞİSEL İÇERİK FİLTRELEME ===');
    console.log('Aktif kategori:', activeCategory);
    
    // DÜZELTME: Doğru selector'ları kullan
    const allCards = Array.from(contentSlider.querySelectorAll('.slider-card, .premium-card, [data-category]'));
    
    console.log('Toplam kart sayısı:', allCards.length);
    
    // Kategori filtreleme uygula
    let filteredCards = allCards;
    if (activeCategory !== 'all') {
      filteredCards = allCards.filter(card => {
        const cardCategory = card.dataset.category;
        console.log(`Kart kategori: ${cardCategory}, Hedef: ${activeCategory}`);
        return cardCategory === activeCategory || cardCategory === activeCategory.toString();
      });
    }
    
    console.log('Filtrelenmiş kart sayısı:', filteredCards.length);
    
    // Tüm kartları gizle
    allCards.forEach(card => {
      card.style.display = 'none';
      card.style.opacity = '0';
    });
    
    // Mevcut boş mesajları temizle
    const existingEmptyMessages = contentSlider.querySelectorAll('.empty-slider-message');
    existingEmptyMessages.forEach(msg => msg.remove());
    
    // Filtrelenmiş kartları göster
    if (filteredCards.length > 0) {
      filteredCards.forEach((card, index) => {
        card.style.display = 'block';
        card.style.opacity = '1';
        
        // Animasyon efekti
        setTimeout(() => {
          card.style.transform = 'scale(1)';
        }, index * 50);
      });
    } else {
      // Hiç kart yoksa boş mesaj göster
      showEmptySliderMessage();
    }
    
    // Slider'ı başa sıfırla
    contentSlider.scrollLeft = 0;
    
    // Butonları güncelle
    setTimeout(() => {
      updateSliderButtons();
    }, 300);
    
    // Animasyon efekti ekle
    addSliderAnimation();
    
    console.log('=== FİLTRELEME TAMAMLANDI ===');
  }
  
  /**
   * Slider için boş durum mesajı gösterir
   */
  function showEmptySliderMessage() {
    const emptyMessage = document.createElement('div');
    emptyMessage.className = 'empty-slider-message';
    emptyMessage.style.cssText = `
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      text-align: center;
      color: #777;
      background: white;
      border-radius: 15px;
      margin: 20px;
      box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    `;
    emptyMessage.innerHTML = `
      <div class="empty-icon" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;">
        <i class="fas fa-search"></i>
      </div>
      <p class="empty-text" style="margin: 0; font-size: 1.1rem;">Bu kategoride içerik bulunamadı.</p>
    `;
    contentSlider.appendChild(emptyMessage);
  }
  
  // ========================================================================
  // TÜM MİZAÇLAR İÇİN İÇERİKLERİ FİLTRELEME
  // ========================================================================
  
  /**
   * Tüm mizaçlar için içerikleri filtreler
   */
function filterAllContents() {
  // ✅ Önce loading göster
  showLoadingIndicator();
  
  // Kısa bir gecikme ile filtreleme yap (UI daha smooth görünür)
  setTimeout(() => {
    allCurrentPage = 1;
    
    if (activeElement === 'all') {
      filteredContents = [...allContents];
    } else {
      filteredContents = allContents.filter(content => 
        content.related_element_name === activeElement
      );
    }
    
    allTotalPages = Math.ceil(filteredContents.length / allItemsPerPage);
    
    // ✅ Loading'i gizle ve içerikleri göster
    hideLoadingIndicator();
    renderAllContents();
    updateAllPageNumbers();
    updateAllPaginationButtons();
    updatePaginationVisibility();
  }, 300);
}
  
  /**
   * Sayfalama kontrollerinin görünürlüğünü günceller
   */
  function updatePaginationVisibility() {
    const allContentsPagination = document.getElementById('allContentsPagination');
    if (!allContentsPagination) return;
    
    if (filteredContents.length > allItemsPerPage) {
      allContentsPagination.style.display = 'flex';
    } else {
      allContentsPagination.style.display = 'none';
    }
  }
  
  // ========================================================================
  // SAYFALAMA FONKSİYONLARI (Değişiklik yok - mevcut kod korundu)
  // ========================================================================
  
  function updateAllPageNumbers() {
    const pageNumbers = document.getElementById('allPageNumbers');
    if (!pageNumbers) return;
    
    pageNumbers.innerHTML = '';
    const maxVisiblePages = 5;
    
    let startPage = Math.max(1, allCurrentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(allTotalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    if (startPage > 1) {
      addPageButton(pageNumbers, 1);
      if (startPage > 2) {
        addPageEllipsis(pageNumbers);
      }
    }
    
    for (let i = startPage; i <= endPage; i++) {
      addPageButton(pageNumbers, i, i === allCurrentPage);
    }
    
    if (endPage < allTotalPages) {
      if (endPage < allTotalPages - 1) {
        addPageEllipsis(pageNumbers);
      }
      addPageButton(pageNumbers, allTotalPages);
    }
  }
  
  function addPageButton(container, pageNumber, isActive = false) {
    const pageButton = document.createElement('button');
    pageButton.className = `page-button${isActive ? ' active' : ''}`;
    pageButton.textContent = pageNumber;
    pageButton.addEventListener('click', () => {
      gotoAllPage(pageNumber);
    });
    container.appendChild(pageButton);
  }
  
  function addPageEllipsis(container) {
    const ellipsis = document.createElement('span');
    ellipsis.className = 'page-ellipsis';
    ellipsis.textContent = '...';
    container.appendChild(ellipsis);
  }
  
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
  
  function gotoAllPage(page) {
    if (page < 1 || page > allTotalPages) return;
    
    allCurrentPage = page;
    renderAllContents();
    updateAllPageNumbers();
    updateAllPaginationButtons();
    
    if (allElementsContents) {
      allElementsContents.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
      });
    }
  }
  
  function initPaginationButtons() {
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
  }
  
  // ========================================================================
  // AJAX İLE İÇERİK ALMA FONKSİYONLARI (Değişiklik yok)
  // ========================================================================
  
function fetchAllContents() {
  console.log('📡 fetchAllContents çağrıldı...');
  console.log('🔍 loadingIndicator:', !!loadingIndicator);
  console.log('🔍 allElementsContents:', !!allElementsContents);
  
  showLoadingIndicator();
  
  fetch('/profiles/api/all_contents/')
    .then(response => {
      console.log('📡 API Response Status:', response.status);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: İçerikler alınırken hata oluştu`);
      }
      return response.json();
    })
    .then(data => {
      console.log('📦 API Response Data:', data);
      console.log('📦 İçerik sayısı:', data.contents ? data.contents.length : 0);
      
      hideLoadingIndicator();
      
      // Global değişkeni güncelle
      allContents = data.contents || [];
      console.log('✅ allContents güncellendi, uzunluk:', allContents.length);
      
      // İçerikler yüklendikten sonra filtreleme yap
      if (allContents.length > 0) {
        console.log('🔄 İçerikler filtreleniyor...');
        filterAllContents();
      } else {
        console.log('⚠️ Hiç içerik bulunamadı');
        showEmptyContentMessage();
      }
    })
    .catch(error => {
      console.error('❌ fetchAllContents hatası:', error);
      hideLoadingIndicator();
      showErrorMessage();
    });
}

  
function hideLoadingIndicator() {
  console.log('✅ Loading gizleniyor...');
  
  const loadingIndicator = document.getElementById('loadingIndicator');
  const contentGrid = document.getElementById('allElementsContents');
  const savedEmptyState = document.getElementById('savedEmptyState');
  
  if (loadingIndicator) {
    loadingIndicator.style.display = 'none';
    loadingIndicator.classList.remove('active');
  }
  
  // ✅ Sadece normal içerikler için grid'i göster
  if (contentGrid && activeElement !== 'saved') {
    contentGrid.style.display = 'grid';
  }
  
  // ✅ Saved empty state'in gizli olduğundan emin ol
  if (savedEmptyState) {
    savedEmptyState.style.display = 'none';
  }
}

  function showErrorMessage() {
    if (allElementsContents) {
      allElementsContents.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-exclamation-circle"></i>
          </div>
          <p class="empty-text">
            İçerikler yüklenirken bir hata oluştu. 
            Lütfen sayfayı yenileyip tekrar deneyin.
          </p>
        </div>
      `;
      allElementsContents.style.display = 'block';
    }
  }
  
  // ========================================================================
  // TÜM MİZAÇLAR İÇİN İÇERİKLERİ GÖSTERME (Değişiklik yok)
  // ========================================================================
  
  function renderAllContents() {
  const allElementsContents = document.getElementById('allElementsContents');
  if (!allElementsContents) return;
  
  allElementsContents.innerHTML = '';
  
  if (filteredContents.length === 0) {
    showEmptyContentMessage();
    return;
  }
  
  // ✅ Grid'in göründüğünden emin ol
  allElementsContents.style.display = 'grid';
  
  const start = (allCurrentPage - 1) * allItemsPerPage;
  const end = start + allItemsPerPage;
  const pageContents = filteredContents.slice(start, end);
  
  pageContents.forEach((content, index) => {
    const card = createContentCard(content, index);
    allElementsContents.appendChild(card);
  });
}
  
  function showEmptyContentMessage() {
  const allElementsContents = document.getElementById('allElementsContents');
  if (!allElementsContents) return;
  
  allElementsContents.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-search"></i>
      </div>
      <p class="empty-text">
        Bu mizaç tipi için henüz içerik bulunmamaktadır.
      </p>
    </div>
  `;
  
  // ✅ Grid'i göster
  allElementsContents.style.display = 'block';
}
  
  function createContentCard(content, index) {
    const card = document.createElement('div');
    card.className = 'content-card animated';
    card.dataset.contentId = content.id;
    card.dataset.category = content.category_id;
    
    const elementClass = content.related_element_name.toLowerCase();
    
    card.innerHTML = `
      <div class="content-image ${content.image ? '' : 'placeholder-image'}" 
           ${content.image ? `style="background-image: url('${content.image}')"` : ''}>
        ${content.image ? '' : '<i class="fas fa-book-open"></i>'}
        <div class="content-element ${elementClass}">
          ${content.related_element_name}
        </div>
        <div class="content-category">
          ${content.category_name}
        </div>
      </div>
      
      <div class="content-header">
        <h3 class="content-title">${content.title}</h3>
        <button class="save-button-header ${content.is_saved ? 'saved' : ''}" 
                data-content-id="${content.id}"
                title="${content.is_saved ? 'Kaydedildi' : 'Kaydet'}">
          <i class="${content.is_saved ? 'fas' : 'far'} fa-bookmark"></i>
        </button>
      </div>
    `;
    
    addCardEventListeners(card, content);
    
    setTimeout(() => {
      card.classList.add('visible');
    }, 50 * (index + 1));
    
    return card;
  }
  
  function addCardEventListeners(card, content) {
    card.addEventListener('click', function(e) {
      if (!e.target.closest('.save-button-header')) {
        openContentModal(content.id);
      }
    });
    
    const saveButton = card.querySelector('.save-button-header');
    if (saveButton) {
      saveButton.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(content.id, this);
      });
    }
  }
  
  // ========================================================================
  // MODAL VE KAYDETME FONKSİYONLARI (Değişiklik yok - mevcut kod korundu)
  // ========================================================================
  
  let currentModalContentId = null;
  
function openContentModal(contentId) {
  currentModalContentId = contentId;
  
  fetch(`/profiles/content/${contentId}/detail/`)
    .then(response => {
      if (!response.ok) {
        throw new Error('İçerik yüklenirken hata oluştu');
      }
      return response.json();
    })
    .then(data => {
      // Mevcut modal doldurma kodları...
      document.getElementById('modalTitle').textContent = data.title;
      document.getElementById('modalCategory').textContent = data.category;
      document.getElementById('modalContent').innerHTML = data.content;
      document.getElementById('modalElement').textContent = data.related_element;
      document.getElementById('modalElement').className = `modal-element ${data.related_element.toLowerCase()}`;
      
      // ✅ YENİ: Header'a görsel ekleme
      const modalHeader = document.querySelector('.modal-header');
      if (modalHeader) {
        if (data.image) {
          modalHeader.style.backgroundImage = `url('${data.image}')`;
          modalHeader.classList.add('has-image');
        } else {
          modalHeader.style.backgroundImage = '';
          modalHeader.classList.remove('has-image');
        }
      }
      
      // Kaydet butonunu güncelle
      updateModalSaveButton(contentId, data.saved);
      
      // Modal'ı göster
      showModal();
    })
    .catch(error => {
      console.error('Hata:', error);
      alert('İçerik yüklenirken bir hata oluştu.');
    });
}
  
  function populateModal(data, contentId) {
  const modalTitle = document.getElementById('modalTitle');
  if (modalTitle) {
    modalTitle.textContent = data.title;
  }
  
  const modalCategory = document.getElementById('modalCategory');
  if (modalCategory) {
    modalCategory.textContent = data.category;
  }
  
  const modalContent = document.getElementById('modalContent');
  if (modalContent) {
    modalContent.innerHTML = data.content;
  }
  
  const modalElement = document.getElementById('modalElement');
  if (modalElement) {
    modalElement.textContent = data.related_element;
    modalElement.className = `modal-element ${data.related_element.toLowerCase()}`;
  }
  
  // ✅ YENİ: Header'a görsel ekleme
  const modalHeader = document.querySelector('.modal-header');
  if (modalHeader) {
    if (data.image) {
      modalHeader.style.backgroundImage = `url('${data.image}')`;
      modalHeader.classList.add('has-image');
    } else {
      modalHeader.style.backgroundImage = '';
      modalHeader.classList.remove('has-image');
    }
  }
  
  updateModalSaveButton(contentId, data.saved);
}
  function updateModalSaveButton(contentId, saved) {
    const saveBtn = document.getElementById('modalSaveBtn');
    if (!saveBtn) return;
    
    saveBtn.dataset.contentId = contentId;
    saveBtn.className = `modal-action-btn${saved ? ' saved' : ''}`;
    saveBtn.innerHTML = saved ? 
      '<i class="fas fa-bookmark"></i> Kaydedildi' : 
      '<i class="far fa-bookmark"></i> Kaydet';
  }
  
  function showModal() {
    contentModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  function hideModal() {
    contentModal.classList.remove('active');
    document.body.style.overflow = '';
  }
  
  function initModalEventListeners() {
    const closeModal = document.getElementById('closeModal');
    if (closeModal) {
      closeModal.addEventListener('click', hideModal);
    }
    
    if (contentModal) {
      contentModal.addEventListener('click', function(e) {
        if (e.target === contentModal) {
          hideModal();
        }
      });
    }
    
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && contentModal.classList.contains('active')) {
        hideModal();
      }
    });
    
    const modalSaveBtn = document.getElementById('modalSaveBtn');
    if (modalSaveBtn) {
      modalSaveBtn.addEventListener('click', function() {
        toggleSave(this.dataset.contentId, this);
      });
    }
  }
  
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
      updateSaveStatus(contentId, data.saved);
      
      // YENİ: Eğer kaydedilenler sekmesindeyse ve içerik kaldırıldıysa
      if (activeElement === 'saved' && !data.saved) {
        const card = button.closest('.content-card');
        if (card) {
          card.style.transition = 'all 0.3s ease';
          card.style.opacity = '0';
          card.style.transform = 'translateY(-20px)';
          
          setTimeout(() => {
            card.remove();
            
            const remainingCards = document.querySelectorAll('#allElementsContents .content-card');
            if (remainingCards.length === 0) {
              showSavedEmptyState();
            }
          }, 300);
        }
      }
    }
  })
  .catch(error => {
    console.error('Kaydetme işlemi hatası:', error);
  });
}

// YENİ FONKSIYON: Loading göstergesi kontrolleri
function showLoadingIndicator() {
  console.log('🔄 Loading gösteriliyor...');
  
  const loadingIndicator = document.getElementById('loadingIndicator');
  const contentGrid = document.getElementById('allElementsContents');
  const savedEmptyState = document.getElementById('savedEmptyState');
  const pagination = document.getElementById('allContentsPagination');
  
  if (loadingIndicator) {
    loadingIndicator.style.display = 'flex';
    loadingIndicator.classList.add('active');
  }
  
  if (contentGrid) {
    contentGrid.style.display = 'none';
    contentGrid.innerHTML = '';
  }
  
  // ✅ Saved empty state'i de gizle
  if (savedEmptyState) {
    savedEmptyState.style.display = 'none';
  }
  
  // Pagination'ı da gizle
  if (pagination) {
    pagination.style.display = 'none';
  }
}
  
  function updateSaveStatus(contentId, isSaved) {
    const saveButtons = document.querySelectorAll(`.save-button-header[data-content-id="${contentId}"]`);
    saveButtons.forEach(btn => {
      btn.classList.toggle('saved', isSaved);
      btn.title = isSaved ? 'Kaydedildi' : 'Kaydet';
      
      const icon = btn.querySelector('i');
      if (icon) {
        icon.className = isSaved ? 'fas fa-bookmark' : 'far fa-bookmark';
      }
    });
    
    const oldSaveButtons = document.querySelectorAll(`.save-button[data-content-id="${contentId}"], .premium-action-button[data-content-id="${contentId}"]`);
    oldSaveButtons.forEach(btn => {
      btn.classList.toggle('saved', isSaved);
      
      const icon = btn.querySelector('i');
      if (icon) {
        icon.className = isSaved ? 'fas fa-bookmark' : 'far fa-bookmark';
      }
      
      const textSpan = btn.querySelector('.save-text');
      if (textSpan) {
        textSpan.textContent = isSaved ? 'Kaydedildi' : 'Kaydet';
      }
    });
    
    const modalSaveBtn = document.getElementById('modalSaveBtn');
    if (modalSaveBtn && modalSaveBtn.dataset.contentId === contentId) {
      updateModalSaveButton(contentId, isSaved);
    }
    
    updateContentInArray(contentId, { is_saved: isSaved });
  }
  
  function updateContentInArray(contentId, updates) {
    const contentIndex = allContents.findIndex(c => c.id == contentId);
    if (contentIndex !== -1) {
      Object.assign(allContents[contentIndex], updates);
    }
  }
  
  // ========================================================================
  // YARDIMCI FONKSİYONLAR
  // ========================================================================
  
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
  
  // ========================================================================
  // ANIMASYON VE GÖRSELLİK FONKSİYONLARI
  // ========================================================================
  
  function addAnimationObserver() {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { 
        threshold: 0.1 
      });
      
      document.querySelectorAll('.animated').forEach(card => {
        observer.observe(card);
      });
    } else {
      document.querySelectorAll('.animated').forEach(card => {
        card.classList.add('visible');
      });
    }
  }
  
  function adjustCardSizes() {
    if (!contentSlider) return;
    
    const cards = contentSlider.querySelectorAll('.premium-card, .slider-card');
    if (!cards.length) return;
    
    cards.forEach(card => {
      if (window.innerWidth <= 768) {
        card.style.width = 'calc(100% - 30px)';
        card.style.maxWidth = '400px';
      } else {
        card.style.width = 'calc(50% - 30px)';
        card.style.maxWidth = '350px';
      }
    });
    
    updateSliderButtons();
  }
  
  // ========================================================================
  // SAYFA İNİSYALİZASYON FONKSİYONLARI
  // ========================================================================
  
  function initPersonalContentCards() {
    if (!contentSlider) return;
    
    const sliderCards = contentSlider.querySelectorAll('.slider-card, .premium-card');
    sliderCards.forEach(card => {
      card.addEventListener('click', function(e) {
        if (!e.target.closest('.save-button-header') && !e.target.closest('.premium-action-button')) {
          openContentModal(this.dataset.contentId);
        }
      });
    });
    
    const headerSaveButtons = contentSlider.querySelectorAll('.save-button-header');
    headerSaveButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(this.dataset.contentId, this);
      });
    });
    
    const saveButtons = contentSlider.querySelectorAll('.save-button, .premium-action-button');
    saveButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(this.dataset.contentId, this);
      });
    });
    
    contentSlider.scrollLeft = 0;
    
    setTimeout(() => {
      updateSliderButtons();
    }, 100);
  }
  
  function initResizeListener() {
    window.addEventListener('resize', adjustCardSizes);
    window.addEventListener('load', adjustCardSizes);
  }
  
  // ========================================================================
  // SAYFA BAŞLATMA - TEK FONKSİYON
  // ========================================================================
  
  // suggestions.js dosyasındaki initPage fonksiyonunu bu şekilde değiştirin:

function initPage() {
  console.log('🚀 Sayfa başlatılıyor...');
  
  // 1. Dropdown filtre sistemi
  initDropdownFilter();
  
  // 2. Slider işlevselliği
  initSliderButtons();
  initSliderScrollListener();
  
  // 3. Element filtre işlevselliği
  initElementFilters();
  
  // 4. Sayfalama işlevselliği
  initPaginationButtons();
  
  // 5. Modal işlevselliği
  initModalEventListeners();
  
  // 6. Kişisel içerik kartları
  initPersonalContentCards();
  
  // 7. Responsive işlevsellik
  initResizeListener();
  
  // 8. Animasyon gözlemcisi ekle
  addAnimationObserver();
  
  // 9. İlk kart boyutlarını ayarla
  adjustCardSizes();
  
  // 10. ✅ HEMEN TÜM İÇERİKLERİ YÜKLE - GECİKME YOK
  console.log('📡 API çağrısı başlatılıyor...');
  if (allElementsContents && loadingIndicator) {
    fetchAllContents();
  } else {
    console.error('❌ Gerekli elementler bulunamadı!', {
      allElementsContents: !!allElementsContents,
      loadingIndicator: !!loadingIndicator
    });
  }
  
  // 11. Kişisel içerik filtresi - kısa gecikme
  setTimeout(() => {
    filterPersonalizedContents();
  }, 500);
  
  console.log('✅ Sayfa başlatma tamamlandı');
}
  // ========================================================================
  // SAYFA BAŞLATMA
  // ========================================================================
  
  initPage();
  
});

document.addEventListener('DOMContentLoaded', function() {
  // URL'de #kesfedin hash'i varsa otomatik scroll yap
  if (window.location.hash === '#kesfedin') {
    setTimeout(() => {
      const targetSection = document.getElementById('kesfedin');
      if (targetSection) {
        targetSection.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }
    }, 1000); // 1 saniye bekle
  }
});


// suggestions.js dosyasında bu satırı bulun (satır 375 civarında):

// YENİ FONKSIYON: Kaydedilmiş içerikler için event listener'ları ekle
function addSavedContentEventListeners() {
  // İçerik kartlarına tıklama olayı
  document.querySelectorAll('#allElementsContents .content-card').forEach(card => {
    card.addEventListener('click', function(e) {
      if (!e.target.closest('.save-button-header')) {
        const contentId = this.dataset.contentId;
        openContentModal(contentId); // ← BU SATIRI DEĞİŞTİRDİK (openContent → openContentModal)
      }
    });
  });
  
  // Kaydet butonlarına olay (kaydedilmiş içeriklerde kaldırma işlemi)
  document.querySelectorAll('#allElementsContents .save-button-header').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const contentId = this.dataset.contentId;
      toggleSaveFromSavedList(contentId, this);
    });
  });
}