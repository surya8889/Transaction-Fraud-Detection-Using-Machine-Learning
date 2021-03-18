import tkinter as tk
from tkinter import ttk, LEFT, END
from tkcalendar import DateEntry
from operator import itemgetter
import pickle
import time

import numpy as np

import sqlite3 as sql

global proc_Mode 
##############################################+=============================================================

root = tk.Tk()

root.geometry("800x500+300+100")
root.title("Trasection Card Master")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)


ttop = tk.Frame(root, width=50,bg='khaki2', height=50, pady=4)
ttop.grid(row=0, column=0, sticky=tk.NSEW)

tbtn = tk.Frame(root, width=50,bg='khaki2', height=50, pady=4)
tbtn.grid(row=1, column=0, sticky=tk.NSEW)

#TM_Status 0 means Fraud trasection 1 means valid transection
State_Name={"Gujarat":0,"Hyderabad":1,"Karnataka":2,"Maharashtra":3,"Punjab":4}

def window():
    root.destroy()

#430
#lbl = tk.Label(root, text="Merchant Master", font=('times', 35,' bold '), height=1, width=30,bg="seashell2",fg="indian red")
#lbl.place(x=430, y=5)

#Create string variables
TMCode =tk.StringVar()
TMMCode=tk.StringVar()
TMMName=tk.StringVar()
TMState=tk.IntVar()
TMMSite=tk.StringVar()
Trans_Amt=tk.DoubleVar()
TCCNo=tk.StringVar()
TCCPin=tk.StringVar()
TM_Status=tk.IntVar()
#proc_Mode=tk.BooleanVar()
global proc_Mode

Mode=tk.BooleanVar()

TMCode =""
TMMCode=""
TMMName=""
TMState=""
TMMSite=""
Trans_Amt=0
TCCNo=""
TCCPin=""
TM_Status=""

proc_Mode=False

###########################################################################################################

def result_lblinfo(txtM):
    TMInfoLB.config(text=txtM)

def lbl_info(msg):
           ProcInfoLB.config(text=msg)
           
def Clear_entry():
    
    TMCodeEL.delete(0, END)
    TMMSiteEL.delete(0, END)
    Trans_AmtEL.delete(0, END)
    TCCNoEL.delete(0, END)
    TCCPinEL.delete(0, END)
    TMStateEL.current(0)
    TMMNameEL.current(0)
    ProcInfoLB.config(text='----------------------Information-----------------------')
    TMInfoLB.config( text='-------------------------Result--------------------------')

    TCode=TMCode_gen()
    TMCodeEL.config(state=tk.NORMAL)
    TMCodeEL.delete(0, END)    
    TMCodeEL.insert(0,TCode)
    TMCodeEL.config(state=tk.DISABLED)
    
    TMMSiteEL.focus_set()



def Cmbo1_value():
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    Sqlstr = "Select MMName,Id From Merchant_master"

    c.execute(Sqlstr)
    
    val_all= c.fetchall()
    
#    Convert into dict
    di=dict(val_all)
    c.close()
    conn.close()
    return di

Shop_CodeNam=Cmbo1_value()

def TMCode_gen():
    TMC_List=[]
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

#    sqlstr="select TMCode from Trans_master WHERE Id=( Select MAX(id) FROM Trans_master)"
    sqlstr="select TMCode from Tamp_master WHERE id=( Select MAX(id) FROM Tamp_master)"
    
    c.execute(sqlstr)

    TMC_List=c.fetchall()
    print(TMC_List)
    if TMC_List!=[]:
        
        nxtno=TMC_List[0][0]
        nxtno=nxtno[2:]
        nxtno="TM"+ str((int(nxtno)+1))
        return nxtno
    else:
        return "TM1"
    
    c.close()
    conn.close()

def check_site():
    SAdd=TMMSiteEL.get()

    if SAdd=="":
        lbl_info("Please Enter Site Address....")
        TMMSiteEL.focus_set()
        return False

    elif SAdd[:5]=='https':
        lbl_info("Safe Site to Shop with....")
        return True
    
    else:
        
        lbl_info("Not a Safe site....")
        TMMSiteEL.focus_set()
        return False
    
