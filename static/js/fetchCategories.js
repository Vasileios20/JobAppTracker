function updateJobTitles(category) {
    const url = `/job/api/get-job-titles/?category=${category}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const jobSelect = document.getElementById('title');
            const companySelect = document.getElementById('company');

            jobSelect.innerHTML = '';
            companySelect.innerHTML = '';

            data.forEach(job => {
                const jobOption = document.createElement('option');
                jobOption.value = job.title;
                jobOption.text = job.title;
                jobSelect.appendChild(jobOption);

                const companyOption = document.createElement('option');
                companyOption.value = job.company;
                companyOption.text = job.company;
                companySelect.appendChild(companyOption);
            });
        })
        .catch(error => console.error('Error fetching job titles:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    const categoryDropdown = document.getElementById('category');
    categoryDropdown.addEventListener('change', (event) => {
        updateJobTitles(event.target.value);
    });
});
