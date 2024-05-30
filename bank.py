import sqlite3
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from datetime import datetime
import time
from tkinter.ttk import Style, Treeview, Scrollbar

try:
    conobj = sqlite3.connect(database="banking.sqlite")
    curobj = conobj.cursor()
    curobj.execute("CREATE TABLE IF NOT EXISTS accounts(acn INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pass TEXT, email TEXT, mob TEXT, bal FLOAT, type TEXT, opendate TEXT, addcard TEXT)")
    curobj.execute("CREATE TABLE IF NOT EXISTS txns(acn INTEGER, amt FLOAT, updatebal FLOAT, type TEXT, txndate TEXT)")
    conobj.close()
    print("Tables created")
except:
    print("Something went wrong, might be tables already exist")

win = Tk()
win.state("zoomed")
win.configure(bg="powder blue")
win.resizable(width=False, height=False)

title = Label(win, text="Banking Automation", font=('arial', 60, 'bold', 'underline'), bg="powder blue")
title.pack()

date = Label(win, text=f"{datetime.now().date()}", font=('arial', 15, 'bold'), fg='green', bg="powder blue")
date.place(relx=.85, rely=.12)


def mainscreen():
    frm = Frame(win)
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.85)
    frm.configure(bg="pink")

    def new():
        frm.destroy()
        newscreen()

    def fp():
        frm.destroy()
        fpscreen()

    def reset():
        e_acn.delete(0, "end")
        e_pass.delete(0, "end")
        e_acn.focus()

    def login():
        acn = e_acn.get()
        pwd = e_pass.get()

        if len(acn) == 0 or len(pwd) == 0:
            messagebox.showerror("Login", "Empty fields are not allowed!")
        else:
            conobj = sqlite3.connect(database="banking.sqlite")
            curobj = conobj.cursor()
            curobj.execute("SELECT * FROM accounts WHERE acn=? AND pass=?", (acn, pwd))
            tup = curobj.fetchone()
            if tup is None:
                messagebox.showerror("Login", "Invalid ACN/PASS")
            else:
                global uname, uacn
                uacn = tup[0]
                uname = tup[1]
                frm.destroy()
                homescreen()

    lbl_acn = Label(frm, text="ACN", font=('arial', 20, 'bold'), bg="pink")
    lbl_acn.place(relx=.3, rely=.1)

    e_acn = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_acn.place(relx=.4, rely=.1)
    e_acn.focus()

    lbl_pass = Label(frm, text="Pass", font=('arial', 20, 'bold'), bg="pink")
    lbl_pass.place(relx=.3, rely=.2)

    e_pass = Entry(frm, font=('arial', 20, 'bold'), bd=5, show="*")
    e_pass.place(relx=.4, rely=.2)

    lgn_btn = Button(frm, command=login, text="login", font=('arial', 20, 'bold'), bd=5)
    lgn_btn.place(relx=.42, rely=.3)

    reset_btn = Button(frm, text="reset", font=('arial', 20, 'bold'), bd=5, command=reset)
    reset_btn.place(relx=.53, rely=.3)

    fp_btn = Button(frm, command=fp, text="forgot password", font=('arial', 20, 'bold'), bd=5, width=16)
    fp_btn.place(relx=.4, rely=.4)

    new_btn = Button(frm, text="create new account", font=('arial', 20, 'bold'), bd=5, width=19, command=new)
    new_btn.place(relx=.38, rely=.5)


