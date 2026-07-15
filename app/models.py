from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher_profile = db.relationship('Teacher', backref='user', uselist=False)
    student_profile = db.relationship('Student', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class SchoolClass(db.Model):
    __tablename__ = 'school_classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g. "S1 A"
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)

    students = db.relationship('Student', backref='school_class', lazy=True)

    def __repr__(self):
        return f'<Class {self.name}>'


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120))  # e.g. "Mathematics"

    classes_taught = db.relationship('SchoolClass', backref='class_teacher', lazy=True,
                                      foreign_keys='SchoolClass.class_teacher_id')

    def __repr__(self):
        return f'<Teacher {self.full_name}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    admission_number = db.Column(db.String(30), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_classes.id'), nullable=True)

    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Student {self.full_name}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)  # e.g. "Mathematics"
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g. "MTH101"

    grades = db.relationship('Grade', backref='subject', lazy=True)

    def __repr__(self):
        return f'<Subject {self.name}>'


class Grade(db.Model):
    """
    This is the core of progress tracking: one row per score,
    per student, per subject, per term. Querying all rows for
    a student ordered by date gives us their progress over time.
    """
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)       # e.g. 78.5
    term = db.Column(db.String(20), nullable=False)   # e.g. "Term 1"
    year = db.Column(db.Integer, nullable=False)       # e.g. 2026
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Grade {self.student_id}-{self.subject_id}: {self.score}>'