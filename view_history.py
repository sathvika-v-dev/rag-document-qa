import sqlite3
conn=sqlite3.connect("chat_history.db")
cursor=conn.cursor()
cursor.execute("SELECT *FROM chat_history")
rows=cursor.fetchall()
for row in rows:
    print(f"ID:{row[0]}")
    print(f"Question:{row[1]}")
    print(f"Answer:{row[2]}")
    print(f"Time:{row[3]}")
    print("---")
conn.close()    