from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("SCREENSHOTBASE_API_KEY")
SCREENSHOT_BASE_ENDPOINT = os.getenv("SCREENSHOTBASE_BASE_ENDPOINT")


@app.route('/', methods=['GET', 'POST'])
def home():
    screenshot_url = None

    if request.method == 'POST':
        target_url = request.form.get('url')
        format_ = request.form.get('format', 'png')
        full_page = request.form.get('full_page') == 'on'

        params = {
            "url": target_url,
            "format": format_,
            "full_page": int(full_page)          
        }
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(SCREENSHOT_BASE_ENDPOINT, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            image_extension = format_ if format_ != 'jpeg' else 'jpg'
            image_path = os.path.join('static', f'screenshot.{image_extension}')
            print(image_path)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            screenshot_url = image_path

        except requests.exceptions.RequestException as e:
            print(f"Error capturing screenshot: {e}")
        
    return render_template('index.html', screenshot=screenshot_url)

if __name__ == '__main__':
    app.run(debug=True)
    