def newscreen():
    frm = Frame(win)
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.85)
    frm.configure(bg="pink")

    def back():
        frm.destroy()
        mainscreen()

    def openacndb():
        bal = 0
        opendate = time.ctime()
        name = e_name.get()
        pwd = e_pass.get()
        email = e_email.get()
        mob = e_mob.get()
        addcard = e_addcard.get()  # New field
        acntype = cb_type.get()

        conobj = sqlite3.connect(database="banking.sqlite")
        curobj = conobj.cursor()
        curobj.execute(
            "INSERT INTO accounts(name, pass, email, mob, bal, type, opendate, addcard) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            (name, pwd, email, mob, bal, acntype, opendate, addcard))
        conobj.commit()
        curobj.close()

        curobj = conobj.cursor()
        curobj.execute("SELECT MAX(acn) FROM accounts")
        tup = curobj.fetchone()
        messagebox.showinfo("New Account", f"Account opened with ACN:{tup[0]}")
        conobj.close()

    lbl_name = Label(frm, text="Name", font=('arial', 20, 'bold'), bg="pink")
    lbl_name.place(relx=.3, rely=.1)

    e_name = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_name.place(relx=.4, rely=.1)
    e_name.focus()

    lbl_pass = Label(frm, text="Pass", font=('arial', 20, 'bold'), bg="pink")
    lbl_pass.place(relx=.3, rely=.2)

    e_pass = Entry(frm, font=('arial', 20, 'bold'), bd=5, show="*")
    e_pass.place(relx=.4, rely=.2)

    lbl_email = Label(frm, text="Email", font=('arial', 20, 'bold'), bg="pink")
    lbl_email.place(relx=.3, rely=.3)

    e_email = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_email.place(relx=.4, rely=.3)

    lbl_mob = Label(frm, text="Mob", font=('arial', 20, 'bold'), bg="pink")
    lbl_mob.place(relx=.3, rely=.4)

    e_mob = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_mob.place(relx=.4, rely=.4)

    lbl_addcard = Label(frm, text="Add Card", font=('arial', 20, 'bold'), bg="pink")
    lbl_addcard.place(relx=.3, rely=.6)

    e_addcard = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_addcard.place(relx=.4, rely=.6)

    lbl_type = Label(frm, text="Type", font=('arial', 20, 'bold'), bg="pink")
    lbl_type.place(relx=.3, rely=.5)

    cb_type = Combobox(frm, values=['Saving', 'Current'], font=('arial', 20, 'bold'))
    cb_type.current(0)
    cb_type.place(relx=.4, rely=.5)

    open_btn = Button(frm, text="open", font=('arial', 20, 'bold'), bd=5, command=openacndb)
    open_btn.place(relx=.42, rely=.7)

    reset_btn = Button(frm, text="reset", font=('arial', 20, 'bold'), bd=5)
    reset_btn.place(relx=.53, rely=.7)

    back_btn = Button(frm, text="back", font=('arial', 20, 'bold'), bd=5, command=back)
    back_btn.place(relx=0, rely=0)


def fpscreen():
    frm = Frame(win)
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.85)
    frm.configure(bg="pink")

    def back():
        frm.destroy()
        mainscreen()

    def recpassdb():
        acn = e_acn.get()
        email = e_email.get()
        mob = e_mob.get()

        conobj = sqlite3.connect(database="banking.sqlite")
        curobj = conobj.cursor()
        curobj.execute("SELECT pass FROM accounts WHERE acn=? AND email=? AND mob=?", (acn, email, mob))
        tup = curobj.fetchone()
        if tup is None:
            messagebox.showerror("Forgot Pass", "Account does not exist")
        else:
            messagebox.showinfo("Forgot Pass", f"Your Pass : {tup[0]}")

    back_btn = Button(frm, text="back", font=('arial', 20, 'bold'), bd=5, command=back)
    back_btn.place(relx=0, rely=0)

    lbl_acn = Label(frm, text="ACN", font=('arial', 20, 'bold'), bg="pink")
    lbl_acn.place(relx=.3, rely=.2)

    e_acn = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_acn.place(relx=.4, rely=.2)
    e_acn.focus()

    lbl_email = Label(frm, text="Email", font=('arial', 20, 'bold'), bg="pink")
    lbl_email.place(relx=.3, rely=.3)

    e_email = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_email.place(relx=.4, rely=.3)

    lbl_mob = Label(frm, text="Mob", font=('arial', 20, 'bold'), bg="pink")
    lbl_mob.place(relx=.3, rely=.4)

    e_mob = Entry(frm, font=('arial', 20, 'bold'), bd=5)
    e_mob.place(relx=.4, rely=.4)

    rec_btn = Button(frm, command=recpassdb, text="recover", font=('arial', 20, 'bold'), bd=5)
    rec_btn.place(relx=.42, rely=.6)

    reset_btn = Button(frm, text="reset", font=('arial', 20, 'bold'), bd=5)
    reset_btn.place(relx=.53, rely=.6)


