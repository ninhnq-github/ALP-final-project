from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from dbConnect import *
from export import *
from tkinter import messagebox
from tkinter import filedialog
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

# Tạo form

app = Tk()
app.title('Phần mềm nhập điểm tự động')
app.geometry('780x400')
img_index = 98

#nút ảnh kế tipe61
def next_btn_click():
    global img_index
    img_index += 1

    if img_index >= len(files or len(files == 0)):
        messagebox.showinfo("Thông báo", "Đã hết tệp trong thư mục hoặc không tồn tại tệp")
    else:
        studentID, point = ScanfImg (files[img_index])
        path_lable = Label(score_frm, text='Đường dẫn: ' + files[img_index], font=('Arial', 10))
        path_lable.place(x=150, y=60)

        mssv_lb = Label(score_frm, text='MSSV: ' + str(studentID), font=('Arial', 14))
        mssv_lb.place(x=500, y=100)

        name_lb = Label(score_frm, text='Họ tên: ', font=('Arial', 14))
        name_lb.place(x=500, y=150)

        score_lb = Label(score_frm, text='Điểm: ' + str(point), font=('Arial', 14))
        score_lb.place(x=500, y=200)

        image = Image.open(files[img_index])
        image = image.resize((400, 300))
        test = ImageTk.PhotoImage(image)
        label = Label(score_frm, image=test)
        label.image = test
        label.place(x=50, y=100)

# nút chọn thư mục
def choose_folder_btn_click():
    app.filename = filedialog.askdirectory(title="Chọn thư mục")
    global files

    files = [f for f in glob.glob(app.filename + "**/*.jpg", recursive=True)]
    # for f in files:
    #     print(f)
    image1 = Image.open(files[0])
    image1 = image1.resize((400, 300))
    
    studentID, point = ScanfImg (files[0])
    print(studentID, point)

    test = ImageTk.PhotoImage(image1)
    label1 = Label(score_frm, image=test)
    label1.image = test
    label1.place(x=50, y=100)

    next_btn = Button(score_frm, text='Ảnh kế tiếp', font=("Consolas", 10, 'bold'), bg='orange', fg='white',
                      command=next_btn_click)
    next_btn.place(x=500, y=300)

    path_lable = Label(score_frm, text='Đường dẫn: ' + files[0], font=('Arial', 10))
    path_lable.place(x=150, y=60)

    mssv_lb = Label(score_frm, text='MSSV: ' + str(studentID), font=('Arial', 14))
    mssv_lb.place(x=500, y=100)

    name_lb = Label(score_frm, text='Họ tên: ' + str(getNameStudent(studentID)), font=('Arial', 14))
    name_lb.place(x=500, y=150)

    score_lb = Label(score_frm, text='Điểm: ' + str(point), font=('Arial', 14))
    score_lb.place(x=500, y=200)

#nút xuất ra file excel
def export_btn_click():
    save_to_excel = Export("D:")
    messagebox.showinfo("Xuất ra file excel", "Tạo file excel thành công tại ổ D:")

#nút nhập điểm
def score_btn_click():
    global score_frm
    score_frm = Toplevel(app)
    score_frm.geometry('900x450')
    score_frm.title("Nhập điểm cho sinh viên")

    lb = Label(score_frm, text='Phần mềm nhập điểm tự động', font=('Arial', 20))
    lb.grid(column=1, row=1)

    choose_folder_btn = Button(score_frm, text='Chọn thư mục', font=("Consolas", 10, 'bold'), bg='orange', fg='white',
                               command=choose_folder_btn_click)
    choose_folder_btn.place(x=50, y=60)

    save_btn = Button(score_frm, text='Lưu điểm', font=("Consolas", 10, 'bold'), bg='orange', fg='white')
    save_btn.place(x=500, y=250)

#Form chính
# Label
lb = Label(app, text='Phần mềm nhập điểm tự động', font=('Arial', 20))
lb.grid(column=1, row=1)

#
score_btn = Button(app, text='Nhập điểm', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white',
                   command=score_btn_click)
score_btn.place(x=10, y=40)

#
export_btn = Button(app, text='Xuất ra file excel', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white',
                    command=export_btn_click)
export_btn.place(x=100, y=40)

#
exit_btn = Button(app, text='Thoát', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white', command=app.destroy)
exit_btn.place(x=250, y=40)

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

# Dừng form
app.mainloop()
