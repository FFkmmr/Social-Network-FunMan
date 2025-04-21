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


document.addEventListener("DOMContentLoaded", function () {
    const closebtn = document.querySelector('.closebtn-index');
    if (closebtn != null) {
        closebtn.addEventListener('click', () => {
            window.location.href = '../';
        });
    }
    
    const backButton = document.querySelector(".circle-back-btn");

    if (backButton) {
        backButton.addEventListener("click", () => {
            window.location.href = "../";
        });
    }
});


// Left panel
document.addEventListener("DOMContentLoaded", function () {
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
            button.addEventListener("click", function () {
                window.location.href = routes[id];
            });
        }
    });
});


// Create the post panel 
document.addEventListener('DOMContentLoaded', function () {
    const textareaFields = document.querySelectorAll('textarea[name="body"], textarea[name="content"], textarea[name="message"], input[name="search"]');
    const submitButtons = document.querySelectorAll('.submit-button, .style-none');

    if (textareaFields.length > 0) {
        window.addEventListener('load', postBtn);
        textareaFields.forEach(textarea => {
            textarea.addEventListener('input', postBtn);
        });
    }
    function postBtn() {
        const isValid = Array.from(textareaFields).some(textarea => textarea.value.trim() !== "");
        
        submitButtons.forEach(button => { 
            if (isValid) {
                button.removeAttribute('disabled');
                button.classList.add('active');
                if (button.classList.contains('style-none')) {
                    button.src = '/static/home/img/paper-plane.png';
                }
            } else {
                button.setAttribute('disabled', true);
                button.classList.remove('active');
                if (button.classList.contains('style-none')) {
                    button.src = '/static/home/img/paper-plane-black.png';
                }
            }
        });
    }
});


// Create the post panel
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.querySelector('textarea[name="content"]');
    
    if (textarea != null) {
        function adjustHeight() {
            textarea.style.height = '80px';  
            textarea.style.height = (textarea.scrollHeight) + 'px';
        }
        textarea.addEventListener('input', adjustHeight);
        adjustHeight();
    }
});


// Likes
document.addEventListener('DOMContentLoaded', function () {
    const comments = document.querySelector('.comments');
    const share = document.querySelector('.share');
    const likes = document.querySelectorAll('.like');
    
    if (comments != null && share != null) {
    likes.forEach(like => {
        like.addEventListener('click', () => {
            const postId = like.dataset.postId;

            fetch(`/toggle-like/${postId}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    like.src = '/static/home/img/post/red-like.png';
                } else {
                    like.src = '/static/home/img/post/void-like-white.png';
                }

                const likeCount = like.nextElementSibling;
                likeCount.textContent = data.total_likes;
            }).catch(error => {
                console.error('Error:', error);
            });
        })
    })
    }
})


document.addEventListener("DOMContentLoaded", function () {
    const followBtn = document.querySelector(".follow-btn");

    if (followBtn) {
        followBtn.addEventListener("click", function () {
            const userId = followBtn.dataset.userId;

            fetch(`/follow/${userId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then(response => response.json())
            .then(data => {
                followBtn.textContent = data.following ? "Unfollow" : "Follow";
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/messages/')) {
        const container = document.querySelector('.messages-area');
        if (container) {
            setTimeout(() => {
                container.scrollTop = container.scrollHeight;
            }, 100); // можно увеличить при необходимости
        }
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("user-search");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value;

        fetch(`/messages/?new-mess-filt=True&search=${encodeURIComponent(query)}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.text())
        

    });
});

