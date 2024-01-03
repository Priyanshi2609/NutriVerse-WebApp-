/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        searchCSV(searchInput.value);
    });

    function searchCSV(query) {
        // Use an XMLHttpRequest or Fetch API to load your CSV file
        // For this example, let's assume data.csv contains your dataset

        fetch('data.csv')
            .then(response => response.text())
            .then(data => {
                const rows = data.split('\n');
                let results = [];

                for (let i = 1; i < rows.length; i++) { // Skip the header row
                    const cols = rows[i].split(',');
                    if (cols.some(col => col.toLowerCase().includes(query.toLowerCase()))) {
                        results.push(cols.join(', '));
                    }
                }

                if (results.length > 0) {
                    searchResults.innerHTML = `<h2>Search Results:</h2><ul><li>${results.join('</li><li>')}</li></ul>`;
                } else {
                    searchResults.innerHTML = '<p>No results found.</p>';
                }
            })
            .catch(error => console.error('Error:', error));
    }
});

