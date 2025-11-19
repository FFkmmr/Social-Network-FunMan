// Глобальные переменные
let selectedFiles = [];
let currentModalIndex = 0;
let modalMediaList = [];

// Очистка формы после отправки
function clearForm() {
    selectedFiles = [];
    const mediaInput = document.getElementById('mediaInput');
    if (mediaInput) {
        mediaInput.value = '';
    }
    updateMediaPreview();
    updatePostButton();
    
    // Очищаем текстовое поле
    const contentInput = document.querySelector('.custom-input');
    if (contentInput) {
        contentInput.value = '';
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeMediaUpload();
    initializePostValidation();
    initializeModalHandlers();
    initializeFormSubmission();
});

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
    updatePostButton();
    updateFileInput(); // Синхронизируем input с массивом файлов
}

// Валидация файла
function isValidFile(file) {
    const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const allowedVideoTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/webm'];
    
    const maxImageSize = 5 * 1024 * 1024; // 5MB
    const maxVideoSize = 100 * 1024 * 1024; // 100MB
    
    if (allowedImageTypes.includes(file.type)) {
        if (file.size > maxImageSize) {
            showError(`Image file "${file.name}" is too large. Maximum size is 5MB.`);
            return false;
        }
        return true;
    }
    
    if (allowedVideoTypes.includes(file.type)) {
        if (file.size > maxVideoSize) {
            showError(`Video file "${file.name}" is too large. Maximum size is 100MB.`);
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
    updatePostButton();
}

// Обновление input файлов
function updateFileInput() {
    const mediaInput = document.getElementById('mediaInput');
    if (!mediaInput) return;
    
    const dt = new DataTransfer();
    selectedFiles.forEach(file => dt.items.add(file));
    mediaInput.files = dt.files;
}

// Валидация кнопки поста
function initializePostValidation() {
    const contentInput = document.querySelector('.custom-input');
    const postButton = document.getElementById('postButton');
    
    if (contentInput && postButton) {
        contentInput.addEventListener('input', updatePostButton);
        updatePostButton(); // Начальная проверка
    }
}

// Обновление состояния кнопки поста
function updatePostButton() {
    const contentInput = document.querySelector('.custom-input');
    const postButton = document.getElementById('postButton');
    
    if (!contentInput || !postButton) return;
    
    const hasContent = contentInput.value.trim().length > 0;
    // Теперь текст обязателен, медиа - опционально
    
    if (hasContent) {
        postButton.disabled = false;
        postButton.classList.add('has-content');
    } else {
        postButton.disabled = true;
        postButton.classList.remove('has-content');
    }
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
}

// Навигация в модальном окне
function navigateModal(direction) {
    if (modalMediaList.length <= 1) return;
    
    currentModalIndex += direction;
    
    if (currentModalIndex < 0) {
        currentModalIndex = modalMediaList.length - 1;
    } else if (currentModalIndex >= modalMediaList.length) {
        currentModalIndex = 0;
    }
    
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
document.addEventListener('DOMContentLoaded', setupPostMediaDisplay);

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