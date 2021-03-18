import tkinter as tk
from tkinter import ttk, LEFT, END
from tkcalendar import DateEntry

import sqlite3 as sql
##############################################+=============================================================

root = tk.Tk()

root.geometry("400x200+300+100")
root.title("Merchant Master")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)


ttop = tk.Frame(root, width=50,bg='khaki2', height=50, pady=4)
ttop.grid(row=0, column=0, sticky=tk.NSEW)

tbtn = tk.Frame(root, width=50,bg='khaki2', height=50, pady=4)
tbtn.grid(row=1, column=0, sticky=tk.NSEW)



#Create string variables
MMCode = tk.StringVar()
MMNam = tk.StringVar()
#MMState= tk.StringVar()
MMSite= tk.StringVar()
Mode=tk.BooleanVar()
Var=tk.IntVar()



def Clear_entry():
    
#    CCNoEL.config(state=tk.NORMAL)
    MMNameEL.delete(0, END)
    MMSiteEL.delete(0, END)
    sval=MMCode_gen()
    MMCodeEL.config(state=tk.NORMAL)
    MMCodeEL.delete(0, END)    
    MMCodeEL.insert(0,sval)
    MMCodeEL.config(state=tk.DISABLED)
#    MMStateEL.current(0)
    MMNameEL.focus_set()



def sel():
#    selection = Mode
#    print(Var.get())
    Clear_entry()
    if int(Var.get())==1:  #Add Mode
        Mode=True
        MMCodeEL.config(state=tk.DISABLED)
    else:
        Mode=False  #EditMode
        Clear_entry()
        MMCodeEL.config(state=tk.NORMAL)


#430
Var.set(1)
R1 = tk.Radiobutton(ttop, text="Add Mode", variable=Var, value=1,
  command=sel,bg='khaki2',fg='brown')
R1.grid( column=0, row=0,sticky=tk.W )

R2 = tk.Radiobutton(ttop, text="Edit Mode", variable=Var, value=2,
  command=sel,bg='khaki2',fg='brown')
R2.grid( column=1, row=0,sticky=tk.W  )



MMCode = ""
MMNam = ""
#MMState= ""
MMSite= ""
#Mode=True


#course=["Maharashtra","Gujarat","Kerala","U.P.","M.P.","Punjab","Himachal Pradesh","Orissa"]
#MMStateEL=ttk.Combobox(ttop,values=course,width=40,textvariable = MMState)
#MMStateEL.state(['readonly'])
#MMStateEL.current(0)




#Set up labels

MMCodeLB = tk.Label(ttop, text='Merchant Code : ',bg='khaki2')  # More labels
MMNameLB = tk.Label(ttop, text='Merchant Name : ',bg='khaki2')  # ^
#MMStateLB = tk.Label(ttop, text='State : ',bg='khaki2')  # ^
MMSiteLB = tk.Label(ttop, text='Site : ',bg='khaki2')  # ^

MMInfoLB = tk.Label(ttop, text='-------',fg='red',bg='khaki2',font=('times', 15,' bold '))  # ^


#Set up text entry boxes

MMCodeEL = tk.Entry(ttop, textvariable = MMCode)  # The entry input
MMNameEL= tk.Entry(ttop, textvariable = MMNam,width=40)  # The entry input
#MMStateEL = tk.Entry(ttop, textvariable = MMSite)    
MMSiteEL = tk.Entry(ttop, textvariable = MMSite,width=45)    


MMCodeLB.grid(row=1, sticky=tk.W)
MMNameLB.grid(row=2, sticky=tk.W)
#MMStateLB.grid(row=3, sticky=tk.W)
MMSiteLB.grid(row=4, sticky=tk.W)
MMInfoLB.grid(row=6,  column=1,sticky=tk.W)


MMCodeEL.grid(row=1, column=1,sticky=tk.W)
MMNameEL.grid(row=2, column=1,sticky=tk.W)
#MMStateEL.grid(row=3, column=1,sticky=tk.W)
MMSiteEL.grid(row=4, column=1,sticky=tk.W)

MMNameEL.focus_set()

def window():
    root.destroy()

       
clrB = tk.Button(tbtn,bg='cyan3', text='Clear',
            command=Clear_entry,width=10)
clrB.grid(column=0, row=4,columnspan=1)  #, sticky=tk.W)
        

def lbl_info(msg):
   MMInfoLB.config(text=msg)

#To Find a record
        
def FindDetails(cNumber):

    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    """
    Returns a entry by the given id
    """
    c.execute(f"SELECT * FROM Merchant_master WHERE MMCode ='{cNumber}'")
    
    return c.fetchone()


    c.close()
    conn.close()
            
#For delete the record
        
