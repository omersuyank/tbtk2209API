from flask import Flask
from flask_cors import CORS
from models.TblUser import TblUser


app = Flask(__name__)
CORS(app)




@app.route('/')
def home():
    return "Flask API Çalışıyor!", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
