const uploadButton = document.getElementById("upload-button");
const searchButton = document.getElementById("search-button");
const fileInput = document.getElementById("file-input");
const searchInput = document.getElementById("search-input");
const results = document.getElementById("results");

uploadButton.addEventListener("click", () => {
    const file = fileInput.files[0];
    if (file) {
        console.log(file);
        fetch("/ingest", {
            method: "POST",
            body: file,
        });
    }
});