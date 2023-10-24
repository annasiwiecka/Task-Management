document.addEventListener("DOMContentLoaded", function() {
    const projectRows = document.querySelectorAll(".project-row");
    projectRows.forEach(row => {
        row.addEventListener("click", function() {
            const projectUrl = this.getAttribute("data-url");
            if (projectUrl) {
                window.location.href = projectUrl;
            }
        });
    });
});