from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Replace with your FastAPI endpoint
API_URL = "http://127.0.0.1:8000/check-xss/"

@app.route('/')
def home():
    name = request.args.get("name", "")
    is_malicious = None
    prediction_score = None

    if name:
        # Call the XSS detection API
        response = requests.post(API_URL, data={"payload": name})
        if response.status_code == 200:
            result = response.json()
            is_malicious = result['is_malicious']
            prediction_score = result['prediction_score']

    return render_template_string('''
        <h1>Test XSS Vulnerability</h1>
        <form method="get">
            <input type="text" name="name" placeholder="Enter text" />
            <button type="submit">Submit</button>
        </form>
        {% if name %}
            <p>Output: {{ name|safe }}</p>
            <p>Is Malicious: {{ is_malicious }}</p>
            <p>Prediction Score: {{ prediction_score }}</p>
        {% endif %}
    ''', name=name, is_malicious=is_malicious, prediction_score=prediction_score)

if __name__ == "__main__":
    app.run(debug=True)
