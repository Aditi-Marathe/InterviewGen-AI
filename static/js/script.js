function startRecording() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Your browser does not support voice input.");
        return;
    }
    var recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
        document.getElementById('answer').value = event.results[0][0].transcript;
    };
    recognition.start();
}