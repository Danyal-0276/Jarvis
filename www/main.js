$(document).ready(function () {
  let siriWave = null;
  let isProcessing = false;
  let voiceEnabled = true;
  let settingsModal = null;

  $(".text").textillate({
    loop: true,
    sync: true,
    in: { effect: "bounceIn" },
    out: { effect: "bounceOut" },
  });

  function initSiriWave() {
    if (!siriWave) {
      siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 840,
        height: 200,
        speed: 0.3,
        amplitude: 1,
        frequency: 2,
        style: "ios9",
        autostart: true,
      });
    }
    return siriWave;
  }

  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: { effect: "fadeInUp", sync: true },
    out: { effect: "fadeOutUp", sync: true },
  });

  function appendMessage(container, role, text) {
    const bubble = $(`<div class="chat-bubble ${role}">${escapeHtml(text)}</div>`);
    $(container).append(bubble);
    $(container).scrollTop($(container)[0].scrollHeight);
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function setThinking(active, message) {
    const wave = initSiriWave();
    if (active) {
      wave.setAmplitude(3);
      wave.setSpeed(0.6);
      $(".siri-message .pp").text(message || "Thinking...");
    } else {
      wave.setAmplitude(1);
      wave.setSpeed(0.3);
      $(".siri-message .pp").text("Hello, I am J.A.R.V.I.S");
    }
  }

  async function sendMessage(text, transcriptEl) {
    if (!text.trim() || isProcessing) return;
    isProcessing = true;
    const container = transcriptEl || "#chatTranscript";
    appendMessage(container, "user", text);
    $("#chatbox").val("");
    setThinking(true, "Thinking...");

    try {
      const result = await eel.chat(text)();
      appendMessage(container, "assistant", result.reply || "No response.");
      if (voiceEnabled && result.reply) {
        await eel.speak_text(result.reply)();
      }
    } catch (err) {
      appendMessage(container, "assistant", "Connection error. Is the backend running?");
    }

    setThinking(false);
    isProcessing = false;
  }

  $("#chatbox").on("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage($(this).val());
    }
  });

  $("#ChatBtn").click(function () {
    sendMessage($("#chatbox").val());
  });

  $("#MicBtn").click(async function () {
    if (isProcessing) return;
    eel.playAssistantSound();
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    $("#voiceTranscript").empty();
    initSiriWave();

    isProcessing = true;
    setThinking(true, "Listening...");

    try {
      const listenResult = await eel.listen_command()();
      if (listenResult.status === "done" && listenResult.text) {
        appendMessage("#voiceTranscript", "user", listenResult.text);
        setThinking(true, "Thinking...");
        const chatResult = await eel.chat(listenResult.text)();
        appendMessage("#voiceTranscript", "assistant", chatResult.reply || "No response.");
        if (voiceEnabled && chatResult.reply) {
          setThinking(true, "Speaking...");
          await eel.speak_text(chatResult.reply)();
        }
      } else {
        appendMessage("#voiceTranscript", "assistant", listenResult.message || "Could not hear you.");
      }
    } catch (err) {
      appendMessage("#voiceTranscript", "assistant", "Voice error. Check microphone setup.");
    }

    setThinking(false);
    isProcessing = false;
  });

  $(document).on("keydown", function (e) {
    if (e.key === "Escape" && !$("#SiriWave").attr("hidden")) {
      $("#SiriWave").attr("hidden", true);
      $("#Oval").attr("hidden", false);
    }
  });

  $("#SettingsBtn").click(function () {
    if (!settingsModal) {
      settingsModal = new bootstrap.Modal(document.getElementById("settingsModal"));
    }
    loadSettings();
    settingsModal.show();
  });

  async function loadSettings() {
    try {
      const s = await eel.get_settings()();
      $("#geminiStatus")
        .text(s.gemini_configured ? "Configured" : "Missing")
        .removeClass("bg-secondary bg-success bg-danger")
        .addClass(s.gemini_configured ? "bg-success" : "bg-danger");
      $("#gmailStatus")
        .text(s.gmail_configured ? "Configured" : "Missing")
        .removeClass("bg-secondary bg-success bg-danger")
        .addClass(s.gmail_configured ? "bg-success" : "bg-warning");
      $("#docCount").text(s.document_count);
      $("#voiceStatus")
        .text(s.voice_enabled ? "Enabled" : "Disabled")
        .removeClass("bg-secondary bg-success")
        .addClass(s.voice_enabled ? "bg-success" : "bg-secondary");
      voiceEnabled = s.voice_enabled;
      const paths = s.allowed_paths.map((p) => `<li>${escapeHtml(p)}</li>`).join("");
      $("#allowedPaths").html(paths);
    } catch (e) {
      console.error("Settings load failed", e);
    }
  }

  $("#reindexBtn").click(async function () {
    $(this).prop("disabled", true).text("Indexing...");
    try {
      const r = await eel.reindex_documents()();
      $("#docCount").text(r.count);
    } catch (e) {
      console.error(e);
    }
    $(this).prop("disabled", false).text("Re-index");
  });

  $("#clearChatBtn").click(async function () {
    await eel.clear_chat()();
    $("#chatTranscript, #voiceTranscript").empty();
    settingsModal.hide();
  });

  async function checkPin() {
    try {
      const s = await eel.get_settings()();
      if (s.pin_enabled) {
        $("#pinOverlay").attr("hidden", false);
      }
    } catch (e) {
      console.error(e);
    }
  }

  $("#pinSubmit").click(async function () {
    const pin = $("#pinInput").val();
    const result = await eel.verify_pin(pin)();
    if (result.status === "ok") {
      $("#pinOverlay").attr("hidden", true);
      $("#pinError").attr("hidden", true);
    } else {
      $("#pinError").attr("hidden", false);
    }
  });

  $("#pinInput").on("keydown", function (e) {
    if (e.key === "Enter") $("#pinSubmit").click();
  });

  checkPin();
});
