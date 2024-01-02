document.addEventListener("DOMContentLoaded", () => {
    const dynamicLinks = document.querySelectorAll(".frame-link");
    const frame = document.getElementById("dynframe");

    dynamicLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault()

            const newlink = link.getAttribute('data-src');
            frame.src = newlink;

            dynamicLinks.forEach((menus) => {
                menus.classList.remove("active");
                menus.classList.add("link-body-emphasis");
            })

            link.classList.add("active");
            link.classList.remove("link-body-emphasis");

        })
    })
})
