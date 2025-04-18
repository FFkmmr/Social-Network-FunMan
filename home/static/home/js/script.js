
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
    const textareaFields = document.querySelectorAll('textarea[name="body"], textarea[name="content"]');
    const submitButtons = document.querySelectorAll('.submit-button');

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
            } else {
                button.setAttribute('disabled', true);
                button.classList.remove('active');
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