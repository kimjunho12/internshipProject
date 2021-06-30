import pymysql
# %%
class MysqlController:
    def __init__(self, host, id, pw, db_name):
        try:
            self.conn = pymysql.connect(user=id, passwd=pw, host=host, db=db_name, charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as err:
            print(err)
        
    def close(self):
        self.conn.close()