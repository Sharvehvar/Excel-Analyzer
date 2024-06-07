from flask import Flask, request, render_template, redirect, url_for
import google.generativeai as genai
import pandas as pd

app = Flask(__name__)

api_key = "AIzaSyBVec6inSuyB7rE4qOPdskMM_UTWQ525GM"

genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files["file"]
        prompt = request.form["prompt"]

        df = pd.read_excel(file)
        data_str = df.to_string(index=False)

        try:
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [data_str, prompt],
                    }
                ]
            )

            response = chat_session.send_message(prompt)

            if response:
                result = response.text
            else:
                result = "No response received from the API."

            return render_template("result.html", result=result)

        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
