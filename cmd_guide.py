#from db_manager import answer_question, insert_video, delete_by_title, insert_question, utterly_obliterate
# the above references an outdated db, please update handle() to fit Posts instead of posts
cmd_help = '<op>fields</op> view post fields<br><op>reorder`[ID1]`[ID2]</op> slides post [ID1] to [ID2], changing parent_post_id\'s as necessary<br><op>child`[ID1]`[ID2]`</op> sets the parent_post_id of [ID1] to [ID2]<br><op>cat`[ID]`[LOCATION]</op> categorizes post [ID] into [LOCATION]<br><op>switch`[ID1]`[ID2]</op> switch id\'s of posts with id\'s [ID1] and [ID2]<br><op>edit`[ID]`[FIELD]`[VAL]</op> to edit post with id [ID] by setting [FIELD] to [VAL]<br><op>del`[IDs]</op> to delete items with [IDs] separated by spaces<br><op>get`[ID]`[FIELD]</op> to view value in [FIELDs comma separated] of post item with [ID]<br><op>post`[TYPE]`[TITLE]`[URL]`[DESC]`[LOCATION]</op> to post [TYPE] with [DESC] and optional [URL for TYPE video or resource] from admin account<br><sp>CTRL-ENT</sp> to submit<br>Separate commands with <op>;</op>'

#from db_init import update, delete, get_field, post
from db_init import *

def handle(s, sess):
  commands = s.replace('\n', '<br/>').split(';')
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
      out += 'type [question, text, video, resource], title, url, user_content, user_update, admin_content, admin_update, location, parent_post_id, poster'
    elif parts[0] == 'switch':
      id1, id2 = parts[1:]
      trade_keys(str(id1), str(id2))
      out += 'traded keys ' + id1 + ' and ' + id2
    elif parts[0] == 'reorder':
      old_id, new_id = parts[1:]
      out += str(reorder(old_id, new_id))
    elif parts[0] == 'child':
      child, parent = parts[1:]
      update(child, 'parent_post_id', parent)
    elif parts[0] == 'cat':
      id, loc = parts[1:]
      update(id, 'location', loc)
    out += '<br>'
  return out

