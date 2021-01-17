import pymysql.cursors
import csv

def getConnect():
    '''
        Lấy kết nối với database
    :return:
    '''
    hname = 'localhost'
    uname = 'root'
    pwd = 'Nmaster2000'
    database = 'identify_digit'

    # Kết nối vào database.
    connection = pymysql.connect(host= hname,  user= uname, password= pwd, db= database)
    return connection

def getStudent():
    '''
        lấy ra danh sách sinh viên có trong talbe từ database
    :return: table
    '''
    connect = getConnect()

    query = "SELECT * FROM student"
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        table = cursor.fetchall()

        return table
    except:
        connect.rollback()
    finally:
        connect.close()

def getNameStudent(mssv):
    '''
        Lấy ra tên sinh viên theo mã số sinh viên, và chỉ 1 dòng đầu tiên
    :param mssv:
    :return: table
    '''
    connect = getConnect()

    query = "SELECT fullname FROM student WHERE MSSV = '%s'" % (''.join(str(mssv)))
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        table = cursor.fetchone()
        return table
    except:
        connect.rollback()
    finally:
        connect.close()


def ExecuteQuery(query):
    '''
        for select, delete:
    '''
    connect = getConnect()
    cursor = connect.cursor()
    try:
        cursor.execute(query=query)
        connect.commit()
        return True
    except:
        connect.rollback()
        return False
    finally:
        connect.close()

def ExecuteNoneQuery(query):
    '''
        for insert, update,...
    '''
    conn = getConnect()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit();
        if cursor.rowcount > 0:
            return True
        else:
            print('Error : Execute unsuccessfully...')
            return False
    except:
        conn.rollback()
        print('Error : Query syntax incorrect or this data existed...')
        return False
    finally:
        conn.close()

def insertScore(mssv, score):
    '''
        Thêm điểm cho học sinh có mssv tương ứng
    :param mssv:
    :param score:
    :return: true or false
    '''
    query = "INSERT INTO student(MSSV, scores) values('%s' , '%s')" % (''.join(mssv), ''.join(score))
    check = ExecuteNoneQuery(query=query)
    return check

def insertStudent(mssv, name, subject, score):
    '''
        Thêm thông tin học viên
    :param mssv:
    :param name:
    :param subject:
    :param score:
    :return: bool
    '''
    query = "INSERT INTO student(MSSV, fullname, subjects ,scores) VALUES ('%s', '%s', '%s', '%s')" % (''.join(mssv),
                                                                                                    ''.join(name),
                                                                                                    ''.join(subject),
                                                                                                    ''.join(score))
    data = ExecuteNoneQuery(query=query)
    return data


def updateStudent(mssv, name, subject, score):
    '''
        Cập nhật thông tin học viên
    :param mssv:
    :param name:
    :param subject:
    :param score:
    :return: bool
    '''
    query = "UPDATE student SET fullname= '%s', subjects= '%s', scores= '%s' WHERE MSSV = '%s'" %(''.join(name),
                                                                                                  ''.join(subject),
                                                                                                  ''.join(score),
                                                                                                  ''.join(mssv))
    check = ExecuteNoneQuery(query=query)
    return check

def updateScore(mssv, score):
    query = "UPDATE student SET scores = '%s' WHERE MSSV = '%s'" %(''.join(score), ''.join(mssv))
    data = ExecuteNoneQuery(query=query)
    return data

def deleteStudent(mssv):
    '''
        Xoá 1 sinh viên trong bảng
    :param mssv:
    :return:
    '''
    query = "DELETE FROM student WHERE MSSV = '%s'" % ''.join(mssv)
    data = ExecuteQuery(query=query)
    return data

def delAllStudent():
    '''
        Xoá toàn bộ sinh viên có trong bảng student
    :return:
    '''
    query = 'DELETE FROM student'
    data = ExecuteQuery(query=query)
    return data

def import_csv_to_mysql(filename):
    '''
     Truyền vào tên file csv cần nhập vào dữ liệu vào mysql
    :param filename:
    :return:
    '''
    file = open(filename, 'r')
    csv_data = csv.reader(file)
    for row in csv_data:
        insertStudent(row[0], row[1], row[2], row[3])

    print('Import Successfull...')


#-----------------------------------------------------
# Xoá sinh viên theo mssv
# d = deleteStudent('18110005')
# print('Delete: ', d)

# Them MSSV, score
# t= insertScore('18110005', '9')
# print('Insert score: ', t)

# cap nhat lai thong tin ca nhan theo  mssv
# k = updateStudent('18110005','Mộng Mơ Giữa hè','PRE', '7')
# print('Update: ', k)

# thêm đầy đủ thông tin sinh viên
# check = insertStudent('18110321', 'Nguyen Hoai Nam', 'Math', '0')
# print('check insert student: ', check)

#Nhập dữ liệu từ file csv vào sql
#import_csv_to_mysql('student.csv')


# Lấy danh sách sinh viên
# table = getStudent()
# for row in table:
#     print(row)


# Lấy tên sinh viên theo mã số
# data = getNameStudent('18110321')
# print('data: ', data[0])

# Xoá toàn bộ sinh viên trong bảng
# check_del = delAllStudent()
# print('check_del: ', check_del)

# Lấy danh sách sinh viên
# table = getStudent()
# if table == None:
#     for row in table:
#         print(row)
# else:
#     print('khong co du lieu trong bang')