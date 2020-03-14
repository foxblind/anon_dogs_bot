import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()

    conn.commit()
    pass