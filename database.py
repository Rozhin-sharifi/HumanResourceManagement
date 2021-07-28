from sqlite3 import connect


class Database():

    @staticmethod
    def select():
        con = connect("HR.db")
        my_cursor = con.cursor()
        my_cursor.execute("SELECT * FROM workers")
        result = my_cursor.fetchall()
        # self.ui.tb1.setText(str(result))
        con.close()
        return result

    @staticmethod
    def insert(na_code,first_name,last_name):
        con = connect("HR.db")
        my_cursor = con.cursor()
        my_cursor.execute(f'INSERT INTO workers(first_name,last_name,na_code) VALUES ("{first_name}","{last_name}","{na_code}")')
        con.commit()
        return True

    @staticmethod
    def update(na_code,first_name,last_name,search_code):
        con = connect("HR.db")
        my_cursor = con.cursor()
        my_cursor.execute(
            f'UPDATE workers SET na_code = "{na_code}" , first_name ="{first_name}" , last_name = "{last_name}" WHERE na_code = "{search_code}" ')
        my_cursor.execute('SELECT * FROM workers')
        con.commit()
        fetch = my_cursor.fetchall()
        return fetch
