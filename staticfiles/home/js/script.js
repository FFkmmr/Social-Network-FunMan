// ============================================================================
// УТИЛИТЫ
// ============================================================================

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ============================================================================
// НАВИГАЦИЯ
// ============================================================================

document.addEventListener("DOMContentLoaded", function () {
    // Кнопка закрытия
    const closebtn = document.querySelector('.closebtn-index');
    if (closebtn) {
        closebtn.addEventListener('click', () => window.location.href = '../');
    }

    // Кнопка закрытия сообщений
    const closebtnmess = document.getElementById('new_comm_btn');
    if (closebtnmess) {
        closebtnmess.addEventListener('click', () => window.location.href = '../messages');
    }
    
    // Кнопка назад
    const backButton = document.querySelector(".circle-back-btn");
    if (backButton) {
        backButton.addEventListener("click", () => window.location.href = "../");
    }

    // Навигация левой панели
    const routes = {
        home: "/",
        messages: "/messages/",
        profile: "/profile/",
        // search: "/search/",
        bookmarks: "/bookmarks/",
        community: "/community/",
        lists: "/lists/",
        // post: "/post/",
    // Toggle posts
        following: "/following/",
        for_u: "/",
    };

    Object.keys(routes).forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener("click", () => window.location.href = routes[id]);
        }
    });
});

// ============================================================================
// СОЗДАНИЕ ПОСТОВ / СООБЩЕНИЙ
// ============================================================================

async function postBtn() {
    const textareaFields = document.querySelectorAll('textarea[name="body"], textarea[name="content"], textarea[name="message"], input[name="search"]');
    const submitButtons = document.querySelectorAll('.submit-button, .style-none');
    const mediaPreviewContainer = document.getElementById('mediaPreviewContainer');
    const isValidImage = mediaPreviewContainer && getComputedStyle(mediaPreviewContainer).display !== 'none';
    
    let isValidText = false;
    const searchInput = document.getElementById("user-search");
    
    if (searchInput) {
        // Валидация для страницы новых сообщений
        const searchValue = searchInput.value.trim();
        if (searchValue !== "") {
            try {
                const response = await fetch(`/validate_recipient/?username=${encodeURIComponent(searchValue)}`);
                const data = await response.json();
                isValidText = data.valid;
            } catch (error) {
                isValidText = false;
            }
        }
    } else {
        // Валидация для других страниц
        isValidText = Array.from(textareaFields).some(textarea => textarea.value.trim() !== "");
    }
    
    // Обновляем состояние кнопок
    submitButtons.forEach(button => { 
        const isActive = isValidText || isValidImage;
        button.classList.toggle('active', isActive);
        button.classList.toggle('disabled', !isActive);
        button.type = isActive ? 'submit' : 'button';
        
        if (button.classList.contains('style-none')) {
            button.src = isActive ? '/static/home/img/paper-plane.png' : '/static/home/img/paper-plane-black.png';
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const textareaFields = document.querySelectorAll('textarea[name="body"], textarea[name="content"], textarea[name="message"], input[name="search"]');
    const submitButtons = document.querySelectorAll('.submit-button, .style-none');

    // Инициализация валидации
    if (textareaFields.length > 0) {
        window.addEventListener('load', postBtn);
        textareaFields.forEach(textarea => textarea.addEventListener('input', postBtn));
    }
    
    // Обработка отправки
    submitButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            if (button.classList.contains('disabled')) {
                e.preventDefault();
                return;
            }

            const searchInput = document.getElementById("user-search");
            if (searchInput) {
                const searchValue = searchInput.value.trim();
                if (searchValue !== "") {
                    try {
                        const response = await fetch(`/validate_recipient/?username=${encodeURIComponent(searchValue)}`);
                        const data = await response.json();
                        
                        if (data.valid) {
                            window.location.href = '../new_chat/' + data.user_id;
                        } else {
                            e.preventDefault();
                            console.log('Cannot create chat:', data.reason);
                        }
                    } catch (error) {
                        console.error('Error validating user:', error);
                        e.preventDefault();
                    }
                } else {
                    e.preventDefault();
                }
            }
        });
    });

    // Поиск пользователей
    const searchInput = document.getElementById("user-search");
    const usersContainer = document.querySelector("[style*='top: 120px']");

    if (usersContainer) {
        usersContainer.addEventListener("click", async (e) => {
            const userSelect = e.target.closest(".user-select");
            if (!userSelect) return;

            const userNameElement = userSelect.querySelector(".user-select-name");
            if (userNameElement) {
                searchInput.value = userNameElement.textContent.trim();
                await postBtn();
            }
        });
    }

    if (searchInput) {
        if (searchInput.value !== "") {
            filterUsers({ target: searchInput });
        }
        searchInput.addEventListener("input", async (e) => {
            await filterUsers(e);
            await postBtn();
        });
    }

    async function filterUsers(e) {
        const response = await fetch(`/filter_users/?search=${encodeURIComponent(e.target.value)}`);
        const data = await response.json();

        usersContainer.innerHTML = data.users.map(user => {
            const formattedId = String(user.id).padStart(4, "0");
            return `
                <div style="height: fit-content;">    
                    <div class="user-select">
                        <div class="content-in-the-post" style="height: fit-content; min-height: 70px; overflow: hidden;">
                            <img class="avatar-in-post" src="/static/home/img/camera.png" alt="">  
                            <div class="post-content" style="height: fit-content;">
                                <div class="post-upside">
                                    <div class="name-user-date">
                                        <a href="/stranger_profile/${user.id}" class="user-select-name">${user.username}</a>
                                        <p>@${formattedId}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join("");
    }
});

// ============================================================================
// АВТОМАТИЧЕСКАЯ ВЫСОТА TEXTAREA
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.querySelector('textarea[name="content"]');
    
    if (textarea) {
        function adjustHeight() {
            textarea.style.height = '80px';  
            textarea.style.height = (textarea.scrollHeight) + 'px';
        }
        textarea.addEventListener('input', adjustHeight);
        adjustHeight();
    }
});

// ============================================================================
// ЛАЙКИ
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    const likes = document.querySelectorAll('.like');
    
    likes.forEach(like => {
        like.addEventListener('click', () => {
            const postId = like.dataset.postId;

            fetch(`/toggle-like/${postId}/`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
            .then(response => response.json())
            .then(data => {
                like.src = data.liked 
                    ? '/static/home/img/post/red-like.png' 
                    : '/static/home/img/post/void-like-white.png';
                
                const likeCount = like.nextElementSibling;
                likeCount.textContent = data.total_likes;
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

// ============================================================================
// ПОДПИСКИ
// ============================================================================

document.addEventListener("DOMContentLoaded", function () {
    const followBtn = document.querySelector(".follow-btn");

    if (followBtn) {
        followBtn.addEventListener("click", function () {
            const userId = followBtn.dataset.userId;

            fetch(`/follow/${userId}/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
            })
            .then(response => response.json())
            .then(data => {
                followBtn.textContent = data.following ? "Unfollow" : "Follow";
            });
        });
    }
});

