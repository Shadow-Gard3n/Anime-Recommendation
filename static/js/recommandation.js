document.addEventListener('DOMContentLoaded', () => {
    
    const recButton = document.getElementById('recButton');
    const animeInput = document.getElementById('animeInput');
    const listElement = document.getElementById('recommendationList');    
    const API_URL = 'http://127.0.0.1:8000';

    recButton.addEventListener('click', handleRecommendation);
    animeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleRecommendation();
        }
    });
    async function handleRecommendation() {
        const animeName = animeInput.value;
        
        if (!animeName) {
            listElement.innerHTML = `<li class="status">Please enter an anime name.</li>`;
            return;
        }

        listElement.innerHTML = `<li class="status">Searching for recommendations...</li>`;

        try {
            const response = await fetch(`${API_URL}/recommend/${encodeURIComponent(animeName)}`);
            if (response.status === 404) {
                const errorData = await response.json();
                listElement.innerHTML = `<li class="status" style="color: #ffc107;">Error: ${errorData.detail}</li>`;
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            listElement.innerHTML = ''; 
            const title = document.createElement('h3');
            title.textContent = `Recommendations for: ${data.searched_anime}`;
            listElement.appendChild(title);

            if (data.recommendations && data.recommendations.length > 0) {
                data.recommendations.forEach(anime => {
                    const li = document.createElement('li');
                    li.textContent = anime;
                    listElement.appendChild(li);
                });
            } else {
                listElement.innerHTML = '<li class="status">No recommendations found.</li>';
            }

        } catch (error) {
            console.error('Fetch error:', error);
            listElement.innerHTML = `<li class="status" style="color: red;">Error fetching data. Is the backend running?</li>`;
        }
    }
});