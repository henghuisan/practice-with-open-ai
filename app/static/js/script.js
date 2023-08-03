// static/js/script.js

$(document).ready(function () {
  $("#sendBtn").on("click", function () {
    var userInput = $("#userInput").val();
    $("#userInput").val("");

    $("#chatbox").append(
      '<div class="d-flex flex-row-reverse py-4"><span class="material-symbols-rounded mx-3"> person </span><span>' +
        userInput +
        "</span></div>"
    );

    $.ajax({
      type: "POST",
      url: "/ai-chatbot/",
      data: { input: userInput },
      beforeSend: function () {
        $("#loading div").removeClass("d-none")
      },
      complete: function () {
        $("#loading div").addClass("d-none")

      },
      success: function (response) {
        displayChatbotResponse(response);
      },
      error: function (error) {
        console.log("Error:", error);
      },
    });
  });
});

function displayChatbotResponse(response) {
  $("#chatbox").append(
    '<div class="d-flex flex-row bg-light py-4"><span class="material-symbols-rounded mx-3"> smart_toy </span><span>' +
      response[response.length - 1].content +
      "</span></div>"
  );
}

