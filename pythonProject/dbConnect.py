import pymysql.cursors
import csv

def getConnect():
    hname = 'localhost'
    uname = 'root'
    pwd = 'Youaretheappleofmyeyes'  # thay password tương ứng với root máy bạn
    database = 'identify_digit'

    # Kết nối vào database.
    connection = pymysql.connect(host=hname, user=uname, password=pwd, db=database)
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
        print('rollback')
    finally:
        connect.close()


def insertScore(mssv, score):
    '''
        Thêm điểm cho học sinh có mssv tương ứng
    :param mssv:
    :param score:
    :return: true or false
    '''
    conn = getConnect()

    query = "INSERT INTO student(MSSV, scores) values('%s' , '%s')" % (''.join(mssv), ''.join(score))
    try:
        cursor = conn.cursor()
        # thực thi query và truyền tham số vào
        cursor.execute(query)
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except:
        conn.rollback()
        return False
    finally:
        conn.close()


def updateStudent(mssv, name, subject, score):
    '''
        Cập nhật thông tin học viên
    :param mssv:
    :param name:
    :param subject:
    :param score:
    :return: bool
    '''
    conn = getConnect()

    query = "UPDATE student SET fullname= '%s', subjects= '%s', scores= '%s' WHERE MSSV = '%s'" % (''.join(name),
                                                                                                   ''.join(subject),
                                                                                                   ''.join(score),
                                                                                                   ''.join(mssv))
    try:
        cursor = conn.cursor()

        # thực thi query và truyền tham số vào
        cursor.execute(query)
        conn.commit();
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except:
        conn.rollback()
        return False
    finally:
        conn.close()


def deleteStudent(mssv):
    '''
        Xoá 1 sinh viên trong bảng
    :param mssv:
    :return:
    '''
    conn = getConnect()

    query = "DELETE FROM student WHERE MSSV = '%s'" % ''.join(mssv)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print('Xoa Thanh Cong')
    except:
        conn.rollback()
        print('Error')
    finally:
        conn.close()


def import_csv_to_mysql(filename):
    '''
     Truyền vào tên file csv cần nhập vào dữ liệu vào mysql
    :param filename: cùng thư mục chứa project
    '''
    file = open(filename, 'r')
    csv_data = csv.reader(file)

    for row in csv_data:
        insertStudent(row[0], row[1], row[2], row[3])

    print('Import Successfull...')
            

def insertStudent(mssv, name, subject, score):
    '''
        Thêm thông tin học viên
    :param mssv:
    :param name:
    :param subject:
    :param score:
    :return: bool
    '''
    conn = getConnect()

    query = "INSERT INTO student(MSSV, fullname, subject,scores) VALUES ('%s', '%s', '%s', '%s')" % (''.join(mssv),
                                                                                                    ''.join(name),
                                                                                                    ''.join(subject),
                                                                                                    ''.join(score))
    cursor = conn.cursor()
    try:
        # thực thi query và truyền tham số vào
        cursor.execute(query)

        conn.commit();
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except:
        conn.rollback()
        return False
    finally:
        conn.close()
        
        
def delAllStudent():
    connect = getConnect()

    query = "DELETE FROM student"
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        connect.commit()
        return True
    except:
        connect.rollback()
        return False
    finally:
        connect.close()

#-----------------------------------------------------
# deleteStudent('18110005')

# t= insertScore('18110005', '9')
# print('Insert: ', t)
#
# k = updateStudent('18110004','Trịnh Mơ','PRE', '7')
# print('Update: ', t)

#table = getStudent()

#for row in table:
#    print(row)