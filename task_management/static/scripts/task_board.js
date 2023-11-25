document.addEventListener("DOMContentLoaded", function () {
    const projectRows = document.querySelectorAll(".project-row");
    projectRows.forEach(row => {
        row.addEventListener("click", function () {
            const projectUrl = this.getAttribute("data-url");
            if (projectUrl) {
                window.location.href = projectUrl;
            }
        });
    });
});

function updatePendingTasksCount() {
    fetch("{% url 'get_pending_tasks' team_id=team.id %}")
        .then(response => response.json())
        .then(data => {
            const pendingTasksCountElement = document.getElementById('pending-tasks-count');
            pendingTasksCountElement.textContent = data.count;
        })
        .catch(error => console.error(error));
}
updatePendingTasksCount();