// Глобальные переменные
let selectedFiles = [];
let currentModalIndex = 0;
let modalMediaList = [];

// Константы
const ANIMATION_DURATION = 300;
const VIDEO_EXTENSIONS = ['.mp4', '.mov', '.webm'];

// Очистка формы после отправки
function clearForm() {
    selectedFiles = [];
    const mediaInput = document.getElementById('mediaInput');
    if (mediaInput) {
        mediaInput.value = '';
    }
    updateMediaPreview();
    
    // Очищаем текстовое поле
    const contentInput = document.querySelector('.custom-input');
    if (contentInput) {
        contentInput.value = '';
    }

    if (typeof postBtn === 'function') {
        postBtn();
    }
}

// Инициализация при загрузке страницы
function initialize() {
    initializeMediaUpload();
    if (typeof postBtn === 'function') {
        postBtn();
    }
    initializeModalHandlers();
    initializeFormSubmission();
}

// Ждем полной загрузки включая стили
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}

// Инициализация обработки отправки формы
function initializeFormSubmission() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Проверка, что файлы синхронизированы с input
            updateFileInput();
            
            // Добавляем индикатор загрузки
            const submitButton = document.getElementById('postButton');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Posting';
                
                // Возвращаем обычное состояние через 5 секунд (на случай ошибки)
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Post';
                }, 5000);
            }
        });
    }
}

// Инициализация загрузки медиа
function initializeMediaUpload() {
    const mediaInput = document.getElementById('mediaInput');
    const galleryBtn = document.getElementById('galleryBtn');
    
    if (mediaInput) {
        mediaInput.addEventListener('change', handleFileSelect);
    }
    
    if (galleryBtn) {
        galleryBtn.addEventListener('click', function(e) {
            e.preventDefault();
            // Сбрасываем значение input'а перед открытием диалога
            // чтобы событие change сработало даже при выборе тех же файлов
            mediaInput.value = '';
            mediaInput.click();
        });
    }
}

// Обработка выбора файлов
function handleFileSelect(event) {
    const newFiles = Array.from(event.target.files);
    
    // Добавляем только новые файлы к уже выбранным
    newFiles.forEach(file => {
        if (isValidFile(file)) {
            // Проверяем, нет ли уже такого файла (по имени и размеру)
            const isDuplicate = selectedFiles.some(existingFile => 
                existingFile.name === file.name && existingFile.size === file.size
            );
            
            if (!isDuplicate) {
                selectedFiles.push(file);
            }
        }
    });
    
    updateMediaPreview();
    updateFileInput(); // Синхронизируем input с массивом файлов
    
    if (typeof postBtn === 'function') {
        postBtn();
    }
}

// Проверка является ли файл видео по URL
function isVideoFile(url) {
    const lowerUrl = url.toLowerCase();
    return VIDEO_EXTENSIONS.some(ext => lowerUrl.includes(ext));
}

// Валидация файла
function isValidFile(file) {
    const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const allowedVideoTypes = ['video/mp4', 'video/quicktime', 'video/webm'];
    
    const maxImageSize = 10 * 1024 * 1024; // 10MB
    const maxVideoSize = 300 * 1024 * 1024; // 300MB
    
    if (allowedImageTypes.includes(file.type)) {
        if (file.size > maxImageSize) {
            showError(`Image file "${file.name}" is too large. Maximum size is 10MB.`);
            return false;
        }
        return true;
    }
    
    if (allowedVideoTypes.includes(file.type)) {
        if (file.size > maxVideoSize) {
            showError(`Video file "${file.name}" is too large. Maximum size is 300MB.`);
            return false;
        }
        return true;
    }
    
    showError(`File type of "${file.name}" is not supported.`);
    return false;
}

