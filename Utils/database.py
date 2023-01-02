import sqlite3

# generate a generic python class that to CRUD operation on a sqlite3 db?
from contextlib import closing
import sqlite3


class SqlExec:

    def __init__(self, db_name, sql, parameters=()):
        self.sql = sql
        self.parameters = parameters
        with closing(sqlite3.connect(db_name)) as self.con,  \
                closing(con.cursor()) as self.cur:
            self.pre_process()
            self.cur.execute(self.sql, parameters=self.parameters)
            self.retval = self.post_process()

    def pre_process(self):
        return

    def post_process_fetchall(self):
        self.retval = self.cur.fetchall

    post_process = post_process_fetchall


class SqlExecLastRowId(SqlExec):

    def post_process(self):
        self.retval = cur.lastrowid


last_row = SqlExecLastRowId("mydb.db", "DELETE FROM FOO WHERE BAR='{}'",
                            paramters=("baz",)).retval
