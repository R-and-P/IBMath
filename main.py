from flask import Flask, render_template, request, url_for, session, redirect
#from db_manager import search_query, search_text, get_all_posts, insert_question
from db_init import *
import hashlib
from cmd_guide import handle, cmd_help
from threading import Thread

#from db_init import trial
#trial()

hash = lambda s: str(hashlib.sha256(s.encode('utf-8')).hexdigest())[:20]

def safe_search(req, default):
  return default if not req.args.get('query') else search(req)

app = Flask(__name__)

@app.route('/test/All posts')
def test_index():
  posts = safe_search(request, select_all())
  return render_template('new_index.html', location = 'All posts', posts = posts)

@app.route('/All posts')
def index():
  if request.args.get('id'):
    id = request.args['id']
    user_content = request.args['user_content']
    user_update = request.args['user_update']
    title = request.args['title']
    update(id, 'user_content', user_content)
    update(id, 'user_update', user_update)
    update(id, 'title', title)
  posts = safe_search(request, select_all())
  return render_template('index.html', location = 'All posts', posts = posts)

@app.route('/edit')
def edit():
  id = request.args['id']
  user_content = get_field(id, 'user_content')[0]
  title = get_field(id, 'title')[0] 
  if session['ip'] == get_field(id, 'poster')[0]:
    return render_template('edit.html', id = id, user_content = user_content, user_update = now(), title = title, ip = get_field(id, 'poster'))
  return page_not_found('');

@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html', message = 'Page not found'), 404

@app.errorhandler(500)
def subpage_not_found(e):
  return render_template('error.html', message = 'Page not found'), 500

@app.route('/Mine')
def mine():
  print('from mine>>>')
  print(session['ip'])
  if request.args.get('question') and not request.args.get('type'):
    post_question(request.args['title'], request.args['question'], 'General', session['ip'], request.args.get('parent'))
  elif request.args.get('type') == 'question':
    post_question(request.args['title'], request.args['question'], 'General', session['ip'])
  elif request.args.get('type') == 'video':
    post_video(request.args['title'], request.args['url'], request.args['question'], 'General', session['ip'])
  elif request.args.get('type') == 'resource':
    post_resource(request.args['title'], request.args['url'],request.args['question'], 'General', session['ip'])
  #posts = get_all_posts()
  posts = safe_search(request, select_query('poster="' + session['ip'] + '"'))
  return render_template('mine.html', location = 'Mine', posts = posts)

@app.route('/Videos')
def videos():
  posts = safe_search(request, select_query("type='video'"))
  return render_template('index.html', location = 'Videos', posts = posts)

@app.route('/Questions')
def questions():
  posts = safe_search(request, select_query("type='question'"))
  return render_template('index.html', location = 'Questions', posts = posts)

@app.route('/Resources')
def resources():
  posts = safe_search(request, select_query("type='resource'"))
  return render_template('index.html', location = 'Resources', posts = posts)

@app.route('/setIP', methods = ['post'])
def setIp():
  session['ip'] = hash(request.form['ip'])
  print('>>>', session['ip'])
  return ''

def search(request):
  search_params = {
    '/All': '',
    '/Mine': 'poster=\'' + session['ip'] + '\'',
    '/Videos': 'type=\'video\''
  }
  if search_params.get(request.args['location']):
    search_params = search_params[request.args['location']]
  else:
    search_params = ''
  posts = select_has_substring(request.args['query'], search_params)
  return posts

@app.route('/page')
def page():
  if request.args.get('query'):
    return render_template('index.html', location = 'All', posts = search(request))
  item = select_query("id='" + request.args['id'] + "'")[0]
  if item[1] == 'video':
    return render_template('video_page.html', item = item, location = 'page', posts = get_responses(item[0]))
  elif item[1] == 'question':
    return render_template('question_page.html', item = item, location = 'page', posts = get_responses(item[0]))
  elif item[1] == 'text':
    return render_template('text_page.html', item = item, location = 'page', posts = get_responses(item[0]))
  elif item[1] == 'resource':
    return redirect(item[3])
    #render_template('resource_page.html', item = item, location = 'page')

@app.route('/ask')
def ask():
  if request.args.get('query'):
    return render_template('index.html', location = 'All', posts = search(request))
  return render_template('ask.html', location = 'ask', parent = request.args.get('ref'))

@app.route('/admin_post')
def admin_post():
  if request.args.get('query'):
    return render_template('index.html', location = 'All', posts = search(request))
  return render_template('admin_post.html', location = 'ask')

@app.route('/cmd')
def cmd_line():
  display = cmd_help
  if request.args.get('command'):
    display = handle(request.args['command'], session)
  return render_template('cmd.html', display = display)

''' TEST
'''
import os
@app.context_processor
def override_url_for():
  return dict(url_for = dated_url_for)
def dated_url_for(endpoint, **vals):
  if endpoint == 'static':
    filename = vals.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path, endpoint, filename)
      vals['q'] = int(os.stat(file_path).st_mtime)
  return url_for(endpoint, **vals)


app.secret_key = 'iuar9378xoh0283409283cdght429348nf230847c23n498237b923'

if __name__ == '__main__':
  #app.run(host='0.0.0.0', port=8080, debug = 1) #test
  Thread(target=app.run,args=("0.0.0.0",8080)).start() #permanent
