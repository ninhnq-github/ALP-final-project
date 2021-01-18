from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from dbConnect import *
from export import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import torch
import matplotlib.pyplot as plt
import numpy as np
import torchvision
from torch import nn, optim
from torchvision import datasets, transforms
import cv2;
from CNNModels import CNNModel
from DigitClassification import *
import glob
from ExcelModule import *
from AndoidCameraConnect import *

# Tạo form

app = Tk()
app.title('Phần mềm nhập điểm tự động')
app.geometry('780x400')
img_index = 0
STUDENT_LIST_LOADED = 0
capture = None

#nút ảnh kế tipe61
def next_btn_click():
    global img_index
    img_index += 1

    if img_index >= len(files or len(files == 0)):
        messagebox.showinfo("Thông báo", "Đã hết tệp trong thư mục hoặc không tồn tại tệp")
        score_frm.focus()
        return 
    else:
        path_lable = Label(score_frm, text='Đường dẫn: ' + files[img_index], font=('Arial', 10))
        path_lable.place(x=150, y=60)

        global studentID, point
        studentID, point, message = ScanfImg(files[img_index])

        if (studentID!=-1):
            studentName = getNameStudent(studentID)[0]
            if (studentName == None):
                studentName = "Không tìm thấy sinh viên"
        else:
            studentID = point = studentName = 'null'
            messagebox.showerror('Quét ảnh không thành công','Chất lượng ảnh chụp chưa đáp ứng yêu cầu quét!')
            score_frm.focus()
            print(message)

        mssv_lb.config(text = 'MSSV: ' + str(studentID))
        name_lb.config(text ='Họ tên: ' + str(studentName))
        score_lb.config(text ='Điểm: ' + str(point))

        image = Image.open(files[img_index])
        image = image.resize((400, 300))
        test = ImageTk.PhotoImage(image)
        img_lb.configure(image=test)
        img_lb.image = test

TAKE_NEW = 0
def take_next_photo_click():
    global TAKE_NEW
    TAKE_NEW = (TAKE_NEW+1)%2
    global img_index
    img_index += 1

    #if (TAKE_NEW!=0):
    ret ,img = capture.read()
    filename = "CAPIMG/IMG" + str(img_index).zfill(5) + ".jpg"
    print(img)
    cv2.imwrite(filename, img)

    path_lable = Label(score_frm, text='Đường dẫn: '+ filename, font=('Arial', 10))
    path_lable.place(x=150, y=60)

    global studentID, point
    studentID, point, message = ScanfImg(filename)

    if (studentID!=-1):
        studentName = getNameStudent(studentID)[0]
        if (studentName == None):
            studentName = "Không tìm thấy sinh viên"
    else:
        studentID = point = studentName = 'null'
        messagebox.showerror('Quét ảnh không thành công','Chất lượng ảnh chụp chưa đáp ứng yêu cầu quét!')
        score_frm.focus()
        print(message)

    mssv_lb.config(text = 'MSSV: ' + str(studentID))
    name_lb.config(text ='Họ tên: ' + str(studentName))
    score_lb.config(text ='Điểm: ' + str(point))

    image = Image.open(filename)
    image = image.resize((400, 300))
    test = ImageTk.PhotoImage(image)
    img_lb.configure(image=test)
    img_lb.image = test
    #else:
    #    Fsrm.place(x=50, y=150)

# nút chọn thư mục
def choose_folder_btn_click():
    app.filename = filedialog.askdirectory(title="Chọn thư mục")
    global files
    score_frm.focus()

    files = [f for f in glob.glob(app.filename + "**/*.jpg", recursive=True)]
    # for f in files:
    #     print(f)

    image = Image.open(files[0])
    image = image.resize((400, 300))
    test = ImageTk.PhotoImage(image)
    img_lb.configure(image=test)
    img_lb.image = test

    next_btn.configure(command=next_btn_click) 

    save_btn.configure(command=save_btn_click) 

    path_lable.config(text = 'Đường dẫn: ' + files[0])

    global studentID, point
    studentID, point, message = ScanfImg(files[0])

    if (studentID!=-1):
        studentName = getNameStudent(studentID)[0]
        studentName = "Không tìm thấy sinh viên"
    else:
        studentID = point = studentName = 'null'
        messagebox.showerror('Quét ảnh không thành công','Chất lượng ảnh chụp chưa đáp ứng yêu cầu quét!')
        score_frm.focus()

    mssv_lb.config(text = 'MSSV: ' + str(studentID))
    name_lb.config(text ='Họ tên: ' + str(studentName))
    score_lb.config(text ='Điểm: ' + str(point))


#nút xuất ra file excel
def export_btn_click():
    
    if (STUDENT_LIST_LOADED==0):
        messagebox.showinfo("Thông báo", "Chưa nhập danh sách sinh viên cần nhập điểm")
        return False
    
    path = filedialog.askopenfilename(title="Chọn file excel lưu điểm của sinh viên",
                                             filetypes=[('Excel file','*.xlsx')])
    save_to_excel = ExportToExcel(app.studentList,path)

    if (save_to_excel):
        messagebox.showinfo("Xuất ra file excel", "Tạo file excel thành công tại: " + path)
    else:
        messagebox.showinfo("Xuất ra file excel", "Lưu file không thành công! Đã xẩy ra lỗi!")


def save_btn_click():
    print(studentID, point)
    if (studentID == 'null' or studentID == None):
        messagebox.showinfo("Thông báo", "Mã số sinh viên không hợp lệ")
        score_frm.focus()
        return False
    if (updateScore(str(studentID), str(point))):
        messagebox.showinfo("Thông báo", 
                            "Lưu thành công điểm: %.2f cho sinh viên: %s"%(getNameStudent(studentID),point))
        score_frm.focus()
        return True
    else:
        messagebox.showinfo("Thông báo", "Không tìm thấy sinh viên trong CSDL")
        score_frm.focus()
        return False