def Chk_Cno(CN,CP):
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    Sqlstr = "Select Cardno,pin From Card_master WHERE Cardno='{0}'".format(CN)

    c.execute(Sqlstr)
    
    CCNo= c.fetchone()
    
    if CCNo[0]!="":
        
        if CP==CCNo[1]:
            msg= "Card details Valid"
            Mode_V=True
        else:
            msg= "Pin is not Correct"
            Mode_V=False
    else:
        
        msg= "Please Check your Card no"
        Mode_V=False
    
    c.close()
    conn.close()
    
    return msg,Mode_V

def chk_Amt(CNo,Ent_Bal):
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    Sqlstr = "Select balance,status From Card_master WHERE Cardno='{0}'".format(CNo)

    c.execute(Sqlstr)

    Tot_bal= c.fetchone()
    
    if Tot_bal[0]!=0:
        
        if int(Ent_Bal) > int(Tot_bal[0]):
            msg= "Balance is not sufficient"
            Mode_V=False
        else:
            msg= "Purchase value is Correct"
            Mode_V=True
    else:
        
        msg= "Deactive Card .....Please Use another card."
        Mode_V=False
    
    c.close()
    conn.close()
    
    return msg,Mode_V
    
def proc_detail():
    
    global proc_Mode 
    CCN=TCCNoEL.get()
    CCP=TCCPinEL.get()
    
    print(TCCNoEL.get())
    if check_site():
        if CCN !="" and CCP !="":
            NextM,Mvalue=Chk_Cno(TCCNoEL.get(),TCCPinEL.get())
            lbl_info(NextM)
            if Mvalue:
                infoM,BMode=chk_Amt(TCCNoEL.get(),Trans_AmtEL.get())
                if BMode:
                    lbl_info(infoM)
                    proc_Mode= True
                else:
                    lbl_info(infoM)
                    Trans_AmtEL.focus_set()
                    proc_Mode= False
            else:
                TCCNoEL.focus_get()
        else:
            lbl_info("Please Enter Details...")
            TCCNoEL.focus_get()
#            print("True")
    
def Model_test(list_val):
    with open('clf_SVM.pkl', 'rb') as f:
        clf_DST = pickle.load(f)
    
#    Predict_to_value=np.array([1,15,1,1000])
    Predict_to_value=np.array(list_val)

    Predict_to_value=Predict_to_value.reshape(1, -1)
    Predict_get_value=clf_DST.predict(Predict_to_value)
    print(Predict_get_value)

    return Predict_get_value

def get_cardid(nos):
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

    Sqlstr = "Select Id From card_master where cardno='{0}'".format(nos)

    c.execute(Sqlstr)
    
    id_val= c.fetchone()
    
    c.close()
    conn.close()
    
    return id_val
    
def SaveDetails():
    Val_set=[]
    global proc_Mode 
    print(proc_Mode)
    if proc_Mode :
#            [1,15,1,1000])
        
        id_V=get_cardid(TCCNoEL.get())
        Val_set=[int(id_V[0]),int(Shop_CodeNam[TMMNameEL.get()]),int(State_Name[TMStateEL.get()]),int(Trans_AmtEL.get())]

        fake_not=Model_test(Val_set)
        
        conn = sql.connect('creditcarddb.db')
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON')
        conn.commit()
    
        """
        Creates the Table if it does not exist
        """
        
        sqlstr= "CREATE TABLE IF NOT EXISTS Tamp_master(id INTEGER PRIMARY KEY AUTOINCREMENT,TMCode TEXT , TMMName INTEGER, TMMState INTEGER, TMMSite TEXT, Trans_Amt FLOAT,TCCNo TEXT,TCCPin TEXT,TM_Status INTEGER)"
    
        c.execute(sqlstr)
