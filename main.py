from flask import Flask, render_template, request, url_for, session, redirect
#from db_manager import search_query, search_text, get_all_posts, insert_question
from db_init import *
import hashlib
import lorem
from cmd_guide import handle
from threading import Thread
'''
import sys
from db_init import db_main
db_main()
sys.exit()
'''
hash = lambda s: str(hashlib.sha256(s.encode('utf-8')).hexdigest())[:20]

def safe_search(req, default):
  return default if not req.args.get('query') else search(req)

app = Flask(__name__)

@app.route('/All posts')
def index():
  posts = safe_search(request, select_all())
  return render_template('index.html', location = 'All posts', posts = posts)

@app.route('/Mine')
def mine():
  if request.args.get('question'):
    post_question(request.args['title'], request.args['question'], 'General', session['ip'])
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
    return render_template('video_page.html', item = item, location = 'page')
  elif item[1] == 'question':
    return render_template('question_page.html', item = item, location = 'page')
  elif item[1] == 'resource':
    return redirect(item[3])
    #render_template('resource_page.html', item = item, location = 'page')

@app.route('/ask')
def ask():
  if request.args.get('query'):
    return render_template('index.html', location = 'All', posts = search(request))
  return render_template('ask.html', location = 'ask')

@app.route('/cmd')
def cmd_line():
  display = '<op>vid`[URL]`[TITLE]`[DESC]</op> to insert embed of [URL] with [TITLE] and [DESC]<br><op>ans`[Q]`[A]</op> to answer [Q] with [A]<br><op>del`[TITLE]</op> to delete item with [TITLE]<br><op>ask`[Q]</op> to ask [Q]<br><op>completely empty database</op> to completely empty database<br><sp>CTRL-ENT</sp> to submit'
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


app.secret_key = 'iuar9378xoh0283409283cn498237b923'

if __name__ == '__main__':
  #app.run(host='0.0.0.0', port=8080, debug = 1) #test
  Thread(target=app.run,args=("0.0.0.0",8080)).start() #permanent
