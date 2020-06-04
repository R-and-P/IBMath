from db_manager import answer_question, insert_video, delete_by_title, insert_question, utterly_obliterate
def handle(s, sess):
  parts = s.split('`')
  if parts[0] == 'vid':
    url = parts[1]
    title = parts[2]
    desc = parts[3]
    insert_video(title, url, sess['ip'], desc)
    return 'Inserted video'
  elif parts[0] == 'ans':
    q = parts[1]
    a = parts[2]
    answer_question(q, a)
    return 'Answered question'
  elif parts[0] == 'del':
    title = parts[1]
    delete_by_title(title)
    return 'Deleted item with title'
  elif parts[0] == 'ask':
    q = parts[1]
    insert_question(q, sess['ip'])
    return 'Inserted question'
  elif parts[0] == 'completely empty database':
    utterly_obliterate()
    return 'Emptied database'