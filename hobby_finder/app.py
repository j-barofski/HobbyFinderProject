from flask import Flask, request, jsonify
from models import db, User, Hobby, SavedHobby

from flask_cors import CORS


app = Flask(__name__) # creates the app
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobby_finder.db' # location of the database
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False # do not want notis

db.init_app(app) # link db and app
    

# CRUD FUNCTIONALITES FOR USERS
@app.route('/users', methods=['POST']) # Create the users
def create_user():
    data = request.json
    new_user = User(
        full_name = data['full_name'],
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
        'full_name': user.full_name,
        'email': user.email
    })

@app.route('/users/<int:user_id>', methods=['PUT']) # Update the users
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.full_name = data.get('full_name', user.full_name)
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
@app.route('/hobbies', methods=['GET']) # Retrieve the hobbies
def get_hobbies():
    hobbies = Hobby.query.all()
    return jsonify([{ # create a list
        'hobby_id': h.hobby_id,
        'hobby_name': h.hobby_name
    } for h in hobbies])


# CRUD FUNCTIONALITES FOR SAVED HOBBIES
@app.route('/users/<int:user_id>/hobbies', methods=['POST']) # Save a hobby to a user
def save_hobbies(user_id):
    try:
        if user_id is None:
            return jsonify({"error": "User ID is missing"}), 400
 
        data = request.json
        print(f"Received data: {data}") 
        
        hobby_id = data.get('hobby_id')

        hobby = Hobby.query.get_or_404(hobby_id)

        # Ensure the hobby exists in the hobbies table
        if not hobby:
            return jsonify({'message': 'Hobby not found'}), 404 
        
        # if hobby already saved
        already_saved = SavedHobby.query.filter_by(user_id=user_id, hobby_id=hobby.hobby_id).first()
        if already_saved:
            return jsonify({'message': 'Hobby already saved'}), 400
        
        # Add to user_hobbies table
        saved_hobbies = SavedHobby(user_id = user_id, hobby_id = hobby.hobby_id)

        db.session.add(saved_hobbies)
        db.session.commit()

        print(f"Hobby {hobby.hobby_name} saved for user {user_id}")
        
        return jsonify({'message': 'Saved Hobby to User'}), 201
    
    except Exception as e:
        print(f"Error saving hobby: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/users/<int:user_id>/hobbies', methods=['GET']) # Retrieve the user's saved hobbies
def get_user_hobbies(user_id):
    saved_hobbies = db.session.query(Hobby).join(SavedHobby).filter(SavedHobby.user_id == user_id).all()
    print(f"User hobbies for {user_id}: {saved_hobbies}")
    saved_hobbies_list = [{'id': hobby.hobby_id, 'name': hobby.hobby_name} for hobby in saved_hobbies]
    return jsonify(saved_hobbies_list)


@app.route('/users/<int:user_id>/hobbies/<int:hobby_id>', methods=['DELETE']) # Delete the user's saved hobbies
def delete_user_hobbies(user_id, hobby_id):
    saved_hobbies = SavedHobby.query.filter_by(user_id = user_id, hobby_id = hobby_id).first() # find first instance from query
    if saved_hobbies:
        db.session.delete(saved_hobbies)
        db.session.commit()
        return jsonify({'message': 'Deleted Hobby From User'}), 200
    else: 
        return jsonify({'message': 'Hobby not found'}), 404

# get hobby names
@app.route('/hobbies/<hobby_name>', methods=['GET'])
def get_hobby_by_name(hobby_name):
    hobby = Hobby.query.filter_by(hobby_name=hobby_name).first()
    if hobby:
        return jsonify({
            "hobby_id": hobby.hobby_id,
            "name": hobby.hobby_name
        })
    else:
        return jsonify({'error': 'Hobby not found'}), 404

# Login for user
@app.route('/login', methods=['POST'])
def login():
    try: 
        if request.method == 'OPTIONS': # pre-flight request
            return '', 200 # 200 and CORS header
        data = request.json
        user = User.query.filter_by(email = data['email']).first() # find user
        if user and user.password == data['password']: # if passwords match
            return jsonify({'message': 'Logged in the User', 'user_id': user.user_id}), 200 # successful login
        else:
            return jsonify({'message': 'Unsuccessful Login Attempt'}), 401 # unsuccessful
    except Exception as e:
        print("Error in /login:", e)
        return jsonify({'message': 'Internal server error'}), 500
        
# Sign up for user
@app.route('/signup', methods=['POST'])
def signup():
    try: 
        if request.method == 'OPTIONS': # pre-flight request
            return '', 200 # 200 and CORS header
        data = request.json
        if not data.get('fullname') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Please fill out the form.'}), 400 # missing input
        
        existing_user = User.query.filter_by(email = data['email']).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 409 # check for existing users
        
        new_user = User( # making the new user
            full_name = data['fullname'],
            email = data['email'],
            password = data['password']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User signed up', 'user_id': new_user.user_id}), 201
    except Exception as e:
        print("Error in /signup:", e)
        return jsonify({'message': 'Internal server error'}), 500
    
# forgot password, resets for now
@app.route('/forgot', methods=['POST'])
def forgot_password():
    try: 
        if request.method == 'OPTIONS': # pre-flight request
            return '', 200 # 200 and CORS header
        
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({'message': 'Please enter your email'}), 400 # missing input
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            return jsonify({'message': 'Resetting password now'}), 200
        else:
            return jsonify({'message': 'Email not found'}), 404

    except Exception as e:
        print("Error in /forgot:", e)
        return jsonify({'message': 'Internal server error'}), 500

# Runs the app on port 5000
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creating DB tables
    app.run(debug=True, host='127.0.0.1', port=5050)  