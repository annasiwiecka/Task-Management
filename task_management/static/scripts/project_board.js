document.addEventListener("DOMContentLoaded", function () {
    const projectRows = document.querySelectorAll(".project-row");
    projectRows.forEach(row => {
        row.addEventListener("click", function () {
            console.log("Project row clicked!");
            const projectUrl = this.getAttribute("data-url");
            if (projectUrl) {
                window.location.href = projectUrl;
            }
        });
    });
});


function updatePendingProjectsCount() {
    fetch("{% url 'get_pending_project' team_id=team.id %}")
        .then(response => response.json())
        .then(data => {
            const pendingProjectsCountElement = document.getElementById('pending-projects-count');
            pendingProjectsCountElement.textContent = data.count;
        })
        .catch(error => console.error(error));
}

updatePendingProjectsCount();