from pc_mania import db, bcrypt, login_manager
from flask_login import UserMixin


class Motherboards(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=30), nullable=False)
    form_factor = db.Column(db.String(length=10), nullable=False)
    socket = db.Column(db.String(length=4), nullable=False)
    chipset = db.Column(db.String(length=5), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class CPU(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    socket = db.Column(db.String(length=5), nullable=False, unique=False)
    base_clock = db.Column(db.Float(), nullable=False, unique=False)
    turbo_clock = db.Column(db.Float(), nullable=False, unique=False)
    number_of_cores = db.Column(db.Integer(), nullable=False)
    number_of_threads = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class Cases(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=80), nullable=False)
    motherboard_form_factor = db.Column(db.String(length=10), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class Cooler(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=80), nullable=False)
    compatible_socket = db.Column(db.String(length=10), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class RAM(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    size = db.Column(db.Integer(), nullable=False)
    ram_type = db.Column(db.String(length=10), nullable=False)
    sticks = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class HDD(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    size_in_tb = db.Column(db.Integer(), nullable=False)
    rpm = db.Column(db.Integer(), nullable=False)
    cache_in_mb = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class GraphicalCard(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    graphic_card = db.Column(db.String(length=30), nullable=False)
    vram = db.Column(db.Integer(), nullable=False)
    tdp = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class SSD(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=100), nullable=False)
    size_in_gb = db.Column(db.Integer(), nullable=False)
    protocol = db.Column(db.String(length=5), nullable=False)
    form_factor = db.Column(db.String(length=5), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class PowerSupply(db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    size = db.Column(db.String(length=5), nullable=False)
    power_supply_watt = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
