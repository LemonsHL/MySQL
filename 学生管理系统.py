from pymysql import *

##################################################
# 用来储存使用经常的数据库防止多次输入 用户名 密码 数据库名
store = 'root', 'asdfgh', 'test'

if len(store) == 0:
    users = input("请输入用户名：")
    passwords = input("请输入密码：")
    databases = input("请输入要使用的数据库名：")
else:
    users, passwords, databases = store


##################################################


# MySql 操作类
class Fun(object):
    def __init__(self):
        try:
            self.conn = connect(host='localhost', port=3306, user=users, password=passwords,
                                database=databases, charset='utf8')
            self.cursor = self.conn.cursor()
            print("成功连接上数据库 %s" % databases)

        except Exception as result:
            print(result)
            print("数据库没有连接上，请查看自己是否有输入错误密码或是否存在该用户！！！")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        for content in self.cursor.fetchall():
            print(content)

    def show_all(self):
        """
        用来查询所有记录
        """
        sql = "select * from student"
        self.execute_sql(sql)
        print("%d rows in set" % self.cursor.rowcount)

    def show_part(self):
        """
        用来查询部分记录
        """
        try:
            sql = """select * from student where sno = '%s'""" % (input("请输入要查询的学生学号："))
            self.execute_sql(sql)
        except Exception as result:
            print(Exception)

    def insert_student(self):
        """
        用来插入（添加）数据
        """
        print("请输入要插入的")
        id = input("学号：")
        name = input("姓名：")
        sex = input("性别：")
        cid = input("班级号：")
        mid = input("学院号：")
        did = input("宿舍号：")
        nation = input("民族：")
        age = input("年龄：")
        birthday = input("生日（格式如：2001-09-02）：")
        location = input("地址：")
        enrol = input("入学日期（格式如：2001-09-02）：")
        sql = """insert into student values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s')""" % (
            id, name, sex, cid, mid, did, nation,
            int(age), birthday, location, enrol)
        self.cursor.execute(sql)
        print("添加信息成功！")
        self.conn.commit()

    def update_student(self):
        """
        修改学生信息
        """
        id = input("请输入要修改学生的学号：")

        # todo(没有完成 不需要修改某项操作)
        print("修改他（她）的")
        name = input("姓名：")
        sex = input("性别：")
        cid = input("班级号：")
        mid = input("学院号：")
        did = input("宿舍号：")
        nation = input("民族：")
        age = input("年龄：")
        birthday = input("生日（格式如：2001-09-02）：")
        location = input("地址：")
        enrol = input("入学日期（格式如：2001-09-02）：")
        sql = """update student set name = '%s', sex = '%s',
                 cid = '%s', mid = '%s', did = '%s',
                 nation = '%s', age = %d, birthday = '%s',
                 location = '%s', enrol = '%s' where id = '%s'""" % (
            name, sex, cid, mid, did, nation, int(age), birthday, location, enrol, id)

        self.cursor.execute(sql)
        print("修改信息成功！")
        self.conn.commit()

    def delete_student(self):
        """
        删除学生信息
        """
        id = input("请输入要删除学生的学号：")
        sql = """delete from student where id = '%s'""" % id
        self.cursor.execute(sql)
        print("删除学生信息成功！！！")
        self.conn.commit()

    @staticmethod
    def show_menu():
        """
        该函数是为了展示功能界面
        """
        # 1.显示系统的功能菜单
        print('---------学生管理系统1.0---------')
        print('+-----------------------------+')
        print('|  1) 添加学生信息              |')
        print('|  2) 修改学生信息              |')
        print('|  3) 删除学生信息              |')
        print('|  4) 显示所有学生              |')
        print('|  5) 查询学生信息              |')
        print('|  6) 退出管理系统              |')
        print('+-----------------------------+')
        return input("请输入要操作前面的序号：")

    def run(self):
        try:
            while True:
                num = self.show_menu()

                if num == '1':
                    self.insert_student()
                elif num == '2':
                    self.update_student()
                elif num == '3':
                    self.delete_student()
                elif num == '4':
                    self.show_all()
                elif num == '5':
                    self.show_part()
                elif num == '6':
                    print("正在退出管理系统，欢迎下次使用！")
                    exit()
                else:
                    print("输入错误，请重新输入！！！")

        except Exception as error:
            print(error)


def main():
    stu = Fun()

    stu.run()


if __name__ == '__main__':
    main()
