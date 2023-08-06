$(document).ready(function () {
  // Cache frequently used elements of AI CHATBOT
  const userInputField = $("#userInput"); // Cache the user input field for later use
  const chatbox = $("#chatbox"); // Cache the chatbox element for later use
  const loadingDiv = $("#loading div"); // Cache the loading div element for later use
  const responseFailedDiv = $("#response-failed div"); // Cache the response-failed div element for later use

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
});
