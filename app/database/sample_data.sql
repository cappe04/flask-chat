BEGIN;

INSERT INTO users(username, password) VALUES("cappe_04", "$2b$12$Jr9nKCkuP6vOMDKPjc.loujRjUmsZEUYPV0GCdaYh/xRqYUbApx5u");
INSERT INTO users(username, password) VALUES("guest", "$2b$12$Jr9nKCkuP6vOMDKPjc.loujRjUmsZEUYPV0GCdaYh/xRqYUbApx5u");

INSERT INTO channels(user_id, channel_name, description) VALUES(1, "Channel A", "This is a description");
INSERT INTO channels(user_id, channel_name, description) VALUES(1, "Channel B", "This is a description");
INSERT INTO channels(user_id, channel_name, description) VALUES(2, "Channel C", "This is a description");
INSERT INTO channels(user_id, channel_name, description) VALUES(2, "Channel D", "This is a description");

COMMIT;