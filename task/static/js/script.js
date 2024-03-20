document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('taskForm').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/add_task', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData.entries())),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            this.reset();
        })
        .catch(error => console.error('Error:', error));
    });
});
