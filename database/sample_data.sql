BEGIN;

INSERT INTO users(rowid, username, password) VALUES(NULL, "Person1", "$2b$12$Exh2YJG5vlvk32jmOkZy/Omtap3uRCj3W3z1XFVDeNa2.xhL4yPgm");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person2", "$2b$12$S..KlAxPYchrwgN/xZFxA.w7jKjR8KnBysuEt047FGvKQsY7vEvoy");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person3", "$2b$12$dOdok/tSuGqNgdDuBem.TeKjvXl8SyNW3GCynR6zsG.xFaGkjLTa6");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person4", "$2b$12$OEphDODcHMHwl.vpkNnpBu8.WVJWGsrLH8Z8nYdVhMqd2zJYeeYqC");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person5", "$2b$12$iozdQF4/A5Td7lvJXi0JbOJPGOQy76gqEgZio6GWNmk6Fi9di62A.");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person6", "$2b$12$SoGR0f6Hqzu2BY4GjivhLunrTxE7W22mStZFCGAskejOnI9QWHU7u");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person7", "$2b$12$v5/8v80DzI51XjpU8V380O2jWvHU16WIxlgoAhxcbKqOzIDIPivWy");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person8", "$2b$12$pTNfQXsgMIl9jlcB9w1K7.tzxPbKxwzlX4flj1WZ1yJCu/aWrbiea");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person9", "$2b$12$16FcC3qc1pJZQ5kLgpQZoe2nyvLoyQIgQ6yJjNIfpTSIftQM2VzNG");
INSERT INTO users(rowid, username, password) VALUES(NULL, "Person10", "$2b$12$rdNnsOIHhzVQQy7qEsi7iuJ3UBmZiBMZ1B6G4VoFbmu.RxuVJ53Ye");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 5, "Channel1");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 4, "Channel2");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 5, "Channel3");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 6, "Channel4");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 1, "Channel5");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 3, "Channel6");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 4, "Channel7");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 9, "Channel8");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 3, "Channel9");
INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, 3, "Channel10");

COMMIT;