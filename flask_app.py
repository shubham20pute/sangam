from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    institute = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    interest = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    business_info = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.name}>'

# Route to render the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        # Get form data
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        institute = request.form['institute']
        user_type = request.form['userType']
        interest = request.form.get('interest')  # May not be present for business owners
        experience = request.form.get('experience')  # May not be present if interest is not selected
        business_info = request.form.get('businessInfo')  # Only for business owners

        # Create a new user instance
        new_user = User(
            name=name,
            mobile=mobile,
            email=email,
            address=address,
            institute=institute,
            user_type=user_type,
            interest=interest,
            experience=experience,
            business_info=business_info
        )

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.id

        flash('Form submitted successfully!', 'success')
        subject = "Congratulations! You've won a Free Voucher!"
        html_content = render_template('voucher.html')

        send_email(email,html_content,subject)

        return render_template('voucher.html', id = user_id, name = name)
        # return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    image_url = request.host_url + "static/voucher_bg.png" # url_for('static', filename='voucher_bg.png')
    html = render_template('voucher.html', ref_id = 420, name = "Shonu eye", img = image_url)
    send_email("shubhamvispute055@gmail.com",html,"Testing")
    return html

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
