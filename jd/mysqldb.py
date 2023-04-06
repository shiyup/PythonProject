import pymysql
import threading


class DataManager():
    # 单例模式，确保每次实例化都调用一个对象。
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataManager, "_instance"):
            with DataManager._instance_lock:
                DataManager._instance = object.__new__(cls)
                return DataManager._instance

        return DataManager._instance

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('127.0.0.1', 'root', 'root', 'test', charset='utf8')

        # 建立游标
        self.cursor = self.conn.cursor()

    def save_data(self, data):
        # 数据库操作----写入
        sql = 'insert into jddurg(shop,durg_name,efficacy,price,comments) values(%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql, data)
            print('保存成功！恭喜！')
            self.conn.commit()
        except Exception as e:
            print('插入数据失败！', e)
            self.conn.rollback()  # 回滚

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接


'''
数据库建表格
CREATE TABLE `jddurg` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`shop` varchar(20) DEFAULT NULL,
  `durg_name` varchar(100) DEFAULT NULL,
  `efficacy` varchar(150) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `comments` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
'''