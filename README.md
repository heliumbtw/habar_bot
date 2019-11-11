# habar_bot
Хабар бот (VK)

1) move settings.py to habar directory

2) create db

conn = sqlite3.connect('tts.db')

c = conn.cursor()

c.execute('''CREATE TABLE tts (date text, qty real)''')
              
conn.commit()