// Обновление превью медиа
function updateMediaPreview() {
    const container = document.getElementById('mediaPreviewContainer');
    const preview = document.getElementById('mediaPreview');
    
    if (!container || !preview) return;
    
    if (selectedFiles.length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.style.display = 'block';
    preview.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const previewItem = createPreviewItem(file, index);
        preview.appendChild(previewItem);
    });

    postBtn();
}

// Создание элемента превью
function createPreviewItem(file, index) {
    const item = document.createElement('div');
    item.className = 'media-preview-item';
    
    const mediaElement = document.createElement(file.type.startsWith('video/') ? 'video' : 'img');
    const url = URL.createObjectURL(file);
    
    if (file.type.startsWith('video/')) {
        mediaElement.src = url;
        mediaElement.muted = true;
        mediaElement.preload = 'metadata';
    } else {
        mediaElement.src = url;
        mediaElement.alt = file.name;
    }
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-media-btn';
    removeBtn.innerHTML = '×';
    removeBtn.onclick = () => removeFile(index);
    
    item.appendChild(mediaElement);
    item.appendChild(removeBtn);
    
    return item;
}

// Удаление файла
function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileInput();
    updateMediaPreview();
    
    if (typeof postBtn === 'function') {
        postBtn();
    }
}

// Обновление input файлов
function updateFileInput() {
    const mediaInput = document.getElementById('mediaInput');
    if (!mediaInput) return;
    
    const dt = new DataTransfer();
    selectedFiles.forEach(file => dt.items.add(file));
    mediaInput.files = dt.files;
}

// Инициализация модальных окон
function initializeModalHandlers() {
    // Закрытие модального окна при клике вне контента
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('media-modal')) {
            closeMediaModal();
        }
        if (e.target.classList.contains('modal-content-container')) {
            closeMediaModal();
        }
    });
    
    // Закрытие по Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMediaModal();
        }
        if (e.key === 'ArrowLeft') {
            navigateModal(-1);
        }
        if (e.key === 'ArrowRight') {
            navigateModal(1);
        }
    });
}

// Открытие модального окна для медиа
function openMediaModal(mediaUrls, startIndex = 0) {
    modalMediaList = Array.isArray(mediaUrls) ? mediaUrls : [mediaUrls];
    currentModalIndex = startIndex;
    
    let modal = document.getElementById('mediaModal');
    
    if (!modal) {
        modal = createMediaModal();
        document.body.appendChild(modal);
    }
    
    updateModalContent();
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Предотвращаем скролл фона
}

// Создание модального окна
function createMediaModal() {
    const modal = document.createElement('div');
    modal.id = 'mediaModal';
    modal.className = 'media-modal';
    
    modal.innerHTML = `
        <div class="modal-content-container">
            <span class="modal-close" onclick="closeMediaModal()">&times;</span>
            <button class="modal-nav modal-prev" onclick="navigateModal(-1)">❮</button>
            <button class="modal-nav modal-next" onclick="navigateModal(1)">❯</button>
            <img id="modalImage" class="modal-media" style="display: none;">
            <video id="modalVideo" class="modal-media" controls style="display: none;">
                <source id="modalVideoSource" src="" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="modal-thumbnails" id="modalThumbnails"></div>
        </div>
    `;
    
    return modal;
}

// Обновление содержимого модального окна
function updateModalContent() {
    const modalImage = document.getElementById('modalImage');
    const modalVideo = document.getElementById('modalVideo');
    const modalVideoSource = document.getElementById('modalVideoSource');
    const prevBtn = document.querySelector('.modal-prev');
    const nextBtn = document.querySelector('.modal-next');
    
    if (!modalImage || !modalVideo) return;
    
    const currentMedia = modalMediaList[currentModalIndex];
    const isVideo = currentMedia.toLowerCase().includes('.mp4') || 
                   currentMedia.toLowerCase().includes('.avi') || 
                   currentMedia.toLowerCase().includes('.mov') ||
                   currentMedia.toLowerCase().includes('.webm');
    
    if (isVideo) {
        modalVideoSource.src = currentMedia;
        modalVideo.load();
        modalVideo.style.display = 'block';
        modalImage.style.display = 'none';
    } else {
        modalImage.src = currentMedia;
        modalImage.style.display = 'block';
        modalVideo.style.display = 'none';
    }
    
    // Показываем навигацию только если больше одного медиа
    const showNav = modalMediaList.length > 1;
    prevBtn.style.display = showNav ? 'block' : 'none';
    nextBtn.style.display = showNav ? 'block' : 'none';
    
    // Обновляем мини-галерею
    updateThumbnails();
}

