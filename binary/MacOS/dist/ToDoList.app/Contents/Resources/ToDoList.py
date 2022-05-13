#! /usr/local/bin/python3

# ver 0.1.0 

import tkinter as tk
from tkinter import messagebox
import sqlite3 as sq
import re
from datetime import datetime

def Main() -> None:
    pad = 5
    lpad = 2
    done_pad = 1
    head_padx = 30
    content_padx = 100
    list_border = 10
    def Add(mainFrame,root) -> None:
        def sort() -> None:
            cur.execute('select * from ToDoList')
            table = cur.fetchall()
            for i in range(len(table)-1):
                for j in range(len(table)-2,i-1,-1):
                    if table[j][3] > table[j+1][3]:
                        temp = table[j]
                        table[j] = table[j+1]
                        table[j+1] = temp
                    elif table[j][3] == table[j+1][3]:
                        if table[j][4] > table[j+1][4]:
                            temp = table[j]
                            table[j] = table[j+1]
                            table[j+1] = temp    
                        elif table[j][4] == table[j+1][4]:
                            if table[j][5] > table[j+1][5]:
                                temp = table[j]
                                table[j] = table[j+1]
                                table[j+1] = temp    
            cur.execute('DELETE FROM ToDoList')
            for i in table:
                cur.execute('insert into ToDoList (Head,Contents,Year,Month,Date) values (?,?,?,?,?)' , [i[1] , i[2] , i[3] , i[4] , i[5]])
        def func_ok() -> None:
            flag=True
            header = headerText.get()
            contents = contentsText.get()
            deadline = deadlineText.get()
            if deadline == '':
                year = 9999
                month = 00
                day = 00
            else:
                deadline = re.sub('\D' , '-' , deadline)
                try:
                    deadline = datetime.strptime(deadline, '%Y-%m-%d')
                    year = deadline.year
                    month = deadline.month
                    day = deadline.day
                
                except :
                    messagebox.showerror('value error','value of deadline error!')
                    flag=False
            
            if flag:
                cur.execute('insert into ToDoList (Head,Contents,Year,Month,Date) values (?,?,?,?,?)' , [header , contents , year , month , day])
                    
                messagebox.showinfo('Add ToDoList' , 'Insert into ToDoList\nheader : '+header+'\ncontents : '+contents+'\ndeadline : '+str(month)+'/'+str(day))
                
                sort()
                
                func_cancel()
            
        def func_cancel() -> None:
            mainFrame.destroy()
            CreateMainWindow()    
            
        mainFrame.destroy()
        
        mainFrame = tk.Frame(root)
        titleFrame = tk.Frame(mainFrame , bg = 'cyan4')
        labelFrame = tk.Frame(mainFrame)
        entryFrame = tk.Frame(mainFrame)
        buttonFrame = tk.Frame(mainFrame , bg = 'dark slate gray')
        
        title = tk.Label(titleFrame , text = 'Add manu' , bg = 'cyan4')
        header = tk.Label(labelFrame , text = 'Heading')
        contents = tk.Label(labelFrame , text = 'Contents')
        deadline = tk.Label(labelFrame , text = 'Deadline')
        
        headerText =  tk.StringVar()
        contentsText = tk.StringVar()
        deadlineText = tk.StringVar()
        
        headerEntry = tk.Entry(entryFrame , textvariable = headerText)
        contentsEntry = tk.Entry(entryFrame , textvariable = contentsText)
        deadlineEntry = tk.Entry(entryFrame , textvariable = deadlineText)
        
        ok = tk.Button(buttonFrame , text = 'OK' , command = func_ok , highlightbackground = 'dark slate gray')
        cancel = tk.Button(buttonFrame , text = 'Cancel' , command = func_cancel , highlightbackground = 'dark slate gray')
        
        title.pack(fill = tk.X , expand = True ,pady = lpad , padx = lpad)
        header.pack(side = tk.TOP , anchor = tk.W , fill = tk.BOTH , expand = True)
        headerEntry.pack(side = tk.TOP , fill = tk.X , expand = True , padx = pad)
        contents.pack(side = tk.TOP , anchor = tk.W , fill = tk.BOTH , expand = True)
        contentsEntry.pack(side = tk.TOP , fill = tk.X , expand = True , padx = pad)
        deadline.pack(side = tk.TOP , anchor = tk.W , fill = tk.BOTH , expand = True)
        deadlineEntry.pack(side = tk.TOP , fill = tk.X , expand = True , padx = pad)
        cancel.pack(side = tk.LEFT , fill = tk.X , expand = True , pady = pad , padx = pad)
        ok.pack(side = tk.RIGHT , fill = tk.X , expand = True , pady = pad , padx = pad)
        
        titleFrame.pack(side = tk.TOP, fill = tk.X)
        buttonFrame.pack(side = tk.BOTTOM , fill = tk.X)
        labelFrame.pack(side = tk.LEFT , fill = tk.Y , padx = pad)
        entryFrame.pack(side = tk.RIGHT , fill = tk.BOTH , expand = True)
        mainFrame.pack(fill = tk.BOTH , expand = True)
        
    def finish(mainFrame,root) -> None:
        def func_ok() -> None:
            doneList=[]
            for i in table:
                if booleanVer[i].get():
                    doneList.append(i)
            if doneList == []:
                messagebox.showerror('no select' , 'please select content(s)')
            else:
                text = ''
                for i in doneList:
                    text=text+i[1]+'\n'
                result = messagebox.askyesno('confirm' , 'Are you finished task(s)?\n'+text)
                if result: 
                    for i in doneList:
                        cur.execute('DELETE FROM ToDoList WHERE id = ?',[i[0]])
                    messagebox.showinfo('finish task(s)' , 'Remove task(s) from ToDoList')
                    mainFrame.destroy()
                    func_cancel()
                        
        def func_cancel() -> None:
            mainFrame.destroy()
            CreateMainWindow()  
            
        mainFrame.destroy()
        mainFrame = tk.Frame(root)
        titleFrame = tk.Frame(mainFrame , bg = 'blue4')
        displayFrame = tk.Frame(mainFrame)
        canvas = tk.Canvas(displayFrame , height = 900)
        scroll_y = tk.Scrollbar(displayFrame, orient="vertical", command=canvas.yview)
        canvasFrame = tk.Frame(canvas)
            
        buttonFrame = tk.Frame(mainFrame , bg = 'dark slate gray')
        addButton = tk.Button(buttonFrame , text='OK' , command = func_ok , highlightbackground = 'dark slate gray')
        doneButton = tk.Button(buttonFrame , text='Cancel' , command = func_cancel , highlightbackground = 'dark slate gray') 
            
        cur.execute('select * from ToDoList')
        table = cur.fetchall()
        
        headFrame = tk.Frame(canvasFrame , bg = 'black')
        contentFrame = tk.Frame(canvasFrame , bg = 'black')
        deadLineFrame = tk.Frame(canvasFrame , bg = 'black')
        
        title = tk.Label(titleFrame , text = 'Finish manu' , bg = 'blue4')
        head = tk.Label(headFrame , text = 'Heading' , borderwidth = list_border)
        content = tk.Label(contentFrame , text = 'Contents' , borderwidth = list_border)
        deadLine = tk.Label(deadLineFrame , text = 'Deadline' , borderwidth = list_border)
        title.pack(fill = tk.X , expand = True ,pady = lpad , padx = lpad)
        head.pack(side = tk.TOP , anchor = tk.W , fill = tk.X , expand = True , ipadx = head_padx , pady = lpad , padx = lpad)
        content.pack(side = tk.TOP , anchor = tk.W , fill = tk.X , expand = True , ipadx = content_padx , pady = lpad , padx = lpad)
        deadLine.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad)
          
        booleanVer = {}
            
        for i in table:
            booleanVer[i] = tk.BooleanVar()    
            head = tk.Checkbutton(headFrame , variable=booleanVer[i] , text = i[1])
            content = tk.Label(contentFrame , text = i[2])
            deadLine = tk.Label(deadLineFrame , text = str(i[3])+"/"+str(i[4])+"/"+str(i[5]))
            head.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad , fill = tk.X , expand = True)
            content.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad , ipadx = done_pad , ipady = done_pad , fill = tk.X , expand = True)
            deadLine.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad , ipadx = done_pad , ipady = done_pad , fill = tk.X , expand = True)
                
        titleFrame.pack(side = tk.TOP, fill = tk.X)
        headFrame.pack(side = tk.LEFT , expand = True , fill = tk.X)  
        contentFrame.pack(side = tk.LEFT , expand = True , fill = tk.X)   
        deadLineFrame.pack(side = tk.LEFT)
            
        canvas.create_window(0, 0, anchor='nw', window=canvasFrame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
            
        addButton.pack(side = tk.RIGHT , fill = tk.BOTH , expand = True , padx = pad , pady = pad)
        doneButton.pack(side = tk.LEFT , fill = tk.BOTH , expand = True , padx = pad , pady = pad)                    
        canvas.pack(fill = tk.BOTH , expand = True , side = tk.LEFT)
        scroll_y.pack(fill = 'y' , side = tk.RIGHT)
        buttonFrame.pack(side = tk.BOTTOM , fill = tk.X)
        displayFrame.pack(fill = tk.BOTH , expand = True)
        mainFrame.pack(fill = tk.BOTH , expand = True)
        
    def CreateMainWindow() -> None:
        mainFrame = tk.Frame(root)
        titleFrame = tk.Frame(mainFrame , bg = 'green')
        displayFrame = tk.Frame(mainFrame)
        canvas = tk.Canvas(displayFrame , height = 900)
        scroll_y = tk.Scrollbar(displayFrame, orient="vertical", command=canvas.yview)
        canvasFrame = tk.Frame(canvas)
            
        buttonFrame = tk.Frame(mainFrame , bg = 'dark slate gray')
        addButton = tk.Button(buttonFrame , text='add' , command = lambda : Add(mainFrame,root) , highlightbackground = 'dark slate gray')
        doneButton = tk.Button(buttonFrame , text='finish' , command = lambda : finish(mainFrame,root) , highlightbackground = 'dark slate gray') 
            
        cur.execute('select * from ToDoList')
        table = cur.fetchall()
            
        headFrame = tk.Frame(canvasFrame , bg = 'black')
        contentFrame = tk.Frame(canvasFrame , bg = 'black')
        deadLineFrame = tk.Frame(canvasFrame , bg = 'black')
            
        title = tk.Label(titleFrame , text = 'Main manu' , bg = 'green')
        head = tk.Label(headFrame , text = 'Heading' , borderwidth = list_border)
        content = tk.Label(contentFrame , text = 'Contents' , borderwidth = list_border)
        deadLine = tk.Label(deadLineFrame , text = 'Deadline' , borderwidth = list_border)
        title.pack(fill = tk.X , expand = True ,pady = lpad , padx = lpad)
        head.pack(side = tk.TOP , anchor = tk.W , fill = tk.X , expand = True , ipadx = head_padx , pady = lpad , padx = lpad)
        content.pack(side = tk.TOP , anchor = tk.W , fill = tk.X , expand = True , ipadx = content_padx , pady = lpad , padx = lpad)
        deadLine.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad)
            
        for i in table:       
            head = tk.Label(headFrame , text = i[1])
            content = tk.Label(contentFrame , text = i[2])
            deadLine = tk.Label(deadLineFrame , text = str(i[4])+"/"+str(i[5]))
            head.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad , fill = tk.X , expand = True)
            content.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad , fill = tk.X , expand = True)
            deadLine.pack(side = tk.TOP , anchor = tk.W , pady = lpad , padx = lpad , fill = tk.X , expand = True)
             
        titleFrame.pack(side = tk.TOP, fill = tk.X)   
        headFrame.pack(side = tk.LEFT , expand = True , fill = tk.X)  
        contentFrame.pack(side = tk.LEFT , expand = True , fill = tk.X)   
        deadLineFrame.pack(side = tk.LEFT)
            
        canvas.create_window(0, 0, anchor='nw', window=canvasFrame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
            
        addButton.pack(side = tk.RIGHT , fill = tk.BOTH , expand = True , padx = pad , pady = pad)
        doneButton.pack(side = tk.LEFT , fill = tk.BOTH , expand = True , padx = pad , pady = pad)                    
        canvas.pack(fill = tk.BOTH , expand = True , side = tk.LEFT)
        scroll_y.pack(fill = 'y' , side = tk.RIGHT)
        buttonFrame.pack(side = tk.BOTTOM , fill = tk.X)
        displayFrame.pack(fill = tk.BOTH , expand = True)
        mainFrame.pack(fill = tk.BOTH , expand = True)
    
    dbname = 'ToDoList.db'
    conn = sq.connect(dbname)
    cur = conn.cursor()
    cur.execute('select * from sqlite_master')
    table = cur.fetchall()
    if table == []:
        print('no exist table!')
        cur.execute('CREATE TABLE ToDoList(id INTEGER PRIMARY KEY AUTOINCREMENT,Head TEXT,Contents TEXT,Year INTEGER,Month INTEGER,Date INTEGER)')
        print('created table')
    else:
        print('exist table')

    root = tk.Tk()
    root.geometry('600x300')
    root.title('To do list')
        
    CreateMainWindow()
        
    root.mainloop()

    conn.commit()
    conn.close()
        
if __name__ == '__main__':
    Main()