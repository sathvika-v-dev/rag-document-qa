import sqlite3
#connect database 
conn=sqlite3.connect("chat_history.db")
cursor=conn.cursor()
#creating table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,           
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAP
               )
               """)
conn.commit()
conn.close()
print("Database and table created successfully")