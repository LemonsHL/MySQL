from pymysql import *
import os

##################################################
# 用来储存使用经常的数据库防止多次输入 用户名 密码 数据库名
store = 'root', 'asdfgh', 'mysql'
if len(store) == 0:
    users = input("请输入用户名：")
    passwords = input("请输入密码：")
    databases = input("请输入要使用的数据库名：")
else:
    users, passwords, databases = store


##################################################


# sql操作类
class SqlFun(object):
    def __init__(self):
        self.current_db = ''
        self.current_tb = ''
        # 初始化（选择账户）
        try:
            self.conn = connect(host='localhost', port=3306, user=users, password=passwords,
                                database=databases, charset='utf8')

        except Exception as result:
            print(result)
            print("数据库没有连接上，请查看自己是否有输入错误密码或是否存在该用户！！！")

        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def show_database(self):
        """
        展示所有的数据库，并选择使用
        :return: NULL
        """
        # 排除自带的数据库
        exclude_list = ["sys", "information_schema", "mysql", "performance_schema"]
        sql = "show databases"  # 显示所有数据库
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        # print(res)
        if not res:  # 判断结果非空
            print("数据库不存在！！！")

        db_list = []  # 数据库列表
        for i in res:
            db_name = i[0]
            # 判断不在排除列表时
            if db_name not in exclude_list:
                db_list.append(db_name)

        if not db_list:
            print("不存在除系统默认以外的数据库！！！")

        print("所有数据库如下(默认除外)：")
        count = 0
        for i in db_list:
            count += 1
            print("{}.{}".format(count, i), end='        ')

        op = int(input("\n选择你要操作的数据库(序号)："))
        self.current_db = db_list[op - 1]
        sql = 'use ' + self.current_db
        self.cursor.execute(sql)

        print("当前使用的数据库为：{}".format(self.current_db))

    def show_dbtable(self):
        """
        展示该数据库下所有的表格
        :return: NULL
        """
        sql = 'show tables'
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        # print(tables)
        tb_list = []  # 定义一个空的列表存放表格名

        # 没有表的情况下
        if not tables:
            print("该数据库下没有表！！！")

        # 遍历所有表名，并追加到tb_list中(方便输出到控制台)
        for i in tables:
            tb_list.append(i)

        print(self.current_db + "下的表格有：")
        count = 0
        for i in tb_list:
            count += 1
            print("{}.{}".format(count, i[0]), end='        ')

        op = int(input("\n选择接下来你要操作的表(序号)："))
        self.current_tb = tb_list[op - 1][0]

    def show_menu(self):
        """
        该函数是为了展示功能界面
        :return: int
        """
        # 1.显示系统的功能菜单 todo(可以用format优化格式，但是具体记不清咋用了）
        print("当前操作的是'{}'下的'{}'表".format(self.current_db, self.current_tb))
        print('---------学生管理系统2.0---------')
        print('+-----------------------------+')
        print('|         1) 添加              |')
        print('|         2) 修改              |')
        print('|         3) 删除              |')
        print('|         4) 显示              |')
        print('|         5) 自定义查询         |')
        print('|         6) 退出系统           |')
        print('+-----------------------------+')
        return input("请输入要操作前面的序号：")

    def add_data(self):
        self.cursor.execute("SELECT * FROM " + self.current_tb)
        self.cursor.fetchall()
        desc = self.cursor.description

        # print(rows)
        # print(desc)
        # print(self.cursor.description)
        desc_date = []
        for i in desc:
            print(i[0], end='    ')
            desc_date.append(i[0])

        add_date = []
        print("\n依次输入上述字段的值：")
        for i in range(len(desc)):
            temp = input()
            add_date.append(temp)

        # print("insert into " + self.current_tb + "(" + ",".join(desc_date) + ") values(" + ",".join(add_date) + ")")
        sql = "insert into " + self.current_tb + "(" + ",".join(desc_date) + ")" + "values(" + ",".join(add_date) + ")"
        self.cursor.execute(sql)
        self.conn.commit()
        print("受影响的行数：{}\n".format(self.cursor.rowcount))
        if self.cursor.rowcount == 0:
            print("插入失败！！！")
        else:
            print("插入成功！！！")

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        for content in self.cursor.fetchall():
            print(content)

    def show_all(self):
        """
        原来查询所有记录
        :return:
        """
        sql = "select * from " + self.current_tb
        print(sql)
        self.execute_sql(sql)
        print("%d rows in set" % self.cursor.rowcount)

    def show_part(self):
        """
        自定义查询
        :return:
        """
        try:
            sql = """select * from student where sno = '%s'""" % (input("请输入要查询的学生学号："))
            self.execute_sql(sql)
        except Exception as result:
            print(Exception)

    def run(self):
        self.show_database()
        self.show_dbtable()
        self.show_menu()
        # self.add_data()
        # self.show_all()
        self.show_part()


def main():
    s = SqlFun()
    s.run()


if __name__ == '__main__':
    main()
