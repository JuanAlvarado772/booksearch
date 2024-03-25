from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
# Adjust CORS settings as needed
CORS(app, origins="http://localhost:3000")


def search_books(query, api_key, start_index, max_results):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query, 'startIndex': start_index, 'maxResults': max_results, 'key': api_key}
    response = requests.get(base_url, params=params)
    print(f"Requesting: {response.url}")  # Debugging log
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")  # Debugging log
        return None


@app.route('/search', methods=['GET'])
def book_search():
    query = request.args.get('query')  # Get the search query from URL parameters
    start_index = request.args.get('startIndex', default=0, type=int)  # Default to 0
    max_results = request.args.get('maxResults', default=40, type=int)  # Default to 10

    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    results = search_books(query, api_key, start_index, max_results)
    if results:
        return jsonify(results)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port)
