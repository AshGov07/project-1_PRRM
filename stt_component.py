# stt_component.py
import streamlit as st
import streamlit.components.v1 as components

def stt():
    stt_html = """
    <script>
      var speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      var recognition = new speechRecognition();
      recognition.continuous = false;
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      document.addEventListener("DOMContentLoaded", function() {
        const btn = document.getElementById("speak-btn");
        btn.onclick = () => {
          recognition.start();
        };
        recognition.onresult = (event) => {
          const result = event.results[0][0].transcript;
          const textarea = document.getElementById("speech-output");
          textarea.value = result;
          textarea.dispatchEvent(new Event("input", { bubbles: true }));
        };
      });
    </script>
    <button id="speak-btn">🎙️ Start Voice Input</button><br>
    <textarea id="speech-output" name="input" style="width: 100%; height: 40px;"></textarea>
    """
    return components.html(stt_html, height=150)