// Обновление мини-галереи
function updateThumbnails() {
    const thumbnailsContainer = document.getElementById('modalThumbnails');
    if (!thumbnailsContainer) return;
    
    if (modalMediaList.length <= 1) {
        thumbnailsContainer.style.display = 'none';
        return;
    }
    
    // Если превью уже созданы, просто обновляем активный класс
    const existingThumbs = thumbnailsContainer.querySelectorAll('.modal-thumbnail');
    if (existingThumbs.length === modalMediaList.length) {
        existingThumbs.forEach((thumb, index) => {
            if (index === currentModalIndex) {
                thumb.classList.add('active');
            } else {
                thumb.classList.remove('active');
            }
        });
        requestAnimationFrame(() => centerActiveThumbnail());
        return;
    }
    
    // Иначе создаём превью с нуля
    thumbnailsContainer.style.display = 'flex';
    thumbnailsContainer.innerHTML = '';
    
    // Добавляем пустые отступы для центрирования
    const spacer = document.createElement('div');
    spacer.style.minWidth = 'calc(50% - 30px)';
    spacer.style.flexShrink = '0';
    thumbnailsContainer.appendChild(spacer);
    
    modalMediaList.forEach((mediaUrl, index) => {
        const isVideo = isVideoFile(mediaUrl);
        
        const thumb = document.createElement(isVideo ? 'video' : 'img');
        thumb.className = 'modal-thumbnail';
        if (index === currentModalIndex) thumb.classList.add('active');
        thumb.src = mediaUrl;
        if (isVideo) {
            thumb.muted = true;
            thumb.preload = 'metadata';
        }
        thumb.onclick = () => {
            currentModalIndex = index;
            updateModalContent();
        };
        
        thumbnailsContainer.appendChild(thumb);
    });
    
    // Добавляем конечный отступ
    const spacerEnd = document.createElement('div');
    spacerEnd.style.minWidth = 'calc(50% - 30px)';
    spacerEnd.style.flexShrink = '0';
    thumbnailsContainer.appendChild(spacerEnd);
    
    // Центрируем активное превью после отрисовки DOM
    requestAnimationFrame(() => centerActiveThumbnail());
}

// Центрирование активного превью
function centerActiveThumbnail() {
    const thumbnailsContainer = document.getElementById('modalThumbnails');
    if (!thumbnailsContainer) return;
    
    const activeThumbnail = thumbnailsContainer.querySelector('.modal-thumbnail.active');
    if (!activeThumbnail) return;
    
    // Проверка, что элементы полностью отрисованы и стили загружены
    const computedStyle = window.getComputedStyle(activeThumbnail);
    if (computedStyle.width === '0px' || activeThumbnail.offsetWidth === 0) {
        requestAnimationFrame(() => centerActiveThumbnail());
        return;
    }
    
    const containerWidth = thumbnailsContainer.offsetWidth;
    const thumbnailLeft = activeThumbnail.offsetLeft;
    const thumbnailWidth = activeThumbnail.offsetWidth;
    
    // Вычисляем позицию для центрирования
    const targetScroll = thumbnailLeft - (containerWidth / 2) + (thumbnailWidth / 2);
    const startScroll = thumbnailsContainer.scrollLeft;
    const distance = targetScroll - startScroll;
    let startTime = null;
    
    function animation(currentTime) {
        if (!startTime) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / ANIMATION_DURATION, 1);
        
        // Easing function (easeInOutQuad)
        const ease = progress < 0.5 
            ? 2 * progress * progress 
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        
        thumbnailsContainer.scrollLeft = startScroll + (distance * ease);
        
        if (progress < 1) {
            requestAnimationFrame(animation);
        }
    }
    
    requestAnimationFrame(animation);
}

