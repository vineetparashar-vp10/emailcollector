from App import db, app


class UserModel(db.Model):
	id = db.Column(db.Integer(), primary_key=True);
	e_mail = db.Column(db.String(length=20), nullable=False);
	password = db.Column(db.String(length=20), nullable=False);

	def __repr__(self):
		return f"User({self.id}, {self.e_mail}, {self.password})\n";
