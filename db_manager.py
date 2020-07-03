'''
import sqlite3 as sq
import datetime as dt
# initialize db
c = sq.connect('posts.db')
c.execute('DROP TABLE posts')
c.execute('CREATE TABLE posts (type TEXT, title TEXT, video TEXT, poster TEXT, date TEXT, description TEXT)')
c.close()


def insert(typ, title, video, poster, description):
  with sq.connect('posts.db') as c:
    c.execute('INSERT INTO posts (type,title,video,poster,date,description) VALUES (?,?,?,?,?,?)', (typ,title,video,poster,dt.datetime.now().strftime('%b %d, %Y'),description))

def insert_question(question, poster):
  with sq.connect('posts.db') as cc:
    if question not in [x[1] for x in cc.execute('SELECT * FROM posts').fetchall()]:
      insert('question', question, '', poster, '')

def insert_video(title, video, poster, description):
  insert('video', title, video, poster, description)

def answer_question(question, answer):
  with sq.connect('posts.db') as cc:
    cc.execute('UPDATE posts SET description="' + answer + '" WHERE title="' + question + '"')

def delete_by_title(title):
  with sq.connect('posts.db') as c:
    c.execute('DELETE FROM posts WHERE title="' + title + '"')

def utterly_obliterate():
  with sq.connect('posts.db') as c:
    c.execute('DELETE FROM posts')

def search_text(s, additional = ''):
  s = s.lower()
  with sq.connect('posts.db') as c:
    results = [x for x in c.execute('SELECT * FROM posts ' + additional).fetchall() if any(s in x[i].lower() for i in range(6))][::-1]
    return results

def search_query(s):
  with sq.connect('posts.db') as c:
    return c.execute('SELECT * FROM posts WHERE ' + s).fetchall()[::-1]

def get_all_posts():
  with sq.connect('posts.db') as c:
    return c.execute('SELECT * FROM posts').fetchall()[::-1]

#search_query, search_text = 1, 1

#insert_video('Complex numbers part 2', 'https://www.youtube.com/embed/9DKDz8DonNU', 'Bob', 'This is a video or smth')

#answer_question('Test 1 man', 'I hope you asdkj asdksdjss dlaksdj lkasjdla skdjasl kdj kas jdl ierj wpe weorweirwoi we rpoi weproiu wjhz ckjbflk jaskj as j')
'''