-- the structure, create tables

-- user information
CREATE TABLE users ( 
    user_id SERIAL PRIMARY KEY, -- unique id
    first_name varchar(100) NOT NULL, -- cannot accept null values
    last_name varchar(100) NOT NULL,
    email varchar(100) UNIQUE NOT NULL, -- email must be unique, all values are different
    password varchar(50) NOT NULL
);

-- hobbies
CREATE TABLE hobbies (
    hobby_id SERIAL PRIMARY KEY,
    hobby_name varchar(100) NOT NULL -- the hobby 
);

-- the user's hobbies
CREATE TABLE user_hobbies ( -- connects the user and hobby tables together
    user_hobby_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE, -- connects the user's id to table
    hobby_id INT REFERENCES hobbies(hobby_id) ON DELETE CASCADE, -- deletes when a user or hobby is removed
    UNIQUE (user_id, hobby_id) -- cannot duplicate hobbies
);