// ============================================================================
// СООБЩЕНИЯ - АВТОСКРОЛЛ
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/messages/')) {
        const container = document.querySelector('.messages-area');
        if (container) {
            setTimeout(() => container.scrollTop = container.scrollHeight, 50);
        }
    }
});

// ============================================================================
// МЕНЮ ПОСТОВ (РЕДАКТИРОВАНИЕ/УДАЛЕНИЕ)
// ============================================================================

document.addEventListener('click', e => {
    const target = e.target;
    
    // Открытие/закрытие меню
    if (target.classList.contains('post-menu-dots')) {
        const postId = target.dataset.postId;
        const menu = document.getElementById(`menu-${postId}`);
        const isOpen = menu?.classList.contains('show');
        
        document.querySelectorAll('.post-menu-dropdown').forEach(m => m.classList.remove('show'));
        
        if (menu && !isOpen) menu.classList.add('show');
        return;
    }
    
    // Действия меню
    if (target.classList.contains('post-menu-item')) {
        const action = target.dataset.action;
        const postId = target.dataset.postId;
        const menu = document.getElementById(`menu-${postId}`);
        if (menu) menu.classList.remove('show');
        
        if (action === 'edit') {
            alert('Редактирование будет добавлено позже');
        } else if (action === 'delete') {
            showConfirm('Удалить пост?', () => {
                fetch(`/delete_post/${postId}/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') }
                }).then(r => {
                    if (r.ok) {
                        const postBlock = document.getElementById(`menu-${postId}`)?.closest('.post-block');
                        if (postBlock) postBlock.remove();
                    }
                });
            });
        }
        return;
    }
    
    // Закрытие меню при клике вне
    if (!target.closest('.post-menu')) {
        document.querySelectorAll('.post-menu-dropdown').forEach(m => m.classList.remove('show'));
    }
});

// ============================================================================
// МОДАЛЬНОЕ ОКНО ПОДТВЕРЖДЕНИЯ
// ============================================================================

function showConfirm(message, onConfirm) {
    let modal = document.getElementById('confirmModal');
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'confirmModal';
        modal.className = 'confirm-modal';
        modal.innerHTML = `
            <div class="confirm-content">
                <p id="confirmMessage"></p>
                <div class="confirm-buttons">
                    <button class="confirm-yes">Да</button>
                    <button class="confirm-no">Отмена</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        modal.querySelector('.confirm-no').onclick = () => modal.classList.remove('show');
        modal.onclick = (e) => e.target === modal && modal.classList.remove('show');
    }
    
    // Обновляем callback каждый раз для корректной работы с разными postId
    modal.querySelector('.confirm-yes').onclick = () => {
        modal.classList.remove('show');
        onConfirm();
    };
    
    document.getElementById('confirmMessage').textContent = message;
    modal.classList.add('show');
}



