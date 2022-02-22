import pymysql

# 打开数据库连接
db = pymysql.connect(host='trans_mysql',
                     port=3310,
                     user='root',
                     password='NB2Ffj!lPTe&yOm5',
                     database='translate_db')


def update_record_progress(row_id, percent):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 更新语句
    sql = "UPDATE tbl_record SET Progress={0} WHERE Id = {1}".format(percent, row_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
