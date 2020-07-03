#from db_manager import answer_question, insert_video, delete_by_title, insert_question, utterly_obliterate
# the above references an outdated db, please update handle() to fit Posts instead of posts
cmd_help = '<op>fields</op> view post fields<br><op>edit`[ID]`[FIELD]`[VAL]</op> to edit post with id [ID] by setting [FIELD] to [VAL]<br><op>del`[IDs]</op> to delete items with [IDs] separated by spaces<br><op>get`[ID]`[FIELD]</op> to view value in [FIELDs comma separated] of post item with [ID]<br><op>post`[TYPE]`[TITLE]`[URL]`[DESC]`[LOCATION]</op> to post [TYPE] with [DESC] and optional [URL for TYPE video or resource] from admin account<br><sp>CTRL-ENT</sp> to submit<br>Separate commands with <op>\\n</op>'

from db_init import update, delete, get_field, post

def handle(s, sess):
  commands = s.split('\n')
  out = ''
  for command in commands:
    parts = command.split('`')
    if parts[0] == 'edit':
      id, field, val = parts[1:]
      update(id, field, val, True)
      out += 'updated ' + field + ' of ' + id + ' with ' + val
    elif parts[0] == 'del':
      ids = parts[1].split(' ')
      for id in ids:
        delete(id)
      out += 'Deleted ' + ', '.join(ids)
    elif parts[0] == 'post':
      type, title, url, desc, location = parts[1:]
      post(type, title, url, desc, location, sess['ip'])
      return 'posted ' + type + ' ' + title
    elif parts[0] == 'get':
      id, field = parts[1:]
      out += field + ' of post ' + id + ': ' + str(get_field(id, field)).replace('\'', '')
    elif parts[0] == 'fields':
      out += 'type, title, url, user_content, user_update, admin_content, admin_update, location, parent_post_id, poster'
    out += '<br>'
  return out

