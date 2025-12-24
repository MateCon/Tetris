CREATE TABLE tetris_user (
  name VARCHAR(20) PRIMARY KEY,
  password VARCHAR(100)
);

CREATE TABLE session (
   id VARCHAR(50) PRIMARY KEY,
   user_name VARCHAR(20) references tetris_user(name),
   creation_date TIMESTAMP,
   duration INTERVAL
);
