$(document).ready(function () {
  // Used elements of SPEECH TO TEXT.
  let mediaRecorder;
  let mediaStream;
  let recordedChunks = [];

  // SPEECH TO TEXT
  // Event listener for voice recording button click
  $("#recordBtn").on("click", startRecording);

  // Event listener for "Stop" button click
  $("#stopBtn").on("click", function () {
    // Stop the recording
    mediaRecorder.stop();

    // Stop the MediaStream
    if (mediaStream) {
      mediaStream.getTracks().forEach((track) => track.stop());
      mediaStream = null;
    }
    // Get the last recorded audio Blob (if any) and call the function to save it
    if (recordedChunks.length > 0) {
      const recordedBlob = new Blob(recordedChunks, { type: "audio/wav" });
      saveAudio(recordedBlob);
    }
  });

  // Function to handle recording and saving the audio
  function startRecording() {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(function (stream) {
        // Create a MediaRecorder object and assign the stream to it
        mediaRecorder = new MediaRecorder(stream);

        // Store the MediaStream object
        mediaStream = stream;

        // Event listener for data available during recording
        mediaRecorder.ondataavailable = function (event) {
          recordedChunks.push(event.data);
        };

        // Event listener for stopping the recording
        mediaRecorder.onstop = function () {
          // Combine the recorded chunks into a single Blob
          const recordedBlob = new Blob(recordedChunks, { type: "audio/wav" });

          // Clear the recordedChunks array for future recordings
          recordedChunks = [];

          // Show the "Save" button and hide the "Stop" button
          $("#loadingBtn").removeClass("d-none");
          $("#stopBtn").addClass("d-none");
          $("#recordBtn").addClass("d-none");

          // Show a message to indicate recording has stopped
          // alert('Recording stopped. Click "Save Audio" to save the recording.');

          // Call the function to handle saving the audio
          saveAudio(recordedBlob);
        };

        // Start recording
        mediaRecorder.start();

        // Show the "Stop" button and hide the "Record" button
        $("#stopBtn").removeClass("d-none");
        $("#recordBtn").addClass("d-none");
        $("#loadingBtn").addClass("d-none");

        // Show a message to indicate recording has started
        // alert('Recording voice... Click "Stop" to stop recording.');
      })
      .catch(function (error) {
        console.error("Error accessing user media:", error);
      });
  }

  // Function to handle saving the audio to the server using Ajax
  function saveAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recorded_audio.wav");

    $.ajax({
      type: "POST",
      url: "/speech-to-text/",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        const { status, result } = data;
        if (status == "success") {
          $("#userInput").val(result);
        } else {
          console.log(result);
          alert("Something went wrong. Please try again.");
        }
        $("#recordBtn").removeClass("d-none");
        $("#stopBtn").addClass("d-none");
        $("#loadingBtn").addClass("d-none");
      },
      error: function (error) {
        alert("Something went wrong. Please try again.");
        console.error("Error saving audio file:", error);
        $("#recordBtn").removeClass("d-none");
        $("#stopBtn").addClass("d-none");
        $("#loadingBtn").addClass("d-none");
      },
    });
  }
});
