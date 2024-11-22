// Mapping of genres to background images
const genreBackgrounds = {
    fantasy: "url('images/fantasy.jpg')",
    romance: "url('images/romance.jpg')",
    thriller: "url('images/thriller.jpg')",
    "sci-fi": "url('images/scifi.jpg')",
    mystery: "url('images/mystery.jpg')",
    detective: "url('images/detective.jpg')",
    youth: "url('images/youth.jpg')",
    adult: "url('images/adult.jpg')",
    educational: "url('images/educational.jpg')"
};

function getRecommendation() {
    const genre = document.getElementById("genre").value.trim().toLowerCase();
    const resultSection = document.getElementById("result");
    const amazonButton = document.getElementById("amazon-button");

    if (!genre) {
        resultSection.textContent = "Please enter a genre.";
        amazonButton.style.display = "none";  // Hide the Amazon button if no genre is entered
        return;
    }

    // Change background if genre has a mapped background
    if (genreBackgrounds[genre]) {
        document.body.style.backgroundImage = genreBackgrounds[genre];
        document.body.style.backgroundSize = "cover"; // Optional for full-screen cover effect
    } else {
        document.body.style.backgroundImage = "none"; // Default if genre isn't matched
    }

    resultSection.textContent = "Loading...";
    amazonButton.style.display = "none";  // Hide the button while loading

    fetch(`http://127.0.0.1:5000/recommend?genre=${encodeURIComponent(genre)}`)
        .then(response => response.json())
        .then(data => {
            if (data.title && data.author) {
                resultSection.textContent = `${data.title} by ${data.author}`;
                amazonButton.style.display = "inline-block";  // Show the Amazon button

                // Set the Amazon button's link
                amazonButton.onclick = () => {
                    window.open(data.amazon_link, '_blank');
                };
            } else {
                resultSection.textContent = data.message || "No recommendation found for this genre.";
                amazonButton.style.display = "none";  // Hide the button if no recommendation
            }
        })
        .catch(error => {
            console.error("Error fetching recommendation:", error);
            resultSection.textContent = "An error occurred. Please try again.";
            amazonButton.style.display = "none";  // Hide the button if there's an error
        });
}
