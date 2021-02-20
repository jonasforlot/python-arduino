
from tkinter import *
######################################################  CREATION D'UN TABLEAU AVEC TKINTER ################################
def tableur(abs,ord,nom_abs,nom_ord,unite_abs,unite_ord):
    root=Tk()
    root.title('Tableur')


    b=Button(root, text=str(nom_abs)+'('+str(unite_abs)+')', width=10)
    b.grid(row=0,column=1,sticky=NSEW)


    b=Button(root, text=str(nom_ord)+'('+str(unite_ord)+')', width=10)
    b.grid(row=0,column=2,sticky=NSEW)


    for m in range(len(abs)):
        b=Button(root, text=str(m+1), width=10)
        b.grid(row=m+1,column=0,sticky=NSEW)



    cols_abs=[]
    for i in range (len (abs)):
        e = Entry(root, justify=CENTER)
        e.grid(row=i+1, column=1, sticky=NSEW)
        e.insert(END, '%.2e'%abs[i])
        cols_abs.append(e)

    cols_ord=[]
    for i in range (len (abs)):
        e = Entry(root, justify=CENTER)
        e.grid(row=i+1, column=2, sticky=NSEW)
        e.insert(END, '%.2e'%ord[i])
        cols_ord.append(e)


    root.mainloop()


# test des fonctions
if __name__ == "__main__":
   
    
    X1=[1,2,3]
    Y1=[1,2,3]
    
    tableur (X1,Y1,'nomX','nomY','unitesx','unitesy')