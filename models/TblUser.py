from config import db

class TblUser(db.Model):
    __tablename__ = "TblUser"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'student' veya 'teacher'
    invite_code = db.Column(db.String(255), nullable=True)  # Sadece öğretmenler için
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<TblUser {self.name} - {self.role}>"