def homescreen():
    frm = Frame(win)
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.85)
    frm.configure(bg="pink")

    def logout():
        frm.destroy()
        mainscreen()

    def detailsscreen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.place(relx=.25, rely=.15, relwidth=.6, relheight=.6)
        ifrm.configure(bg="white")

        lbl = Label(ifrm, text="This is Account Details Screen", font=('arial', 25, 'bold'), bg="white", fg='green')
        lbl.pack()

        conobj = sqlite3.connect(database="banking.sqlite")
        curobj = conobj.cursor()
        curobj.execute("SELECT * FROM accounts WHERE acn=?", (uacn,))
        tup = curobj.fetchone()

        lbl_acn = Label(ifrm, text=f"Account No:\t{tup[0]}", font=('arial', 15,), bg="white")
        lbl_acn.place(relx=.2, rely=.2)

        lbl_bal = Label(ifrm, text=f"ACN Balance:\t{tup[5]}", font=('arial', 15,), bg="white")
        lbl_bal.place(relx=.2, rely=.3)

        lbl_open = Label(ifrm, text=f"Open date:\t{tup[7]}", font=('arial', 15,), bg="white")
        lbl_open.place(relx=.2, rely=.4)


        
        
    def depositscreen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.6)
        ifrm.configure(bg="white")
        
        def depdb():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where acn=?",(uacn,))
            bal=curobj.fetchone()[0]
            curobj.close()
            curobj=conobj.cursor()
            curobj.execute("update accounts set bal=bal+? where acn=?",(amt,uacn))
            curobj.execute("insert into txns values(?,?,?,?,?)",(uacn,amt,bal+amt,"Cr.",time.ctime()))
            conobj.commit()
            conobj.close()
            
            messagebox.showinfo("Deposit",f"Amount deposited,updated bal:{bal+amt}")
            
        lbl=Label(ifrm,text="This is Deposit Screen",font=('arial',25,'bold'),bg="white",fg='green')
        lbl.pack()
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',15,'bold'),bg="white")
        lbl_amt.place(relx=.2,rely=.3)
        
        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.3)
        
        dep_btn=Button(ifrm,command=depdb,text="deposit",font=('arial',15,'bold'),bd=5)
        dep_btn.place(relx=.4,rely=.4)
    
    def withdrawscreen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.6)
        ifrm.configure(bg="white")
        
        def withdrawdb():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where acn=?",(uacn,))
            bal=curobj.fetchone()[0]
            curobj.close()
            if bal>amt:
                curobj=conobj.cursor()
                curobj.execute("update accounts set bal=bal-? where acn=?",(amt,uacn))
                curobj.execute("insert into txns values(?,?,?,?,?)",(uacn,amt,bal-amt,"Db.",time.ctime()))
                conobj.commit()
                messagebox.showinfo("Withdraw",f"Amount withdrawn,updated bal:{bal-amt}")
        
            else:
                messagebox.showwarning("Withdraw",f"Insufficient Bal:{bal}")
                
            conobj.close()
            
            
        lbl=Label(ifrm,text="This is withdraw Screen",font=('arial',25,'bold'),bg="white",fg='green')
        lbl.pack()
    
        lbl_amt=Label(ifrm,text="Amount",font=('arial',15,'bold'),bg="white")
        lbl_amt.place(relx=.2,rely=.3)
        
        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.3)
        
        with_btn=Button(ifrm,command=withdrawdb,text="withdraw",font=('arial',15,'bold'),bd=5)
        with_btn.place(relx=.4,rely=.4)
    
    def historyscreen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.6)
        ifrm.configure(bg="white")
        
        lbl=Label(ifrm,text="This is History Screen",font=('arial',25,'bold'),bg="white",fg='green')
        lbl.pack()
    
        tv=Treeview(ifrm)
        tv.place(x=60,y=100,height=100,width=600)
        
        
        style = Style()
        style.configure("Treeview.Heading", font=('Arial',10,'bold'),foreground='brown')

        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(x=650,y=100,height=100)
        tv.configure(yscrollcommand=sb.set)
        
        tv['columns']=('date','amt','type','upbal')
        
        tv.column('date',width=80,anchor='c')
        tv.column('amt',width=40,anchor='c')
        tv.column('type',width=40,anchor='c')
        tv.column('upbal',width=40,anchor='c')
        
        tv.heading('date',text='Txn Date')
        tv.heading('amt',text='Amount')
        tv.heading('type',text='Txn type')
        tv.heading('upbal',text='Updated Bal')
        
        tv['show']='headings'
        
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from txns where acn=?",(uacn,))
        
        for row in curobj:
            tv.insert("","end",values=(row[4],row[1],row[3],row[2]))
        
    
    def transferscreen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.6)
        ifrm.configure(bg="white")
        
        def transfer():
            to=e_to.get()
            amt=float(e_amt.get())
            
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from accounts where acn=?",(to,))
            tup=curobj.fetchone()
            curobj.close()
            if tup==None:
                messagebox.showerror("Transfer","To ACN does not exist")
            else:
                curobj=conobj.cursor()
                curobj.execute("select bal from accounts where acn=?",(uacn,))
                bal=curobj.fetchone()[0]
                curobj.close()
                if bal>=amt:
                    curobj=conobj.cursor()
                    curobj.execute("update accounts set bal=bal+? where acn=?",(amt,to))
                    curobj.execute("update accounts set bal=bal-? where acn=?",(amt,uacn))
                    curobj.execute("insert into txns values(?,?,?,?,?)",(to,amt,bal+amt,"Cr.",time.ctime()))
                    curobj.execute("insert into txns values(?,?,?,?,?)",(uacn,amt,bal-amt,"Db.",time.ctime()))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Transfer",f"Rs. {amt} is transfered to {to} ACN")
                    
                else:
                    messagebox.showinfo("Transfer",f"Insufficient Bal:{bal}")
                
            
        lbl=Label(ifrm,text="This is Transfer Screen",font=('arial',25,'bold'),bg="white",fg='green')
        lbl.pack()
        
        lbl_to=Label(ifrm,text="To ACN",font=('arial',15,'bold'),bg="white")
        lbl_to.place(relx=.2,rely=.3)
        
        e_to=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_to.place(relx=.35,rely=.3)
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',15,'bold'),bg="white")
        lbl_amt.place(relx=.2,rely=.4)
        
        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.4)
        
        btn=Button(ifrm,command=transfer,text="Transfer",font=('arial',15,'bold'),bd=5)
        btn.place(relx=.4,rely=.5)
        
        
    def updatescreen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.6)
        ifrm.configure(bg="white")
        
        def update():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update accounts set name=?,pass=?,email=?,mob=? where acn=?",(name,pwd,email,mob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Profile Updated")
            ifrm.destroy()
            global uname
            uname=name
            updatescreen()
            
        lbl=Label(ifrm,text="This is Update Profile Screen",font=('arial',25,'bold'),bg="white",fg='green')
        lbl.pack()
    
        lbl_name=Label(ifrm,text="Name",font=('arial',15,'bold'),bg="white")
        lbl_name.place(relx=.1,rely=.2)
        
        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_name.place(relx=.1,rely=.25)
        
        lbl_pass=Label(ifrm,text="Pass",font=('arial',15,'bold'),bg="white")
        lbl_pass.place(relx=.1,rely=.4)
        
        e_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_pass.place(relx=.1,rely=.45)
        
        lbl_email=Label(ifrm,text="Email",font=('arial',15,'bold'),bg="white")
        lbl_email.place(relx=.5,rely=.2)
        
        e_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_email.place(relx=.5,rely=.25)
        
        lbl_mob=Label(ifrm,text="Mob",font=('arial',15,'bold'),bg="white")
        lbl_mob.place(relx=.5,rely=.4)
        
        e_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_mob.place(relx=.5,rely=.45)
        
        btn=Button(ifrm,text="update",font=('arial',15,'bold'),command=update)
        btn.place(relx=.5,rely=.6)
    
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from accounts where acn=?",(uacn,))
        tup=curobj.fetchone()
        curobj.close()
        
        e_name.insert(0,tup[1])
        e_pass.insert(0,tup[2])
        e_email.insert(0,tup[3])
        e_mob.insert(0,tup[4])
        
        
        
    lbl_wel=Label(frm,text=f"Welcome,{uname}",font=('arial',15,'bold'),bg="pink")
    lbl_wel.place(relx=0,rely=0)
    
    logout_btn=Button(frm,text="logout",font=('arial',15,'bold'),command=logout)
    logout_btn.place(relx=.93,rely=0)
    
    details_btn=Button(frm,text="Details",font=('arial',20,'bold'),width=12,command=detailsscreen)
    details_btn.place(relx=0,rely=.1)
    
    deposit_btn=Button(frm,command=depositscreen,text="Deposit",font=('arial',20,'bold'),width=12)
    deposit_btn.place(relx=0,rely=.2)
    
    withdraw_btn=Button(frm,command=withdrawscreen,text="Withdraw",font=('arial',20,'bold'),width=12)
    withdraw_btn.place(relx=0,rely=.3)
    
    profile_btn=Button(frm,command=updatescreen,text="Update profile",font=('arial',20,'bold'),width=12)
    profile_btn.place(relx=0,rely=.4)
    
    history_btn=Button(frm,command=historyscreen,text="History",font=('arial',20,'bold'),width=12)
    history_btn.place(relx=0,rely=.5)
    
    trans_btn=Button(frm,command=transferscreen,text="Transfer",font=('arial',20,'bold'),width=12)
    trans_btn.place(relx=0,rely=.6)
    
mainscreen()
win.mainloop()