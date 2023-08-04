// static/js/script.js

$(document).ready(function () {
  // Cache frequently used elements of AI CHATBOT
  const userInputField = $("#userInput"); // Cache the user input field for later use
  const chatbox = $("#chatbox"); // Cache the chatbox element for later use
  const loadingDiv = $("#loading div"); // Cache the loading div element for later use
  const responseFailedDiv = $("#response-failed div"); // Cache the response-failed div element for later use
  // Used elements of SPEECH TO TEXT
  let mediaRecorder;
  let recordedChunks = [];

  // AI CHATBOT
  $("#sendUserInputBtn").on("click", function () {
    responseFailedDiv.addClass("d-none"); // Hide the response-failed div initially

    const userInput = userInputField.val(); // Get the user input value
    userInputField.val(""); // Clear the user input field

    // Append the user input to the chatbox
    chatbox.append(
      $('<div class="d-flex flex-row-reverse py-4">') // Create a new div element with classes for user input
        .append(
          $('<span class="material-symbols-rounded mx-3"> person </span>') // Create a new span element with person icon
        )
        .append($("<span>").text(userInput)) // Create a new span element with the user input text
    );

    // Send user input to the AI chatbot endpoint using AJAX
    $.ajax({
      type: "POST",
      url: "/ai-chatbot/",
      data: { input: userInput },
      beforeSend: function () {
        loadingDiv.removeClass("d-none"); // Show the loading div before making the AJAX request
      },
      complete: function () {
        loadingDiv.addClass("d-none"); // Hide the loading div after the AJAX request is complete
      },
      success: function (data) {
        const { status, messages } = data;
        if (status === "success") {
          displayChatbotResponse(messages[messages.length - 1]); // Display the chatbot response
        } else {
          responseFailedDiv.removeClass("d-none"); // Show the response-failed div if there is an error
        }
      },
      error: function (error) {
        console.log("Error:", error);
        responseFailedDiv.removeClass("d-none"); // Show the response-failed div if there is an error
      },
    });
  });

  function displayChatbotResponse(message) {
    // Append the chatbot response to the chatbox
    $("#chatbox").append(
      $('<div class="d-flex flex-row bg-light py-4">') // Create a new div element with classes for chatbot response
        .append(
          $('<span class="material-symbols-rounded mx-3"> smart_toy </span>')
        ) // Create a new span element with smart_toy icon
        .append($("<span>").text(message.content)) // Create a new span element with the chatbot response text
    );
  }

  // SPEECH TO TEXT
  // Event listener for voice recording button click
  $("#recordBtn").on("click", startRecording);

  // Event listener for "Stop" button click
  $("#stopBtn").on("click", function () {
    // Stop the recording
    mediaRecorder.stop();

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
          $("#recordBtn").removeClass("d-none");
          $("#stopBtn").addClass("d-none");

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
          console.log(result)
          alert("Something went wrong. Please try again.")
        }
      },
      error: function (error) {
        alert("Something went wrong. Please try again.")
        console.error("Error saving audio file:", error);
      },
    });
  }
});
