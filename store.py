import sqlite3
import datetime

def process_data(*arg):
    connect = sqlite3.connect('main.db')
    cur = connect.cursor()
    
    try:
        cur.execute('''CREATE TABLE members
               (date, chat_id, username, first_name)''')
    except:
        pass
    # Insert a row of data
    chat_id = arg[0]
    uname = arg[1]
    fname = arg[2]
    row =  cur.execute(f"SELECT * FROM members WHERE first_name = '{fname}' AND chat_id = '{chat_id}'")
    row = cur.fetchall()
    if len(row)!=0:
        print("The user already exist ;)")
    else:
        cur.execute(f"INSERT INTO members VALUES ('{datetime.datetime.today()}', '{chat_id}','{uname}','{fname}')")
            
    connect.commit()
    connect.close()

def read_data():
    connect = sqlite3.connect('main.db')
    cur = connect.cursor()
    header = '''date || chat_id || username || first_name\n'''
    data = [header]
    counter = 0
    for row in cur.execute('SELECT * FROM members ORDER BY first_name'):
        txt = f'''{row[0][:19]} || <code>{row[1]}</code> || {row[2]} || {row[3]}\n'''
        if len(data[counter])>=3500:
            data.append(txt)
            counter+=1
        else:
            data[counter] += txt
    connect.close()
    return data