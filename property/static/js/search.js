document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("location-search");
    const resultsBox = document.getElementById("autocomplete-results");

    let debounceTimer = null;

    input.addEventListener("input", () => {
        const query = input.value.trim();

        // Clear results if empty
        if (query.length < 1) {
            resultsBox.innerHTML = "";
            resultsBox.style.display = "none";
            return;
        }

        // Debounce (avoid spamming API)
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            fetch(`/api/autocomplete/?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => renderResults(data.suggestions))
                .catch(() => {
                    resultsBox.innerHTML = "";
                    resultsBox.style.display = "none";
                });
        }, 300);
    });

    function renderResults(suggestions) {
        resultsBox.innerHTML = "";

        if (!suggestions || suggestions.length === 0) {
            resultsBox.style.display = "none";
            return;
        }

        suggestions.forEach(loc => {
            const item = document.createElement("div");
            item.className = "autocomplete-item";
            item.innerHTML = `
                <strong>${loc.name}</strong>, ${loc.city}, ${loc.country}
                <span class="count">(${loc.property_count})</span>
            `;

            item.addEventListener("click", () => {
                // Redirect to property list filtered by location ID
                window.location.href = `/properties?location=${loc.id}`;
            });

            resultsBox.appendChild(item);
        });

        resultsBox.style.display = "block";
    }

    // Hide suggestions when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".autocomplete-wrapper")) {
            resultsBox.innerHTML = "";
            resultsBox.style.display = "none";
        }
    });
});


const searchBtn = document.getElementById("search");
const searchInput = document.getElementById("location-search");

function makeSearch() {
    const searchTerm = searchInput.value.trim();
    if (searchTerm.length < 1) return;
    // Encode special characters in URL
    window.location.href = `/properties?location=${encodeURIComponent(searchTerm)}`;
}

// Search on button click
searchBtn.addEventListener("click", makeSearch);

// Search when pressing Enter in input
searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        makeSearch();
    }
});
