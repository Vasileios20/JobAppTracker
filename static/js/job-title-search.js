document.addEventListener('DOMContentLoaded', function() {
    const jobTitleInput = document.getElementById('job-title');
    const jobSuggestions = document.getElementById('job-suggestions');

    // Replace with your Adzuna App ID and API key
    const appId = 'your-app-id';
    const apiKey = 'your-api-key';

    jobTitleInput.addEventListener('input', function() {
        const query = jobTitleInput.value;
        if (query.length > 2) {
            // Fetch job titles from Adzuna API
            fetch(`https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=${'0b635271'}&app_key=${'fc12e9732357f5404e4d30137d1203ce'}&what=${'software'}`)
                .then(response => response.json())
                .then(data => {
                    // Clear previous suggestions
                    jobSuggestions.innerHTML = '';

                    // Display job title suggestions
                    data.results.slice(0, 5).forEach(job => {
                        const li = document.createElement('li');
                        li.textContent = job.title;
                        li.classList.add('list-group-item', 'list-group-item-action');
                        li.addEventListener('click', function() {
                            jobTitleInput.value = job.title;
                            jobSuggestions.innerHTML = '';
                        });
                        jobSuggestions.appendChild(li);
                    });
                })
                .catch(error => console.error('Error fetching job titles:', error));
        } else {
            jobSuggestions.innerHTML = '';
        }
    });
});