from tombhub.database import init_db
import sqlite3

con = sqlite3.connect("tempdb.sqlite")
c = con.cursor()
def drop_table(table):
    c.execute("drop table if exists %s;" % (table))
    con.commit()
    con.close()

if __name__ == '__main__':
    drop_table('threads')
    init_db()
