import mysql.connector
from mysql.connector import Error

class Person:
    def __init__(self, ID=0, name='', gender=0, birth_day=0, work_day=0, phone_number=0,
                 education_background='', address='', job=''):
        self.ID = ID
        self.name = name
        self.gender = gender
        self.birth_day = birth_day
        self.work_day = work_day
        self.phone_number = phone_number
        self.education_background = education_background
        self.address = address
        self.job = job

def print_people(people):
    print("\033[0;36mID    Name   Gender  Birth Day\tWork Day  Phone Number\tEducation Background\tAddress\tJob\033[0m")
    for p in people:
        print(
            f"{p.ID:<5}{p.name:<8}{p.gender:<8}{p.birth_day:<11}{p.work_day:<10}{p.phone_number:<16}{p.education_background:<20}{p.address:<10}{p.job}")

def create_people(n, connection):
    people = []
    for i in range(n):
        print(f"\033[0;33m第{i + 1}个人的数据:\033[0m")
        ID = int(input("-ID: "))
        name = input("-姓名: ")
        gender = int(input("-性别: "))
        birth_day = int(input("-生日: "))
        work_day = int(input("-工作日: "))
        phone_number = int(input("-电话号码: "))
        education_background = input("-教育经历: ")
        address = input("-地址: ")
        job = input("-职业: ")

        person = Person(ID, name, gender, birth_day, work_day, phone_number, education_background, address, job)
        people.append(person)
        insert_person(connection, person)
    return people

def delete_person(people, n, d, connection):
    index_to_delete = next((i for i, p in enumerate(people) if p.ID == d), None)
    if index_to_delete is not None:
        del people[index_to_delete]
        delete_person_from_db(connection, d)
        return True
    return False

def delete_person_from_db(connection, id):
    delete_query = "DELETE FROM persons WHERE ID = %s"
    cursor = connection.cursor()
    cursor.execute(delete_query, (id,))
    connection.commit()

def update_person(people, id, connection):
    for p in people:
        if p.ID == id:
            while True:
                print("1.ID 2.名字 3.性别 4.生日 5.工作日 6.电话号码 7.教育经历 8.地址 9.职业 0.修改完成")
                key = int(input("*修改哪些数据: "))
                if key == 1:
                    new_id = int(input("-输入新ID: "))
                    p.ID = new_id
                    update_person_in_db(connection, p, 'ID', new_id)
                elif key == 2:
                    p.name = input("-输入新名字: ")
                    update_person_in_db(connection, p, 'name', p.name)
                elif key == 3:
                    p.gender = int(input("-输入新性别: "))
                    update_person_in_db(connection, p, 'gender', p.gender)
                elif key == 4:
                    p.birth_day = int(input("-输入新生日: "))
                    update_person_in_db(connection, p, 'birth_day', p.birth_day)
                elif key == 5:
                    p.work_day = int(input("-输入新工作日: "))
                    update_person_in_db(connection, p, 'work_day', p.work_day)
                elif key == 6:
                    p.phone_number = int(input("-输入新电话号码: "))
                    update_person_in_db(connection, p, 'phone_number', p.phone_number)
                elif key == 7:
                    p.education_background = input("-输入新教育经历: ")
                    update_person_in_db(connection, p, 'education_background', p.education_background)
                elif key == 8:
                    p.address = input("-输入新地址: ")
                    update_person_in_db(connection, p, 'address', p.address)
                elif key == 9:
                    p.job = input("-输入新职业: ")
                    update_person_in_db(connection, p, 'job', p.job)
                elif key == 0:
                    return
                else:
                    print("-重新输入")

def update_person_in_db(connection, person, field, value):
    update_query = f"UPDATE persons SET {field} = %s WHERE ID = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (value, person.ID))
    connection.commit()

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("成功连接mysql")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("成功查询")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS persons (
        ID INT ,
        name VARCHAR(255),
        gender INT,
        birth_day INT,
        work_day INT,
        phone_number INT,
        education_background VARCHAR(255),
        address VARCHAR(255),
        job VARCHAR(255)
    );
    """
    execute_query(connection, create_table_query)

def insert_person(connection, person):
    insert_query = """
    INSERT INTO persons (ID, name, gender, birth_day, work_day, phone_number, education_background, address, job)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    cursor.execute(insert_query, (
        person.ID, person.name, person.gender, person.birth_day, person.work_day, person.phone_number,
        person.education_background, person.address, person.job))
    connection.commit()

