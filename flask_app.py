from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from utils import *
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

def generate_uuid():
    return str(uuid.uuid4()) 

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
    code = db.Column(db.String(40), unique=True, nullable=False, default=generate_uuid)

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

        code = new_user.code

        flash('Form submitted successfully!', 'success')
        subject = "Congratulations! You've won a Free Voucher!"
        link = request.host_url + "voucher/"+str(code)
        html_content = render_template('voucher_link.html', link = link)

        send_email_in_background(email,html_content,subject)

        image_url = request.host_url + "static/voucher_bg.png" # url_for('static', filename='voucher_bg.png')
        #html = render_template('voucher.html', ref_id = 420, name = "Shonu eye", img = image_url)

        return render_template('voucher.html', id =new_user.id, name = name, img = image_url)
        # return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/voucher/<token>', methods=['GET'])
def voucher(token):
    image_url = request.host_url + "static/voucher_bg.png" # url_for('static', filename='voucher_bg.png')

    user = User.query.filter_by(code=token).first()

    if user:

        html = render_template('voucher.html', id = user.id, name = user.name, img = image_url)
        # html = render_template('voucher_link.html', ref_id = 420, name = "Shonu eye", img = image_url)

        #send_email("shubhamvispute055@gmail.com",html,"Testing")
        return html
    else:
        return "It looks like link is invalid...",500
    

@app.route('/test', methods=['GET', 'POST'])
def test():
    image_url = request.host_url + "static/voucher_bg.png" # url_for('static', filename='voucher_bg.png')
    #html = render_template('voucher.html', ref_id = 420, name = "Shonu eye", img = image_url)
    html = render_template('voucher_link.html', ref_id = 420, name = "Shonu eye", img = image_url)

    #send_email("shubhamvispute055@gmail.com",html,"Testing")
    return html


with app.app_context():
        db.create_all()  # Create tables if they don't exist

if __name__ == '__main__':
    app.run(debug=True)
