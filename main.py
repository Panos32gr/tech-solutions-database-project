import tkinter.messagebox
from tkinter import *
from random import *
import sqlite3

guest_flag = False
transition_flag = False
if transition_flag == False:
    # admin database and data table creation
    adminlogincon = sqlite3.connect("admins.db")
    y = adminlogincon.cursor()



    admintable = (""" CREATE TABLE IF NOT EXISTS admins (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL UNIQUE
    )""")
    y.execute(admintable)
    adminlogincon.commit()



    #login window
    login = Tk()
    login.title("Login")
    login.geometry("900x600")

    # Guidance buttons
    guide_button_admin =  Button(login, width=23, text="Login as Administrator", command= lambda: admin_login())
    guide_button_guest = Button(login, width=23, text="Continue as Guest", command= lambda: guest_forwading()) 
    guide_button_reg = Button(login, width=23, text="Register new Administrator", command= lambda:admin_registry())
    guide_button_admin.place(x=350, y=200)
    guide_button_reg.place(x=350, y=250)
    guide_button_guest.place(x=350, y=300)

# Administrator login function
    def admin_login():
        log_window = Toplevel(login, width=400, height=300)
        log_window.title("Administrator Login.")
        username_label = Label(log_window, text="Admin Username:")
        username_label.place(x=40, y=90)
        username_entry  = Entry(log_window, width=40)
        username_entry.place(x=40, y=120)


        password_label = Label(log_window, text="Password:")
        password_label.place(x=40, y=150)
        password_entry = Entry(log_window, width=40)
        password_entry.place(x=40, y=180)

        login_confirm_button = Button(log_window, text="Confirm.", command= lambda: login_attempt(username_data=username_entry, password_data=password_entry))
        login_confirm_button.place(x=230, y=210)
        
        def login_attempt(username_data, password_data):
            l1 =username_data.get()
            l2 =password_data.get()
            username_val ="""SELECT * FROM admins WHERE username = ? AND password = ?"""
            y.execute(username_val,[l1,l2])
            validation = y.fetchall()
            if validation:
                tkinter.messagebox.showinfo(title="Success",message="Verification Complete.")
                login.destroy()
                global transition_flag
                transition_flag = True
            else:
                tkinter.messagebox.showwarning(title="Oops",message="We checked our data, and yours weren't there. Please try again.")

    
    # Administrator registry function
    def admin_registry():
        reg_window = Toplevel(login, width=400, height=300)
        reg_window.title("Administrator Registry.")
        
        username_label = Label(reg_window, text="Admin Username:")
        username_label.place(x=40, y=50)
        username_entry  = Entry(reg_window, width=40)
        username_entry.place(x=40, y=80)


        password_label = Label(reg_window, text="Password(4 characters at least.):")
        password_label.place(x=40, y=120)
        password_entry = Entry(reg_window, width=40)
        password_entry.place(x=40, y=150)
        
        four_digit_label = Label(reg_window, text="Safety password:")
        four_digit_entry = Entry(reg_window, width=20)
        four_digit_label.place(x=40, y=180)
        four_digit_entry.place(x=40, y=210)

        registry_confirm_button = Button(reg_window, text="Confirm.", command= lambda: registry_attempt(username_data=username_entry, password_data=password_entry, safety_data=four_digit_entry))
        registry_confirm_button.place(x=260, y=250)

        def registry_attempt(username_data, password_data, safety_data):
            adminonly_password = "1746"                                 #Registration safety 4 digit password
            r1 = username_data.get()
            r2 = password_data.get()
            r3 = safety_data.get()
            if len(r1) <= 0:
                tkinter.messagebox.showwarning(title="Invalid Username", message="Please enter a Username.")
                if len(r2) <= 0:
                    tkinter.messagebox.showwarning(title="Invalid password", message="Password need to be at least one number or letter long.")
                    if r3 != adminonly_password:
                        tkinter.messagebox.showwarning(title="Invalid safety password", message="Please enter the correct safety password.")
            else:
                try:
                    data_query = "INSERT INTO admins VALUES (?,?)"
                    data_tuple = (r1, r2)
                    y.execute(data_query, data_tuple)
                    adminlogincon.commit()
                    reg_window.destroy()
                    login.destroy()
                    global transition_flag
                    transition_flag = True
                except sqlite3.Error or TypeError or sqlite3.OperationalError:
                    tkinter.messagebox.showwarning(title="Oops", message="Database error, please check your number input and/or database availability")
    # destroys guidance button window and proceeds with main programm code with guest user click
    def guest_forwading():
        login.destroy()
        global guest_flag
        global transition_flag
        transition_flag = True
        guest_flag = True

    login.mainloop()
#main programm code

