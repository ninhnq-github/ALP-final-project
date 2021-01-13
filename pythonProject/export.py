from openpyxl import Workbook
import dbConnect

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