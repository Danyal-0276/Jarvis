$(document).ready(function () {
  $(".text").textillate({
    loop: true,
    sync: true,
    in: { effect: "bounceIn" },
    out: { effect: "bounceOut" },
  });
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 840,
    height: 200,
    speed: 0.3,
    amplitude: 1,
    frequency: 2,
    style: "ios9",
    autostart: true,
  });

  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: { effect: "fadeInUp", sync: true },
    out: { effect: "fadeOutUp", sync: true },
  });

  // Mic Button click event
  $("#MicBtn").click(function () {
   
    eel.playAssistantSound();
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
  });

});
