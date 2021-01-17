import pandas as pd
from openpyxl import Workbook
from dbConnect import *

def ExcelFile(path, subject='None'): #Nhập dữ liệu file excel ở địa chỉ path
    xl = pd.ExcelFile(path)
    df = pd.read_excel(xl, 0, header=None)
    table = []
    for i in range(len(df.iloc[:, 0])-1):
        table.append([])
        table[i].append(df.at[i+1, 1])
        table[i].append(str(df.at[i+1, 2]) + str(df.at[i+1, 3]))
        table[i].append(subject)
        table[i].append('0')
    return table

def Export(path): #xuất dữ liệu sang file excel ở địa chỉ path
    book = Workbook()
    sheet = book.active    
    sheet['A1'] = 'MSSV'
    sheet['B1'] = 'Họ tên'
    sheet['C1'] = 'Môn thi'
    sheet['D1'] = 'Điểm'
    table = dbConnect.getStudent()
    for i in range(len(table)):
        sheet['A' + str(i + 2)] = table[i][0]
        sheet['B' + str(i + 2)] = table[i][1]
        sheet['C' + str(i + 2)] = table[i][2]
        sheet['D' + str(i + 2)] = table[i][3]
        book.save(path + "/BangDiem.xlsx")


ExcelFile('D:\CODE\PYTHON\ALP-final-project\APL-project\STDList.xlsx','Math')

def importExcelData(path, subject):
    table = ExcelFile(path, subject)
    for row in table:
        if (str(row[0])!='nan'):
            print(insertStudent(row[0],row[1],row[2],row[3]))

def fromExcelToCsv(path,csvname):
    file = open(csvname,"w", encoding="utf-8")
    table = ExcelFile(path, 'Math')
    for row in table:
        if (str(row[0])!='nan'):
            #print('%s,%s,%s,%s'%(row[0],row[1],row[2],row[3]))
            file.write('%s,%s,%s,%s\n'%(row[0],row[1],row[2],row[3]))
    file.close()

importExcelData('D:\CODE\PYTHON\ALP-final-project\APL-project\STDList.xlsx','Math')
#fromExcelToCsv('D:\CODE\PYTHON\ALP-final-project\APL-project\STDList.xlsx','D:\CODE\PYTHON\ALP-final-project\APL-project\StudentList.csv')

#import_csv_to_mysql(filename)