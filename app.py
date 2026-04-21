from flask import Flask, send_from_directory, request
import subprocess
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/update', methods=['POST'])
def webhook():
    """GitHub webhook: push 後自動 git pull"""
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(
        ['git', 'pull', 'origin', 'main'],
        cwd=repo_dir,
        capture_output=True, text=True
    )
    return f'OK: {result.stdout}', 200

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
