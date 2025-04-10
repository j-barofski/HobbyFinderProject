from flask import Flask, request, jsonify
from models import db, User, Hobby, SavedHobby

from flask_cors import CORS

app = Flask(__name__) # creates the app
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobby_finder.db' # location of the database
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False # do not want notis

db.init_app(app) # link db and app
    

# CRUD FUNCTIONALITES FOR USERS
@app.route('/users', methods=['POST']) # Create the users
def create_user():
    data = request.json
    new_user = User(
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Added User'}), 201

@app.route('/users/<int:user_id>', methods=['GET']) # Retrieve the users info
def get_user(user_id):
    user = User.query.get_or_404(user_id) # if not found, raise a 404 error
    return jsonify({ # create a list
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    })

@app.route('/users/<int:user_id>', methods=['PUT']) # Update the users
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    db.session.commit()
    return jsonify({'message': 'Updated User'})

@app.route('/users/<int:user_id>', methods=['DELETE']) # Delete the users
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Deleted User'})


# CRUD FUNCTIONALITES FOR HOBBIES
@app.route('/hobbies', methods=['POST']) # Create the hobbies
def create_hobby():
    data = request.json
    new_hobby = Hobby(
        hobby_name = data['name'],
    )
    db.session.add(new_hobby)
    db.session.commit()
    return jsonify({'message': 'Added Hobby'}), 201

@app.route('/hobbies', methods=['GET']) # Retrieve the hobbies
def get_hobby():
    hobbies = Hobby.query.all()
    return jsonify([{ # create a list
        'hobby_id': h.hobby_id,
        'hobby_name': h.hobby_name
    } for h in hobbies])

@app.route('/hobbies/<int:hobby_id>', methods=['PUT']) # Update the hobbies
def update_hobby(hobby_id):
    hobby = Hobby.query.get_or_404(hobby_id)
    data = request.json
    hobby.hobby_name = data.get('hobby_name', hobby.hobby_name)
    db.session.commit()
    return jsonify({'message': 'Updated Hobby'})

@app.route('/hobbies/<int:hobby_id>', methods=['DELETE']) # Delete the hobbies
def delete_hobby(hobby_id):
    hobby = Hobby.query.get_or_404(hobby_id)
    db.session.delete(hobby)
    db.session.commit()
    return jsonify({'message': 'Deleted Hobby'})


# CRUD FUNCTIONALITES FOR SAVED HOBBIES
@app.route('/users/<int:user_id>/hobbies', methods=['POST']) # Save a hobby to a user
def save_hobby(user_id):
    data = request.json
    hobby = Hobby.query.get_or_404(data['hobby_id'])

    # Add to user_hobbies table
    saved_hobby = SavedHobby(user_id = user_id, hobby_id = hobby.hobby_id)

    # if hobby already saved
    already_saved = SavedHobby.query.filter_by(user_id=user_id, hobby_id=hobby.hobby_id).first()
    if already_saved:
        return jsonify({'message': 'Hobby already saved'}), 409

    db.session.add(saved_hobby)
    db.session.commit()
    return jsonify({'message': 'Saved Hobby to User'}), 201


@app.route('/users/<int:user_id>/hobbies', methods=['GET']) # Retrieve the user's saved hobbies
def get_user_hobbies(user_id):
    user = User.query.get_or_404(user_id)
    hobbies = user.hobbies 
    return jsonify([{ # create a list
        'id': hobby.hobby_id,
        'name': hobby.hobby_name,
    }for hobby in hobbies])

@app.route('/users/<int:user_id>/hobbies/<int:hobby_id>', methods=['DELETE']) # Delete the user's saved hobbies
def delete_user_hobbies(user_id, hobby_id):
    saved_hobby = SavedHobby.query.filter_by(user_id = user_id, hobby_id = hobby_id).first() # find first instance from query
    db.session.delete(saved_hobby)
    db.session.commit()
    return jsonify({'message': 'Deleted Hobby From User'})



# Login for user
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email = data['email']).first() # find user
    if user and user.password == data['password']: # if passwords match
        return jsonify({'message': 'Logged in the User', 'user_id': user.user_id}) # successful login
    else:
        return jsonify({'message': 'Unsuccessful Login Attempt'}) # unsuccessful
    
# Sign up for user
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data.get('fullname') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Please fill out the form.'}), 400 # missing input
    
    existing_user = User.query.filter_by(email = data['email']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409 # check for existing users
    
    new_user = User( # making the new user
        fullname = data['fullname'],
        email = data['email'],
        password = data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User signed up', 'user_id': new_user.user_id}), 201


# Runs the app on port 5500
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5500)  