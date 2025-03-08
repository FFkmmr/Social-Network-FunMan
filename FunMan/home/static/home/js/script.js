
document.addEventListener("DOMContentLoaded", function () {
    const backButton = document.querySelector(".circle-back-btn");

    if (backButton) {
        backButton.addEventListener("click", () => {
            window.location.href = "../";
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const routes = {
        home: "/",
        messages: "/messages/",
        profile: "/profile/",
        // search: "/search/",
        bookmarks: "/bookmarks/",
        community: "/community/",
        lists: "/lists/",
        post: "/post/"
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
document.addEventListener('DOMContentLoaded', function () {
    const textareaField = document.querySelector('textarea[name="content"]');
    const submitButton = document.getElementById('submit-button');
    if (textareaField != null) {
        textareaField.addEventListener('input', function () {
        if (textareaField.value.trim() !== "") {
            submitButton.removeAttribute('disabled');
            submitButton.classList.add('active'); 
        } else {
            submitButton.setAttribute('disabled', true);
            submitButton.classList.remove('active');
        }
        });
    }
});
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
// /////////////////////////////////////////////////////////////////
// document.addEventListener('DOMContentLoaded', function () {
//     const comments = document.querySelectorAll('.comments');
//     const share = document.querySelector('.share');
//     const likes = document.querySelector('.like');

//     if (share != null && likes != null) {
//         comments.forEach(comment => {
//         comment.addEventListener('click', () => {
//             const postId = comment.dataset.postId;
            
//             fetch(`/write-comment/${postId}/`, {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//             })
//             .then(response => response.json())
//             .then(data => {

//                 const commentCount = comment.nextElementSibling;
//                 commentCount.textContent = data.total_comments;
//             }).catch(error => {
//                 console.error('Error:', error);
//             });
//         })
//     })
//     }
// })
// ...............................................................