def scaner_btn_click():
    url =  simpledialog.askstring(title="Input", prompt="Nhập đường link liên kết đến scaner")
    
    global capture
    check, capture = getCameraStream(url)
    global Fsrm

    if (check == True):
        Fsrm = Frame(score_frm, width=400, height=300, background="bisque")
        Fsrm.grid()
        lmain = Label(Fsrm)
        lmain.grid()
        lmain.configure( width=400, height=300, background="bisque")
        Fsrm.place(x=50, y=150)
        video_stream(lmain,capture)
        next_btn.configure(command=take_next_photo_click)
        return True
    else:
        messagebox.showinfo("Thông báo", "Không tìm thấy scaner!")
        score_frm.focus()
        return False

#nút nhập điểm
def score_btn_click():
    
    if (STUDENT_LIST_LOADED==0):
        messagebox.showinfo("Thông báo", "Chưa nhập danh sách sinh viên cần nhập điểm")
        return False

    global score_frm
    score_frm = Toplevel(app)
    score_frm.geometry('900x550')
    score_frm.title("Nhập điểm cho sinh viên")

    lb = Label(score_frm, text='Phần mềm nhập điểm tự động', font=('Arial', 20))
    lb.grid(column=1, row=1)

    global path_lable
    path_lable = Label(score_frm, text='Đường dẫn: ', font=('Arial', 10))
    path_lable.place(x=150, y=60)

    global next_btn 
    next_btn = Button(score_frm, text='Ảnh kế tiếp', font=("Consolas", 10, 'bold'), bg='orange', fg='white' )
    next_btn.place(x=500, y=300)

    choose_folder_btn = Button(score_frm, text='Chọn thư mục', font=("Consolas", 10, 'bold'), bg='orange', fg='white',
                               command=choose_folder_btn_click)
    choose_folder_btn.place(x=50, y=60)

    choose_folder_btn = Button(score_frm, text='Liên kết Scaner', font=("Consolas", 10, 'bold'), bg='orange', fg='white',
                               command=scaner_btn_click)
    choose_folder_btn.place(x=50, y=110)

    global save_btn
    save_btn = Button(score_frm, text='Lưu điểm', font=("Consolas", 10, 'bold'), bg='orange', fg='white')
    save_btn.place(x=500, y=250)

    global mssv_lb
    mssv_lb = Label(score_frm, text='MSSV: ' , font=('Arial', 14))
    mssv_lb.place(x=500, y=100)

    global name_lb
    name_lb = Label(score_frm, text='Họ tên: ', font=('Arial', 14))
    name_lb.place(x=500, y=150)

    global score_lb
    score_lb = Label(score_frm, text='Điểm: ', font=('Arial', 14))
    score_lb.place(x=500, y=200)

    global img_lb 
    image = Image.open('meow.jpg')
    image = image.resize((400, 300))
    test = ImageTk.PhotoImage(image)
    img_lb = Label(score_frm, image=test)
    img_lb.image = test
    img_lb.place(x=50, y=150)

    score_frm.focus_force()


def importStudentList(path):

    check_del = delAllStudent()
    USER_INP = simpledialog.askstring(title="Input", prompt="Nhập tên / mã môn thi")
    importExcelData(app.studentList,USER_INP)
    # Tree View
    tree_view = ttk.Treeview(app, selectmode='browse')
    tree_view.place(x=30, y=100)

    # Constructing vertical scrollbar with tree view
    verscrlbar = ttk.Scrollbar(app, orient="vertical", command=tree_view.yview)

    # Configuring tree view
    tree_view.configure(xscrollcommand=verscrlbar.set)

    # Defining number of columns
    tree_view["columns"] = ("1", "2", "3", "4")

    # Defining heading
    tree_view['show'] = 'headings'

    # Assigning the width and anchor to  the`
    # respective columns
    tree_view.column("1", width=150, anchor='c')
    tree_view.column("2", width=220, anchor='c')
    tree_view.column("3", width=220, anchor='c')
    tree_view.column("4", width=100, anchor='c')

    # Assigning the heading names to the
    # respective columns
    tree_view.heading("1", text="MSSV   ")
    tree_view.heading("2", text="Họ tên")
    tree_view.heading("3", text="Môn thi")
    tree_view.heading("4", text="Điểm")

    # Inserting the items and their features to the
    # columns built

    result = getStudent()
    for row in result:
        tree_view.insert("", 'end', text="L1", values=(row[0], row[1], row[2], row[3]))



def load_btn_click():
    try:
        app.studentList = filedialog.askopenfilename(title="Chọn file excel chứa danh sách sinh viên")
        importStudentList(app.studentList)
        global STUDENT_LIST_LOADED
        STUDENT_LIST_LOADED = 1
        return True
    except:
        messagebox.showinfo("Thông báo", "Danh sách nhập không hợp lệ!")
        return False
    #print(STUDENT_LIST_LOADED)
    
#Form chính
# Label
lb = Label(app, text='Phần mềm nhập điểm tự động', font=('Arial', 20))
lb.grid(column=1, row=1)
#
score_btn = Button(app, text='Nhập điểm', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white',
                   command=score_btn_click)
score_btn.place(x=10, y=40)
score_btn = Button(app, text='Nhập danh sách sinh viên', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white',
                   command=load_btn_click)
score_btn.place(x=100, y=40)
#
export_btn = Button(app, text='Xuất ra file excel', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white',
                    command=export_btn_click)
export_btn.place(x=300, y=40)
#
exit_btn = Button(app, text='Thoát', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white', command=app.destroy)
exit_btn.place(x=450, y=40)


# Dừng form
app.mainloop()
