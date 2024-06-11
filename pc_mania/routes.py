from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from pc_mania import app, db
from pc_mania.forms import AddingForm, LoginForm, RegisterForm
from pc_mania.models import (CPU, HDD, RAM, SSD, Cases, Cooler, GraphicalCard,
                             Motherboards, PowerSupply, User)


class Configuration:

    def __init__(self):
        self.socket: str = ""
        self.form_factor: str = ""
        self.price = 0
        self.required_watts: int = 0
        self.configuration: dict = {}
        self.is_motherboard_chosen: bool = False
        self.is_chosen_everything: bool = self.get_state_of_choice()

    def get_socket(self):
        return self.socket

    def set_socket(self, socket: str):
        self.socket = socket

    def get_form_factor(self):
        return self.form_factor

    def set_form_factor(self, form_factor: str):
        self.form_factor = form_factor

    def null_price(self):
        self.price = 0

    def get_total_price(self):
        return self.price

    def increase_price(self, value: int):
        self.price += value

    def get_configuration(self):
        return self.configuration

    def add_item_to_configuration(self, item_name: str, item: dict):
        self.configuration[f'{item_name}'] = item

    def get_required_watts(self):
        return self.required_watts

    def add_watts_to_watts_field(self, watts: int):
        self.required_watts += watts

    def get_motherboard_choice_status(self):
        return self.is_motherboard_chosen

    def set_motherboard_status(self, new_value: bool):
        self.is_motherboard_chosen = new_value

    def get_state_of_choice(self):
        return len(self.get_configuration()) == 8

    def set_state_of_choice(self, new_value: bool):
        self.is_chosen_everything = new_value


configuration = Configuration()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('constructor_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('constructor_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/submit')
def submit_build_page():
    flash('Success! We will start building your PC as soon as possible. We will e-mail '
          'you when it is done', category='success')
    if len(configuration.get_configuration()) == 9:
        configuration.configuration = {}
        configuration.set_motherboard_status(False)
        configuration.set_state_of_choice(False)
        configuration.null_price()
    return redirect(url_for('home_page'))


@app.route('/motherboards', methods=['GET', 'POST'])
@login_required
def motherboards_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = Motherboards.query.filter_by(name=added_item).first()
        if added_item_object:
            configuration.set_socket(added_item_object.socket)
            configuration.set_form_factor(added_item_object.form_factor)
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('motherboard', dict_item_to_add)
            configuration.set_motherboard_status(True)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        motherboards = Motherboards.query.all()
        return render_template('motherboards.html', motherboards=motherboards,
                               adding_form=adding_form)


@app.route('/cpus', methods=['GET', 'POST'])
@login_required
def cpus_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = CPU.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('cpu', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        cpus = CPU.query.filter(CPU.socket == configuration.get_socket()).all()
        return render_template('cpus.html', cpus=cpus, adding_form=adding_form)


@app.route('/coolers', methods=['GET', 'POST'])
@login_required
def coolers_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = Cooler.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('cooler', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        coolers = Cooler.query.filter(Cooler.compatible_socket == configuration.get_socket()).all()
        return render_template('coolers.html', coolers=coolers, adding_form=adding_form)


@app.route('/cases', methods=['GET', 'POST'])
@login_required
def cases_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = Cases.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('case', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        cases = Cases.query.filter(Cases.motherboard_form_factor == configuration.get_form_factor()).all()
        return render_template('cases.html', cases=cases, adding_form=adding_form)


@app.route('/rams', methods=['GET', 'POST'])
@login_required
def rams_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = RAM.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('ram', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        rams = RAM.query.all()
        return render_template('ram.html', rams=rams, adding_form=adding_form)


@app.route('/hdds', methods=['GET', 'POST'])
@login_required
def hdds_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = HDD.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('hdd', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        hdds = HDD.query.all()
        return render_template('hdd.html', hdds=hdds, adding_form=adding_form)


@app.route('/graphical_cards', methods=['GET', 'POST'])
@login_required
def graphical_cards_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = GraphicalCard.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('graphical_card', dict_item_to_add)
            configuration.add_watts_to_watts_field(dict_item_to_add["tdp"])
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        graphical_cards = GraphicalCard.query.all()
        return render_template('graphical_cards.html', graphical_cards=graphical_cards,
                               adding_form=adding_form)


@app.route('/ssds', methods=['GET', 'POST'])
@login_required
def ssds_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = SSD.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('ssd', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('constructor_page'))
    elif request.method == "GET":
        ssds = SSD.query.all()
        return render_template('ssd.html', ssds=ssds, adding_form=adding_form)


@app.route('/power_supplies', methods=['GET', 'POST'])
@login_required
def power_supplies_page():
    adding_form = AddingForm()
    if request.method == "POST":
        added_item = request.form.get('added_item')
        added_item_object = PowerSupply.query.filter_by(name=added_item).first()
        if added_item_object:
            dict_item_to_add: dict = added_item_object.__dict__
            dict_item_to_add.pop('_sa_instance_state')
            dict_item_to_add.pop('id')
            configuration.add_item_to_configuration('power_supply', dict_item_to_add)
            configuration.increase_price(dict_item_to_add["price"])
        return redirect(url_for('configuration_page'))
    elif request.method == "GET":
        required_minimum_watts_power = configuration.get_required_watts()
        power_supplies = PowerSupply.query.filter(PowerSupply.power_supply_watt >= required_minimum_watts_power)
        return render_template('power_supply.html', power_supplies=power_supplies,
                               adding_form=adding_form)


@app.route('/constructor')
@login_required
def constructor_page():
    if len(configuration.get_configuration()) == 9:
        configuration.configuration = {}
        configuration.set_motherboard_status(False)
        configuration.set_state_of_choice(False)
        configuration.null_price()
    return render_template('constructor.html',
                           motherboard_choice_status=configuration.get_motherboard_choice_status(),
                           is_chosen_everything=configuration.get_state_of_choice())


@app.route('/configuration')
@login_required
def configuration_page():
    return render_template('configuration.html',
                           config=configuration.get_configuration(),
                           total_cost=configuration.get_total_price())
