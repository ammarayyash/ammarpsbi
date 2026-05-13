import sqlite3
import datetime
import os

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
print('Using DB:', DB)
conn = sqlite3.connect(DB)
c = conn.cursor()
# Create table for UniqueStreak if not exists (simple schema)
c.execute('''CREATE TABLE IF NOT EXISTS dashboard_uniquestreak (
 id integer primary key autoincrement,
 user_id integer not null,
 streak_value integer not null,
 note varchar(200),
 achieved_at datetime
);''')
# create unique index
c.execute('CREATE UNIQUE INDEX IF NOT EXISTS uq_user_streak ON dashboard_uniquestreak(user_id, streak_value);')
# find user id
# Try to find a user named 'ammar' by username, email, or first_name
c.execute("SELECT id, username, email, first_name FROM auth_user WHERE username LIKE '%ammar%' OR email LIKE '%ammar%' OR first_name LIKE '%ammar%' LIMIT 1")
row = c.fetchone()
if not row:
    print('User with name/email containing "ammar" not found in auth_user table.')
    conn.close()
    raise SystemExit(1)
uid = row[0]
print('Found user: id=%s username=%s email=%s first_name=%s' % row)
# Update userprofile streak_days and last_streak_date
today = datetime.date.today().isoformat()
c.execute("UPDATE dashboard_userprofile SET streak_days=?, last_streak_date=? WHERE user_id=?", (25, today, uid))
print('Updated dashboard_userprofile rows affected:', conn.total_changes)
# Insert unique streak record for 25 if not exists
now = datetime.datetime.now().isoformat()
try:
    c.execute("INSERT OR IGNORE INTO dashboard_uniquestreak (user_id, streak_value, note, achieved_at) VALUES (?,?,?,?)", (uid, 25, 'Reached 25-day streak', now))
    print('Inserted unique streak (if not existed).')
except Exception as e:
    print('Error inserting unique streak:', e)

conn.commit()
conn.close()
print('Done')
