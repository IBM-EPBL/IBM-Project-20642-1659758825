import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,comments TEXT)')
def add_userdata(username,comments):
c.execute('INSERT INTO usertable(username,comments) VALUES
(?,?)',(username,comments))
conn.commit()
def login_user(username,comments):
c.execute('SELECT * FROM usertable WHERE username =? AND comments =
?',(username,comments))
data = c.fetchall()
return data
def select_all():
c.execute('SELECT * FROM usertable')
data1 = c.fetchall()
return data1
def create_likestable():
c.execute('CREATE TABLE IF NOT EXISTS likestable(counts TEXT)')
def add_likesdata(counts):
c.execute('INSERT INTO likestable(counts) VALUES (?)',(counts))
conn.commit()
def count_likes():
c.execute('SELECT count(*) FROM likestable')
data1 = c.fetchall()
return data1
