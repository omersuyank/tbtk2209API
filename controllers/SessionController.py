from flask import Blueprint, request, jsonify
import pyodbc
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import datetime
import bcrypt

session_controller = Blueprint('session_controller', __name__)

SECRET_KEY = "nR3$Wz9#1Y!2q@T8pL*oJx&7M^aK%6XzC4wV5Q+u0B=ErHjP3f9GdNc$#tO"


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=104.247.167.130\\mssqlserver2022;"
    "DATABASE=huseyi98_tbtk2209db;"
    "UID=huseyi98_tbtk2209db;"
    "PWD=zm3Y49k!1"
    "TrustServerCertificate=yes;"
)








@session_controller.route('/register', methods=['POST'])
def register_user():
    try:
        # JSON verisini al
        data = request.get_json()
        print("Gelen JSON:", data)  # JSON verisini yazdır

        # Gerekli alanları kontrol et
        required_fields = ['name', 'surname', 'email', 'phone', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        # Alanları al
        name = data['name']
        surname = data['surname']
        email = data['email']
        phone = data['phone']
        password = data['password'].encode('utf-8')  # Şifreyi encode et
        role = "user"
        is_active = 1

        # Şifreyi bcrypt ile hashle
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO TblUser (name, surname, email, phone, password, role, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, surname, email, phone, hashed_password, role, is_active)
            )
            db.commit()


        return jsonify({"message": "Kullanıcı başarıyla eklendi!"}), 200
    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@session_controller.route('/login', methods=['POST'])
def login():
    """Mail ve şifre ile giriş yapar ve statü bilgisini döner."""
    try:
        # JSON verisini al
        data = request.get_json()
        print("Gelen JSON:", data)

        # JSON'daki gerekli anahtarları kontrol et
        if not all(k in data for k in ('email', 'password')):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        email = data['email']
        password = data['password'].encode('utf-8')  # Kullanıcının girdiği şifreyi encode et

        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, name, surname, role, password FROM TblUser WHERE email = ?  AND is_active = 1",
                (email,)
            )
            result = cursor.fetchone()

        if result:
            user_id, name, surname, role, hashed_password = result
            hashed_password = hashed_password.encode('utf-8')  # Veritabanındaki hash'i encode et

            # Girilen şifre ile hashlenmiş şifreyi karşılaştır
            if bcrypt.checkpw(password, hashed_password):
                # JWT oluştur
                payload = {
                    "id": result[0],
                    "name": result[1],
                    "surname": result[2],
                    "role": result[3],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1 saat geçerli
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

                return jsonify({"message": "Giriş başarılı!", "User": {"id": user_id, "name": name, "surname": surname, "role": role}, "token": token}), 200
            else:
                return jsonify({"error": "Geçersiz e-posta veya şifre"}), 401
        else:
            return jsonify({"error": "Geçersiz e-posta veya şifre"}), 401

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