// Навигация в модальном окне
function navigateModal(direction) {
    if (modalMediaList.length <= 1) return;
    
    currentModalIndex = (currentModalIndex + direction + modalMediaList.length) % modalMediaList.length;
    updateModalContent();
}

// Закрытие модального окна
function closeMediaModal() {
    const modal = document.getElementById('mediaModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Возвращаем скролл
        
        // Останавливаем видео если воспроизводится
        const modalVideo = document.getElementById('modalVideo');
        if (modalVideo) {
            modalVideo.pause();
        }
    }
}

// Обработка отображения медиа в постах
function setupPostMediaDisplay() {
    document.querySelectorAll('.clickable-media').forEach(img => {
        img.addEventListener('click', function() {
            const mediaItem = this.closest('.post-media-item');
            const postId = mediaItem.dataset.postId;
            const mediaIndex = parseInt(mediaItem.dataset.mediaIndex);
            
            const mediaDataScript = document.querySelector(`.post-media-data[data-post-id="${postId}"]`);
            if (mediaDataScript) {
                const mediaUrls = JSON.parse(mediaDataScript.textContent);
                openMediaModal(mediaUrls, mediaIndex);
            }
        });
    });
    
    // Обработка кликов на видео в постах - только открытие галереи
    document.querySelectorAll('.post-media-item video').forEach(video => {
        video.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const mediaItem = this.closest('.post-media-item');
            const postId = mediaItem.dataset.postId;
            const mediaIndex = parseInt(mediaItem.dataset.mediaIndex);
            
            const mediaDataScript = document.querySelector(`.post-media-data[data-post-id="${postId}"]`);
            if (mediaDataScript) {
                const mediaUrls = JSON.parse(mediaDataScript.textContent);
                openMediaModal(mediaUrls, mediaIndex);
            }
        });
    });
    
    // Обработка клика на счетчик дополнительных медиа
    document.querySelectorAll('.media-count-overlay').forEach(overlay => {
        overlay.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const mediaIndex = parseInt(this.dataset.mediaIndex);
            
            const mediaDataScript = document.querySelector(`.post-media-data[data-post-id="${postId}"]`);
            if (mediaDataScript) {
                const mediaUrls = JSON.parse(mediaDataScript.textContent);
                openMediaModal(mediaUrls, mediaIndex);
            }
        });
    });
}

// Показ ошибки
function showError(message) {
    // Создаем или обновляем элемент для показа ошибок
    let errorDiv = document.getElementById('media-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'media-error';
        errorDiv.style.cssText = `
            background-color: #ff4444;
            color: white;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            display: none;
        `;
        
        const container = document.getElementById('mediaPreviewContainer');
        if (container) {
            container.parentNode.insertBefore(errorDiv, container);
        } else {
            const form = document.querySelector('form');
            if (form) {
                form.appendChild(errorDiv);
            }
        }
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Скрываем ошибку через 5 секунд
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Вызываем настройку отображения медиа в постах после загрузки
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupPostMediaDisplay);
} else {
    setupPostMediaDisplay();
}

// Также настраиваем для динамически загружаемого контента
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    const mediaItems = node.querySelectorAll('.post-media-item img');
                    if (mediaItems.length > 0) {
                        setupPostMediaDisplay();
                    }
                }
            });
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

// Экспортируем функции для глобального использования
window.openMediaModal = openMediaModal;
window.closeMediaModal = closeMediaModal;
window.navigateModal = navigateModal;