def select_all_persons(connection):
    select_query = "SELECT * FROM persons"
    return execute_read_query(connection, select_query)

def main():
    database_host = "localhost"
    database_user = "root"
    database_password = "q3231423581"
    database_name = "runoob"

    connection = create_connection(database_host, database_user, database_password, database_name)

    create_table(connection)

    n = int(input("职工数量："))
    people = create_people(n, connection)

    print("\033[0;32m************************菜单**************************\033[0m")
    print("1. 输出所有数据")
    print("2. 查找ID")
    print("3. 查找职业")
    print("4. 按照ID排序")
    print("5. 按照名字排序")
    print("6. 按照生日排序")
    print("7. 男女分开")
    print("8. 修改数据")
    print("9. 添加数据")
    print("10. 输出在文件中")
    print("11. 删除数据")
    print("12. 数据库")
    print("0. 退出程序")
    print("\033[0;32m******************************************************\033[0m")

    while True:
        key = int(input("\n\033[0;33m@输入操作：\033[0m"))
        if key == 1:
            print_people(people)
        elif key == 2:
            id = int(input("查找的人的ID: "))
            found = [p for p in people if p.ID == id]
            if found:
                print_people(found)
            else:
                print("没有此ID!")
        elif key == 3:
            job = input("要查找的职业: ")
            matching_people = [p for p in people if p.job == job]
            if matching_people:
                print("\033[0;36m")
                print("ID    Name   Gender  Birth Day\tWork Day  Phone Number\tEducation Background\tAddress\tJob")
                print("\033[0m")
                print_people(matching_people)
            else:
                print("没有找到匹配的职业!")
        elif key == 4:
            people.sort(key=lambda p: p.ID)
            print("排序后:")
            print_people(people)
        elif key == 5:
            people.sort(key=lambda p: p.name)
            print("排序后:")
            print_people(people)
        elif key == 6:
            people.sort(key=lambda p: p.birth_day)
            print("排序后:")
            print_people(people)
        elif key == 7:
            people.sort(key=lambda p: p.gender)
            print("排序后:")
            print_people(people)
        elif key == 8:
            id = int(input("修改谁的数据: "))
            update_person(people, id, connection)
        elif key == 9:
            add_person(people, connection)
        elif key == 10:
            write_to_file(people)
        elif key == 11:
            id = int(input("删除的人的ID: "))
            if delete_person(people, len(people), id, connection):
                print("成功删除!")
            else:
                print("删除失败")
        elif key == 12:
            # 显示所有数据
            people = select_all_persons(connection)
            print_people(people)
        elif key == 0:
            break
        else:
            print("重新输入!")

    connection.close()

def add_person(people, connection):
    ID = int(input("-ID: "))
    name = input("-姓名: ")
    gender = int(input("-性别: "))
    birth_day = int(input("-生日: "))
    work_day = int(input("-工作日: "))
    phone_number = int(input("-电话号码: "))
    education_background = input("-教育经历: ")
    address = input("-地址: ")
    job = input("-职业: ")
    person = Person(ID, name, gender, birth_day, work_day, phone_number, education_background, address, job)
    people.append(person)
    insert_person(connection, person)

def write_to_file(people, filename="output.txt"):
    with open(filename, "w") as file:
        file.write("ID\tName\tGender\tBirth Day\tWork Day\tPhone Number\tEducation Background\tAddress\tJob\n")
        for p in people:
            file.write(
                f"{p.ID}\t{p.name}\t{p.gender}\t{p.birth_day}\t{p.work_day}\t{p.phone_number}\t{p.education_background}\t{p.address}\t{p.job}\n")

if __name__ == "__main__":
    main()