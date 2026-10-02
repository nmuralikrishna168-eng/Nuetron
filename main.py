import sys
from PyQt6.QtWidgets import QApplication
from ui.glass_ui import NuetronMainWindow
from core.speech_engine import SpeechEngine, VoiceListenerThread
from core.local_llm import LocalLLM
from core.gemini_builder import GeminiWebBuilder
from actions.app_control import AppController
from actions.researcher import Researcher
from actions.screen_scanner import ScreenScanner
from config import USER_NAME


class NuetronController:
    """Main orchestrator for NUETRON v16 AI assistant."""

    def __init__(self, ui: NuetronMainWindow):
        self.ui = ui
        self.speech = SpeechEngine()
        self.llm = LocalLLM()
        self.web_builder = GeminiWebBuilder()
        self.screen_scanner = ScreenScanner()

        self.ui.user_submitted.connect(self.process_command)

        self.voice_thread = VoiceListenerThread()
        self.voice_thread.command_received.connect(self.handle_wake_word)
        self.voice_thread.status_updated.connect(self.ui.update_status)
        self.voice_thread.start()

    def handle_wake_word(self, detected_text: str):
        self.ui.append_log("SYSTEM", "Wake-Word 'Neutron' Activated.")
        intro = f"Greetings {USER_NAME.split()[0]}. I am Nuetron, your desktop assistant. What is your command?"
        self.ui.append_log("NUETRON", intro)
        self.speech.speak(intro)

        clean_command = detected_text.replace("neutron", "").strip()
        if clean_command:
            self.process_command(clean_command)

    def process_command(self, cmd: str):
        cmd_lower = cmd.lower()

        if self._match_intent(cmd_lower, ["play", "youtube", "song", "video"]):
            self._handle_youtube(cmd_lower)
        elif self._match_intent(cmd_lower, ["research", "do research"]):
            self._handle_research(cmd_lower)
        elif self._match_intent(cmd_lower, ["build website", "create a website", "create website"]):
            self._handle_website_builder(cmd_lower)
        elif self._match_intent(cmd_lower, ["scan screen", "read screen", "capture screen"]):
            self._handle_screen_scan()
        elif self._match_intent(cmd_lower, ["tell a story", "story"]):
            self._handle_story(cmd_lower)
        else:
            self._handle_general_query(cmd)

    def _match_intent(self, text: str, keywords: list) -> bool:
        return any(keyword in text for keyword in keywords)

    def _handle_youtube(self, cmd: str):
        query = cmd.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
        self.ui.append_log("NUETRON", f"🎵 Opening YouTube and playing: {query}...")
        self.speech.speak(f"Playing {query} on YouTube")
        AppController.play_youtube_video(query)

    def _handle_research(self, cmd: str):
        topic = cmd.replace("research", "").replace("do research", "").replace("on", "").replace("about", "").strip()
        self.ui.append_log("NUETRON", f"📚 Initiating research on: {topic}...")
        self.speech.speak(f"Conducting research on {topic}. Writing it directly to your notepad.")

        research_summary = self.llm.query(
            prompt=f"Provide a comprehensive, high-value structured research brief on: '{topic}'. Include Key Insights, Analysis, and Conclusions.",
            system_prompt="You are an expert executive research analyst with deep domain knowledge.",
        )
        Researcher.write_research_report(topic, research_summary)
        self.ui.append_log("NUETRON", "✅ Research sheet generated successfully in Notepad.")
        self.speech.speak("Your research report has been generated.")

    def _handle_website_builder(self, cmd: str):
        req = cmd.replace("build website", "").replace("create a website", "").replace("create website", "").replace("for", "").strip()
        self.ui.append_log("NUETRON", f"🌐 Designing full-stack website via Gemini API for: {req}...")
        self.speech.speak("Generating your dynamic website structure and packaging zip archive.")
        zip_file = self.web_builder.build_and_run(req)
        self.ui.append_log("NUETRON", f"✅ Website generated and launched. Archive: {zip_file}")
        self.speech.speak("Your website is ready and running in your browser.")

    def _handle_screen_scan(self):
        self.ui.append_log("NUETRON", "📸 Scanning monitor view...")
        self.speech.speak("Scanning your current desktop screen.")
        path = self.screen_scanner.capture_screen()
        self.ui.append_log("NUETRON", f"✅ Screenshot captured at {path}")
        self.speech.speak("Screen scan complete. Image saved to disk.")

    def _handle_story(self, cmd: str):
        self.ui.append_log("NUETRON", "📖 Composing story via local Ollama...")
        self.speech.speak("Here is a story for you.")
        story = self.llm.query(cmd, system_prompt="You are an imaginative, expressive storyteller with vivid descriptions.")
        self.ui.append_log("NUETRON", story)
        self.speech.speak(story[:250])

    def _handle_general_query(self, cmd: str):
        self.ui.append_log("NUETRON", "🤔 Processing local reasoning...")
        reply = self.llm.query(cmd)
        self.ui.append_log("NUETRON", reply)
        self.speech.speak(reply[:180])


def main():
    app = QApplication(sys.argv)
    window = NuetronMainWindow()
    controller = NuetronController(window)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
