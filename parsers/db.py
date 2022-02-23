import pymysql


class DB(object):
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(host='trans_mysql',
                                  port=3306,
                                  user='root',
                                  password='NB2Ffj!lPTe&yOm5',
                                  database='translate_db')

    def update_record_progress(self, row_id, percent):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 更新语句
        sql = "UPDATE tbl_record SET Progress={0} WHERE Id = {1}".format(percent, row_id)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.db.rollback()

    def close(self):
        self.db.close()
