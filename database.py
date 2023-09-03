import sqlite3 as sql

class Sql:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.create_table()

    def execute_query(self, query, param=None, pandas = "no"):
        try:
            with sql.connect(self.db_name) as conn:
                if pandas == "no":
                    cur = conn.cursor()
                    if param:
                        cur.execute(query, param)
                    else:
                        cur.execute(query)
                    conn.commit()
                    return cur
                else:
                    df = pd.read_sql(query, conn)
                    return df
                        
        except sql.Error as e:
            return f"Error executing query: {e}"
            
    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            status TEXT,
            date TEXT
        )'''
        self.execute_query(query)

    def insert(self, task, status, date):
        query = '''INSERT INTO tasks (task, status, date) VALUES (?, ?, ?);'''
        self.execute_query(query, (task, status, date))

    def get_all_data(self):
        query = '''SELECT id, task, status, date FROM tasks'''
        result = self.execute_query(query)
        return result
    
    def search(self, column, search_term):
        query = '''SELECT id, task, status, date FROM tasks WHERE {} LIKE ?;'''.format(column)
        result = self.execute_query(query, ('%' + search_term + '%',))
        return result
    
    def delete(self, id):
        query = '''DELETE FROM tasks WHERE id = ?;'''
        self.execute_query(query, (id,))

    def update(self, id, status):
        query = '''UPDATE tasks SET status = ? WHERE id = ?;'''
        self.execute_query(query, (status, id))
    

