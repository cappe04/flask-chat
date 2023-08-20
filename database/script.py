import itertools
import random
import bcrypt

def write():
    passwords = itertools.permutations("abc123")
    with open("database/sample_data.sql", "+a") as file:
        for i in range(10):
            pasword = bcrypt.hashpw("".join(next(passwords)).encode(), bcrypt.gensalt()).decode()
            file.write("\n")
            file.write(f"INSERT INTO users(rowid, username, password) VALUES(NULL, \"Person{i+1}\", \"{pasword}\");")
        for i in range(10):
            file.write("\n")
            file.write(f"INSERT INTO channels(rowid, user_id, channel_name) VALUES(NULL, {random.randint(1, 10)}, \"Channel{i + 1}\");")

        file.write("\n\nCOMMIT;")

write()