from App import db, app
from App.models import UserModel
from flask import Flask, render_template, request, redirect, url_for, session, flash
from App.sendmails import Sendmail

store_email = None;
store_password = None;
global val_e_mail
val_e_mail = None; 

@app.route('/', methods=['GET', 'POST'])
def home():
	global val_e_mail
	if "email" in session:
		if request.method == 'POST':
			session['searching'] = "search";

			return redirect(url_for("search"));

		return render_template("home.html", account_mail=session['email']) 
	else:	
		return redirect(url_for("login"))

@app.route('/search', methods=['GET', 'POST'])
def search():
	if 'searching' in session:
		search = request.form.get("search");
		print(search)
		search_res = "%{}%".format(search);
		
		check_pass_word = UserModel.query.filter(UserModel.password.like(search_res)).all()
		check_mail = UserModel.query.filter(UserModel.e_mail.like(search_res)).all()
		
		return render_template('search_results.html', infor=check_mail);
	else:
		return redirect(url_for('home'))	

@app.route('/login', methods=['GET', 'POST'])
def login():
	global val_e_mail
	if request.method == 'POST':
		val_e_mail = request.form.get('e_mail');
		password = request.form.get('password');
		user = UserModel.query.filter_by(e_mail=val_e_mail).first();
		pass_word = UserModel.query.filter_by(password=password).first();
		if val_e_mail == "" and password == "":
			flash("Empty E-mail or Password", category="danger")
		else:	
			if user:
				if pass_word:
					session['email'] = val_e_mail;
					return redirect(url_for("home"))
				else:
					flash("Incorrect Password, Try Again", category='danger')
			else:
				flash("Incorrect E-Mail, Try Again", category='danger')			
	return render_template('login.html');



@app.route('/verify', methods=['GET', 'POST'])

def Verify():
	global p
	global sent
	print(p)
	if store_email != None:
		while p < 1:
			sent = Sendmail(store_email);
			p+=1;

		if request.method == 'POST':
			store_ver_1 = request.form.get('ver1');
			store_ver_2 = request.form.get('ver2');
			store_ver_3 = request.form.get('ver3');
			store_ver_4 = request.form.get('ver4');

			full_code = str(store_ver_1) + str(store_ver_2) + str(store_ver_3) + str(store_ver_4);
			if full_code == sent.orignal_code:
				storing_email_and_pass_in_db = UserModel(e_mail=store_email, password=store_password);
				db.session.add(storing_email_and_pass_in_db);
				db.session.commit();
				return redirect(url_for("login"));

		return render_template('verify.html', v_mail=store_email);
	elif 'password' in session:
		return redirect(url_for("/"));
	else:
		return redirect(url_for("login"));

			
@app.route('/signIn', methods=['GET', 'POST'])
def Signup():
	global store_email
	global store_password
	global p
	p = 0;
	if request.method == 'POST':
		store_email = request.form.get('st_mail');
		store_password = request.form.get('st_password');
		retype_password = request.form.get('confirm_password');
		print(str(p) + "during signup");
		if (store_password == retype_password != ""):
			return redirect(url_for("Verify"));
			
	return render_template("sign_in.html");

@app.route('/account-creation', methods=['GET', 'POST'])
def account():
	return render_template('account_creation.html')

@app.route('/logout')
def logout():
	#session.pop('password', None);
	return redirect(url_for("login"));









