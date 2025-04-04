from flask import Flask, request, jsonify
from models import db, User, Hobby, UserHobby

app = Flask(__name__) # creates the app

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

@app.route('/users/<int:user_id', methods=['PUT']) # Update the users
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    db.session.commit()
    return jsonify({'message': 'Updated User'})

@app.route('/users/<int:user_id', methods=['DELETE']) # Delete the users
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

@app.route('/hobbies/<int:hobby_id', methods=['PUT']) # Update the hobbies
def update_hobby(hobby_id):
    hobby = Hobby.query.get_or_404(hobby_id)
    data = request.json
    hobby.name = data.get('hobby_name', hobby.hobby_name)
    db.session.commit()
    return jsonify({'message': 'Updated Hobby'})

@app.route('/hobbies/<int:hobby_id', methods=['DELETE']) # Delete the hobbies
def delete_hobby(hobby_id):
    hobby = Hobby.query.get_or_404(hobby_id)
    db.session.delete(hobby)
    db.session.commit()
    return jsonify({'message': 'Deleted Hobby'})


# CRUD FUNCTIONALITES FOR USER HOBBIES
@app.route('/users/<int:user_id>/hobbies', methods=['POST']) # Add a hobby to a user
def add_hobby(user_id):
    data = request.json
    hobby = Hobby.query.get_or_404(data['hobby_id'])

    # Add to user_hobbies table
    user_hobby = UserHobby(user_id = user_id, hobby_id = hobby.hobby_id)
    db.session.add(user_hobby)
    db.session.commit()
    return jsonify({'message': 'Added Hobby to User'}), 201

@app.route('/users/<int:user_id>/hobbies', methods=['GET']) # Retrieve the user's hobbies
def get_user_hobbies(user_id):
    user = User.query.get_or_404(user_id)
    hobbies = user.hobbies 
    return jsonify([{ # create a list
        'id': hobby.hobby_id,
        'name': hobby.hobby_name,
    }for hobby in hobbies])

@app.route('/users/<int:user_id/hobbies/<int:hobby_id>', methods=['DELETE']) # Delete the user's hobbies
def delete_user_hobbies(user_id, hobby_id):
    user_hobby = User.query.filter_by(user_id = user_id, hobby_id = hobby_id).first() # find first instance from query
    db.session.delete(user_hobby)
    db.session.commit()
    return jsonify({'message': 'Deleted Hobby From User'})