#        print(fake_not[0])   
#        print(fake_not)
        
        if fake_not==1:
            
            print(proc_Mode)

            #TM_Status 0 means Fraud trasection 1 means valid transection
            #State_Name[TMStateEL.get()]
            #Shop_CodeNam[TMMNameEL.get()]
            
            transData = [(None,TMCodeEL.get(), Shop_CodeNam[TMMNameEL.get()], State_Name[TMStateEL.get()], TMMSiteEL.get(),Trans_AmtEL.get(),TCCNoEL.get(),TCCPinEL.get(),1)]
            
            for element in transData:
                
                c.execute("INSERT INTO Tamp_master VALUES (?,?,?,?,?,?,?,?,?)", element)
            
            time.sleep(16)
            
            result_lblinfo("Transaction Successfully done!! AS Genuine ENTRY<<======")
            
        else:

            transData = [(None,TMCodeEL.get(), Shop_CodeNam[TMMNameEL.get()], State_Name[TMStateEL.get()], TMMSiteEL.get(),Trans_AmtEL.get(),TCCNoEL.get(),TCCPinEL.get(),0)]
            
            for element in transData:
                
                c.execute("INSERT INTO Tamp_master VALUES (?,?,?,?,?,?,?,?,?)", element)
                
            time.sleep(19)
            
            result_lblinfo("Transaction done!! AS FAKE ENTRY<<======")
            
        conn.commit()
#        Clear_entry()
    else:
        result_lblinfo("Transaction Pending ..Please Check the details")
        
                    
