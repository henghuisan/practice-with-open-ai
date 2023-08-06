$(document).ready(function () {
  // generate essay
  $("#generateEssayBtn").on("click", function () {
    const essayIdea = $("#essayIdea").val();
    const essayWordCount = $("#essayWordCount").val();
    console.log(essayIdea);
    console.log(essayWordCount);

    // Send user input to the AI chatbot endpoint using AJAX
    $.ajax({
      type: "POST",
      url: "/essay-generator/",
      data: { essayIdea: essayIdea, essayWordCount: essayWordCount },
      beforeSend: function () {
        $("#loadingEssayResult").removeClass("d-none");
      },
      complete: function () {
        $("#loadingEssayResult").addClass("d-none");
      },
      success: function (data) {
        console.log("success");
        console.log(data);
        $("#essayResult").val(data.result);
      },
      error: function (error) {
        console.log(error);
        $("#responseFailedMsg").removeClass("d-none");
      },
    });
  });

  // copy essay
  $("#copyEssayBtn").on("click", function () {
    $("#essayResult").select();

    // Copy the selected text to the clipboard
    document.execCommand("copy");

    $("#essayCopiedMsg").removeClass("d-none");
    console.log("Text copied to clipboard!");

    // Hide the message after 1 second
    setTimeout(() => {
      $("#essayCopiedMsg").addClass("d-none");
    }, 2000);
  });
});
