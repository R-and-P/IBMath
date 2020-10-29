import sqlite3 as sq
import datetime as dt

now = lambda: dt.datetime.now().strftime('%d %B, %Y')

def init():
  with sq.connect('Posts.db') as c:
    c.execute('CREATE TABLE posts (id INTEGER PRIMARY KEY, type text, title text, url text, user_content text, user_update text, admin_content text, admin_update text, location text, parent_post_id text, poster text)')

def insert(typ, title, url, user_content, user_update, admin_content, admin_update, location, parent_post_id, poster):
  with sq.connect('Posts.db') as c:
    c.execute('INSERT INTO posts (type, title, url, user_content, user_update, admin_content, admin_update, location, parent_post_id, poster) VALUES (?,?,?,?,?,?,?,?,?,?)', (typ, title, url, user_content, user_update, admin_content, admin_update, location, parent_post_id, poster))

def select_all():
  with sq.connect('Posts.db') as c:
    return c.execute('SELECT * FROM posts').fetchall()[::-1]

def get_responses(id):
  with sq.connect('Posts.db') as c:
    return c.execute('SELECT * FROM Posts WHERE parent_post_id=' + str(id)).fetchall()[::-1]

def get_field(id, field):
  with sq.connect('Posts.db') as c:
    return c.execute('SELECT ' + field + ' FROM posts WHERE id=' + id).fetchall()[0]

def select_query(q):
  with sq.connect('Posts.db') as c:
    if q == '':
      return select_all()
    return c.execute('SELECT * FROM posts WHERE ' + q).fetchall()[::-1]

def update(id, field, value, is_admin = False):
  with sq.connect('Posts.db') as c:
    command = 'UPDATE Posts SET ' + field + '=\'' + value + '\' WHERE id=' + id
    print(command)
    c.execute(command)
    if is_admin:
      c.execute('UPDATE Posts SET admin_update=\'' + now() + '\' WHERE id=' + id)
    else:
      c.execute('UPDATE Posts SET user_update=\'' + now() + '\' WHERE id=' + id)

def delete(id):
  with sq.connect('Posts.db') as c:
    c.execute('DELETE FROM Posts WHERE id=' + id)

def post_question(title, question, location, poster, parent = ''):
  insert('question', title, '', question, now(), '', '', location, parent, poster)

def answer_question(id, answer):
  update(id, 'admin_content', answer, True)

def respond_to_post(id, content, poster):
  insert('response', '', '', content, now(), search_query("id='" + id + "'")[0][-2], id, poster)

def edit_question(id, question):
  update(id, 'user_content', question, False)

# now() in post_video and post_resource go to user_update because no distinction between user and admin is needed as only admin may post videos and resources

def trade_keys(id1, id2):
  id1, id2 = str(id1), str(id2)
  id2_id = str(id2) #str(get_field(id2, 'id')[0])
  id1_id = str(id1) #str(get_field(id1, 'id')[0])
  update(id2, 'id', '-1')
  with sq.connect('Posts.db') as c:
    c.execute('UPDATE Posts SET parent_post_id=-1 WHERE parent_post_id=' + id2)
  update(id1, 'id', '-2')
  with sq.connect('Posts.db') as c:
    c.execute('UPDATE Posts SET parent_post_id=-2 WHERE parent_post_id=' + id1)
  update('-2', 'id', id2_id)
  with sq.connect('Posts.db') as c:
    c.execute('UPDATE Posts SET parent_post_id=' + id2_id + ' WHERE parent_post_id=-2')
  update('-1', 'id', id1_id)
  with sq.connect('Posts.db') as c:
    c.execute('UPDATE Posts SET parent_post_id=' + id1_id + ' WHERE parent_post_id=-1')

def reorder(old_id, new_id):
  #slides post with id old_id to id new_id
  old_id, new_id = int(old_id), int(new_id)
  if old_id > new_id:
    for i in range(old_id, new_id, -1):
      print(i)
      trade_keys(i, i - 1)
  elif new_id > old_id:
    for i in range(old_id, new_id):
      print(i)
      trade_keys(i, i + 1)

def post_video(title, url, description, location, poster):
  insert('video', title, url, description, now(), '', '', location, '', poster)

def post_resource(title, url, description, location, poster):
  insert('resource', title, url, description, now(), '', '', location, '', poster)

def post(type, title, url, desc, location, poster):
  if type == 'video':
    post_video(title, url, desc, location, poster)
  elif type == 'resource':
    post_resource(title, url, desc, location, poster)
  elif type == 'question':
    post_question(title, desc, location, poster)
  elif type == 'text':
    insert('text', title, '', desc, now(), '', '', 'misc', '', poster)

def trial():
  with sq.connect('Posts.db') as c:
    try:
      c.execute('DROP TABLE posts')
    except:
      pass
  init()

def select_has_substring(s, params):
  return [x for x in select_query(params) if any(s.lower() in str(y).lower() for y in x[1:])]

#trial()