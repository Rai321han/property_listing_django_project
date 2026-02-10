document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("location-search");
    const resultsBox = document.getElementById("autocomplete-results");
    const searchForm = document.getElementById("search-form");

    let debounceTimer = null;

    // Autocomplete fetch
    input.addEventListener("input", () => {
        const query = input.value.trim();
        if (query.length < 1) {
            resultsBox.innerHTML = "";
            resultsBox.style.display = "none";
            return;
        }

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
                // Redirect with location_text + location ID
                const locationText = `${loc.name}, ${loc.city}, ${loc.country}`;
                window.location.href = `/properties?location_text=${encodeURIComponent(locationText)}&location=${loc.id}`;
            });

            resultsBox.appendChild(item);
        });

        resultsBox.style.display = "block";
    }

    // Hide suggestions when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".search-wrapper")) {
            resultsBox.innerHTML = "";
            resultsBox.style.display = "none";
        }
    });

    // Search form submit
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const term = input.value.trim();
        if (term.length < 1) return;
        window.location.href = `/properties?location=${encodeURIComponent(term)}`;
    });
});