def on_focus_out(event):
    
    MMAdd=""
    
    conn = sql.connect('creditcarddb.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()

#    sqlstr="select TMCode from Trans_master WHERE Id=( Select MAX(id) FROM Trans_master)"
    MMc=Shop_CodeNam[TMMNameEL.get()]
#    print(MMc)
    sqlstr="select MMSite from Merchant_master WHERE id={0}".format(MMc)
    
    c.execute(sqlstr)

    MMAdd=c.fetchall()
#    print(MMAdd[0][0])
    TMMSiteEL.delete(0, END)
    if MMAdd!="":
        TMMSiteEL.insert(0, MMAdd[0][0])
    else:
        TMMSiteEL.insert(0, " ")
    
    c.close()
    conn.close()
    
###########################################################################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
###########################################################################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def Cmbo1_sel(event):
    selection=Shop_CodeNam[TMMNameEL.get()]  #
    print(selection)

#Shop_Name=[lis[1] for lis in Shop_CodeNam]
#Shop_Name=list(map(itemgetter(1),Shop_CodeNam))

TMMNameEL=ttk.Combobox(ttop,values=list(Shop_CodeNam.keys()),width=40, textvariable = TMMName)
TMMNameEL.state(['readonly'])
TMMNameEL.bind("<<ComboboxSelected>>", Cmbo1_sel)  #lambda event: print(Shop_CodeNam.keys()))
TMMNameEL.current(0)




TMStateEL=ttk.Combobox(ttop,values=list(State_Name.keys()),width=40,textvariable = TMState)
TMStateEL.state(['readonly'])
TMStateEL.bind("<<ComboboxSelected>>", lambda event: print(State_Name[TMStateEL.get()]))

TMStateEL.current(0)


#Set up labels
TMCodeLB = tk.Label(ttop, text='Transection Code : ',bg='khaki2')  # More labels =""
#TMMCodeLB = tk.Label(ttop, text='Merchant Code : ',bg='khaki2')  # More labels=""
TMMNameLB = tk.Label(ttop, text='Merchant Name : ',bg='khaki2')  # More labels=""
TMStateLB = tk.Label(ttop, text='State : ',bg='khaki2')  # More labels=""
TMMSiteLB = tk.Label(ttop, text='Address\Site Name: ',bg='khaki2')  # More labels=""
Trans_AmtLB = tk.Label(ttop, text='Purchase Amount : ',bg='khaki2')  # More labels=0
DCoLB0 = tk.Label(ttop, text='----------------',fg='brown',bg='khaki2',font=('times', 18,' bold '))  # ^
DCoLB1 = tk.Label(ttop, text='--------------------------------------------------------------------------------------',fg='brown',bg='khaki2',font=('times', 18,' bold '))  # ^

TCCNoLB = tk.Label(ttop, text='Credit Card No : ',bg='khaki2')  # More labels""
TCCPinLB = tk.Label(ttop, text='PIN : ',bg='khaki2')  # More labels=""

DCoLB2 = tk.Label(ttop, text='----------------',fg='brown',bg='khaki2',font=('times', 18,' bold '))  # ^
DCoLB3 = tk.Label(ttop, text='--------------------------------------------------------------------------------------',fg='brown',bg='khaki2',font=('times', 18,' bold '))  # ^

ClrB = tk.Button(ttop, text='Clear',bg='cyan3', fg='red',command=Clear_entry,width=10) 
ProcB = tk.Button(ttop, text='Process Details',bg='cyan3', fg='red',command=proc_detail,width=15) 

DCoLB4 = tk.Label(ttop, text='----------------',fg='brown',bg='khaki2',font=('times', 18,' bold '))  # ^
DCoLB5 = tk.Label(ttop, text='--------------------------------------------------------------------------------------',fg='brown',bg='khaki2',font=('times', 18,' bold '))  # ^


ProcInfoLB= tk.Label(ttop, text='----------------------Information-----------------------',fg='brown',bg='khaki2',font=('times', 15,' bold '))  # ^


TM_StatusLB = tk.Label(ttop, text='Status : ',bg='khaki2')  # More labels=""


TMInfoLB = tk.Label(ttop, text='------------Result---------------',fg='brown',bg='khaki2',font=('times', 15,' bold '))  # ^


TMCodeLB.grid(row=1, sticky=tk.W)
TMMNameLB.grid(row=2, sticky=tk.W)
TMStateLB.grid(row=3, sticky=tk.W)
TMMSiteLB.grid(row=4, sticky=tk.W)
Trans_AmtLB.grid(row=5, sticky=tk.W)
DCoLB0.grid(row=6, column=0, sticky=tk.W)
DCoLB1.grid(row=6, column=1, sticky=tk.W)

BuyB = tk.Button(ttop, text='Purchase',bg='cyan3', fg='red',command=SaveDetails,width=15) 

TCCNoLB.grid(row=8, sticky=tk.W)
TCCPinLB.grid(row=9, sticky=tk.W)

DCoLB2.grid(row=10, column=0, sticky=tk.W)
DCoLB3.grid(row=10, column=1, sticky=tk.W)

ClrB.grid(column=0, row=11,columnspan=1, padx=5,sticky=tk.W)
ProcB.grid(column=0, row=12,columnspan=1, padx=5,sticky=tk.W)

DCoLB4.grid(row=13, column=0, sticky=tk.W)
DCoLB5.grid(row=13, column=1, sticky=tk.W)


BuyB.grid(column=0, row=15,columnspan=1, padx=5,sticky=tk.W)
ProcInfoLB.grid(column=1,row=12, sticky=tk.W)

#TM_StatusLB.grid(row=15, sticky=tk.W)
TMInfoLB.grid(row=17,  column=1,sticky=tk.W)


####################################################################
#Set up text entry boxes

TMCodeEL = tk.Entry(ttop, textvariable = TMCode)
TMMCodeEL = tk.Entry(ttop, textvariable = TMMCode)
TMMSiteEL = tk.Entry(ttop,width=70, textvariable = TMMSite)
Trans_AmtEL = tk.Entry(ttop, textvariable = Trans_Amt)
TCCNoEL = tk.Entry(ttop, textvariable = TCCNo,width=40)
TCCPinEL = tk.Entry(ttop, textvariable =TCCPin)
TM_StatusEL = tk.Entry(ttop, textvariable = TM_Status)


TMCodeEL.grid(row=1, column=1,sticky=tk.W)
TMMNameEL.grid(row=2, column=1,sticky=tk.W)
TMStateEL.grid(row=3, column=1,sticky=tk.W)
TMMSiteEL.grid(row=4, column=1,sticky=tk.W)
Trans_AmtEL.grid(row=5, column=1,sticky=tk.W)


TCCNoEL.grid(row=8, column=1,sticky=tk.W)
TCCPinEL.grid(row=9, column=1,sticky=tk.W)
#TM_StatusEL.grid(row=15, column=1,sticky=tk.W)

ExtB = tk.Button(tbtn, text='Exit',bg='cyan3', fg='red',
            command=window,width=10) 
ExtB.grid(column=3, row=4,columnspan=1, padx=5)


Clear_entry()

###########################################################################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
###########################################################################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
TMMNameEL.bind('<FocusOut>', on_focus_out)

root.mainloop()