from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    equipments = db.relationship('Equipment', backref='department', lazy=True, cascade='all, delete-orphan')
    personnel = db.relationship('Personnel', backref='department', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(100))
    employee_id = db.Column(db.String(50), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    equipments = db.relationship('Equipment', backref='assigned_personnel', lazy=True)
    
    def __repr__(self):
        return f'<Personnel {self.name} {self.last_name}>'

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    equipments = db.relationship('Equipment', backref='area', lazy=True, cascade='all, delete-orphan')
    personnel = db.relationship('Personnel', backref='area', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Area {self.name}>'

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    serial = db.Column(db.String(100), unique=True, nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)  # Laptop, Desktop, Monitor, etc.
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False, default='Disponible')  # Disponible, Asignado, Mantenimiento, Baja
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=True)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 o IPv6 (máx 45 caracteres)
    physical_address = db.Column(db.String(50), nullable=True)  # Dirección MAC
    specifications = db.Column(db.Text, nullable=True)  # Especificaciones técnicas (RAM, Procesador, etc.)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assignment_date = db.Column(db.DateTime, nullable=True)
    purchase_date = db.Column(db.DateTime)
    warranty_expiry = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    assignments = db.relationship('Assignment', backref='equipment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Equipment {self.code}>'

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    assignment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Activa')  # Activa, Devuelta, Cancelada
    notes = db.Column(db.Text)
    assigned_by = db.Column(db.String(100))  # Usuario que realizó la asignación
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    personnel = db.relationship('Personnel', backref='assignments', lazy=True)
    
    def __repr__(self):
        return f'<Assignment {self.equipment.code} -> {self.personnel.name}>'

