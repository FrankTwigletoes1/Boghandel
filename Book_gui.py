import tkinter as tk
import tkinter.ttk as ttk
from Book_data import Book, Books_data
from urllib.request import urlopen
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import io
class Book_gui(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        self.data = Books_data(False)
        self.build_GUI()
        self.opdater_tabel()

    def opdater_tabel(self):
        l = self.data.get_book_list(200)

        self.db_view.delete(*self.db_view.get_children())
        for b in l:
        #Funktioner anvendt til at vise titlerne i GUI (self.lbl_titel.configure)
            self.db_view.insert("", tk.END, values=(b.titel, b.forfatter, b.aarstal, b.get_rating(), b.id, b.count))

    def on_book_selected(self, event):

        def ImgUrl(root, url):
            global image
            with urlopen(url) as connection:
                raw_data = connection.read()
            im = Image.open(io.BytesIO(raw_data))
            image = ImageTk.PhotoImage(im)
            return image


        curItem = self.db_view.item(self.db_view.focus())['values']
        
        if len(curItem) > 0:
            b = self.data.get_book(curItem[4])
            #Viste titler i GUI
            self.lbl_titel.configure(text="Titel: {}\nForfatter: {}\nÅrstal: {}\nRating: {:.2f}\nCount: {}".format(b.titel, b.forfatter, b.aarstal, b.get_rating(), b.count))
            self.can.delete("all")
            print(b.ratings[0]/sum(b.ratings))
            print(b.imgurl)
            self.can.create_rectangle(10,190,30,190-200*(b.ratings[0]/sum(b.ratings)))
            widget = tk.Label(root, image=ImgUrl(root,b.imgurl))
            widget.pack()
            

    def slet_bog(self):    
        curItem = self.db_view.item(self.db_view.focus())['values']

        # Sletter bogen
        def delete_book():
            b = Book()
            b.titel = curItem[0]
            b.forfatter = curItem[1]
            b.aarstal = curItem[2]
            b.id = int(curItem[4])
            self.data.slet_bog(b)
            self.opdater_tabel()
            dlg.destroy()
            dlg.update()

        #Ødelægger vinduet
        def close():
            dlg.destroy()
            dlg.update()

        #Viser bogens data i vinduet
        if len(curItem) > 0:
            b = self.data.get_book(curItem[4])

            dlg = tk.Toplevel()
            #Viser tekst af vinduet
            lbl_titel = ttk.Label(dlg, text="Vil du slette " + b.titel + "?\n")
            lbl_titel.grid(column =0, row = 0)
            en_titel = ttk.Entry(dlg)
            #Opstiller knapper "Fortryd og "Bekræft"
            but_annuller = ttk.Button(dlg, text="Fortryd", command=close)
            but_annuller.grid(column=1,row=3)
            but_ok = ttk.Button(dlg, text="Bekræft", command=delete_book)
            but_ok.grid(column=0,row=3)

    def rediger_bog(self):
        def change_book():
            b.titel = en_titel.get()
            b.forfatter = en_forfatter.get()
            self.data.update_book(b)
            b.give_rating(sc_rating.scale.get())
            self.opdater_tabel()
            dlg.destroy()
            dlg.update()

        def close():
            dlg.destroy()
            dlg.update()

        curItem = self.db_view.item(self.db_view.focus())['values']

        if len(curItem) > 0:
            b = self.data.get_book(curItem[4])

            dlg = tk.Toplevel()

            lbl_titel = ttk.Label(dlg, text='Titel')
            lbl_titel.grid(column =0, row = 0)
            en_titel = ttk.Entry(dlg)
            en_titel.grid(column=1, row=0)
            en_titel.delete(0, tk.END)
            en_titel.insert(0, b.titel)

            lbl_forfatter = ttk.Label(dlg, text='Forfatter')
            lbl_forfatter.grid(column =0, row = 1)
            en_forfatter = ttk.Entry(dlg)
            en_forfatter.grid(column=1, row=1)
            en_forfatter.delete(0, tk.END)
            en_forfatter.insert(0, b.forfatter)

            lbl_rating = ttk.Label(dlg, text='Rating')
            lbl_rating.grid(column =0, row = 2)
            sc_rating = ttk.LabeledScale(dlg, from_ = 0, to = 5)
            sc_rating.value = b.get_rating()
            sc_rating.grid(column=1, row=2)

            but_annuller = ttk.Button(dlg, text="Annuller", command=close)
            but_annuller.grid(column=1,row=3)
            but_ok = ttk.Button(dlg, text="Gem ændringer", command=change_book)
            but_ok.grid(column=0,row=3)



    def build_GUI(self):
        right_frame = ttk.Frame(self)
        top_frame = ttk.Frame(right_frame)
        data_frame = ttk.Frame(right_frame)
        knap_frame = ttk.Frame(self)

        self.edit_button = ttk.Button(knap_frame, text="Rediger bog", command=self.rediger_bog)
        self.edit_button.pack(side=tk.LEFT)

        self.del_button = ttk.Button(knap_frame, text="Slet bog", command=self.slet_bog)
        self.del_button.pack(side=tk.LEFT)

        self.db_view = ttk.Treeview(data_frame, column=("column1", "column2", "column3", "column4", "column5", "column6"), show='headings')
        self.db_view.bind("<ButtonRelease-1>", self.on_book_selected)
        self.db_view.heading("#1", text="Titel")
        self.db_view.heading("#2", text="Forfatter")
        self.db_view.heading("#3", text="Årstal")
        self.db_view.heading("#4", text="Rating")
        self.db_view.heading("#5", text="ID")
        self.db_view.heading("#6", text='Count')
        self.db_view["displaycolumns"]=("column1", "column2", "column3", "column4", "column5", "column6")
        ysb = ttk.Scrollbar(data_frame, command=self.db_view.yview, orient=tk.VERTICAL)
        self.db_view.configure(yscrollcommand=ysb.set)
        self.db_view.pack(side = tk.TOP, fill=tk.BOTH)

        #Top Frame
        self.can = tk.Canvas(top_frame, width=200, height=200)
        self.can.grid(column=0, row=0, rowspan=2)

        self.lbl_titel = ttk.Label(top_frame, text='Titel')
        self.lbl_forfatter = ttk.Label(top_frame, text='Forfatter')
        self.lbl_titel.grid(column=0, row=0)
        self.lbl_forfatter.grid(column=0, row=1)

        top_frame.pack(side=tk.TOP)
        data_frame.pack(side = tk.TOP)
        knap_frame.pack(side = tk.LEFT, fill=tk.Y)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.pack()

root = tk.Tk()
root.geometry("1200x500")

app = Book_gui(root)

app.master.title('Bøger')
app.mainloop()
