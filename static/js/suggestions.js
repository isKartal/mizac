// ==========================================================================
// SAYFA YÜKLENDİĞİNDE ÇALIŞACAK ANA FONKSİYON
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
  
  // ========================================================================
  // FİLTRE YAPIŞKAN DAVRANIŞI
  // ========================================================================
  
  /**
   * Sayfa kaydırıldığında filtrelerin yapışkan davranışını kontrol eder
   */
  window.addEventListener('scroll', function() {
    // Ana filtre konteyner için
    if (filterContainer) {
      if (window.scrollY > 300) {
        filterContainer.classList.add('scrolled');
      } else {
        filterContainer.classList.remove('scrolled');
      }
    }
    
    // İkincil filtre konteyner için
    if (secondaryFilterContainer) {
      if (window.scrollY > 700) {
        secondaryFilterContainer.classList.add('scrolled');
      } else {
        secondaryFilterContainer.classList.remove('scrolled');
      }
    }
  });
  
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
    // Sol kaydırma butonu
    if (prevSlideButton) {
      prevSlideButton.addEventListener('click', function() {
        scrollSlider('left');
      });
    }
    
    // Sağ kaydırma butonu
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
    
    // Sol butonu güncelle
    if (prevSlideButton) {
      const isAtStart = scrollLeft <= 10;
      prevSlideButton.style.opacity = isAtStart ? "0.5" : "1";
      prevSlideButton.style.pointerEvents = isAtStart ? "none" : "all";
    }
    
    // Sağ butonu güncelle
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
    
    // Sayfa yüklendiğinde butonları güncelle
    setTimeout(function() {
      updateSliderButtons();
    }, 100);
  }
  
  // ========================================================================
  // FİLTRE BUTONLARI İÇİN OLAY DİNLEYİCİLERİ
  // ========================================================================
  
  /**
   * Kategori filtre butonlarına olay dinleyicilerini ekler
   */
  function initCategoryFilters() {
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
        addSliderAnimation();
      });
    });
  }
  
  /**
   * Sıralama filtre butonlarına olay dinleyicilerini ekler
   */
  function initSortFilters() {
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
        addSliderAnimation();
      });
    });
  }
  
  /**
   * Element sekmesi filtre butonlarına olay dinleyicilerini ekler
   */
  function initElementFilters() {
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
        addContentAnimation();
      });
    });
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
  // KİŞİSEL İÇERİKLERİ FİLTRELEME FONKSİYONU
  // ========================================================================
  
  /**
   * Kişisel içerikleri filtreler ve gösterir
   */
  function filterPersonalizedContents() {
    if (!contentSlider) return;
    
    // Tüm kartları al
    const allCards = Array.from(contentSlider.querySelectorAll('.slider-card'));
    
    // Kategori filtreleme uygula
    let filteredCards = allCards;
    if (activeCategory !== 'all') {
      filteredCards = allCards.filter(card => 
        card.dataset.category === activeCategory
      );
    }
    
    // Tüm kartları gizle
    allCards.forEach(card => {
      card.style.display = 'none';
    });
    
    // Mevcut boş mesajları temizle
    const existingEmptyMessages = contentSlider.querySelectorAll('.empty-slider-message');
    existingEmptyMessages.forEach(msg => msg.remove());
    
    // Filtrelenmiş kartları göster
    if (filteredCards.length > 0) {
      filteredCards.forEach(card => {
        card.style.display = '';
        contentSlider.appendChild(card); // Sıralamayı uygulamak için DOM'a tekrar ekle
      });
    } else {
      // Hiç kart yoksa boş mesaj göster
      showEmptySliderMessage();
    }
    
    // Slider'ı başa sıfırla
    contentSlider.scrollLeft = 0;
    
    // Butonları güncelle
    updateSliderButtons();
  }
  
  /**
   * Slider için boş durum mesajı gösterir
   */
  function showEmptySliderMessage() {
    const emptyMessage = document.createElement('div');
    emptyMessage.className = 'empty-slider-message';
    emptyMessage.innerHTML = `
      <div class="empty-icon">
        <i class="fas fa-search"></i>
      </div>
      <p class="empty-text">Bu filtrelere uygun içerik bulunamadı.</p>
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
    // Sayfalamayı sıfırla
    allCurrentPage = 1;
    
    // Element filtreleme uygula
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
    
    // Sayfalama kontrollerini güncelle
    updateAllPageNumbers();
    updateAllPaginationButtons();
    updatePaginationVisibility();
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
  // SAYFALAMA FONKSİYONLARI
  // ========================================================================
  
  /**
   * Sayfa numaralarını günceller
   */
  function updateAllPageNumbers() {
    const pageNumbers = document.getElementById('allPageNumbers');
    if (!pageNumbers) return;
    
    pageNumbers.innerHTML = '';
    
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
      addPageButton(pageNumbers, 1);
      
      // Arada çok fazla sayfa varsa ... ekle
      if (startPage > 2) {
        addPageEllipsis(pageNumbers);
      }
    }
    
    // Sayfa numaralarını oluştur
    for (let i = startPage; i <= endPage; i++) {
      addPageButton(pageNumbers, i, i === allCurrentPage);
    }
    
    // Son sayfa bağlantısı ekle
    if (endPage < allTotalPages) {
      // Arada çok fazla sayfa varsa ... ekle
      if (endPage < allTotalPages - 1) {
        addPageEllipsis(pageNumbers);
      }
      
      addPageButton(pageNumbers, allTotalPages);
    }
  }
  
  /**
   * Sayfa butonu ekler
   * @param {Element} container - Butonun ekleneceği konteyner
   * @param {number} pageNumber - Sayfa numarası
   * @param {boolean} isActive - Aktif sayfa olup olmadığı
   */
  function addPageButton(container, pageNumber, isActive = false) {
    const pageButton = document.createElement('button');
    pageButton.className = `page-button${isActive ? ' active' : ''}`;
    pageButton.textContent = pageNumber;
    pageButton.addEventListener('click', () => {
      gotoAllPage(pageNumber);
    });
    container.appendChild(pageButton);
  }
  
  /**
   * Sayfa numaraları arasına üç nokta ekler
   * @param {Element} container - Üç noktanın ekleneceği konteyner
   */
  function addPageEllipsis(container) {
    const ellipsis = document.createElement('span');
    ellipsis.className = 'page-ellipsis';
    ellipsis.textContent = '...';
    container.appendChild(ellipsis);
  }
  
  /**
   * Sayfalama butonlarını günceller
   */
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
  
  /**
   * Belirtilen sayfaya gider
   * @param {number} page - Gidilecek sayfa numarası
   */
  function gotoAllPage(page) {
    if (page < 1 || page > allTotalPages) return;
    
    allCurrentPage = page;
    
    // İçerikleri göster
    renderAllContents();
    
    // Sayfalama kontrollerini güncelle
    updateAllPageNumbers();
    updateAllPaginationButtons();
    
    // Sayfa başına kaydır
    if (allElementsContents) {
      allElementsContents.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
      });
    }
  }
  
  /**
   * Sayfalama butonlarına olay dinleyicilerini ekler
   */
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
  // AJAX İLE İÇERİK ALMA FONKSİYONLARI
  // ========================================================================
  
  /**
   * AJAX ile tüm içerikleri getirir
   */
  function fetchAllContents() {
    showLoadingIndicator();
    
    fetch('/profiles/api/all_contents/')
      .then(response => {
        if (!response.ok) {
          throw new Error('İçerikler alınırken hata oluştu');
        }
        return response.json();
      })
      .then(data => {
        hideLoadingIndicator();
        
        // Tüm içerikleri diziye aktar
        allContents = data.contents;
        
        // Filtreleme yap ve içerikleri göster
        filterAllContents();
      })
      .catch(error => {
        console.error('Hata:', error);
        hideLoadingIndicator();
        showErrorMessage();
      });
  }
  
  /**
   * Yükleniyor göstergesini gösterir
   */
  function showLoadingIndicator() {
    if (loadingIndicator) {
      loadingIndicator.style.display = 'flex';
    }
    if (allElementsContents) {
      allElementsContents.style.display = 'none';
    }
  }
  
  /**
   * Yükleniyor göstergesini gizler
   */
  function hideLoadingIndicator() {
    if (loadingIndicator) {
      loadingIndicator.style.display = 'none';
    }
    if (allElementsContents) {
      allElementsContents.style.display = 'grid';
    }
    
    const pagination = document.getElementById('allContentsPagination');
    if (pagination) {
      pagination.style.display = 'flex';
    }
  }
  
  /**
   * Hata mesajı gösterir
   */
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
  // TÜM MİZAÇLAR İÇİN İÇERİKLERİ GÖSTERME
  // ========================================================================
  
  /**
   * Tüm mizaçlar için içerikleri render eder
   */
  function renderAllContents() {
    if (!allElementsContents) return;
    
    allElementsContents.innerHTML = '';
    
    // İçerik yoksa boş durum mesajı göster
    if (filteredContents.length === 0) {
      showEmptyContentMessage();
      return;
    }
    
    // Sayfalama için içerikleri filtrele
    const start = (allCurrentPage - 1) * allItemsPerPage;
    const end = start + allItemsPerPage;
    const pageContents = filteredContents.slice(start, end);
    
    // Kartları oluştur ve ekle
    pageContents.forEach((content, index) => {
      const card = createContentCard(content, index);
      allElementsContents.appendChild(card);
    });
  }
  
  /**
   * Boş içerik mesajı gösterir
   */
  function showEmptyContentMessage() {
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
  }
  
  /**
   * İçerik kartı oluşturur (Kaydet butonu başlık sağında)
   * @param {Object} content - İçerik verisi
   * @param {number} index - Kart sırası (animasyon için)
   * @returns {Element} Oluşturulan kart elementi
   */
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
      
      <!-- Yeni Header Yapısı: Başlık ve Kaydet Butonu Yan Yana -->
      <div class="content-header">
        <h3 class="content-title">${content.title}</h3>
        <button class="save-button-header ${content.is_saved ? 'saved' : ''}" 
                data-content-id="${content.id}"
                title="${content.is_saved ? 'Kaydedildi' : 'Kaydet'}">
          <i class="${content.is_saved ? 'fas' : 'far'} fa-bookmark"></i>
        </button>
      </div>
    `;
    
    // Olay dinleyicilerini ekle
    addCardEventListeners(card, content);
    
    // Animasyon için sınıf ekle
    setTimeout(() => {
      card.classList.add('visible');
    }, 50 * (index + 1));
    
    return card;
  }
  
  /**
   * Kart için olay dinleyicilerini ekler (Güncellenmiş versiyon)
   * @param {Element} card - Kart elementi
   * @param {Object} content - İçerik verisi
   */
  function addCardEventListeners(card, content) {
    // Karta tıklama olayı ekle (buton hariç)
    card.addEventListener('click', function(e) {
      if (!e.target.closest('.save-button-header')) {
        openContentModal(content.id);
      }
    });
    
    // Kaydetme butonuna olay ekle
    const saveButton = card.querySelector('.save-button-header');
    if (saveButton) {
      saveButton.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(content.id, this);
      });
    }
  }
  
  // ========================================================================
  // İÇERİK DETAY MODALI FONKSİYONLARI
  // ========================================================================
  
  let currentModalContentId = null;
  
  /**
   * İçerik detay modalını açar
   * @param {number} contentId - İçerik ID'si
   */
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
        populateModal(data, contentId);
        showModal();
      })
      .catch(error => {
        console.error('Hata:', error);
        alert('İçerik yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.');
      });
  }
  
  /**
   * Modal içeriğini doldurur (BEĞENİ BUTONU KALDIRILMIŞ)
   * @param {Object} data - İçerik verisi
   * @param {number} contentId - İçerik ID'si
   */
  function populateModal(data, contentId) {
    // Modal başlığını ayarla
    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) {
      modalTitle.textContent = data.title;
    }
    
    // Kategori bilgisini göster
    const modalCategory = document.getElementById('modalCategory');
    if (modalCategory) {
      modalCategory.textContent = data.category;
    }
    
    // İçeriği göster
    const modalContent = document.getElementById('modalContent');
    if (modalContent) {
      modalContent.innerHTML = data.content;
    }
    
    // Element bilgisini göster
    const modalElement = document.getElementById('modalElement');
    if (modalElement) {
      modalElement.textContent = data.related_element;
      modalElement.className = `modal-element ${data.related_element.toLowerCase()}`;
    }
    
    // Sadece kaydetme durumunu güncelle (beğenme kaldırıldı)
    updateModalSaveButton(contentId, data.saved);
  }
  
  /**
   * Modal kaydetme butonunu günceller
   * @param {number} contentId - İçerik ID'si
   * @param {boolean} saved - Kaydetme durumu
   */
  function updateModalSaveButton(contentId, saved) {
    const saveBtn = document.getElementById('modalSaveBtn');
    if (!saveBtn) return;
    
    saveBtn.dataset.contentId = contentId;
    saveBtn.className = `modal-action-btn${saved ? ' saved' : ''}`;
    saveBtn.innerHTML = saved ? 
      '<i class="fas fa-bookmark"></i> Kaydedildi' : 
      '<i class="far fa-bookmark"></i> Kaydet';
  }
  
  /**
   * Modalı gösterir
   */
  function showModal() {
    contentModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  /**
   * Modalı gizler
   */
  function hideModal() {
    contentModal.classList.remove('active');
    document.body.style.overflow = '';
  }
  
  /**
   * Modal için olay dinleyicilerini ekler (BEĞENİ BUTONU KALDIRILMIŞ)
   */
  function initModalEventListeners() {
    // Kapatma butonu
    const closeModal = document.getElementById('closeModal');
    if (closeModal) {
      closeModal.addEventListener('click', hideModal);
    }
    
    // Modal dışına tıklama ile kapatma
    if (contentModal) {
      contentModal.addEventListener('click', function(e) {
        if (e.target === contentModal) {
          hideModal();
        }
      });
    }
    
    // ESC tuşu ile modalı kapatma
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && contentModal.classList.contains('active')) {
        hideModal();
      }
    });
    
    // Sadece kaydetme butonuna olay ekle (beğeni butonu kaldırıldı)
    const modalSaveBtn = document.getElementById('modalSaveBtn');
    if (modalSaveBtn) {
      modalSaveBtn.addEventListener('click', function() {
        toggleSave(this.dataset.contentId, this);
      });
    }
  }
  
  // ========================================================================
  // KAYDETME FONKSİYONLARI (BEĞENİ FONKSİYONLARI KALDIRILDI)
  // ========================================================================
  
  /**
   * İçeriği kaydetme/kaydetmeme işlemini yapar
   * @param {number} contentId - İçerik ID'si
   * @param {Element} button - Tıklanan buton elementi
   */
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
      }
    })
    .catch(error => {
      console.error('Kaydetme işlemi hatası:', error);
    });
  }
  
  /**
   * Tüm kaydetme butonlarının durumunu günceller (Güncellenmiş versiyon)
   * @param {number} contentId - İçerik ID'si
   * @param {boolean} isSaved - Kaydetme durumu
   */
  function updateSaveStatus(contentId, isSaved) {
    // Header kaydet butonlarını güncelle
    const saveButtons = document.querySelectorAll(`.save-button-header[data-content-id="${contentId}"]`);
    saveButtons.forEach(btn => {
      btn.classList.toggle('saved', isSaved);
      btn.title = isSaved ? 'Kaydedildi' : 'Kaydet';
      
      const icon = btn.querySelector('i');
      if (icon) {
        icon.className = isSaved ? 'fas fa-bookmark' : 'far fa-bookmark';
      }
    });
    
    // Eski save-button sınıfına sahip butonları da güncelle (geriye dönük uyumluluk)
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
    
    // Modal butonunu güncelle
    const modalSaveBtn = document.getElementById('modalSaveBtn');
    if (modalSaveBtn && modalSaveBtn.dataset.contentId === contentId) {
      updateModalSaveButton(contentId, isSaved);
    }
    
    // Veri dizisinde güncelle
    updateContentInArray(contentId, { is_saved: isSaved });
  }
  
  /**
   * İçerik dizisindeki belirli bir içeriği günceller
   * @param {number} contentId - İçerik ID'si
   * @param {Object} updates - Güncellenecek alanlar
   */
  function updateContentInArray(contentId, updates) {
    const contentIndex = allContents.findIndex(c => c.id == contentId);
    if (contentIndex !== -1) {
      Object.assign(allContents[contentIndex], updates);
    }
  }
  
  // ========================================================================
  // YARDIMCI FONKSİYONLAR
  // ========================================================================
  
  /**
   * CSRF token'ını alır
   * @param {string} name - Cookie adı
   * @returns {string|null} Cookie değeri
   */
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
  
  /**
   * Otomatik görünürlük animasyonları için gözlemci ekler
   */
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
      }, { 
        threshold: 0.1 
      });
      
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
  
  /**
   * Mobil cihazlar için kart boyutlarını ayarlar
   */
  function adjustCardSizes() {
    if (!contentSlider) return;
    
    const cards = contentSlider.querySelectorAll('.premium-card');
    if (!cards.length) return;
    
    // Ekran genişliğine göre kart genişliklerini ayarla
    cards.forEach(card => {
      if (window.innerWidth <= 768) {
        // Mobil görünüm: Her satırda 1 kart
        card.style.width = 'calc(100% - 30px)';
        card.style.maxWidth = '400px';
      } else {
        // Tablet ve masaüstü görünüm: Her satırda 2 kart
        card.style.width = 'calc(50% - 30px)';
        card.style.maxWidth = '350px';
      }
    });
    
    // Kaydırma olayını tetikle
    updateSliderButtons();
  }
  
  // ========================================================================
  // SAYFA İNİSYALİZASYON FONKSİYONLARI
  // ========================================================================
  
  /**
   * Kişisel içerik kartlarına olay dinleyicilerini ekler (GÜNCELLENMIŞ VERSİYON)
   */
  function initPersonalContentCards() {
    if (!contentSlider) return;
    
    // Kartlara tıklama olayı ekle
    const sliderCards = contentSlider.querySelectorAll('.slider-card');
    sliderCards.forEach(card => {
      card.addEventListener('click', function(e) {
        // YENİ: save-button-header sınıfını da kontrol et
        if (!e.target.closest('.save-button-header') && !e.target.closest('.premium-action-button')) {
          openContentModal(this.dataset.contentId);
        }
      });
    });
    
    // YENİ: Header kaydet butonlarına olay ekle
    const headerSaveButtons = contentSlider.querySelectorAll('.save-button-header');
    headerSaveButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(this.dataset.contentId, this);
      });
    });
    
    // ESKİ: Eski kaydet butonlarına da olay ekle (geriye dönük uyumluluk)
    const saveButtons = contentSlider.querySelectorAll('.save-button, .premium-action-button');
    saveButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSave(this.dataset.contentId, this);
      });
    });
    
    // Slider'ı başa sıfırla
    contentSlider.scrollLeft = 0;
    
    // Butonları güncelle
    setTimeout(() => {
      updateSliderButtons();
    }, 100);
  }
  
  /**
   * Pencere boyutu değişikliklerini dinler
   */
  function initResizeListener() {
    window.addEventListener('resize', adjustCardSizes);
    window.addEventListener('load', adjustCardSizes);
  }
  
  /**
   * Sayfayı başlatır - tüm işlevleri çalıştırır
   */
  function initPage() {
    // Slider işlevselliği
    initSliderButtons();
    initSliderScrollListener();
    
    // Filtre işlevselliği
    initCategoryFilters();
    initSortFilters();
    initElementFilters();
    
    // Sayfalama işlevselliği
    initPaginationButtons();
    
    // Modal işlevselliği
    initModalEventListeners();
    
    // Kişisel içerik kartları
    initPersonalContentCards();
    
    // Responsive işlevsellik
    initResizeListener();
    
    // Tüm içerikleri getir ve göster
    if (allElementsContents && loadingIndicator) {
      fetchAllContents();
    }
    
    // Animasyon gözlemcisi ekle
    addAnimationObserver();
    
    // İlk kart boyutlarını ayarla
    adjustCardSizes();
    
    console.log('Sayfa başarıyla yüklendi ve hazır.');
  }
  
  // ========================================================================
  // SAYFA BAŞLATMA
  // ========================================================================
  
  // Sayfa yüklendiğinde tüm işlemleri başlat
  initPage();
  
});