function analyzeResume() {

    const file = document.getElementById("resume").files[0];

    if (!file) {
        alert("Please upload your resume.");
        return;
    }

    document.getElementById("result").innerHTML =
        "<h2>Resume uploaded successfully!</h2>";
}