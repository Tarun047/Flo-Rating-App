from tkinter import *
import tkinter as tk
import CryptTools
import Transaction
class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.v=IntVar()
        self.LEVEL = [("Exceptional",5),("Exceed expectations",4),("Meet expectations",3),("Satisfactory",2),("Unsatisfactory",1)]
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.ID_LBL = Label(self,text="Enter an Intern Id: ")
        self.ID_LBL.pack()
        self.RAT_LBL = Label(self,text="Choose a Rating Level")
        self.RAT_LBL.pack()
        for text,num in self.LEVEL:
            Radiobutton(self,text=text,variable=self.v,value = num).pack(anchor=tk.W)
        self.SUBMIT=Button(self,text="Submit",command=self.createChain)
        self.SUBMIT.pack()
        self.QUIT=Button(self,text="Quit",command=self.quit)
        self.QUIT.pack({"side":"bottom"})
    def createChain(self):
        print("Enter number of Interns: ")
        k = int(input())
        out = subprocess.check_output(["flo-cli","--testnet","listunspent"])
        dat = json.loads(out)
        print(type(dat))
    def submit(self):
        pass
#GUI
"""
root = Tk()
root.title("Flo Rating App")
root.geometry('320x240')
app = Application(master=root)
app.mainloop()
"""


key = CryptTools.keyGen()
ct = CryptTools.encryptMsg("HelloTarun",key)
send = ct.encode().hex()
#txid = Transaction.writeDatatoBlockchain(send,"oPXCQNVnzkLRgHqzhz6kWc8XyErSdVhAdn",0.0003)
#recv = Transaction.readDatafromBlockchain(txid)
ct = bytes.fromhex(recv).decode()
pt = CryptTools.decryptMsg(ct,key)
