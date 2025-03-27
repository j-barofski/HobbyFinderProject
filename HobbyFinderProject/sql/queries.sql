-- store the tables

-- users
INSERT INTO users(first_name, last_name, email, password) -- add users and their info to the table
VALUES ('test', 'example', 'test@example.com', 'test_password'),
       ('second', 'test', 'second@test.com', 'second_password');

-- hobbies
INSERT INTO hobbies(hobby_name) -- add hobbies to table
VALUES ('testing'),
       ('learning');

-- user_hobbies
INSERT INTO user_hobbies(user_id, hobby_id) -- uses the ids from the user and hobby
VALUES (1, 2), -- user id connected to hobby 2
       (2, 1); 

-- Retrieves the user's hobbies
SELECT hobby.hobby_name -- gets the hobby from the hobbies table
FROM hobbies AS hobby -- using hobby as an alias
JOIN user_hobbies AS user_hobby ON hobby.hobby_id = user_hobby.hobby_id -- combine the tables, connects the hobbies with the users
WHERE user_hobby.user_id = 1; -- gets the hobby from the 1st user, -- temporary

-- Removes users
DELETE FROM users WHERE user_id = 2; -- removes the 2nd user, temporary test