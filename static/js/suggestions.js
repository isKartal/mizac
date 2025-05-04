document.addEventListener('DOMContentLoaded', function() {
    // ----- DEĞİŞKENLER -----
    let allContents = []; // Tüm içerikler
    let filteredContents = []; // Filtrelenmiş içerikler
    
    // Sayfalama değişkenleri - kişisel içerikler
    const itemsPerPage = 3; // DEĞİŞTİRİLDİ: 6'dan 3'e düşürüldü
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
    const personalizedContents = document.getElementById('personalizedContents');
    const allElementsContents = document.getElementById('allElementsContents');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const contentModal = document.getElementById('contentModal');
    const filterContainer = document.getElementById('filterContainer');
    
    // ----- FİLTRE YAPIŞKAN DAVRANIŞI -----
    window.addEventListener('scroll', function() {
      if (filterContainer) {
        if (window.scrollY > 300) {
          filterContainer.classList.add('scrolled');
        } else {
          filterContainer.classList.remove('scrolled');
        }
      }
    });
    
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
        if (personalizedContents) {
          personalizedContents.style.opacity = '0';
          personalizedContents.style.transform = 'translateY(20px)';
          
          setTimeout(() => {
            personalizedContents.style.opacity = '1';
            personalizedContents.style.transform = 'translateY(0)';
          }, 300);
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
        if (personalizedContents) {
          personalizedContents.style.opacity = '0';
          personalizedContents.style.transform = 'translateY(20px)';
          
          setTimeout(() => {
            personalizedContents.style.opacity = '1';
            personalizedContents.style.transform = 'translateY(0)';
          }, 300);
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
          allElementsContents.style.transform = 'translateY(20px)';
          
          setTimeout(() => {
            allElementsContents.style.opacity = '1';
            allElementsContents.style.transform = 'translateY(0)';
          }, 300);
        }
      });
    });
    
    // ----- KİŞİSEL İÇERİKLERİ FİLTRELEME FONKSİYONU -----
    function filterPersonalizedContents() {
      // Sayfalamayı sıfırla
      currentPage = 1;
      
      // İçerikleri filtrele
      let filtered = Array.from(personalizedContents.querySelectorAll('.content-card'));
      
      // Kategori filtreleme
      if (activeCategory !== 'all') {
        filtered = filtered.filter(card => card.dataset.category === activeCategory);
      }
      
      // Önce tüm kartları gizle
      personalizedContents.querySelectorAll('.content-card').forEach(card => {
        card.style.display = 'none';
      });
      
      // Sırala
      if (activeSort === 'popular') {
        filtered.sort((a, b) => {
          const aLikes = parseInt(a.querySelector('.like-count').textContent) || 0;
          const bLikes = parseInt(b.querySelector('.like-count').textContent) || 0;
          return bLikes - aLikes;
        });
      } else {
        // Varsayılan "en yeni" sıralamasını backend'den koru
      }
      
      // Toplam sayfa sayısını hesapla
      totalPages = Math.ceil(filtered.length / itemsPerPage);
      
      // Sayfa numaralarını güncelle
      updatePageNumbers();
      
      // İlk sayfadaki içerikleri göster
      const start = (currentPage - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      filtered.slice(start, end).forEach(card => {
        card.style.display = '';
      });
      
      // Sayfalama butonlarını güncelle
      updatePaginationButtons();
      
      // Sayfalama kontrollerini göster veya gizle
      const paginationControls = document.querySelector('.pagination-controls');
      if (paginationControls) {
        if (filtered.length > itemsPerPage) {
          paginationControls.style.display = 'flex';
        } else {
          paginationControls.style.display = 'none';
        }
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
    function updatePageNumbers() {
      const pageNumbers = document.getElementById('pageNumbers');
      if (!pageNumbers) return;
      
      pageNumbers.innerHTML = '';
      
      for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.className = 'page-button' + (i === currentPage ? ' active' : '');
        pageButton.textContent = i;
        pageButton.addEventListener('click', () => {
          gotoPage(i);
        });
        pageNumbers.appendChild(pageButton);
      }
    }
    
    // Tüm içerikler için sayfa numaralarını güncelle
    function updateAllPageNumbers() {
      const pageNumbers = document.getElementById('allPageNumbers');
      if (!pageNumbers) return;
      
      pageNumbers.innerHTML = '';
      
      for (let i = 1; i <= allTotalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.className = 'page-button' + (i === allCurrentPage ? ' active' : '');
        pageButton.textContent = i;
        pageButton.addEventListener('click', () => {
          gotoAllPage(i);
        });
        pageNumbers.appendChild(pageButton);
      }
    }
    
    // Sayfalama butonlarını güncelle
    function updatePaginationButtons() {
      const prevPageBtn = document.getElementById('prevPage');
      const nextPageBtn = document.getElementById('nextPage');
      
      if (prevPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
      }
      
      if (nextPageBtn) {
        nextPageBtn.disabled = currentPage === totalPages;
      }
    }
    
    // Tüm içerikler için sayfalama butonlarını güncelle
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
    
    // Belirli bir sayfaya git
    function gotoPage(page) {
      if (page < 1 || page > totalPages) return;
      
      currentPage = page;
      
      // İçerikleri filtrele
      let filtered = Array.from(personalizedContents.querySelectorAll('.content-card'));
      
      // Kategori filtreleme
      if (activeCategory !== 'all') {
        filtered = filtered.filter(card => card.dataset.category === activeCategory);
      }
      
      // Sırala
      if (activeSort === 'popular') {
        filtered.sort((a, b) => {
          const aLikes = parseInt(a.querySelector('.like-count').textContent) || 0;
          const bLikes = parseInt(b.querySelector('.like-count').textContent) || 0;
          return bLikes - aLikes;
        });
      }
      
      // Tüm kartları gizle
      personalizedContents.querySelectorAll('.content-card').forEach(card => {
        card.style.display = 'none';
      });
      
      // Mevcut sayfadaki kartları göster
      const start = (currentPage - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      filtered.slice(start, end).forEach(card => {
        card.style.display = '';
      });
      
      // Sayfa numaralarını güncelle
      updatePageNumbers();
      
      // Sayfalama butonlarını güncelle
      updatePaginationButtons();
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
    }
    
    // ----- SAYFALAMA BUTONLARINA OLAY EKLE -----
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn) {
      prevPageBtn.addEventListener('click', function() {
        gotoPage(currentPage - 1);
      });
    }
    
    if (nextPageBtn) {
      nextPageBtn.addEventListener('click', function() {
        gotoPage(currentPage + 1);
      });
    }
    
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
      pageContents.forEach(content => {
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
          <p class="content-description">${content.short_description ? content.short_description.substring(0, 100) + (content.short_description.length > 100 ? '...' : '') : ''}</p>
          <div class="content-actions">
            <button class="action-button like-button ${content.is_liked ? 'liked' : ''}" 
                    data-content-id="${content.id}">
              <i class="${content.is_liked ? 'fas' : 'far'} fa-heart"></i>
              <span class="like-count">${content.like_count || 0}</span>
            </button>
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
        
        // Beğenme butonuna olay ekle
        card.querySelector('.like-button').addEventListener('click', function(e) {
          e.stopPropagation();
          toggleLike(content.id, this);
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
        }, 100 * (pageContents.indexOf(content) + 1));
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
          
          // Element bilgisini göster
          document.getElementById('modalElement').textContent = data.related_element;
          document.getElementById('modalElement').className = `modal-element ${data.related_element.toLowerCase()}`;
          
          // Beğenme durumunu güncelle
          const likeBtn = document.getElementById('modalLikeBtn');
          likeBtn.dataset.contentId = contentId;
          likeBtn.className = `modal-action-btn${data.liked ? ' liked' : ''}`;
          likeBtn.innerHTML = data.liked ? 
            '<i class="fas fa-heart"></i> Beğenildi' : 
            '<i class="far fa-heart"></i> Beğen';
          
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
    
    // Modal butonlarına olay ekle
    document.getElementById('modalLikeBtn').addEventListener('click', function() {
      toggleLike(this.dataset.contentId, this);
    });
    
    document.getElementById('modalSaveBtn').addEventListener('click', function() {
      toggleSave(this.dataset.contentId, this);
    });
    
    // ----- BEĞENME/KAYDETME FONKSİYONLARI -----
    // Beğenme işlevi
    function toggleLike(contentId, button) {
      fetch(`/profiles/content/${contentId}/toggle_like/`, {
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
          // Beğenme durumunu güncelle
          updateLikeStatus(contentId, data.liked, data.like_count);
        }
      })
      .catch(error => console.error('Hata:', error));
    }
    
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
    
    // Beğenme durumunu güncelle
    function updateLikeStatus(contentId, isLiked, likeCount) {
      // Kart butonlarını güncelle
      const likeButtons = document.querySelectorAll(`.like-button[data-content-id="${contentId}"]`);
      likeButtons.forEach(btn => {
        btn.classList.toggle('liked', isLiked);
        const icon = btn.querySelector('i');
        icon.className = isLiked ? 'fas fa-heart' : 'far fa-heart';
        
        const countSpan = btn.querySelector('.like-count');
        if (countSpan) {
          countSpan.textContent = likeCount;
        }
      });
      
      // Modal butonunu güncelle
      const modalLikeBtn = document.getElementById('modalLikeBtn');
      if (modalLikeBtn.dataset.contentId === contentId) {
        modalLikeBtn.classList.toggle('liked', isLiked);
        modalLikeBtn.innerHTML = isLiked ? 
          '<i class="fas fa-heart"></i> Beğenildi' : 
          '<i class="far fa-heart"></i> Beğen';
      }
      
      // Tüm içerikler dizisinde ilgili içeriği güncelle
      const contentIndex = allContents.findIndex(c => c.id == contentId);
      if (contentIndex !== -1) {
        allContents[contentIndex].is_liked = isLiked;
        allContents[contentIndex].like_count = likeCount;
      }
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
      if (modalSaveBtn.dataset.contentId === contentId) {
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
    
    // ----- SAYFA İNİT -----
    // Kişisel içerik kartlarına tıklama olayı ekle
    if (personalizedContents) {
      Array.from(personalizedContents.querySelectorAll('.content-card')).forEach(card => {
        card.addEventListener('click', function(e) {
          if (!e.target.closest('.action-button')) {
            openContentModal(this.dataset.contentId);
          }
        });
      });
    
      // Beğenme butonlarına olay ekle
      personalizedContents.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function(e) {
          e.stopPropagation();
          toggleLike(this.dataset.contentId, this);
        });
      });
      
      // Kaydetme butonlarına olay ekle
      personalizedContents.querySelectorAll('.save-button').forEach(button => {
        button.addEventListener('click', function(e) {
          e.stopPropagation();
          toggleSave(this.dataset.contentId, this);
        });
      });
    }
    
    // Kişisel içerikler için sayfalamayı başlat
    filterPersonalizedContents();
    
    // Tüm içerikleri getir ve göster
    fetchAllContents();
    
    // Kaydırma animasyonları için gözlemci ekle
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.content-card').forEach(card => {
      observer.observe(card);
      card.classList.add('animated');
    });
  });