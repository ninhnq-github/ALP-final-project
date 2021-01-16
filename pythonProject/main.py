from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from dbConnect import *
from export import *
from tkinter import messagebox
# Tạo form

app = Tk()
app.title('Phần mềm nhập điểm tự động')
app.geometry('780x400')


def export_btn_click():
    save_to_excel = Export("D:\HK1_2020-2021\Advanced Programming Language\excel")
    messagebox.showinfo("Xuất ra file excel", "Tạo file excel thành công: D:\HK1_2020-2021\Advanced Programming Language\excel")

def score_btn_click():
    score_frm = Toplevel(app)
    score_frm.title("Nhập điểm cho sinh viên")
    score_frm.geometry('780x400')

    lb = Label(score_frm, text='Phần mềm nhập điểm tự động', font=('Arial', 20))
    lb.grid(column=1, row=1)

    # using PIL
    image1 = Image.open("meow.jpg")
    image1 = image1.resize((400, 300))

    test = ImageTk.PhotoImage(image1)
    label1 = Label(score_frm, image=test)
    label1.image = test
    label1.place(x=50, y=100)

    mssv_lb = Label(score_frm, text='MSSS: ', font=('Arial', 14))
    mssv_lb.place(x=500, y=100)

    name_lb = Label(score_frm, text='Họ tên: ', font=('Arial', 14))
    name_lb.place(x=500, y=150)

    score_lb = Label(score_frm, text='Điểm: ', font=('Arial', 14))
    score_lb.place(x=500, y=200)

    scan_btn = Button(score_frm, text='Quét', font=("Consolas", 10, 'bold'), bg='orange', fg='white')
    scan_btn.place(x=50, y=60)

    save_btn = Button(score_frm, text='Lưu điểm', font=("Consolas", 10, 'bold'), bg='orange', fg='white')
    save_btn.place(x=500, y=250)


# Label
lb = Label(app, text='Phần mềm nhập điểm tự động', font=('Arial', 20))
lb.grid(column=1, row=1)

#
score_btn = Button(app, text='Nhập điểm', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white',
                   command=score_btn_click)
score_btn.place(x=10, y=40)

#
export_btn = Button(app, text='Xuất ra file excel', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white', command=export_btn_click)
export_btn.place(x=100, y=40)

#
exit_btn = Button(app, text='Thoát', font=("Consolas", 10, 'bold'), bg='RoyalBlue1', fg='white', command=app.destroy)
exit_btn.place(x=250, y=40)

# Tree View
tree_view = ttk.Treeview(app, selectmode='browse')
tree_view.place(x=30, y=100)

# Constructing vertical scrollbar with treeview
verscrlbar = ttk.Scrollbar(app, orient="vertical", command=tree_view.yview)

# Configuring treeview
tree_view.configure(xscrollcommand=verscrlbar.set)

# Defining number of columns
tree_view["columns"] = ("1", "2", "3", "4")

# Defining heading
tree_view['show'] = 'headings'

# Assigning the width and anchor to  the
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
