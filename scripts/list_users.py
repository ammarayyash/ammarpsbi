import sqlite3, os
DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
print('Using DB:', DB)
conn = sqlite3.connect(DB)
c = conn.cursor()
for row in c.execute('SELECT id, username, email, first_name, last_name FROM auth_user ORDER BY id'):
    print(row)
conn.close()
