import sqlite3, json, os
p = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(p)
cur = conn.cursor()
out=[]
try:
    cur.execute("SELECT id, name, bio, name_color, bio_color FROM content_director")
    rows = cur.fetchall()
    for r in rows:
        out.append({'id': r[0], 'name': r[1], 'bio': r[2], 'name_color': r[3], 'bio_color': r[4]})
    with open('director_values.json','w',encoding='utf-8') as f:
        json.dump(out,f,ensure_ascii=False,indent=2)
    print('WROTE director_values.json')
except Exception as e:
    with open('director_values_error.txt','w',encoding='utf-8') as f:
        f.write(str(e))
    print('ERROR written')
finally:
    conn.close()

