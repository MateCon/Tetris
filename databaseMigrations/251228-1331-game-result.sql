CREATE TABLE result (
   user_name VARCHAR(20) references tetris_user(name),
   score INT,
   last_level INT,
   lines INT,
   creation_date TIMESTAMP,
   time_of_play INT
);
