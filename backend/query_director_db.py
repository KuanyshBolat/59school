import sqlite3, json, os
db = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(db)
cur = conn.cursor()
try:
    cur.execute("SELECT id, name, bio, name_color, bio_color FROM content_director")
    rows = cur.fetchall()
    out = []
    for r in rows:
        out.append({'id': r[0], 'name': r[1], 'bio': r[2], 'name_color': r[3], 'bio_color': r[4]})
    print(json.dumps(out, ensure_ascii=False, indent=2))
except Exception as e:
    print('ERROR', e)
finally:
    conn.close()