if transition_flag:
    # DATABASE CREATION IF IT DOESN'T EXIST AND CONNECTION
    conn = sqlite3.connect("Clients.db")

    x = conn.cursor()


    table = ("""CREATE TABLE IF NOT EXISTS clients (
            Clientnumber INTEGER PRIMARY KEY,
            Firstname TEXT NOT NULL,
            Lastname TEXT NOT NULL,
            Address INTEGER NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Phone TEXT NOT NULL,
            Services TEXT NOT NULL
    )""")
    x.execute(table)
    conn.commit()

    # tkinter UI
    tsdb = Tk()
    tsdb.title("Tech Solutions clients.")
    tsdb.geometry("1000x600")
    tsdb.configure(bg="white")



    # navigation buttons
    if guest_flag:
        navb = Button(tsdb, text="New Client", width=30, command=lambda: newclient(), state=DISABLED)
        navb.place(x="400", y="50")
    else:
        navb = Button(tsdb, text="New Client", width=30, command=lambda: newclient())
        navb.place(x="400", y="50")

    navb3 = Button(tsdb, text="Client List", width=30, command=lambda: client_search())
    navb3.place(x="400", y="100")


    # client registration
    def newclient():
        client_regist = Toplevel(tsdb, width="800", height="700")
        client_regist.title("Register New Client")
        save_button = Button(client_regist, text="Save Client",
                            command=lambda: dataimport(client_no=client_no_generation, d1=name_box, d2=surname_box, d3=address_box, d4=email, d5=phone, d6=workinfo_box))
        save_button.place(x=600, y=650)
        cancel_button = Button(client_regist, text="Cancel", command=lambda: toplvlclose())
        cancel_button.place(x=700, y=650)

        # close top window with cancel button function
        def toplvlclose():
            client_regist.destroy()

        # client serial number generation and display in new client window
        client_no_generation = randint(1, 10000)
        client_number_display = Label(client_regist, font="BOLD", text="Client number:" + " " + str(client_no_generation))
        client_number_display.place(x=500, y=20)

        # name
        name_label = Label(client_regist, text="Name:")
        name_box = Entry(client_regist, width=40)
        name_label.place(x=0, y=0)
        name_box.place(x=0, y=30)
        # surname
        surname_label = Label(client_regist, text="Last name:")
        surname_box = Entry(client_regist, width=40)
        surname_label.place(x=0, y=55)
        surname_box.place(x=0, y=85)
        # address
        address_label = Label(client_regist, text="Address:")
        address_box = Entry(client_regist, width=40)
        address_label.place(x=0, y=125)
        address_box.place(x=0, y=155)
        # phone
        email_label = Label(client_regist, text="E-mail:")
        email = Entry(client_regist, width=40)
        email_label.place(x=0, y=185)
        email.place(x=0, y=215)
        # email
        phone_label = Label(client_regist, text="Phone:")
        phone = Entry(client_regist, width=40)
        phone_label.place(x=0, y=245)
        phone.place(x=0, y=275)
        # Services Provided and general info
        workinfo_label = Label(client_regist, text="Services provided:")
        workinfo_box = Text(client_regist, width=50, height=20)
        workinfo_label.place(x=0, y=305)
        workinfo_box.place(x=0, y=335)

        # data retrieving from entries and storing them to sqlite database
        def dataimport(client_no, d1, d2, d3, d4, d5, d6):
            client_number_import = client_no
            name = d1.get()
            surname = d2.get()
            addrs = d3.get()
            eml = d4.get()
            telephone = d5.get()
            work = d6.get("1.0", "end-1c")
            data_query = "INSERT INTO clients VALUES (?,?,?,?,?,?,?)"
            data_tuple = (client_number_import, name, surname, addrs, eml, telephone, work)
            x.execute(data_query, data_tuple)
            conn.commit()
            toplvlclose()


    # an entire client list display(tool to help user search clients with their 4 digit number by providing the 4 digit plus first name and last name)
    def client_search():
        search_nav = Toplevel(tsdb, width=450, height=250)
        search_nav.title("Search Navigation")
        with_number = Button(search_nav, width=20, text="Client Number Search", command=lambda: search_with_number())
        with_number.place(x=140, y=70)
        full_list = Button(search_nav, width=20, text="Full List", command=lambda: entire_list())
        full_list.place(x=140, y=120)
        def entire_list():
            try:
                k = 0
                list_window = Toplevel(search_nav, width=600,  height=400)
                list_window.title("Client List")
                retrieve_list = """SELECT Clientnumber, Firstname, Lastname FROM clients"""
                x.execute(retrieve_list)
                list_query = x.fetchall()
                for i in list_query:
                    list_display = Label(list_window, text=i)
                    list_display.place(x=0, y=k)
                    k += 25  
            except sqlite3.Error and sqlite3.OperationalError and TypeError:
                    tkinter.messagebox.showwarning(title="Oops", message="Database error, please check your number input and/or database availability")    
        # UI for search with user entry for client number
        def search_with_number():
            win = Toplevel(tsdb, width=450, height=150)
            search_label = Label(win, text="Enter Client Number:")
            search_label.place(x=30, y=10)
            search_box = Entry(win, width=40)
            search_box.place(x=30, y=40)
            search_button = Button(win, text="Search", width=20, command=lambda: obtain_data(cl_num=search_box))
            search_button.place(x=250, y=95)
            # Retrieves data from sqlite database and injects it to a tkinter label
            def obtain_data(cl_num):
                p1 = 0
                p2 = 0
                key_list = ["Client number:", "First Name:", "Last Name:", "Address:", "E-mail:", "Phone:", "Services:"]
                client_number = cl_num.get()
                try:
                    number_search = f"""SELECT * FROM clients WHERE Clientnumber = {client_number}"""
                    x.execute(number_search)
                    retrieve_data = x.fetchone()
                    data_window = Toplevel(win, width=300, height=300)
                    if guest_flag:
                        edit_button = Button(data_window, width=10, text = "Edit", command=lambda: editclient(), state=DISABLED)
                        edit_button.place(x=100, y=250)
                        clientdelete = Button(data_window, text="Delete Client", command=lambda: clientremoval(), state=DISABLED)
                        clientdelete.place(x=200, y=250)
                    else:
                        edit_button = Button(data_window, width=10, text = "Edit", command=lambda: editclient())
                        edit_button.place(x=100, y=250)
                        clientdelete = Button(data_window, text="Delete Client", command=lambda: clientremoval())
                        clientdelete.place(x=200, y=250)
                    for i in retrieve_data:
                        display_label = Label(data_window, text=i)
                        display_label.place(x=100, y=p1)
                        p1 += 25
                    for j in key_list:
                        display_label = Label(data_window, text=j)
                        display_label.place(x=0, y=p2)
                        p2 += 25
                except sqlite3.Error and sqlite3.OperationalError and TypeError:
                    tkinter.messagebox.showwarning(title="Oops", message="Database error, please check your number input and/or database availability")
                # edit client data user interface and code
                def editclient():
                    edit_host = Toplevel(data_window, width=400, height=400)
                    edit_host.title("Client Edit")
                    option_config = Button(edit_host, text="Confirm", command= lambda:optionselect())
                    option_config.place(x=250, y=100)
                    menu = StringVar()
                    menu.set("Select client attribute to edit")
                    dropdown = OptionMenu(edit_host, menu, "First name", "Last name", "Address", "E-mail", "Phone", "Services")
                    dropdown.place(x=50, y=100)
                    def optionselect():
                        comparison_list = ["First name", "Last name", "Address", "Email", "Phone", "Services"]
                        selected_option = menu.get()
                        for i in comparison_list:
                            if selected_option == i:
                                text_label = Label(edit_host, text=i)
                                text_label.place(x=50, y=160)
                                edit_entry = Entry(edit_host, width=40)
                                edit_entry.place(x=50, y=200)
                                edit_config = Button(edit_host, text="Edit", width=20, command=lambda: changeinfo(alterations=edit_entry, fourdigit=client_number))
                                edit_config.place(x=350, y=350)
                        def changeinfo(alterations, fourdigit):
                            new_info = alterations.get()
                            db_connection = sqlite3.connect("clients.db")
                            cur = db_connection.cursor()
                            edit_query = f"""UPDATE clients SET {selected_option.replace(" ", "")} = ? WHERE Clientnumber = ?"""
                            query_tuple = (new_info, fourdigit)
                            cur.execute(edit_query, query_tuple)
                            db_connection.commit()
                            edit_host.destroy()
                            db_connection.close()

                # client deletion user interface and code
                def clientremoval():
                    confirm_window = Toplevel(data_window, width=500, height=200)
                    confirm_window.title("Delete Client.")
                    q_label = Label(confirm_window, text=f"Are you sure you want to delete client {client_number}?")
                    q_label.place(x=100, y=50)
                    accept_button = Button(confirm_window, width=20, text="Confirm", command= lambda: deleteconfirm())
                    accept_button.place(x=80, y=160)
                    decline_button = Button(confirm_window, width=20, text="Cancel", command= lambda: deletecancel())
                    decline_button.place(x=250, y=160)
                    def deleteconfirm():
                        db_connection = sqlite3.connect("clients.db")
                        cur = db_connection.cursor()
                        delete_query = f"""DELETE FROM clients WHERE Clientnumber = {client_number} """
                        cur.execute(delete_query)
                        db_connection.commit()
                        db_connection.close()
                        confirm_window.destroy()
                        data_window.destroy()
                    
                    def deletecancel():
                        confirm_window.destroy()





tsdb.mainloop()
