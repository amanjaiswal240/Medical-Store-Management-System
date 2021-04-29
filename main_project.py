from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
import datetime
import time
import re
import random
import os
import webbrowser as wb
from fpdf import FPDF

connection = pymysql.connect("localhost", "root", "", "medical_store_management")


def splash_win():
    splash_root = Tk()
    splash_scr = SplashScreen(splash_root)
    splash_root.mainloop()


class SplashScreen:
    def __init__(self, splash):
        self.splash = splash
        self.splash.title("Splash Screen")
        self.splash.overrideredirect(True)
        self.splash.resizable(0, 0)
        image = PhotoImage(file=r"images\splash_img.png")
        height = 300
        width = 500
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)

        self.splash.geometry("{}x{}+{}+{}".format(width, height, x, y))

        Label(self.splash, image=image).pack()

        bglbl = Label(self.splash, image=image)
        bglbl.image = image
        bglbl.pack()
        self.splash.after(4000, self.main)

    def main(self):
        self.splash.destroy()
        root = Tk()
        app = SystemLogin(root)

        def on_closing():
            if messagebox.askyesno("Exit","Do you really want to exit"):
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()


class SystemLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Medical Store Login Window")
        self.master.config(bg='#f0f7ff')
        bg_color = '#f0f7ff'

        icon = PhotoImage(file=r"images\logo.png")
        self.master.iconphoto(False, icon)

        height = 300
        width = 500
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)

        self.master.geometry("{}x{}+{}+{}".format(width, height, x, y))

        ############### VARIABLES ##############
        self.Username = StringVar()
        self.Password = StringVar()

        title = Label(self.master, text="Login To System", bd=12, relief=GROOVE, bg='#2a6287', fg="white",
                      font=("arial",16,"bold"), pady=6).pack(fill=X)

        lbl_user = Label(self.master, text="Username:", bg=bg_color, fg="#2a6287", font=("arial", 16, "bold")).place(x=35,
                                                                                                               y=100)
        ent_user = Entry(self.master, textvariable=self.Username, font=("arial", 16)).place(x=210, y=100)
        lbl_passwd = Label(self.master, text="Password:", height="1", bg=bg_color, fg="#2a6287",
                       font=("arial", 16, "bold")).place(x=35, y=160)
        ent_passwd = Entry(self.master, textvariable=self.Password, show='*', font=("arial", 16)).place(x=210, y=160)

        login_btn = Button(self.master, text="Log In",command=self.Login_System, width=16, bd=4, bg="#2a6287",
                           fg="white", font="arial 16 bold").place(x=140, y=230)

    def Login_System(self):
        user = (self.Username.get())
        passwd = (self.Password.get())

        with connection.cursor() as cur:
            cur.execute("select * from admin")
            rows = cur.fetchall()

        user_name=rows[0][1]
        user_passwd=rows[0][2]

        if (user == "" or passwd == ""):
            messagebox.showinfo("Login System", "Fill the Login Details")
        elif (user == user_name and passwd == user_passwd):
            self.master.withdraw()
            self.Login_Window()
        else:
            messagebox.showerror("Login System", "Invalid Login Details")
            self.Username.set("")
            self.Password.set("")

    def Login_Window(self):
        self.loginWindow = Toplevel(self.master)
        self.app = DashBoard(self.loginWindow)

        def on_closing():
            if messagebox.askyesno("Exit","Do you really want to exit"):
                self.loginWindow.destroy()
                self.master.destroy()

        self.loginWindow.protocol("WM_DELETE_WINDOW", on_closing)
        self.loginWindow.mainloop()


