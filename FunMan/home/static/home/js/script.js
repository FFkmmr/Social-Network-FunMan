
document.addEventListener("DOMContentLoaded", function () {
    const backButton = document.querySelector(".circle-back-btn");

    if (backButton) {
        backButton.addEventListener("click", () => {
            window.location.href = "../";
        });
    }
});

// document.addEventListener("DOMContentLoaded", function () {
//     const bookmarksbtn = document.getElementById("bookmarks");

//     if (bookmarksbtn) {
//         bookmarksbtn.addEventListener("click", function () {
//             window.location.href = "/bookmarks/";
//         })
//     }
// });
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
