import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("API"))
        self.system_prompt = open("system_prompt.txt").read()

    def chat_completion(self, messages):
        contents = []
        
        for m in messages:
            role = "model" if m["role"] == "assistant" else "user"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=m["content"])]
                )
            )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt
            )
        )

        return response.text
