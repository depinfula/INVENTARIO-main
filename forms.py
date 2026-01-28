from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from datetime import datetime
from models import Department, Personnel, Area, Equipment

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class DepartmentForm(FlaskForm):
    name = StringField('Nombre del Departamento', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[Optional()])
    submit = SubmitField('Guardar')

class AreaForm(FlaskForm):
    name = StringField('Nombre de la Biblioteca', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[Optional()])
    location = StringField('Ubicación', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Guardar')

class EquipmentForm(FlaskForm):
    code = StringField('Código', validators=[DataRequired(), Length(max=50)])
    serial = StringField('Serial', validators=[DataRequired(), Length(max=100)])
    equipment_type = SelectField('Tipo de Equipo', 
                                choices=[('Laptop', 'Laptop'), ('Desktop', 'Desktop'), 
                                        ('Monitor', 'Monitor'), ('Impresora', 'Impresora'),
                                        ('Tablet', 'Tablet'), ('Servidor', 'Servidor'),
                                        ('Router', 'Router'), ('Switch', 'Switch'),
                                        ('Disco Duro', 'Disco Duro'), ('Memoria RAM', 'Memoria RAM'),
                                        ('Procesador', 'Procesador'), ('Tarjeta Gráfica', 'Tarjeta Gráfica'),
                                        ('Tarjeta Madre', 'Tarjeta Madre'), ('Tarjeta de Red', 'Tarjeta de Red'),
                                        ('Tarjeta de Sonido', 'Tarjeta de Sonido'), ('Tarjeta de Video', 'Tarjeta de Video'),
                                        ('Teclado', 'Teclado'), ('Mouse', 'Mouse'), ('Audífonos', 'Audífonos'),('Regulador','Regulador'),
                                        ('Otro', 'Otro')],
                                validators=[DataRequired()])
    brand = StringField('Marca', validators=[Optional(), Length(max=100)])
    model = StringField('Modelo', validators=[Optional(), Length(max=100)])
    status = SelectField('Estatus', 
                        choices=[('Disponible', 'Disponible'), ('Asignado', 'Asignado'),
                                ('Mantenimiento', 'Mantenimiento'), ('Baja', 'Baja')],
                        validators=[DataRequired()])
    department_id = SelectField('Departamento', coerce=int, validators=[DataRequired()])
    area_id = SelectField('Biblioteca', coerce=lambda x: int(x) if x else None, validators=[Optional()])
    assigned_to_id = SelectField('Asignado a', coerce=lambda x: int(x) if x else None, validators=[Optional()])
    image = FileField('Foto del Equipo', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')])
    ip_address = StringField('Dirección IP', validators=[Optional(), Length(max=45)])
    physical_address = StringField('Dirección Física (MAC)', validators=[Optional(), Length(max=50)], 
                                   render_kw={"placeholder": "Ej: 00:1B:44:11:3A:B7"})
    specifications = TextAreaField('Especificaciones Técnicas', validators=[Optional()], 
                                   render_kw={"rows": 5, "placeholder": "Ej: RAM: 8GB DDR4, Procesador: Intel Core i5, Disco: 256GB SSD, etc."})
    registration_date = DateField('Fecha de Registro', validators=[DataRequired()], default=datetime.utcnow)
    assignment_date = DateField('Fecha de Asignación', validators=[Optional()])
    purchase_date = DateField('Fecha de Compra', validators=[Optional()])
    warranty_expiry = DateField('Vencimiento de Garantía', validators=[Optional()])
    notes = TextAreaField('Notas', validators=[Optional()])
    submit = SubmitField('Guardar')
    
    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        from models import db
        departments = Department.query.order_by(Department.name).all()
        self.department_id.choices = [(d.id, d.name) for d in departments] if departments else []
        
        areas = Area.query.order_by(Area.name).all()
        self.area_id.choices = [('', 'Ninguna')] + [(a.id, a.name) for a in areas] if areas else [('', 'Ninguna')]
        
        personnel = Personnel.query.order_by(Personnel.name).all()
        self.assigned_to_id.choices = [('', 'Ninguno')] + [(p.id, f'{p.name} {p.last_name}') 
                                                           for p in personnel] if personnel else [('', 'Ninguno')]

class PersonnelForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    position = StringField('Cargo', validators=[Optional(), Length(max=100)])
    employee_id = StringField('ID de Empleado', validators=[Optional(), Length(max=50)])
    department_id = SelectField('Departamento', coerce=int, validators=[DataRequired()])
    area_id = SelectField('Biblioteca', coerce=lambda x: int(x) if x else None, validators=[Optional()])
    submit = SubmitField('Guardar')
    
    def __init__(self, *args, **kwargs):
        super(PersonnelForm, self).__init__(*args, **kwargs)
        from models import db
        departments = Department.query.order_by(Department.name).all()
        self.department_id.choices = [(d.id, d.name) for d in departments] if departments else []
        
        areas = Area.query.order_by(Area.name).all()
        self.area_id.choices = [('', 'Ninguna')] + [(a.id, a.name) for a in areas] if areas else [('', 'Ninguna')]

class AssignmentForm(FlaskForm):
    equipment_id = SelectField('Equipo', coerce=int, validators=[DataRequired()])
    personnel_id = SelectField('Personal', coerce=int, validators=[DataRequired()])
    assignment_date = DateField('Fecha de Asignación', validators=[DataRequired()])
    return_date = DateField('Fecha de Devolución', validators=[Optional()])
    status = SelectField('Estatus', 
                        choices=[('Activa', 'Activa'), ('Devuelta', 'Devuelta'), ('Cancelada', 'Cancelada')],
                        validators=[DataRequired()])
    notes = TextAreaField('Notas', validators=[Optional()])
    submit = SubmitField('Guardar')
    
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        from models import db
        # Solo mostrar equipos disponibles o asignados
        equipments = Equipment.query.filter(Equipment.status.in_(['Disponible', 'Asignado'])).order_by(Equipment.code).all()
        self.equipment_id.choices = [(e.id, f'{e.code} - {e.equipment_type} ({e.brand or ""} {e.model or ""})') 
                                     for e in equipments] if equipments else []
        
        personnel = Personnel.query.order_by(Personnel.name).all()
        self.personnel_id.choices = [(p.id, f'{p.name} {p.last_name} - {p.department.name}') 
                                    for p in personnel] if personnel else []
