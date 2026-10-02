import os
import json
import zipfile
import subprocess
import google.generativeai as genai
from config import GEMINI_API_KEY, GENERATED_PROJECTS_DIR


class GeminiWebBuilder:
    """Full-stack web project generator using Gemini API."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.generated_dir = GENERATED_PROJECTS_DIR
        os.makedirs(self.generated_dir, exist_ok=True)

    def build_and_run(self, requirement: str, project_name: str = "generated_site") -> str:
        """Build a website and launch it automatically."""
        try:
            prompt = f"""
            You are an elite Full Stack Web Developer. Build a complete, responsive modern web project for: '{requirement}'.
            Return the result ONLY as a single valid JSON object without markdown syntax or backticks, with the following format:
            {{
                "index.html": "<content>",
                "style.css": "<content>",
                "app.js": "<content>"
            }}
            Ensure HTML is modern, CSS is beautiful with gradients and animations, and JS is functional.
            """

            response = self.model.generate_content(prompt)
            raw_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            files = json.loads(raw_text)

            output_dir = os.path.join(os.getcwd(), self.generated_dir, project_name)
            os.makedirs(output_dir, exist_ok=True)

            for filename, content in files.items():
                with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
                    f.write(content)

            zip_path = f"{output_dir}.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, filenames in os.walk(output_dir):
                    for file in filenames:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, output_dir)
                        zipf.write(file_path, arcname=arcname)

            index_path = os.path.join(output_dir, "index.html")
            subprocess.Popen(f'start "" "{index_path}"', shell=True)
            return zip_path
        except Exception as e:
            return f"Error building website: {e}"

    def generate_code(self, requirement: str) -> dict:
        """Generate code files without launching."""
        try:
            prompt = f"""
            Generate complete, production-ready code for: '{requirement}'.
            Return ONLY a valid JSON object without markdown, with file names as keys and content as values.
            """
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(raw_text)
        except Exception as e:
            return {"error": str(e)}
