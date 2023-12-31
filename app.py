from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://nusyoman:manis@cluster0.wjeaswn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # Mengambil data dari MongoDB
    articles = list(db.diary.find({}))
    for article in articles:
        article['_id'] = str(article['_id'])  # Mengubah _id menjadi string
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
