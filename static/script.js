// JavaScript code for handling button click events

// Function to trigger the file input when the "Upload Audio" button is clicked
document.getElementById("upload-button").addEventListener("click", function () {
    document.getElementById("audio-file").click();
});

// Function to handle the selected audio file when it changes
document.getElementById("audio-file").addEventListener("change", function () {
    var selectedFile = this.files[0];
    if (selectedFile) {
        document.getElementById("output").innerHTML = "Selected file: " + selectedFile.name;
    }
});

// Function to handle the "Submit" button click event (customize this based on your needs)
document.getElementById("submit-button").addEventListener("click", function () {
    // Add your code to handle the submission of the audio file here
    // For example, you can send it to a server for processing.
});
