from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":

        email_content = request.form["email_content"]

        prompt = f"""
You are a cybersecurity analyst.

Analyze the following email for phishing indicators.

Email:
{email_content}

Provide:
1. Risk Level
2. Suspicious Indicators
3. Explanation
4. Final Verdict
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)