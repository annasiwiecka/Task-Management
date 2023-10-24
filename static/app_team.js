$(document).ready(function() {
    var currentPath = window.location.pathname;

    $(".nav-link").each(function() {
        var linkPath = $(this).attr("href");
        
        if (currentPath === linkPath) {
            $(this).closest(".nav-link").addClass("active");
            $(this).attr("aria-current", "page");
        }
    });
});