from flask import Flask, render_template, request, session, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Search history list
search_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    topic = request.form['topic']
    search_results = search_topic(topic)

    # Add search query to search history
    search_history.append(topic)

    # Limit search history to 5 most recent queries
    if len(search_history) > 5:
        search_history.pop(0)

    return render_template('results.html', topic=topic, results=search_results)

@app.route('/history')
def history():
    return render_template('history.html', search_history=search_history)

def search_topic(topic):
    # Use Wikipedia API to retrieve the specific section
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": topic,
        "format": "json",
        "prop": "text",
        "section": 0  # Specify the section number you want to retrieve
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "parse" in data and "text" in data["parse"]:
        html_content = data["parse"]["text"]["*"]
        return [html_content]

    return []

if __name__ == '__main__':
    app.run()
