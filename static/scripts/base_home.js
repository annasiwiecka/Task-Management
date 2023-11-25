$(document).ready(function() {
    var currentPath = window.location.pathname;
    $(".nav.flex-column a").each(function() {
        var linkPath = $(this).attr("href");
        if (currentPath.startsWith(linkPath)) {
            $(this).addClass("active");
        }
    });
});

$(document).ready(function() {
    $.get('/get_notification_count/', function(data) {
        $('#notification-count').text(data.count);
    });
});