class DashBoard:
    def __init__(self, master):
        self.master = master
        self.master.title("Medical Store Management System")
        self.master.geometry("1200x640+0+0")
        self.master.resizable(0, 0)
        self.bg_color = "#202B35"
        self.sm_bg_color = "#2a6287"
        self.master.configure(bg=self.bg_color)

        icon = PhotoImage(file=r"images\logo.png")
        self.master.iconphoto(False, icon)

        ################## Variables ##############
        self.total_price = 0.0
        self.today_date = datetime.date.today()
        self.to_date_lbl = StringVar()
        self.to_date_lbl.set(self.change_date_format(str(self.today_date)))

        self.Username = StringVar()
        self.Password = StringVar()
        ################ add_new_pro_variables ##########

        self.add_pro_name = StringVar()
        self.add_category = StringVar()
        self.add_quantity = StringVar()
        self.add_supplier = StringVar()
        self.add_manu_date = StringVar()
        self.add_exp_date = StringVar()
        self.add_buy_price = StringVar()
        self.add_sell_price = StringVar()

        ################ manage_pro_variables ##########

        self.mn_pro_id = StringVar()
        self.mn_pro_name = StringVar()
        self.mn_category = StringVar()
        self.mn_quantity = StringVar()
        self.mn_supplier = StringVar()
        self.mn_manu_date = StringVar()
        self.mn_exp_date = StringVar()
        self.mn_buy_price = StringVar()
        self.mn_sell_price = StringVar()
        self.search_pro_name = StringVar()
        self.search_pro_supp = StringVar()
        # self.search_pro_date= StringVar()

        ################ add_new_supplier_variables ##########

        self.supplier_name = StringVar()
        self.contact_no = StringVar()
        self.search_supp_name = StringVar()

        ################ add_new_purchase_variable ##########

        self.pur_supplier = StringVar()
        self.pur_entry_date = StringVar()
        self.pur_category = StringVar()
        self.pur_pro_name = StringVar()
        self.pur_manu_date = StringVar()
        self.pur_exp_date = StringVar()
        self.pur_quantity = StringVar()
        self.purch_unit_price = StringVar()
        self.sell_unit_price = StringVar()
        self.pur_bill_no = StringVar()
        y = random.randint(1000, 9999)
        self.pur_bill_no.set(str(y))
        self.pur_total_price = StringVar()
        self.pur_total_price.set("0.0")

        ################ POS_sale_variables ##########

        self.customer = StringVar()
        self.cust_contact = StringVar()
        self.entry_date = StringVar()

        self.bill_no = StringVar()
        x = random.randint(1000, 9999)
        self.bill_no.set(str(x))

        self.search_sale_item = StringVar()
        self.selected_item_lbl = StringVar()
        self.selected_quantity_lbl = StringVar()
        self.selected_price_lbl = StringVar()
        self.select_quantity_to_sale = StringVar()
        self.paid_rs = StringVar()
        self.return_rs = StringVar()
        self.total_price_sale = StringVar()
        self.total_price_sale.set("0.0")
        self.return_rs.set("0.0")

        ################ Manage_sale_variables ##########
        self.search_mn_sale_item = StringVar()

        ################ Manage_pur_variables ##########
        self.search_mn_pur_supp = StringVar()

        def clock():
            hour = time.strftime("%I")
            minute = time.strftime("%M")
            second = time.strftime("%S")

            timer_lbl.config(text=hour + ":" + minute + ":" + second)
            timer_lbl.after(1000, clock)

        def add_new_product():
            hide_all_frames()
            add_product_frame.pack(fill="both", expand=1)

        def change_user_details():
            hide_all_frames()
            change_user_frame.pack(fill="both", expand=1)

        def manage_product():
            hide_all_frames()
            manage_product_frame.pack(fill="both", expand=1)

        def pos_sale():
            hide_all_frames()
            pos_sale_frame.pack(fill="both", expand=1)

        def manage_sale():
            hide_all_frames()
            manage_sale_frame.pack(fill="both", expand=1)

        def add_supplier():
            hide_all_frames()
            add_supplier_frame.pack(fill="both", expand=1)

        def add_purchase():
            hide_all_frames()
            add_purchase_frame.pack(fill="both", expand=1)

        def manage_purchase():
            hide_all_frames()
            manage_purchase_frame.pack(fill="both", expand=1)

        def out_of_stock():
            hide_all_frames()
            out_of_stock_frame.pack(fill="both", expand=1)

        def expired_products():
            hide_all_frames()
            expired_product_frame.pack(fill="both", expand=1)

        def hide_all_frames():
            add_product_frame.pack_forget()
            change_user_frame.pack_forget()
            manage_product_frame.pack_forget()
            pos_sale_frame.pack_forget()
            manage_sale_frame.pack_forget()
            add_supplier_frame.pack_forget()
            add_purchase_frame.pack_forget()
            manage_purchase_frame.pack_forget()
            out_of_stock_frame.pack_forget()
            expired_product_frame.pack_forget()

        title = Label(self.master, text="Medical Store Management System", bd=12, relief=GROOVE, bg=self.sm_bg_color,
                      fg="white", font=("arial", 18, "bold"), pady=6).pack(fill=X)

        ################################ Navigation Frame #################################

        nav_frame = Frame(self.master, width=300, height=640)
        nav_frame.pack(side=LEFT)

        brand_frame = Frame(nav_frame, width=300, height=100, bd=12, relief=GROOVE)
        brand_frame.pack(side=TOP)

        nav_btn_frame = Frame(nav_frame, width=300, height=5400, bd=12, relief=GROOVE)
        nav_btn_frame.pack(side=BOTTOM)

        ################################ Funcionalities Frame ##############################

        add_product_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        change_user_frame = Frame(self.master, width=900, height=640, bg="#d7dbe0")
        manage_product_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        pos_sale_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        pos_sale_frame.pack(fill="both", expand=1)
        manage_sale_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        add_supplier_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        add_purchase_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        manage_purchase_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        out_of_stock_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)
        expired_product_frame = Frame(self.master, width=900, height=640, bg=self.bg_color)

        #################################### Navigation Buttons #############################

        load_img = PhotoImage(file="images\\logo.png")
        logo_img = load_img.subsample(8, 8)
        my_lbl = Label(brand_frame, image=logo_img)
        my_lbl.image = logo_img
        my_lbl.place(x=6, y=4)
        timer_lbl = Label(brand_frame, font=("Helvetica", 20), fg="white", bd=2, bg=self.sm_bg_color, relief=GROOVE)
        timer_lbl.place(x=155, y=6)
        clock()
        today_date_lbl = Label(brand_frame, font=("Helvetica", 13, "bold"), fg=self.sm_bg_color,
                               textvariable=self.to_date_lbl)
        today_date_lbl.place(x=180, y=48)

        add_product_btn = Button(nav_btn_frame, text="Add New Item", command=add_new_product, width=10, bd=2,
                                 bg=self.sm_bg_color,
                                 fg="white", font="arial 10 bold", padx="16", pady="5").place(x=10, y=50)
        change_user_passwd_btn = Button(nav_btn_frame, text="Change Password", command=change_user_details, width=10, bd=2,
                                    bg=self.sm_bg_color, fg="white",font="arial 10 bold",padx="16",pady="5").place(x=140,y=50)
        manage_product_btn = Button(nav_btn_frame, text="Manage Product", command=manage_product, width=10, bd=2,
                                    bg=self.sm_bg_color,
                                    fg="white", font="arial 10 bold", padx="16", pady="5").place(x=10, y=130)
        POs_sale_btn = Button(nav_btn_frame, text="POS Sale", command=pos_sale, width=10, bd=2, bg=self.sm_bg_color,
                              fg="white", font="arial 10 bold", padx="16", pady="5").place(x=140, y=130)
        add_supplier_btn = Button(nav_btn_frame, text="Add Supplier", command=add_supplier, width=10, bd=2,
                                  bg=self.sm_bg_color,
                                  fg="white", font="arial 10 bold", padx="16", pady="5").place(x=10, y=210)
        add_purchase_btn = Button(nav_btn_frame, text="Add New Purchase", command=add_purchase, width=10, bd=2,
                                  bg=self.sm_bg_color,
                                  fg="white", font="arial 10 bold", padx="16", pady="5").place(x=140, y=210)
        manage_sale_btn = Button(nav_btn_frame, text="Manage Sale", command=manage_sale, width=10, bd=2,
                                 bg=self.sm_bg_color,
                                 fg="white", font="arial 10 bold", padx="16", pady="5").place(x=10, y=290)
        manage_purchase_btn = Button(nav_btn_frame, text="Manage Purchase", command=manage_purchase, width=10, bd=2,
                                     bg=self.sm_bg_color,
                                     fg="white", font="arial 10 bold", padx="16", pady="5").place(x=140, y=290)
        out_of_stock_btn = Button(nav_btn_frame, text="Out of Stock", command=out_of_stock, width=10, bd=2,
                                  bg=self.sm_bg_color,
                                  fg="white", font="arial 10 bold", padx="16", pady="5").place(x=10, y=370)
        expired_btn = Button(nav_btn_frame, text="Expired Products", command=expired_products, width=10, bd=2,
                             bg=self.sm_bg_color,
                             fg="white", font="arial 10 bold", padx="16", pady="5").place(x=140, y=370)

        ######################## add_product_frame ###########################

        title = Label(add_product_frame, text="Add New Product", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        new_product_form = Frame(add_product_frame, width=900, height=560, bd=2, relief=GROOVE)
        new_product_form.pack(side=TOP, expand=1)
        pro_name_lbl = Label(new_product_form, text="Product Name", fg=self.sm_bg_color,
                             font=("arial", 12, "bold")).place(x=40, y=40)
        pro_name_ent = Entry(new_product_form, font=("arial", 12), textvariable=self.add_pro_name).place(x=200, y=40)
        category_lbl = Label(new_product_form, text="Category", fg=self.sm_bg_color,
                             font=("arial", 12, "bold")).place(x=480, y=40)
        category_ent = Entry(new_product_form, font=("arial", 12), textvariable=self.add_category).place(x=640, y=40)
        quantity_lbl = Label(new_product_form, text="Quantity", fg=self.sm_bg_color,
                             font=("arial", 12, "bold")).place(x=40, y=120)
        quantity_ent = Entry(new_product_form, font=("arial", 12), textvariable=self.add_quantity).place(x=200, y=120)
        supplier_lbl = Label(new_product_form, text="Supplier", fg=self.sm_bg_color,
                             font=("arial", 12, "bold")).place(x=480, y=120)
        supplier_ent = Entry(new_product_form, font=("arial", 12), textvariable=self.add_supplier).place(x=640, y=120)
        manu_date_lbl = Label(new_product_form, text="Manufacture Date", fg=self.sm_bg_color,
                              font=("arial", 12, "bold")).place(x=40, y=200)
        manu_date_ent = DateEntry(new_product_form, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", maxdate=self.today_date,
                                  textvariable=self.add_manu_date).place(x=200, y=200)
        exp_date_lbl = Label(new_product_form, text="Expiry Date", fg=self.sm_bg_color,
                             font=("arial", 12, "bold")).place(x=480, y=200)
        exp_date_ent = DateEntry(new_product_form, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", mindate=self.today_date,
                                 textvariable=self.add_exp_date).place(x=640, y=200)
        buy_price_lbl = Label(new_product_form, text="Buying Price", fg=self.sm_bg_color,
                              font=("arial", 12, "bold")).place(x=40, y=280)
        buy_price_ent = Entry(new_product_form, font=("arial", 12), textvariable=self.add_buy_price).place(x=200, y=280)
        sell_price_lbl = Label(new_product_form, text="Selling Price", fg=self.sm_bg_color,
                               font=("arial", 12, "bold")).place(x=480, y=280)
        sell_price_ent = Entry(new_product_form, font=("arial", 12), textvariable=self.add_sell_price).place(x=640,
                                                                                                             y=280)

        add_product_btn = Button(new_product_form, text="Add Item", command=self.add_new_product, width=16, bd=2,
                                 bg=self.sm_bg_color, fg="white",
                                 font="arial 20 bold").place(x=560, y=420)

        ######################## change_user_frame ############################

        title = Label(change_user_frame, text="Change Admin Details", bd=2, relief=GROOVE, bg=self.sm_bg_color,
                      fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        user_change_fr = Frame(change_user_frame, width=500, height=300, bd=2, relief=GROOVE)
        user_change_fr.place(x=200, y=160)

        user_title_fr = Frame(user_change_fr, width=500, height=60, bd=10, relief=GROOVE,bg='#2a6287')
        user_title_fr.place(x=0, y=0)

        self.user_update_title = Label(user_change_fr, text="Enter the current Username and Password",bg='#2a6287',
                      fg="white",
                      font=("arial", 16, "bold"), padx=5, pady=5)
        self.user_update_title.place(x=35, y=11)

        lbl_user = Label(user_change_fr, text="Username:", fg=self.sm_bg_color,
                         font=("arial", 16, "bold")).place(
            x=35,
            y=100)
        ent_user = Entry(user_change_fr, font=("arial", 16), textvariable=self.Username).place(x=210, y=100)
        lbl_passwd = Label(user_change_fr, text="Password:", height="1", fg=self.sm_bg_color,
                           font=("arial", 16, "bold")).place(x=35, y=160)
        ent_passwd = Entry(user_change_fr, show='*', font=("arial", 16), textvariable=self.Password).place(x=210, y=160)

        check_for_user_btn = Button(user_change_fr, text="Verify Admin", width=10, bd=4, bg="#2a6287",
                                    fg="white", font="arial 16 bold", command=self.check_for_user_details).place(x=60,
                                                                                                                 y=230)

        self.change_passwd_btn = Button(user_change_fr, text="Update", width=10, bd=4, bg="#2a6287",
                                        fg="white", font="arial 16 bold", state=DISABLED,
                                        command=self.change_use_details)
        self.change_passwd_btn.place(x=300, y=230)

        ######################## manage_product_frame ########################

        title = Label(manage_product_frame, text="Manage Product", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        stock_details = Frame(manage_product_frame, width=600, height=550, bd=2, relief=GROOVE)
        stock_details.pack(side=LEFT, expand=1)

        search_item = Frame(stock_details, width=600, height=80, bd=2, relief=GROOVE)
        search_item.pack(side=TOP, expand=1)

        search_item_lbl = Label(search_item, text="Search By Product name", fg=self.sm_bg_color,
                                font=("arial", 10, "bold")).place(x=16, y=25)
        search_item_ent = Entry(search_item, font=("arial", 10), width="16", textvariable=self.search_pro_name).place(
            x=185, y=25)
        or_lbl = Label(search_item, text="OR", fg="green",
                       font=("arial", 10, "bold")).place(x=325, y=25)
        search_supp_lbl = Label(search_item, text="Suplier name", fg=self.sm_bg_color,
                                font=("arial", 10, "bold")).place(x=370, y=25)
        search_supp_ent = Entry(search_item, font=("arial", 10), width="16", textvariable=self.search_pro_supp).place(
            x=465, y=25)
        item_list = Frame(stock_details, width=600, height=470, bd=2, relief=GROOVE)
        item_list.pack(side=BOTTOM, expand=1)
        item_list.pack_propagate(False)

        item_scroll_y = Scrollbar(item_list, orient=VERTICAL)
        item_scroll_y.pack(side=RIGHT, fill=Y)
        item_scroll_x = Scrollbar(item_list, orient=HORIZONTAL)
        item_scroll_x.pack(side=BOTTOM, fill=X)

        self.item_list_trv = ttk.Treeview(item_list, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), show="headings",
                                          height="22", yscrollcommand=item_scroll_y.set,
                                          xscrollcommand=item_scroll_x.set)
        self.item_list_trv.pack()

        item_scroll_y.config(command=self.item_list_trv.yview)
        item_scroll_x.config(command=self.item_list_trv.xview)

        style = ttk.Style()
        style.configure("Treeview.Heading")
        # style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 8))

        self.item_list_trv["columns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.item_list_trv.column(1, width=40, anchor=CENTER)
        self.item_list_trv.column(2, width=120, anchor=CENTER)
        self.item_list_trv.column(3, width=100, anchor=CENTER)
        self.item_list_trv.column(4, width=80, anchor=CENTER)
        self.item_list_trv.column(5, width=120, anchor=CENTER)
        self.item_list_trv.column(6, width=120, anchor=CENTER)
        self.item_list_trv.column(7, width=120, anchor=CENTER)
        self.item_list_trv.column(8, width=120, anchor=CENTER)
        self.item_list_trv.column(9, width=100, anchor=CENTER)
        self.item_list_trv.column(10, width=100, anchor=CENTER)

        self.item_list_trv.heading(1, text="ID")
        self.item_list_trv.heading(2, text="Product name")
        self.item_list_trv.heading(3, text="Category")
        self.item_list_trv.heading(4, text="Quantity")
        self.item_list_trv.heading(5, text="Supplier name")
        self.item_list_trv.heading(6, text="Manufacture Date")
        self.item_list_trv.heading(7, text="Expiry Date")
        self.item_list_trv.heading(8, text="Entry Date")
        self.item_list_trv.heading(9, text="Buy Price")
        self.item_list_trv.heading(10, text="Sell Price")

        self.item_list_trv['show'] = 'headings'

        with connection.cursor() as cur:
            cur.execute("select * from add_product")
            rows = cur.fetchall()
            self.rows_pro_item(rows)

        self.item_list_trv.bind("<Double 1>", self.getrow_pro_item)
        self.search_pro_name.trace_variable("w", self.search_pro_by_name)
        self.search_pro_supp.trace_variable("w", self.search_pro_by_supp_name)

        product_details = Frame(manage_product_frame, width=300, height=550, bd=2, relief=GROOVE)
        product_details.pack(side=RIGHT, expand=1)

        pro_title_frame = Frame(product_details, width=300, height=80, bd=2, relief=GROOVE)
        pro_title_frame.pack(side=TOP, expand=1)

        search_item_lbl = Label(pro_title_frame, text="Product Details", fg=self.sm_bg_color,
                                font=("arial", 20, "bold"), padx="5", pady="5").place(x=35, y=16)

        pro_details_frame = Frame(product_details, width=300, height=470, bd=2, relief=GROOVE)
        pro_details_frame.pack(side=BOTTOM, expand=1)

        pro_name_lbl = Label(pro_details_frame, text="Product Name", fg=self.sm_bg_color,
                             font=("arial", 10, "bold")).place(x=10, y=10)
        pro_name_ent = Entry(pro_details_frame, font=("arial", 10), textvariable=self.mn_pro_name).place(x=130, y=10)
        category_lbl = Label(pro_details_frame, text="Category", fg=self.sm_bg_color,
                             font=("arial", 10, "bold")).place(x=10, y=50)
        category_ent = Entry(pro_details_frame, font=("arial", 10), textvariable=self.mn_category).place(x=130, y=50)
        quantity_lbl = Label(pro_details_frame, text="Quantity", fg=self.sm_bg_color,
                             font=("arial", 10, "bold")).place(x=10, y=90)
        quantity_ent = Entry(pro_details_frame, font=("arial", 10), textvariable=self.mn_quantity).place(x=130, y=90)
        supplier_lbl = Label(pro_details_frame, text="Supplier", fg=self.sm_bg_color,
                             font=("arial", 10, "bold")).place(x=10, y=130)
        supplier_ent = Entry(pro_details_frame, font=("arial", 10), textvariable=self.mn_supplier).place(x=130, y=130)
        manu_date_lbl = Label(pro_details_frame, text="Manufacture Date", fg=self.sm_bg_color,
                              font=("arial", 10, "bold")).place(x=10, y=170)
        manu_date_ent = DateEntry(pro_details_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", maxdate=self.today_date,
                                  textvariable=self.mn_manu_date).place(x=130, y=170)
        exp_date_lbl = Label(pro_details_frame, text="Expiry Date", fg=self.sm_bg_color,
                             font=("arial", 10, "bold")).place(x=10, y=210)
        exp_date_ent = DateEntry(pro_details_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", mindate=self.today_date,
                                 textvariable=self.mn_exp_date).place(x=130, y=210)
        buy_price_lbl = Label(pro_details_frame, text="Buying Price", fg=self.sm_bg_color,
                              font=("arial", 10, "bold")).place(x=10, y=250)
        buy_price_ent = Entry(pro_details_frame, font=("arial", 10), textvariable=self.mn_buy_price).place(x=130, y=250)
        sell_price_lbl = Label(pro_details_frame, text="Selling Price", fg=self.sm_bg_color,
                               font=("arial", 10, "bold")).place(x=10, y=290)
        sell_price_ent = Entry(pro_details_frame, font=("arial", 10), textvariable=self.mn_sell_price).place(x=130,
                                                                                                             y=290)

        update_pro_btn = Button(pro_details_frame, text="Update Item", command=self.update_product, width=10, bd=2,
                                bg=self.sm_bg_color, fg="white",
                                font="arial 12 bold").place(x=20, y=380)
        del_pro_btn = Button(pro_details_frame, text="Delete Item", command=self.del_product, width=10, bd=2,
                             bg=self.sm_bg_color, fg="white",
                             font="arial 12 bold").place(x=160, y=380)

        ######################## POS_sale_frame ########################

        title = Label(pos_sale_frame, text="POS Sale Frame", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        customer_information = Frame(pos_sale_frame, width=900, height=95, bd=2, relief=GROOVE)
        customer_information.pack(side=TOP, expand=1)

        cust_name_lbl = Label(customer_information, text="Customer Name", fg=self.sm_bg_color,
                              font=("arial", 10, "bold")).place(x=15, y=33)
        cust_name_ent = Entry(customer_information, font=("arial", 10), width="18", textvariable=self.customer).place(
            x=130, y=33)
        contact_lbl = Label(customer_information, text="Contact No.", fg=self.sm_bg_color,
                            font=("arial", 10, "bold")).place(x=350, y=33)
        contact_ent = Entry(customer_information, font=("arial", 10), width="16", textvariable=self.cust_contact).place(
            x=435, y=33)
        bill_no_lbl = Label(customer_information, text="Bill No.", fg=self.sm_bg_color,
                            font=("arial", 10, "bold")).place(x=670, y=33)
        bill_no_ent = Entry(customer_information, font=("arial", 10), width="18", textvariable=self.bill_no).place(
            x=740, y=33)

        new_sale = Frame(pos_sale_frame, width=400, height=470, bd=2, relief=GROOVE)
        new_sale.pack(side=LEFT, expand=1)

        search_sale_item = Frame(new_sale, width=400, height=60, bd=2, relief=GROOVE)
        search_sale_item.pack(side=TOP, expand=1)

        search_sale_item_lbl = Label(search_sale_item, text="Search Item by Name", fg=self.sm_bg_color,
                                     font=("arial", 11, "bold")).place(x=20, y=18)
        search_sale_item_ent = Entry(search_sale_item, font=("arial", 11), width="18",
                                     textvariable=self.search_sale_item).place(x=210, y=18)

        sale_item_details_fr = Frame(new_sale, width=400, height=300, bd=2, relief=GROOVE)
        sale_item_details_fr.pack(side=TOP, expand=1)

        search_item_details_fr = Frame(sale_item_details_fr, width=210, height=300, bd=2, relief=GROOVE)
        search_item_details_fr.pack(side=LEFT, expand=1)

        pos_item_name_lbl = Label(search_item_details_fr, text="Item Name:-", fg=self.sm_bg_color,
                                  font=("arial", 10, "bold")).place(x=10, y=20)
        pos_item_name_ent = Label(search_item_details_fr, text="", fg="dark green",
                                  font=("arial", 10, "bold"), textvariable=self.selected_item_lbl).place(x=110, y=20)
        pos_quantity_lbl = Label(search_item_details_fr, text="Avail Quantity:-", fg=self.sm_bg_color,
                                 font=("arial", 10, "bold")).place(x=10, y=80)
        pos_quantity_ent = Label(search_item_details_fr, text="", fg="dark green",
                                 font=("arial", 10, "bold"), textvariable=self.selected_quantity_lbl).place(x=110, y=80)
        pos_price_lbl = Label(search_item_details_fr, text="Price:-", fg=self.sm_bg_color,
                              font=("arial", 10, "bold")).place(x=10, y=140)
        pos_price_ent = Label(search_item_details_fr, text="", fg="dark green",
                              font=("arial", 10, "bold"), textvariable=self.selected_price_lbl).place(x=110, y=140)

        search_list_item_fr = Frame(sale_item_details_fr, width=186, height=300, bd=2, relief=GROOVE)
        search_list_item_fr.pack(side=RIGHT, expand=1)
        search_list_item_fr.pack_propagate(False)

        self.search_item_list_box = Listbox(search_list_item_fr)
        self.search_item_list_box.pack(expand=1, fill=BOTH)

        with connection.cursor() as cur:
            cur.execute("select product_name from add_product")
            rows = cur.fetchall()
            self.item_name_list(rows)

        self.search_sale_item.trace_variable("w", self.search_sale_item_by_name)
        self.search_item_list_box.bind('<<ListboxSelect>>', self.selected_list_item)

        add_to_cart_fr = Frame(new_sale, width=400, height=80, bd=2, relief=GROOVE)
        add_to_cart_fr.pack(side=TOP, expand=1)

        sale_quantity_lbl = Label(add_to_cart_fr, text="Quantity", fg=self.sm_bg_color,
                                  font=("arial", 11, "bold")).place(x=20, y=25)
        sale_quantiy_ent = Entry(add_to_cart_fr, font=("arial", 11), width="12",
                                 textvariable=self.select_quantity_to_sale).place(x=100, y=25)
        add_to_cart_btn = Button(add_to_cart_fr, text="Add to Cart", command=self.add_to_cart, width=10, bd=2,
                                 bg=self.sm_bg_color, fg="white",
                                 font="arial 12 bold").place(x=260, y=20)

        show_receipt = Frame(pos_sale_frame, width=500, height=470, bd=2, relief=GROOVE)
        show_receipt.pack(side=RIGHT, expand=1)

        bill_area_fr = Frame(show_receipt, width=500, height=340, bd=2, relief=GROOVE)
        bill_area_fr.pack(side=TOP, expand=1)
        bill_area_fr.pack_propagate(False)

        sale_item_scroll_y = Scrollbar(bill_area_fr, orient=VERTICAL)
        sale_item_scroll_y.pack(side=RIGHT, fill=Y)

        self.sale_item_trv = ttk.Treeview(bill_area_fr, columns=(1, 2, 3, 4), show="headings", height="10",
                                          yscrollcommand=sale_item_scroll_y.set)

        sale_item_scroll_y.config(command=self.sale_item_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))
        # style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 13))

        self.sale_item_trv["columns"] = (1, 2, 3, 4)
        self.sale_item_trv.column(1, width=170, anchor=CENTER)
        self.sale_item_trv.column(2, width=105, anchor=CENTER)
        self.sale_item_trv.column(3, width=105, anchor=CENTER)
        self.sale_item_trv.column(4, width=105, anchor=CENTER)

        self.sale_item_trv.heading(1, text="Product Name")
        self.sale_item_trv.heading(2, text="Quantity")
        self.sale_item_trv.heading(3, text="Unit Price")
        self.sale_item_trv.heading(4, text="Price")

        self.sale_item_trv['show'] = 'headings'

        self.sale_item_trv.pack(expand=1, fill=BOTH)

        amount_area = Frame(show_receipt, width=500, height=100, bd=2, relief=GROOVE)
        amount_area.pack(side=BOTTOM, expand=1)

        self.total_price_fr = Frame(amount_area, width=100, height=100, bd=2, relief=GROOVE)
        self.total_price_fr.pack(side=LEFT, expand=1)

        total_price_lb = Label(self.total_price_fr, text="Total Price. ", fg=self.sm_bg_color,
                               font=("arial", 11, "bold")).place(x=5, y=15)
        rs_lb = Label(self.total_price_fr, text="Rs. ", fg=self.sm_bg_color,
                      font=("arial", 11, "bold")).place(x=5, y=50)
        total_price_en = Label(self.total_price_fr, text="0.0", fg="dark green",
                               font=("arial", 11, "bold"), textvariable=self.total_price_sale).place(x=30, y=50)

        checkout_fr = Frame(amount_area, width=400, height=100, bd=2, relief=GROOVE)
        checkout_fr.pack(side=RIGHT, expand=1)

        paid_lbl = Label(checkout_fr, text="Paid", fg=self.sm_bg_color,
                         font=("arial", 11, "bold")).place(x=20, y=15)
        paid_ent = Entry(checkout_fr, font=("arial", 11), width="14", textvariable=self.paid_rs).place(x=90, y=15)
        return_lbl = Label(checkout_fr, text="Return", fg=self.sm_bg_color,
                           font=("arial", 11, "bold")).place(x=20, y=50)
        return_ent = Entry(checkout_fr, text="0.0", font=("arial", 11), width="14", textvariable=self.return_rs).place(
            x=90, y=50)
        checkout_btn = Button(checkout_fr, text="Generate Bill", command=self.validation_for_sale, width=10, bd=2,
                              bg=self.sm_bg_color, fg="white",
                              font="arial 12 bold").place(x=250, y=30)

        self.paid_rs.trace_variable("w", self.paid_to_return)

        ######################## manage_sale_frame ########################

        title = Label(manage_sale_frame, text="Manage Sales", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        search_sale = Frame(manage_sale_frame, width=900, height=80, bd=2, relief=GROOVE)
        search_sale.pack(side=TOP, expand=1)

        search_customer_lbl = Label(search_sale, text="Search By Customer name", fg=self.sm_bg_color,
                                    font=("arial", 10, "bold")).place(x=16, y=25)
        search_customer_ent = Entry(search_sale, font=("arial", 10), width="20",
                                    textvariable=self.search_mn_sale_item).place(x=220, y=25)
        del_sale_btn = Button(search_sale, text="Delete", command=self.del_sale_bill, width=10, bd=2,
                              bg=self.sm_bg_color, fg="white",
                              font="arial 12 bold").place(x=550, y=20)
        show_sale_btn = Button(search_sale, text="Show", command=self.show_sale_bill, width=10, bd=2,
                               bg=self.sm_bg_color, fg="white",
                               font="arial 12 bold").place(x=750, y=20)

        sale_list = Frame(manage_sale_frame, width=900, height=470, bd=2, relief=GROOVE)
        sale_list.pack(side=TOP, expand=1)
        sale_list.pack_propagate(False)

        sale_list_scroll_y = Scrollbar(sale_list, orient=VERTICAL)
        sale_list_scroll_y.pack(side=RIGHT, fill=Y)

        self.mn_sale_trv = ttk.Treeview(sale_list, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height="22",
                                        yscrollcommand=sale_list_scroll_y.set)
        self.mn_sale_trv.pack()

        sale_list_scroll_y.config(command=self.mn_sale_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))

        self.mn_sale_trv["columns"] = (1, 2, 3, 4, 5, 6, 7, 8)
        self.mn_sale_trv.column(1, width=60, anchor=CENTER)
        self.mn_sale_trv.column(2, width=155, anchor=CENTER)
        self.mn_sale_trv.column(3, width=135, anchor=CENTER)
        self.mn_sale_trv.column(4, width=110, anchor=CENTER)
        self.mn_sale_trv.column(5, width=103, anchor=CENTER)
        self.mn_sale_trv.column(6, width=110, anchor=CENTER)
        self.mn_sale_trv.column(7, width=110, anchor=CENTER)
        self.mn_sale_trv.column(8, width=110, anchor=CENTER)

        self.mn_sale_trv.heading(1, text="ID")
        self.mn_sale_trv.heading(2, text="Customer name")
        self.mn_sale_trv.heading(3, text="Contact No")
        self.mn_sale_trv.heading(4, text="Entry Date")
        self.mn_sale_trv.heading(5, text="Bill No")
        self.mn_sale_trv.heading(6, text="Total Price")
        self.mn_sale_trv.heading(7, text="Paid Rs.")
        self.mn_sale_trv.heading(8, text="Return Rs.")

        self.mn_sale_trv['show'] = 'headings'
        # self.mn_sale_trv.bind("<Double 1>",self.get)

        with connection.cursor() as cur:
            cur.execute("select * from add_new_sale")
            rows = cur.fetchall()
            self.rows_sale_item(rows)

        self.search_mn_sale_item.trace_variable("w", self.search_mn_sale_item_by_name)

        ######################## add_supplier_frame ########################

        title = Label(add_supplier_frame, text="Add New Supplier", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        new_supplier = Frame(add_supplier_frame, width=900, height=170, bd=2, relief=GROOVE)
        new_supplier.pack(side=TOP, expand=1)

        supplier_name_lbl = Label(new_supplier, text="Supplier Name", fg=self.sm_bg_color,
                                  font=("arial", 12, "bold")).place(x=50, y=30)
        supplier_name_ent = Entry(new_supplier, font=("arial", 12), width="20", textvariable=self.supplier_name).place(
            x=210, y=30)
        contact_lbl = Label(new_supplier, text="Contact No.", fg=self.sm_bg_color,
                            font=("arial", 12, "bold")).place(x=520, y=30)
        contact_ent = Entry(new_supplier, font=("arial", 12), width="20", textvariable=self.contact_no).place(x=650,
                                                                                                              y=30)
        save_btn = Button(new_supplier, text="Save", command=self.validation_for_add_supp, width=10, bd=2,
                          bg=self.sm_bg_color, fg="white",
                          font="arial 14 bold").place(x=190, y=100)
        update_btn = Button(new_supplier, text="Update", command=self.update_supplier, width=10, bd=2,
                            bg=self.sm_bg_color, fg="white",
                            font="arial 14 bold").place(x=390, y=100)
        delete_btn = Button(new_supplier, text="Delete", command=self.del_supplier, width=10, bd=2,
                            bg=self.sm_bg_color, fg="white",
                            font="arial 14 bold").place(x=590, y=100)

        manage_supplier = Frame(add_supplier_frame, width=900, height=380, bd=2, relief=GROOVE)
        manage_supplier.pack(side=BOTTOM, expand=1)

        search_supplier = Frame(manage_supplier, width=900, height=80, bd=2, relief=GROOVE)
        search_supplier.pack(side=TOP, expand=1)

        search_supplier_lbl = Label(search_supplier, text="Search Supplier By Name", fg=self.sm_bg_color,
                                    font=("arial", 12, "bold")).place(x=30, y=25)
        search_supplier_ent = Entry(search_supplier, font=("arial", 12), width="20",
                                    textvariable=self.search_supp_name).place(x=240, y=25)
        edit_btn = Button(search_supplier, text="Edit", command=self.getrow_supplier, width=10, bd=2,
                          bg=self.sm_bg_color, fg="white",
                          font="arial 14 bold").place(x=660, y=20)

        supplier_details = Frame(manage_supplier, width=900, height=300, bd=2, relief=GROOVE)
        supplier_details.pack(side=BOTTOM, expand=1)
        supplier_details.pack_propagate(False)

        sup_list_scroll_y = Scrollbar(supplier_details, orient=VERTICAL)
        sup_list_scroll_y.pack(side=RIGHT, fill=Y)

        self.supplier_trv = ttk.Treeview(supplier_details, columns=(1, 2, 3), show="headings", height="14",
                                         yscrollcommand=sup_list_scroll_y.set)

        sup_list_scroll_y.config(command=self.supplier_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))
        # style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 10))

        self.supplier_trv["columns"] = (1, 2, 3)
        self.supplier_trv.column(1, width=296, anchor=CENTER)
        self.supplier_trv.column(2, width=296, anchor=CENTER)
        self.supplier_trv.column(3, width=295, anchor=CENTER)

        self.supplier_trv.heading(1, text="Supplier ID")
        self.supplier_trv.heading(2, text="Supplier name")
        self.supplier_trv.heading(3, text="Contact No")

        self.supplier_trv['show'] = 'headings'

        self.supplier_trv.pack()

        with connection.cursor() as cur:
            cur.execute("select id,supplier_name,contact_no from add_supplier")
            rows = cur.fetchall()
            self.rows_supp_trv(rows)

        # self.supplier_trv.bind("<Double-1>", getrow_supplier)

        self.search_supp_name.trace_variable("w", self.search_supp_by_name)

        ######################### add_purchase_frame ########################

        title = Label(add_purchase_frame, text="Add New Purchase", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        supplier = Frame(add_purchase_frame, width=900, height=80, bd=2, relief=GROOVE)
        supplier.pack(side=TOP, expand=1)

        supplier_name_lbl = Label(supplier, text="Supplier Name", fg=self.sm_bg_color,
                                  font=("arial", 12, "bold")).place(x=20, y=25)
        supplier_name_ent = Entry(supplier, font=("arial", 12), width="20", textvariable=self.pur_supplier).place(x=150,
                                                                                                                  y=25)
        pur_bill_no_lbl = Label(supplier, text="Bill No.", fg=self.sm_bg_color,
                                font=("arial", 12, "bold")).place(x=620, y=25)
        pur_bill_no_ent = Entry(supplier, font=("arial", 12), width="16", textvariable=self.pur_bill_no).place(
            x=700, y=25)

        purchase_items = Frame(add_purchase_frame, width=400, height=470, bd=2, relief=GROOVE)
        purchase_items.pack(side=LEFT, expand=1)

        category_lbl = Label(purchase_items, text="Category", fg=self.sm_bg_color,
                             font=("arial", 11, "bold")).place(x=30, y=30)
        category_ent = Entry(purchase_items, font=("arial", 11), textvariable=self.pur_category).place(x=190, y=30)
        product_lbl = Label(purchase_items, text="Product Name", fg=self.sm_bg_color,
                            font=("arial", 11, "bold")).place(x=30, y=75)
        product_ent = Entry(purchase_items, font=("arial", 11), textvariable=self.pur_pro_name).place(x=190, y=75)
        manu_date_lbl = Label(purchase_items, text="Manufacture Date", fg=self.sm_bg_color,
                              font=("arial", 11, "bold")).place(x=30, y=120)
        manu_date_ent = DateEntry(purchase_items, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", maxdate=self.today_date,
                                  textvariable=self.pur_manu_date).place(x=190, y=120)
        expiry_date_lbl = Label(purchase_items, text="Expiry Date", fg=self.sm_bg_color,
                                font=("arial", 11, "bold")).place(x=30, y=165)
        expiry_date_ent = DateEntry(purchase_items, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", mindate=self.today_date,
                                    textvariable=self.pur_exp_date).place(x=190, y=165)
        quantity_lbl = Label(purchase_items, text="Quantity", fg=self.sm_bg_color,
                             font=("arial", 11, "bold")).place(x=30, y=210)
        quantity_ent = Entry(purchase_items, font=("arial", 11), textvariable=self.pur_quantity).place(x=190, y=210)
        purchase_unit_price_lbl = Label(purchase_items, text="Purchase Unit Price", fg=self.sm_bg_color,
                                        font=("arial", 11, "bold")).place(x=30, y=255)
        purchase_unit_price_ent = Entry(purchase_items, font=("arial", 11), textvariable=self.purch_unit_price).place(
            x=190, y=255)
        sell_unit_price_lbl = Label(purchase_items, text="sell Unit Price", fg=self.sm_bg_color,
                                    font=("arial", 11, "bold")).place(x=30, y=300)
        sell_unit_price_ent = Entry(purchase_items, font=("arial", 11), textvariable=self.sell_unit_price).place(x=190,
                                                                                                                 y=300)

        add_to_cart_btn = Button(purchase_items, text="Add to Cart", command=self.pur_add_to_cart, width=10, bd=2,
                                 bg=self.sm_bg_color, fg="white",
                                 font="arial 16 bold").place(x=200, y=370)

        purchase_receipt = Frame(add_purchase_frame, width=500, height=470, bd=2, relief=GROOVE)
        purchase_receipt.pack(side=RIGHT, expand=1)

        pur_bill_area = Frame(purchase_receipt, width=500, height=370, bd=2, relief=GROOVE)
        pur_bill_area.pack(side=TOP, expand=1)
        pur_bill_area.pack_propagate(False)

        pur_item_scroll_y = Scrollbar(pur_bill_area, orient=VERTICAL)
        pur_item_scroll_y.pack(side=RIGHT, fill=Y)
        pur_item_scroll_x = Scrollbar(pur_bill_area, orient=HORIZONTAL)
        pur_item_scroll_x.pack(side=BOTTOM, fill=X)

        self.pur_item_trv = ttk.Treeview(pur_bill_area, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height="10",
                                         yscrollcommand=pur_item_scroll_y.set, xscrollcommand=pur_item_scroll_x.set)
        pur_item_scroll_y.config(command=self.pur_item_trv.yview)
        pur_item_scroll_x.config(command=self.pur_item_trv.xview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))
        # style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 13))

        self.pur_item_trv["columns"] = (1, 2, 3, 4, 5, 6, 7)
        self.pur_item_trv.column(1, width=100, anchor=CENTER)
        self.pur_item_trv.column(2, width=120, anchor=CENTER)
        self.pur_item_trv.column(3, width=100, anchor=CENTER)
        self.pur_item_trv.column(4, width=120, anchor=CENTER)
        self.pur_item_trv.column(5, width=120, anchor=CENTER)
        self.pur_item_trv.column(6, width=120, anchor=CENTER)
        self.pur_item_trv.column(7, width=120, anchor=CENTER)

        self.pur_item_trv.heading(1, text="Category")
        self.pur_item_trv.heading(2, text="Product_Name")
        self.pur_item_trv.heading(3, text="Quantity")
        self.pur_item_trv.heading(4, text="Manufacture Date")
        self.pur_item_trv.heading(5, text="Expiry Date")
        self.pur_item_trv.heading(6, text="Pur Unit Price")
        self.pur_item_trv.heading(7, text="Sell Unit Price")

        self.pur_item_trv['show'] = 'headings'

        self.pur_item_trv.pack(expand=1, fill=BOTH)

        amount_area = Frame(purchase_receipt, width=500, height=100, bd=2, relief=GROOVE)
        amount_area.pack(side=BOTTOM, expand=1)

        pur_total_lbl = Label(amount_area, text="Total", fg=self.sm_bg_color,
                              font=("arial", 12, "bold")).place(x=30, y=30)
        pur_total_rs = Label(amount_area, text="Rs. ", fg=self.sm_bg_color,
                             font=("arial", 12, "bold")).place(x=90, y=30)
        pur_total_ent = Label(amount_area, font=("arial", 12, "bold"), textvariable=self.pur_total_price).place(x=115,
                                                                                                                y=30)

        checkout_btn = Button(amount_area, text="Checkout", command=self.validation_for_purchase, width=10, bd=2,
                              bg=self.sm_bg_color, fg="white",
                              font="arial 16 bold").place(x=320, y=17)

        ######################### manage_purchase_frame ########################

        title = Label(manage_purchase_frame, text="Manage Purchase", bd=2, relief=GROOVE, bg=self.sm_bg_color,
                      fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        search_purchase = Frame(manage_purchase_frame, width=900, height=80, bd=2, relief=GROOVE)
        search_purchase.pack(side=TOP, expand=1)

        search_supplier_lbl = Label(search_purchase, text="Search By Supplier name", fg=self.sm_bg_color,
                                    font=("arial", 10, "bold")).place(x=16, y=25)
        search_supplier_ent = Entry(search_purchase, font=("arial", 10), width="20",
                                    textvariable=self.search_mn_pur_supp).place(x=220, y=25)
        del_pur_btn = Button(search_purchase, text="Delete", command=self.del_purchase_items, width=10, bd=2,
                             bg=self.sm_bg_color, fg="white",
                             font="arial 12 bold").place(x=550, y=20)
        show_pur_btn = Button(search_purchase, text="Show", command=self.show_purchase_items, width=10, bd=2,
                              bg=self.sm_bg_color, fg="white",
                              font="arial 12 bold").place(x=750, y=20)

        purchase_list = Frame(manage_purchase_frame, width=900, height=222, bd=2, relief=GROOVE)
        purchase_list.pack(side=TOP, expand=1)
        purchase_list.pack_propagate(False)

        pur_list_scroll_y = Scrollbar(purchase_list, orient=VERTICAL)
        pur_list_scroll_y.pack(side=RIGHT, fill=Y)

        self.pur_list_trv = ttk.Treeview(purchase_list, columns=(1, 2, 3, 4, 5), show="headings", height="10",
                                         yscrollcommand=pur_list_scroll_y.set)
        self.pur_list_trv.pack(expand=1, fill=BOTH)

        pur_list_scroll_y.config(command=self.pur_list_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))
        self.pur_list_trv["columns"] = (1, 2, 3, 4, 5)
        self.pur_list_trv.column(1, width=100, anchor=CENTER)
        self.pur_list_trv.column(2, width=200, anchor=CENTER)
        self.pur_list_trv.column(3, width=200, anchor=CENTER)
        self.pur_list_trv.column(4, width=200, anchor=CENTER)
        self.pur_list_trv.column(5, width=200, anchor=CENTER)

        self.pur_list_trv.heading(1, text="ID")
        self.pur_list_trv.heading(2, text="Supplier Name")
        self.pur_list_trv.heading(3, text="Entry Date")
        self.pur_list_trv.heading(4, text="Bill No")
        self.pur_list_trv.heading(5, text="Total Price")

        self.pur_list_trv['show'] = 'headings'

        with connection.cursor() as cur:
            cur.execute("select * from add_purchase")
            rows = cur.fetchall()
            self.rows_pur_list(rows)

        self.search_mn_pur_supp.trace_variable("w", self.search_mn_purchase_by_name)

        purchase_item_list = Frame(manage_purchase_frame, width=900, height=235, bd=2, relief=GROOVE)
        purchase_item_list.pack(side=BOTTOM, expand=1)
        purchase_item_list.pack_propagate(False)

        pur_item_list_scroll_y = Scrollbar(purchase_item_list, orient=VERTICAL)
        pur_item_list_scroll_y.pack(side=RIGHT, fill=Y)

        self.pur_item_list_trv = ttk.Treeview(purchase_item_list, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings",
                                              height="10",
                                              yscrollcommand=pur_item_list_scroll_y.set)
        self.pur_item_list_trv.pack(expand=1, fill=BOTH)

        pur_item_list_scroll_y.config(command=self.pur_item_list_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))
        self.pur_item_list_trv["columns"] = (1, 2, 3, 4, 5, 6, 7, 8)
        self.pur_item_list_trv.column(1, width=40, anchor=CENTER)
        self.pur_item_list_trv.column(2, width=120, anchor=CENTER)
        self.pur_item_list_trv.column(3, width=120, anchor=CENTER)
        self.pur_item_list_trv.column(4, width=60, anchor=CENTER)
        self.pur_item_list_trv.column(5, width=120, anchor=CENTER)
        self.pur_item_list_trv.column(6, width=120, anchor=CENTER)
        self.pur_item_list_trv.column(7, width=120, anchor=CENTER)
        self.pur_item_list_trv.column(8, width=120, anchor=CENTER)

        self.pur_item_list_trv.heading(1, text="ID")
        self.pur_item_list_trv.heading(2, text="Product Name")
        self.pur_item_list_trv.heading(3, text="Category")
        self.pur_item_list_trv.heading(4, text="Quantity")
        self.pur_item_list_trv.heading(5, text="Manufacture Date")
        self.pur_item_list_trv.heading(6, text="Expiry Date")
        self.pur_item_list_trv.heading(7, text="Pur Unit Price")
        self.pur_item_list_trv.heading(8, text="Sell Unit price")

        self.pur_item_list_trv['show'] = 'headings'

        ######################### out_of_stock_frame ########################.

        title = Label(out_of_stock_frame, text="Out of Stock", bd=2, relief=GROOVE, bg=self.sm_bg_color, fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        out_lbl_fr = Frame(out_of_stock_frame, width=900, height=80, bd=2, relief=GROOVE)
        out_lbl_fr.pack(side=TOP, expand=1)

        title_lbl = Label(out_lbl_fr, text="The following items are low in Stock", fg="red",
                          font=("arial", 16, "bold")).place(x=250, y=25)

        out_list_fr = Frame(out_of_stock_frame, width=900, height=470, bd=2, relief=GROOVE)
        out_list_fr.pack(side=TOP, expand=1)
        out_list_fr.pack_propagate(False)

        out_of_stock_scroll_y = Scrollbar(out_list_fr, orient=VERTICAL)
        out_of_stock_scroll_y.pack(side=RIGHT, fill=Y)

        self.out_of_stock_trv = ttk.Treeview(out_list_fr, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), show="headings",
                                             height="22", yscrollcommand=out_of_stock_scroll_y.set)
        self.out_of_stock_trv.pack()

        out_of_stock_scroll_y.config(command=self.out_of_stock_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading")
        # style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 8))

        self.out_of_stock_trv["columns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.out_of_stock_trv.column(1, width=40, anchor=CENTER)
        self.out_of_stock_trv.column(2, width=120, anchor=CENTER)
        self.out_of_stock_trv.column(3, width=80, anchor=CENTER)
        self.out_of_stock_trv.column(4, width=70, anchor=CENTER)
        self.out_of_stock_trv.column(5, width=120, anchor=CENTER)
        self.out_of_stock_trv.column(6, width=115, anchor=CENTER)
        self.out_of_stock_trv.column(7, width=85, anchor=CENTER)
        self.out_of_stock_trv.column(8, width=85, anchor=CENTER)
        self.out_of_stock_trv.column(9, width=80, anchor=CENTER)
        self.out_of_stock_trv.column(10, width=80, anchor=CENTER)

        self.out_of_stock_trv.heading(1, text="ID")
        self.out_of_stock_trv.heading(2, text="Product name")
        self.out_of_stock_trv.heading(3, text="Category")
        self.out_of_stock_trv.heading(4, text="Quantity")
        self.out_of_stock_trv.heading(5, text="Supplier name")
        self.out_of_stock_trv.heading(6, text="Manufacture Date")
        self.out_of_stock_trv.heading(7, text="Expiry Date")
        self.out_of_stock_trv.heading(8, text="Entry Date")
        self.out_of_stock_trv.heading(9, text="Buy Price")
        self.out_of_stock_trv.heading(10, text="Sell Price")

        self.out_of_stock_trv['show'] = 'headings'

        with connection.cursor() as cur:
            cur.execute("select * from add_product where quantity<=5")
            rows = cur.fetchall()
            self.rows_out_of_stocks_item(rows)

        ######################### expired_product_frame ########################

        title = Label(expired_product_frame, text="Expired Products", bd=2, relief=GROOVE, bg=self.sm_bg_color,
                      fg="white",
                      font=("arial", 12, "bold"), pady=8).pack(fill=X)

        expire_lbl_fr = Frame(expired_product_frame, width=900, height=80, bd=2, relief=GROOVE)
        expire_lbl_fr.pack(side=TOP, expand=1)

        title_lbl = Label(expire_lbl_fr, text="The following items are Expired", fg="red",
                          font=("arial", 16, "bold")).place(x=270, y=25)

        expired_list_fr = Frame(expired_product_frame, width=900, height=470, bd=2, relief=GROOVE)
        expired_list_fr.pack(side=TOP, expand=1)
        expired_list_fr.pack_propagate(False)

        expired_scroll_y = Scrollbar(expired_list_fr, orient=VERTICAL)
        expired_scroll_y.pack(side=RIGHT, fill=Y)

        self.expired_pro_trv = ttk.Treeview(expired_list_fr, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), show="headings",
                                            height="22", yscrollcommand=expired_scroll_y.set)
        self.expired_pro_trv.pack()

        expired_scroll_y.config(command=self.expired_pro_trv.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading")
        # style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 8))

        self.expired_pro_trv["columns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.expired_pro_trv.column(1, width=40, anchor=CENTER)
        self.expired_pro_trv.column(2, width=120, anchor=CENTER)
        self.expired_pro_trv.column(3, width=80, anchor=CENTER)
        self.expired_pro_trv.column(4, width=70, anchor=CENTER)
        self.expired_pro_trv.column(5, width=120, anchor=CENTER)
        self.expired_pro_trv.column(6, width=115, anchor=CENTER)
        self.expired_pro_trv.column(7, width=85, anchor=CENTER)
        self.expired_pro_trv.column(8, width=85, anchor=CENTER)
        self.expired_pro_trv.column(9, width=80, anchor=CENTER)
        self.expired_pro_trv.column(10, width=80, anchor=CENTER)

        self.expired_pro_trv.heading(1, text="ID")
        self.expired_pro_trv.heading(2, text="Product name")
        self.expired_pro_trv.heading(3, text="Category")
        self.expired_pro_trv.heading(4, text="Quantity")
        self.expired_pro_trv.heading(5, text="Supplier name")
        self.expired_pro_trv.heading(6, text="Manufacture Date")
        self.expired_pro_trv.heading(7, text="Expiry Date")
        self.expired_pro_trv.heading(8, text="Entry Date")
        self.expired_pro_trv.heading(9, text="Buy Price")
        self.expired_pro_trv.heading(10, text="Sell Price")

        self.expired_pro_trv['show'] = 'headings'

        with connection.cursor() as cur:
            query = "select * from add_product where expiry_date < now()"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_expired_pro_items(rows)

    ######################## Functions of Operation ######################

    def formating(self, date):
        date_str = date
        format_str = '%d/%m/%Y'
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        return datetime_obj.date().isoformat()

    def change_date_format(self, dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3/\\2/\\1', dt)

    def clear_widget_for_add_pro(self):
        self.add_pro_name.set("")
        self.add_quantity.set("")
        self.add_category.set("")
        self.add_buy_price.set("")
        self.add_sell_price.set("")
        self.add_supplier.set("")
        self.add_manu_date.set(self.change_date_format(str(self.today_date)))
        self.add_exp_date.set(self.change_date_format(str(self.today_date)))

    def clear_widget_for_mn_pro(self):
        self.mn_quantity.set("")
        self.mn_pro_name.set("")
        self.mn_exp_date.set(self.change_date_format(str(self.today_date)))
        self.mn_category.set("")
        self.mn_buy_price.set("")
        self.mn_supplier.set("")
        self.mn_sell_price.set("")
        self.mn_manu_date.set(self.change_date_format(str(self.today_date)))

    def clear_widget_for_new_pur(self):
        self.pur_item_trv.delete(*self.pur_item_trv.get_children())
        self.pur_supplier.set("")
        self.pur_pro_name.set("")
        self.pur_quantity.set("")
        self.pur_category.set("")
        self.purch_unit_price.set("")
        self.pur_manu_date.set(self.change_date_format(str(self.today_date)))
        self.pur_exp_date.set(self.change_date_format(str(self.today_date)))
        self.sell_unit_price.set("")
        self.pur_total_price.set("")
        y = random.randint(1000, 9999)
        self.pur_bill_no.set(str(y))

    def clear_widget_for_pos_sale(self):
        self.sale_item_trv.delete(*self.sale_item_trv.get_children())
        x = random.randint(1000, 9999)
        self.bill_no.set(str(x))
        self.customer.set("")
        self.cust_contact.set("")
        self.total_price_sale.set("0.0")
        self.paid_rs.set("")
        self.return_rs.set("0.0")

    def clear_widget_for_supp(self):
        self.supplier_name.set("")
        self.contact_no.set("")

    def check_for_user_details(self):
        user = (self.Username.get())
        passwd = (self.Password.get())

        with connection.cursor() as cur:
            cur.execute("select * from admin")
            rows = cur.fetchall()

        user_name=rows[0][1]
        user_passwd=rows[0][2]

        if (user == "" or passwd == ""):
            messagebox.showinfo("Login System", "Fill the Login Details")
        elif (user == user_name and passwd == user_passwd):
            self.user_update_title.config(text="Enter the new Username and Password")
            self.change_passwd_btn.config(state=NORMAL)
        else:
            messagebox.showerror("Login System", "Invalid Login Details")
            self.Username.set("")
            self.Password.set("")

    def change_use_details(self):
        user = (self.Username.get())
        passwd = (self.Password.get())
        if (user == "" or passwd == ""):
            messagebox.showinfo("Login System", "Fill the Login Details")
        elif len(passwd)>8:
            messagebox.showinfo("Login System", "Password must be a maximum of 8 digits")
        else:
            # Create Cursor
            with connection.cursor() as cur:
                cur.execute(
                    "update admin set name=%s,password=%s where id=1",
                    (user, passwd))

                # Commit cursor
                connection.commit()
                # Close Connection
                # connection.close()
                messagebox.showinfo("Info", "Successfully updated")
            self.user_update_title.config(text="Enter the current Username and Password")
            self.change_passwd_btn.config(state=DISABLED)
            self.Username.set("")
            self.Password.set("")

    ####################### Add_Supplier_Frame_Function #####################

    def validation_for_add_supp(self):
        supplier_name = str(self.supplier_name.get())
        contact_no = str(self.contact_no.get())
        if supplier_name == "" or contact_no == "":
            messagebox.showerror("Error", "Fill all the details")
        elif contact_no.isdigit():
            if len(contact_no) != 10:
                messagebox.showerror("Error", "Contact no. must be of 10 Digit")
            else:
                self.add_new_supplier()
        else:
            messagebox.showerror("Error", "Character is not allowed")

    def add_new_supplier(self):
        supplier_name = str(self.supplier_name.get())
        contact_no = str(self.contact_no.get())

        # Create Cursor
        with connection.cursor() as cur:
            cur.execute(
                "INSERT INTO add_supplier(supplier_name, contact_no)"
                " VALUES(%s, %s)",
                (supplier_name, contact_no))

            # Commit cursor
            connection.commit()
            # Close Connection
            # connection.close()
            self.update_supp_trv()
            self.clear_widget_for_supp()

    def rows_supp_trv(self, rows):
        self.supplier_trv.delete(*self.supplier_trv.get_children())
        for i in rows:
            self.supplier_trv.insert('', 'end', values=i)

    def getrow_supplier(self):
        items = self.supplier_trv.item(self.supplier_trv.focus())
        if (items['values']) == "":
            messagebox.showerror("Error", "Select the supplier from below")
        else:
            self.supplier_name.set(items['values'][1])
            self.contact_no.set(items['values'][2])

    def update_supp_trv(self):
        with connection.cursor() as cur:
            query = "select id,supplier_name,contact_no from add_supplier"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_supp_trv(rows)

    def search_supp_by_name(self, *args):
        pattern = self.search_supp_name.get()
        with connection.cursor() as cur:
            if len(pattern) > 0:
                query = "select id,supplier_name,contact_no from add_supplier where supplier_name REGEXP '^" + pattern + "'"
                cur.execute(query)
                rows = cur.fetchall()
                self.rows_supp_trv(rows)
            else:
                self.update_supp_trv()

    def update_supplier(self):
        supplier_name = str(self.supplier_name.get())
        contact_no = str(self.contact_no.get())
        if supplier_name == "" or contact_no == "":
            messagebox.showerror("Error", "Select the Supplier")
        elif contact_no.isdigit():
            if len(contact_no) != 10:
                messagebox.showerror("Error", "Contact no. must be of 10 Digit")
            else:
                items = self.supplier_trv.item(self.supplier_trv.focus())
                fix_supp_name = (items['values'][1])
                if supplier_name == fix_supp_name:
                    if messagebox.askyesno("Supplier Update", "Are you sure, you want to update this Supplier"):
                        # Create Cursor
                        with connection.cursor() as cur:
                            cur.execute(
                                "update add_supplier set contact_no=%s where supplier_name=%s",
                                (contact_no, supplier_name))

                            # Commit cursor
                            connection.commit()
                            self.update_supp_trv()
                            self.clear_widget_for_supp()
                            # Close Connection
                            # connection.close()
                    else:
                        return True
                else:
                    messagebox.showerror("Error", "First you have to add the new Supplier")
        else:
            messagebox.showerror("Error", "Character is not allowed")

    def del_supplier(self):
        supplier_name = str(self.supplier_name.get())
        if supplier_name == "":
            messagebox.showerror("Error", "Select the Supplier")
        else:
            items = self.supplier_trv.item(self.supplier_trv.focus())
            fix_supp_name = (items['values'][1])
            if supplier_name == fix_supp_name:
                if messagebox.askyesno("Confirm Delete", "Are you sure, you want to delete this supplier"):
                    # Create Cursor
                    with connection.cursor() as cur:
                        cur.execute(
                            "delete from add_supplier where supplier_name=%s",
                            (supplier_name))
                        # Commit cursor
                        connection.commit()
                        self.update_supp_trv()
                        self.clear_widget_for_supp()

                        # Close Connection
                        # connection.close()
                else:
                    return True
            else:
                messagebox.showerror("Error", "This Supplier is not in the database")

    #######################################################################

    ####################### Add_Product_Frame_Functions #####################

    def add_new_product(self):
        pro_name = str(self.add_pro_name.get())
        category = str(self.add_category.get())
        quantity = str(self.add_quantity.get())
        supplier = str(self.add_supplier.get())
        manu_date = self.formating(str(self.add_manu_date.get()))
        exp_date = self.formating(str(self.add_exp_date.get()))
        buy_price = str(self.add_buy_price.get())
        sell_price = str(self.add_sell_price.get())

        if pro_name == "" or category == "" or quantity == "" or supplier == "" or buy_price == "" or sell_price == "":
            messagebox.showerror("Error", "Fill all the details")
        else:
            with connection.cursor() as cur:
                query = "select id from add_supplier where supplier_name=%s"
                val = cur.execute(query, (supplier))
            if (val == 1):
                # Create Cursor
                with connection.cursor() as cur:
                    cur.execute(
                        "INSERT INTO add_product(product_name, category, quantity, supplier_name, manufacture_date,expiry_date,entry_date,buying_price,sell_price)"
                        " VALUES(%s, %s, %s, %s,%s,%s, %s, %s, %s)",
                        (pro_name, category, quantity, supplier, manu_date, exp_date, self.today_date, buy_price,
                         sell_price))

                    # Commit cursor
                    connection.commit()
                    messagebox.showinfo("Info", "Successfully added")
                    # Close Connection
                    self.update_pro_trv()
                    self.update_out_of_stock_trv()
                    self.update_expired_pro_trv()
                    self.update_item_name_list()
                    self.clear_widget_for_add_pro()
            else:
                messagebox.showinfo("Error", "First you have to add the new supplier")

    #######################################################################

    ####################### Manage_Product_Frame_Functions #####################

    def rows_pro_item(self, rows):
        self.item_list_trv.delete(*self.item_list_trv.get_children())
        for i in rows:
            self.item_list_trv.insert('', 'end', values=i)

    def getrow_pro_item(self, event):
        items = self.item_list_trv.item(self.item_list_trv.focus())
        self.mn_pro_id.set(items['values'][0])
        self.mn_pro_name.set(items['values'][1])
        self.mn_category.set(items['values'][2])
        self.mn_quantity.set(items['values'][3])
        self.mn_supplier.set(items['values'][4])
        self.mn_manu_date.set(self.change_date_format(items['values'][5]))
        self.mn_exp_date.set(self.change_date_format(items['values'][6]))
        self.mn_buy_price.set(items['values'][8])
        self.mn_sell_price.set(items['values'][9])

    def update_pro_trv(self):
        with connection.cursor() as cur:
            query = "select * from add_product"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_pro_item(rows)

    def search_pro_by_name(self, *args):
        pattern = self.search_pro_name.get()
        with connection.cursor() as cur:
            if len(pattern) > 0:
                query = "select * from add_product where product_name REGEXP '^" + pattern + "'"
                cur.execute(query)
                rows = cur.fetchall()
                self.rows_pro_item(rows)
            else:
                self.update_pro_trv()

    def search_pro_by_supp_name(self, *args):
        pattern = self.search_pro_supp.get()
        with connection.cursor() as cur:
            if len(pattern) > 0:
                query = "select * from add_product where supplier_name REGEXP '^" + pattern + "'"
                cur.execute(query)
                rows = cur.fetchall()
                self.rows_pro_item(rows)
            else:
                self.update_pro_trv()

    def update_product(self):
        pro_id = str(self.mn_pro_id.get())
        pro_name = str(self.mn_pro_name.get())
        category = str(self.mn_category.get())
        quantity = str(self.mn_quantity.get())
        supplier = str(self.mn_supplier.get())
        manu_date = self.formating(str(self.mn_manu_date.get()))
        exp_date = self.formating(str(self.mn_exp_date.get()))
        buy_price = str(self.mn_buy_price.get())
        sell_price = str(self.mn_sell_price.get())

        if pro_name == "" or category == "" or quantity == "" or supplier == "" or buy_price == "" or sell_price == "":
            messagebox.showerror("Error", "Select the item and Fill all the details")
        elif messagebox.askyesno("Product Update", "Are you sure, you want to update this Product"):
            # Create Cursor
            with connection.cursor() as cur:
                cur.execute(
                    "update add_product set product_name=%s, category=%s, quantity=%s, supplier_name=%s, manufacture_date=%s,expiry_date=%s"
                    ",buying_price=%s,sell_price=%s where id=%s",
                    (pro_name, category, quantity, supplier, manu_date, exp_date, buy_price, sell_price, pro_id))

                # Commit cursor
                connection.commit()
                self.update_pro_trv()
                self.update_out_of_stock_trv()
                self.update_expired_pro_trv()
                self.update_item_name_list()
                self.clear_widget_for_mn_pro()
                # Close Connection
                # connection.close()
        else:
            return True

    def del_product(self):
        pro_name = str(self.mn_pro_name.get())
        if pro_name == "":
            messagebox.showerror("Error", "Select the Item")
        elif messagebox.askyesno("Confirm Delete", "Are you sure, you want to delete this product"):
            # Create Cursor
            with connection.cursor() as cur:
                cur.execute(
                    "delete from add_product where product_name=%s",
                    (pro_name))
                # Commit cursor
                connection.commit()
                self.update_pro_trv()
                self.update_out_of_stock_trv()
                self.update_expired_pro_trv()
                self.update_item_name_list()
                self.clear_widget_for_mn_pro()

                # Close Connection
                # connection.close()
        else:
            return True

    #######################################################################

    ####################### POS_sale_details_treeview #####################

    def item_name_list(self, rows):
        self.search_item_list_box.delete(0, END)
        for i in rows:
            self.search_item_list_box.insert(0, i)

    def update_item_name_list(self):
        self.search_item_list_box.delete(0, END)
        with connection.cursor() as cur:
            cur.execute("select product_name from add_product")
            rows = cur.fetchall()
            self.item_name_list(rows)

    def search_sale_item_by_name(self, *args):
        pattern = self.search_sale_item.get()
        if len(pattern) > 0:
            with connection.cursor() as cur:
                query = "select product_name from add_product where product_name REGEXP '^" + pattern + "'"
                cur.execute(query)
                rows = cur.fetchall()
                self.item_name_list(rows)
        else:
            self.update_item_name_list()

    def show_list_item(self, rows):
        self.selected_item_lbl.set(rows[0][0])
        self.selected_quantity_lbl.set(rows[0][1])
        self.selected_price_lbl.set(rows[0][2])

    def selected_list_item(self, event):
        w = event.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)
        with connection.cursor() as cur:
            query = "select product_name,quantity,sell_price from add_product where product_name=%s"
            cur.execute(query, (value))
            rows = cur.fetchall()
            self.show_list_item(rows)

    def add_to_cart(self):
        # global self.total_price
        quantity = self.select_quantity_to_sale.get()
        if self.selected_item_lbl.get() == "":
            messagebox.showerror("Error", "Select the Item")
        elif quantity == "":
            messagebox.showerror("Error", "Select the Quantity")
        else:
            pro_name = self.selected_item_lbl.get()
            quantity = (self.select_quantity_to_sale.get())
            unit_price = float(self.selected_price_lbl.get())
            price = float(quantity) * unit_price
            self.sale_item_trv.insert('', 'end', values=(pro_name, quantity, unit_price, price))
            self.total_price = price + self.total_price
            self.total_price_sale.set(self.total_price)

    def validation_for_sale(self):
        cust_name = self.customer.get()
        cont_num = self.cust_contact.get()
        if cust_name == "" or cont_num == "":
            messagebox.showerror("Error", "Customer details are must")
        elif cont_num is not None:
            if cont_num.isdigit():
                if len(cont_num) != 10:
                    messagebox.showerror("Error", "Contact no. must be of 10 digit")
                elif self.sale_item_trv.get_children() == ():
                    messagebox.showerror("Error", "Add the item in cart")
                elif self.paid_rs.get() == "":
                    messagebox.showerror("Error", "Pay the amount")
                else:
                    if self.paid_rs.get() >= self.total_price_sale.get():
                        self.generate_sale_bill()
                    else:
                        messagebox.showerror("Error", "Pay the whole amount")
            else:
                messagebox.showerror("Error", "character is not allowed")

    def paid_to_return(self, *args):
        paid_rs = (self.paid_rs.get())
        if len(paid_rs) > 0:
            if float(paid_rs) > (float(self.total_price_sale.get())):
                self.return_rs.set((float(paid_rs)) - float(self.total_price_sale.get()))
            else:
                self.return_rs.set("0.0")
        else:
            self.return_rs.set("0.0")

    def generate_sale_bill(self):
        bill_no = self.bill_no.get()
        cust_name = self.customer.get()
        cust_cont = self.cust_contact.get()
        total_rs = self.total_price_sale.get()
        paid_rs = self.paid_rs.get()
        return_rs = self.return_rs.get()

        with connection.cursor() as cur:
            cur.execute(
                "INSERT INTO add_new_sale(customer_name, contact_no, entry_date, bill_no, total_price, paid_rs,return_rs)"
                " VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (cust_name, cust_cont, self.today_date, bill_no, total_rs, paid_rs, return_rs))

            # Commit cursor
            connection.commit()

        for line in self.sale_item_trv.get_children():
            p_name = self.sale_item_trv.item(line)['values'][0]
            qty = self.sale_item_trv.item(line)['values'][1]

            with connection.cursor() as cur:
                cur.execute(
                    "select quantity from add_product where product_name=%s",
                    (p_name))
            rows = cur.fetchall()

            remain_qty = (int(rows[0][0]) - qty)

            with connection.cursor() as cur:
                cur.execute(
                    "update add_product set quantity=%s where product_name=%s",
                    (remain_qty, p_name))

            # Commit cursor
            connection.commit()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.set_font_size(18)
        pdf.cell(200, 20, txt="Welcome To My Shop",
                 ln=1, align='C')
        pdf.set_font_size(15)
        pdf.cell(120, 10, txt=f"Bill Number : {self.bill_no.get()}",
                 ln=0)
        pdf.cell(100, 10, txt=f"Phone Number : {self.cust_contact.get()}",
                 ln=1)
        pdf.cell(120, 10, txt=f"Customer Name : {self.customer.get()}",
                 ln=0)
        pdf.cell(100, 10, txt=f"Date : {self.change_date_format(str(self.today_date))}",
                 ln=1)
        pdf.cell(300, 1,
                 txt="--------------------------------------------------------------------------------------------------------------",
                 ln=1)
        pdf.cell(55, 10, txt="Products", ln=0)
        pdf.cell(55, 10, txt="QTY", ln=0)
        pdf.cell(55, 10, txt="Unit Price", ln=0)
        pdf.cell(55, 10, txt="Price", ln=1)
        pdf.cell(220, 1,
                 txt="--------------------------------------------------------------------------------------------------------------",
                 ln=1)

        for line in self.sale_item_trv.get_children():
            for value in self.sale_item_trv.item(line)['values']:
                pdf.set_font_size(12)
                pdf.cell(55, 10, txt=f"{value}",
                         ln=0)
            pdf.cell(1, 8, ln=1)

        pdf.set_font_size(15)
        pdf.cell(220, 1,
                 txt="--------------------------------------------------------------------------------------------------------------",
                 ln=1)
        pdf.cell(200, 10, txt=f"Total Amount: Rs. {self.total_price_sale.get()}",
                 ln=1)
        pdf.cell(220, 1,
                 txt="--------------------------------------------------------------------------------------------------------------",
                 ln=1)
        pdf.cell(100, 10, txt=f"Paid: Rs. {self.paid_rs.get()}",
                 ln=0)
        pdf.cell(100, 10, txt=f"Return: Rs. {self.return_rs.get()}",
                 ln=1)
        pdf.cell(220, 1,
                 txt="--------------------------------------------------------------------------------------------------------------",
                 ln=1)

        pdf.output("saved_files\\" + str(self.bill_no.get()) + ".pdf")
        wb.open_new_tab("saved_files\\" + str(self.bill_no.get()) + ".pdf")

        self.clear_widget_for_pos_sale()
        self.update_sale_trv()
        self.update_pro_trv()

    ###########################################################################

    ####################### Manage_sale_details_functions #####################

    def rows_sale_item(self, rows):
        self.mn_sale_trv.delete(*self.mn_sale_trv.get_children())
        for i in rows:
            self.mn_sale_trv.insert('', 'end', values=i)

    def update_sale_trv(self):
        with connection.cursor() as cur:
            query = "select * from add_new_sale"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_sale_item(rows)

    def search_mn_sale_item_by_name(self, *args):
        pattern = self.search_mn_sale_item.get()
        if len(pattern) > 0:
            with connection.cursor() as cur:
                query = "select * from add_new_sale where customer_name REGEXP '^" + pattern + "'"
                cur.execute(query)
                rows = cur.fetchall()
                self.rows_sale_item(rows)
        else:
            self.update_sale_trv()

    def show_sale_bill(self):
        items = self.mn_sale_trv.item(self.mn_sale_trv.focus())
        if items['values'] == "":
            messagebox.showinfo("Info", "Select the Sale")
        else:
            bill_no = items['values'][4]
            wb.open_new_tab("saved_files\\" + str(bill_no) + ".pdf")

    def del_sale_bill(self):
        items = self.mn_sale_trv.item(self.mn_sale_trv.focus())
        if items['values'] == "":
            messagebox.showinfo("Info", "Select the Sale")
        else:
            bill_no = items['values'][4]
            # Create Cursor
            with connection.cursor() as cur:
                cur.execute(
                    "delete from add_new_sale where bill_no=%s",
                    (bill_no))
                # Commit cursor
                connection.commit()
                # Close Connection
                # connection.close()
            os.remove("saved_files\\" + str(bill_no) + ".pdf")
            self.update_sale_trv()

    ###########################################################################

    ####################### New_Purchase_details_treeview #####################

    def pur_add_to_cart(self):
        # global self.total_price
        pro_name = str(self.pur_pro_name.get())
        category = str(self.pur_category.get())
        quantity = str(self.pur_quantity.get())
        manu_date = self.formating(str(self.pur_manu_date.get()))
        exp_date = self.formating(str(self.pur_exp_date.get()))
        sell_unit_price = str(self.sell_unit_price.get())
        pur_unit_price = str(self.purch_unit_price.get())
        if category == "" or pro_name == "" or quantity == "" or pur_unit_price == "" or sell_unit_price == "":
            messagebox.showerror("Error", "Select the item and fill all te details")
        else:
            pur_unit_price = float(self.purch_unit_price.get())
            price = float(quantity) * pur_unit_price
            self.pur_item_trv.insert('', 'end', values=(
            category, pro_name, quantity, manu_date, exp_date, pur_unit_price, sell_unit_price))
            self.total_price = price + self.total_price
            self.pur_total_price.set(self.total_price)

    def validation_for_purchase(self):
        supp_name = self.pur_supplier.get()
        if supp_name == "":
            messagebox.showerror("Error", "Enter the supplier name")
        elif supp_name.isdigit():
            messagebox.showerror("Error", "Supplier name should be alphanumeric")
        elif self.pur_item_trv.get_children() == ():
            messagebox.showerror("Error", "Add the item in cart")
        else:
            with connection.cursor() as cur:
                query = "select * from add_supplier where supplier_name=%s"
                cur.execute(query, (supp_name))
                rows = cur.fetchall()
                if rows == ():
                    messagebox.showerror("Error", "First you have to add the new supplier")
                else:
                    self.pur_checkout()

    def pur_checkout(self):
        supplier = str(self.pur_supplier.get())
        bill_no = str(self.pur_bill_no.get())
        total_price = str(self.pur_total_price.get())
        # Create Cursor
        with connection.cursor() as cur:
            cur.execute(
                "INSERT INTO add_purchase(supplier_name, entry_date, bill_no, total_price)"
                " VALUES(%s, %s, %s, %s)",
                (supplier, self.today_date, bill_no, total_price))

            # Commit cursor
            connection.commit()
            # Close Connection

        for line in self.pur_item_trv.get_children():
            pro_name = self.pur_item_trv.item(line)['values'][0]
            category = self.pur_item_trv.item(line)['values'][1]
            quantity = self.pur_item_trv.item(line)['values'][2]
            manu_date = self.pur_item_trv.item(line)['values'][3]
            exp_date = self.pur_item_trv.item(line)['values'][4]
            pur_unit_price = self.pur_item_trv.item(line)['values'][5]
            sell_unit_price = self.pur_item_trv.item(line)['values'][6]
            pur_bill_no = self.pur_bill_no.get()

            with connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO purchase_products(product_name, category, quantity, manufacture_date, expiry_date, pur_unit_price, sell_unit_price, bill_no)"
                    " VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                    (pro_name, category, quantity, manu_date, exp_date, pur_unit_price, sell_unit_price, pur_bill_no))

                # Commit cursor
                connection.commit()
        self.clear_widget_for_new_pur()
        self.update_rows_pur_trv()

    ###########################################################################

    ####################### Manage_Purchase_Frame_Function #####################

    def rows_pur_list(self, rows):
        self.pur_list_trv.delete(*self.pur_list_trv.get_children())
        for i in rows:
            self.pur_list_trv.insert('', 'end', values=i)

    def update_rows_pur_trv(self):
        with connection.cursor() as cur:
            query = "select * from add_purchase"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_pur_list(rows)

    def search_mn_purchase_by_name(self, *args):
        pattern = self.search_mn_pur_supp.get()
        if len(pattern) > 0:
            with connection.cursor() as cur:
                query = "select * from add_purchase where supplier_name REGEXP '^" + pattern + "'"
                cur.execute(query)
                rows = cur.fetchall()
                self.rows_pur_list(rows)
        else:
            self.update_rows_pur_trv()

    def rows_pur_item_list(self, rows):
        self.pur_item_list_trv.delete(*self.pur_item_list_trv.get_children())
        for i in rows:
            self.pur_item_list_trv.insert('', 'end', values=i)

    def show_purchase_items(self):
        items = self.pur_list_trv.item(self.pur_list_trv.focus())
        if items['values'] == "":
            messagebox.showinfo("Info", "Select the Purchase")
        else:
            bill_no = items['values'][3]
            with connection.cursor() as cur:
                query = "select * from purchase_products where bill_no=%s"
                cur.execute(query, (bill_no))
                rows = cur.fetchall()
                self.rows_pur_item_list(rows)

    def del_purchase_items(self):
        items = self.pur_list_trv.item(self.pur_list_trv.focus())
        if items['values'] == "":
            messagebox.showinfo("Info", "Select the purchase")
        else:
            bill_no = items['values'][3]
            with connection.cursor() as cur:
                cur.execute(
                    "delete from add_purchase where bill_no=%s",
                    (bill_no))
                # Commit cursor
                connection.commit()
            with connection.cursor() as cur:
                cur.execute(
                    "delete from purchase_products where bill_no=%s",
                    (bill_no))
                # Commit cursor
                connection.commit()
            self.pur_item_list_trv.delete(*self.pur_item_list_trv.get_children())
            self.update_rows_pur_trv()

    ###########################################################################

    ####################### Out_of_stock_Frame_Function #####################

    def rows_out_of_stocks_item(self, rows):
        self.out_of_stock_trv.delete(*self.out_of_stock_trv.get_children())
        for i in rows:
            self.out_of_stock_trv.insert('', 'end', values=i)

    def update_out_of_stock_trv(self):
        with connection.cursor() as cur:
            query = "select * from add_product where quantity<=5"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_out_of_stocks_item(rows)

    ####################### Expired_Pro_Frame_Function #####################

    def rows_expired_pro_items(self, rows):
        self.expired_pro_trv.delete(*self.expired_pro_trv.get_children())
        for i in rows:
            self.expired_pro_trv.insert('', 'end', values=i)

    def update_expired_pro_trv(self):
        with connection.cursor() as cur:
            query = "select * from add_product where expiry_date < now()"
            cur.execute(query)
            rows = cur.fetchall()
            self.rows_expired_pro_items(rows)

    ###########################################################################

if __name__ == '__main__':
    splash_win()
