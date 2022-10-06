import sqlite3
import sys
import traceback

conn = sqlite3.connect('users_storage.db') #users_storage.db

db_cursor = conn.cursor()

# db_cursor.execute("""CREATE TABLE users(
#   id integer primary key autoincrement not null,
#   firstname text not null,
#   lastname text not null,
#   email text unique not null,
#   password text not null
#   )""")

# conn.execute("DROP TABLE users;")
db_cursor.execute("SELECT * FROM users")
resources = db_cursor.fetchall()
print(resources)
class Users:
  def insert_user (user):
    print(user)
    with conn:
      try:
        db_cursor.execute("INSERT INTO users VALUES (NULL, :firstname, :lastname, :email, :password)", {'firstname': user['first_name'], 'lastname': user['last_name'], 'email': user['email'], 'password': user['password']})
        return True
      except sqlite3.Error as err:
        return ' '.join(err.args)
    # conn.close()

  def get_user (email):
    db_cursor.execute("SELECT * FROM users WHERE email=:email", {'email': email})
    return db_cursor.fetchone()

  
# conn.close()

print('db connected')
