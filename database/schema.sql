DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS messages;

CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    profile_picture BLOB
);

CREATE TABLE channels(
    channel_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    channel_name VARCHAR(30) NOT NULL
);

CREATE TABLE messages(
    message_id INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    message TEXT,
    post_time INTEGER
);
