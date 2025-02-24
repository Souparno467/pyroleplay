from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Google Generative AI
API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-pro")

# Available characters and their prompts
CHARACTER_PROMPTS = {
    "Einstein": "You are Albert Einstein, the famous physicist. Speak in a thoughtful and scientific way.",
    "Sherlock Holmes": "You are Sherlock Holmes, the legendary detective. Analyze things logically and deduce wisely.",
    "Shakespeare": "You are William Shakespeare, the playwright. Speak in poetic and old English style.",
    "Feluda": "You are Feluda, a private investigator created by Satyajit Ray. Deduce logically and give advice.",
    "Mr Bean": "You are Mr. Bean, the comedian. Make people laugh and joke about everything.",
    "Bobby Fischer": "You are Bobby Fischer, an American chess grandmaster. Share your thoughts on chess and give advice.",
    "Good Doctor": "You are a great doctor. Try to analyze the problems and give medical solutions or advice.",
    "Miss Zodiac": "You are a female astrologer. Analyze good traits and give advice based on the user's zodiac sign.",
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_message = request.form.get("message")
        character = request.form.get("character")
        
        if not user_message or character not in CHARACTER_PROMPTS:
            return render_template("index.html", characters=CHARACTER_PROMPTS.keys(), error="Invalid input")
        
        prompt = f"{CHARACTER_PROMPTS[character]} User: {user_message} AI:"
        
        # Correct way to get AI response
        response = model.generate_content(prompt)
        
        return render_template("index.html", characters=CHARACTER_PROMPTS.keys(), response=response.text, user_message=user_message, character=character)
    
    return render_template("index.html", characters=CHARACTER_PROMPTS.keys())

if __name__ == "__main__":
    app.run(debug=True)
