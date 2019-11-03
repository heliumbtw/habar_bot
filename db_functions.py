import sqlite3
import datetime


def datetime_now():
    now = datetime.datetime.now()
    return str(now.day) + '.' + str(now.month) + '.' + str(now.year)


# create db
# conn = sqlite3.connect('tts.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE tts
#              (date text, qty real)''')
# conn.commit()

class tts_db:
    def __init__(self):
        self.conn = self.create_conn()
        self.cursor = self.conn.cursor()

    def create_conn(self):
        try:
            self.conn = sqlite3.connect('tts.db')
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(e)
        return self.conn

    def check_tts(self, qty):
        self.cursor.execute('SELECT * FROM tts WHERE date=?', (datetime_now(),))
        result = self.cursor.fetchone()
        if result is not None:
            if result['qty'] + qty < 155000:
                self.cursor.execute("""Update tts set qty = ? where date = ?""",
                                    (result['qty'] + qty, result['date']))
                self.conn.commit()
                return True
            else:
                return 155000 - result['qty']
        else:
            self.cursor.execute("insert into tts values (?, ?)", (datetime_now(), 0))
            self.conn.commit()
            return self.check_tts(qty)