def Deletedetails():
    Del_rec=FindDetails(MMCodeEL.get())
    
    if Del_rec is not None:
        conn = sql.connect('creditcarddb.db')
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON')
        conn.commit()

        """
        Delete a entry by the given id
        """
        delsql="Delete from Merchant_master WHERE MMCode='{0}'".format(MMCodeEL.get())
        lbl_info("------Record Deleted------")
        c.execute(delsql)
        conn.commit()
        
        
        Clear_entry()
        c.close()
        conn.close()
    else:
        lbl_info("------Record Not Deleted------")
                
#For Saveing the detail
                            
def SaveDetails():
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    """
    Creates the Table if it does not exist
    """
    
    sqlstr= "CREATE TABLE IF NOT EXISTS Merchant_master(id INTEGER PRIMARY KEY AUTOINCREMENT,MMCode TEXT,MMName TEXT, MMSite TEXT)"

    c.execute(sqlstr)
    
#    customerData = [(None, MMCode.get(), MMNam.get(), MMState.get(), MMSite.get())]
    customerData = [(None, MMCodeEL.get(), MMNameEL.get(), MMSiteEL.get())]
    if Mode:
        for element in customerData:
            
            c.execute("INSERT INTO Merchant_master VALUES (?,?,?,?)", element)
            
        conn.commit()
        lbl_info("--------Saved New Record--------")
        Clear_entry()
    else:

        c.execute("""UPDATE Merchant_master SET MMName='{0}',
                  MMSite={1} WHERE MMCode='{2}' """.format(MMNam.get(), 
                  MMSite.get(),MMCode.get()))
        conn.commit()
        
        lbl_info("--------Saved Updated Record--------")
#        CCNoEL.config(state=tk.NORMAL)
        
    c.close()
    conn.close()

def MMCode_gen():
    MMC_List=[]
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    """
    Select all Code from Merchant master
           
    """
    sqlstr="select MMCode from Merchant_master WHERE Id=( Select MAX(Id) FROM Merchant_master)"

    c.execute(sqlstr)
    conn.commit()

    MMC_List=c.fetchall()
    
    if MMC_List!=[]:
        
        nxtno=MMC_List[0][0]
        nxtno=nxtno[2:]
        nxtno="MM"+ str((int(nxtno)+1))
        return nxtno
    else:
        return "MM1"
    
    c.close()
    conn.close()
        
def on_focus_out(event):
    
#    MMAdd=""
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

#    sqlstr="select TMCode from Trans_master WHERE Id=( Select MAX(id) FROM Trans_master)"
    MMc=MMCodeEL.get()
#    print(MMc)
    sqlstr="select MMName,MMSite from Merchant_master WHERE MMCode='{0}'".format(MMc)
#    print(sqlstr)
    c.execute(sqlstr)

    MMdetail=c.fetchall()

    MMSiteEL.delete(0, END)
    MMNameEL.delete(0, END)
#    print(MMdetail)
    if MMdetail!="":
        MMNameEL.insert(0, MMdetail[0][0])
        MMSiteEL.insert(0, MMdetail[0][1])
    else:        
        MMNameEL.delete(0, END)
        MMSiteEL.delete(0, END)
        
    c.close()
    conn.close()
       
        
#Save Details button
saveCustomerDetails = tk.Button(tbtn,bg='cyan3', width=10,text = "Save Details", command = SaveDetails)
saveCustomerDetails.grid(row=4,column=1,columnspan=1, padx=5)


DelB = tk.Button(tbtn, text='Delete Entry',bg='cyan3', fg='red',
            command=Deletedetails,width=10) 
DelB.grid(column=2, row=4,columnspan=1, padx=5)

ExtB = tk.Button(tbtn, text='Exit',bg='cyan3', fg='red',
            command=window,width=10) 
ExtB.grid(column=3, row=4,columnspan=1, padx=5)

#CCNoEL.focus()

   

def Update_D():
    
    MMDetail=()
    
    if MMCodeEL.get()!="":
        CNo=MMCodeEL.get()
        CNo=int(CNo[2:])-1
        CNo="MM" + str(CNo)
        
        MMDetail=FindDetails(CNo)
#                print(cardDetail)
        if MMDetail is not None:
            
            MMInfoLB.config(text="---------Edit Mode----------")
            Mode=False
            Clear_entry()
#            MMCodeEL.config(state=tk.DISABLED)
            MMNameEL.insert(0,MMDetail[1])
#            MMStateEL.insert(0,MMDetail[2])
            MMSiteEL.insert(0,MMDetail[3])

        else:
            
            MMInfoLB.config(text="---------ADD Mode---------") 
            Mode=True
            Clear_entry()
    
    MMNameEL.focus_set()
#
#
#CCNoEL.bind('<FocusOut>', on_focus_out)
sval=MMCode_gen()
MMCodeEL.config(state=tk.NORMAL)    
MMCodeEL.insert(0,sval)
MMCodeEL.config(state=tk.DISABLED)    


MMCodeEL.bind('<FocusOut>', on_focus_out)

root.mainloop()
    
#        

################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 


