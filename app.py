

from flask import Flask, render_template, request, redirect, url_for,session,flash
import os
import requests
import time
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from flask import Response

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
UPLOAD_FOLDER = 'static/uploads'
app.secret_key = "pASSWORD11212121"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if 'token' not in session:
        return redirect('/login')

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        video = request.files.get('video')

        if not title or not video:
            flash("Title and video required")
            return redirect('/upload')

        api_url = "https://tubeboxservers-production.up.railway.app/api/admin/videos"

        headers = {
            "Authorization": f"Bearer {session['token']}"
        }

        files = {
            "video": (video.filename, video.stream, video.mimetype)
        }

        data = {
            "title": title,
            "description": description
        }

        response = requests.post(
            api_url,
            headers=headers,
            files=files,
            data=data
        )
        print(response.status_code)
        print(response.text)

        if response.status_code == 201:
            flash("Video uploaded successfully!")
            return redirect('/upload')
        else:
            try:
                flash(response.json().get("error", response.text))
            except:
                flash(response.text)

    return render_template("upload.html")

import time
from flask import make_response

@app.route('/videos')
def videos_page():
    # ✅ Always check session first
    if 'token' not in session:
        return redirect('/login')
    print("=== /videos HIT ===")
    return render_template("videos.html",);
    # ✅ Always check session first
    if 'token' not in session:
        return redirect('/login')
    print("=== /videos HIT ===")

    token = session.get('token')
    print("TOKEN:", token)

    if not token:
        print("NO TOKEN → redirecting")
        return redirect('/login')
    api_url = f"https://tubeboxservers-production.up.railway.app/api/admin/videos?_={int(time.time())}"
    print("BEFORE API CALL")
    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    try:
        response = requests.get(api_url, timeout=20, headers=headers)

        print("Status:", response.status_code)

        if response.status_code == 200:
            videos = response.json()
            print("Data:", videos)
        else:
            videos = []
            flash("Could not load videos.")

    except Exception as e:
        print("Videos Error:", e)
        videos = []
        flash("Server connection failed.")

    # ✅ Prevent browser caching
    resp = make_response(render_template("videos.html", videos=videos))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    print("BEFORE API CALL")
    return resp

@app.route('/telegram')
def telegram():
    if 'token' not in session:
        return redirect('/login')
    return render_template('telegram.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms-and-condition')
def terms():
    return render_template('terms.html')

@app.route('/why-choose-us')
def why():
    return render_template('why.html')

@app.route('/ads')
def ads():
    if 'token' not in session:
        return redirect('/login')
    return render_template('ads.html')

@app.route('/dmca')
def dmca():
    return render_template('dmca.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/social')
def social():
    return render_template('social.html')
@app.route('/trending')
def trending():
    return render_template('trending.html')
@app.route('/feature')
def feature():
    return render_template('feature.html')


@app.route('/analytics')
def analytics():
    if 'token' not in session:
        return redirect('/login')
    return render_template('analytics.html')
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
@app.route('/app')
def download():
    return redirect("https://play.google.com/store/apps/details?id=com.tube.box.entertainment.app&hl=en_IN")



@app.route('/.well-known/assetlinks.json')
def asset_links():
    data = [
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.starwish.tubeboxs",
      "sha256_cert_fingerprints": [
        "24:5E:C1:5F:01:10:24:30:30:D6:F9:46:A8:C8:88:BA:C7:4F:11:87:E7:67:AD:1C:CE:B1:3D:89:6C:AA:68:F5"
      ]
    }
  }
]
    return Response(
        json.dumps(data),
        mimetype='application/json'
    )



@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        api_url = "https://tubeboxservers-production.up.railway.app/api/admin/login"

        payload = {
            "username": username,
            "password": password
        }

        response = requests.post(api_url, json=payload)

        if response.status_code == 200:

            data = response.json()

            # Save everything in session
            session['token'] = data['token']
            session['admin_id'] = data['admin']['id']
            session['admin_username'] = data['admin']['username']

            return render_template("login_success.html", token=data['token'])

        else:
            flash("Invalid username or password")

    return render_template("login.html")

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('download'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

