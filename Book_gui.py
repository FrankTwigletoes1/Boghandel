import tkinter as tk
import tkinter.ttk as ttk
from Book_data import Book, Books_data
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
import csv


class storeIMG():
    def _init_(self, image = None):
        self.image = image


class Book_gui(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.imgS = storeIMG()
        self.data = Books_data(False)
        self.build_GUI()
        self.opdater_tabel()

    #opdater_tabel opdaterer tabellen, men også indeholder funktionen for søgning.
    def opdater_tabel(self):
        s_text = self.search_entry.get()

        self.db_view.delete(*self.db_view.get_children())

        for b in self.data.get_book_list(200):
            if s_text:
                idx = b.titel.lower().find(s_text)

                if idx < 0: continue

           
            self.db_view.insert("", tk.END, values=(b.titel, b.forfatter, b.aarstal, b.get_rating(), b.id, b.count, str(b.get_pris()) + " kr."))

    def on_book_selected(self, event):

        curItem = self.db_view.item(self.db_view.focus())['values']

        if len(curItem) > 0:

            #Virker nu, skal li fixes da den ikke sletter det gamle canvas/sted hvor den tegner billedet
            b = self.data.get_book(curItem[4])
            with urlopen(b.imgurl) as connection: 
                raw_data = connection.read()
                print("read data")
            im = Image.open(io.BytesIO(raw_data))
            #print(im)
            self.imgS.image = ImageTk.PhotoImage(im)
            #print(self.imgS.image)
            self.imageWidget.configure(image=self.imgS.image)


 
            self.bog_information.configure(text="Titel: {}\nForfatter: {}\nÅrstal: {}\nRating: {}\nCount: {}".format(b.titel, b.forfatter, b.aarstal,b.get_rating(), b.count))
            self.can.delete("all")
            #print(b.ratings[0]/sum(b.ratings))
            #print(b.imgurl)
            self.can.create_rectangle(10,190,30,190-200*(b.ratings[0]/sum(b.ratings)))

            

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
    
    #Buy History receipt
    def BHR(self):
        #Get Buy History
        def GBH(): 
            with open('data/buy_history.csv', 'r') as reader:
                lines = reader.readlines()
            return lines

        #Close window
        def close():
            BHRTopLevel.destroy()
            BHRTopLevel.update()
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.Y)
        data_frame = ttk.Frame(bottom_frame)
        data_frame.pack(side=tk.TOP, fill=tk.Y)


        BHRTopLevel = tk.Toplevel()
        TLtitel = ttk.Label(BHRTopLevel, text='Købshistorik')
        
        
        self.BH_view = ttk.Treeview(data_frame, column=("column1", "column2", "column3", "column4"), show='headings')
        self.BH_view.heading("#1", text="dsa")
        self.BH_view.heading("#2", text="dsa")
        self.BH_view.heading("#3", text="das")
        self.BH_view.heading("#4", text="das")
        self.BH_view.column("#1", width=50)
        self.BH_view.column("#2", width=50)
        self.BH_view.column("#3", width=50)
        self.BH_view.column("#4", width=50)

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
        
            
        dlg = tk.Toplevel()
        lbl_titel = ttk.Label(dlg, text='Titel')

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

    #Tilføjer til kurven (nedenstående liste/treeview, altså indkøbskurven).
    def add_basket(self):
        curItem = self.db_view.item(self.db_view.focus())['values'] # Vælger værdierne for den nuværende markeret bog
        
        # Hvis der er blevet valgt en bog at tilføje
        if len(curItem) > 0:
            b = self.data.get_book(curItem[4]) # Finder informationen vedrørende den nuværende bog
            self.samlet_pris += b.get_pris() # Opdatere den samlet pris
            self.buy_view.insert("", tk.END, values=(b.id, b.titel, b.count, str(b.get_pris()) + " kr.")) # Tilføjer bogen til 'buy_view' listen

        # Opdatere den samlet pris ediketen
        self.label_samlet_pris.configure(text="Samlet pris: " + str(self.samlet_pris) + " kr.")

    def buy(self):
        #print(b.titel)
        for line in self.buy_view.get_children():
            buyData = self.buy_view.item(line)['values']
            with open('data/buy_history.csv', 'a', newline='') as csvfile:
                dictNames =  ["bookId", "price", "titel"]
                writer = csv.DictWriter(csvfile, fieldnames=dictNames)
                print(buyData)
                writer.writeheader()
                writer.writerow({'bookId': buyData[0], 'price': buyData[3], 'titel': buyData[1]})
                
        for child in self.buy_view.get_children(): self.buy_view.delete(child)

           
    def build_GUI(self):
        # Variabel definitioner
        self.samlet_pris = 0

        # Frame grid
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.Y)
        knap_frame = ttk.Frame(self)
        knap_frame.pack(side=tk.TOP, fill=tk.Y)
        top_frame = ttk.Frame(bottom_frame)
        top_frame.pack(side=tk.TOP)
        data_frame = ttk.Frame(bottom_frame)
        data_frame.pack(side=tk.TOP, fill=tk.Y)
        buy_frame = ttk.Frame(bottom_frame)
        buy_frame.pack(side=tk.BOTTOM, fill=tk.Y)
        buy_frame_label = ttk.LabelFrame(buy_frame, text="Indkøbskurv")
        buy_frame_label.pack(fill=tk.BOTH)
        buy_frame_list = ttk.Frame(buy_frame_label)
        buy_frame_list.pack(side=tk.RIGHT, fill=tk.Y)
        buy_frame_info = ttk.Frame(buy_frame_label)
        buy_frame_info.pack(side=tk.LEFT, fill=tk.Y)
        self.pack(padx=20, pady=2)
        
        # Buttons
        self.find_button = ttk.Button(knap_frame, text='Find', command=self.opdater_tabel) # Søgeknappen
        self.find_button.pack(side=tk.RIGHT)
        self.search_entry = ttk.Entry(knap_frame) #Søgefeltet
        self.search_entry.pack(side=tk.RIGHT, fill=tk.X, padx=5)
        self.Label_search = ttk.Label(knap_frame, text='Søg:') #'Søg:' teksten
        self.Label_search.pack(side=tk.RIGHT)
        self.edit_button = ttk.Button(knap_frame, text="Rediger bog", command=self.rediger_bog) #Redigeringsknappen
        self.edit_button.pack(side=tk.RIGHT, padx=1)
        self.del_button = ttk.Button(knap_frame, text="Slet bog", command=self.slet_bog) #Sletknappen
        self.del_button.pack(side=tk.RIGHT, padx=1)
        self.BHR_button = ttk.Button(knap_frame, text="Købs Historie", command=self.BHR) #Buy History Knappen
        self.BHR_button.pack(side=tk.RIGHT, padx=1)
        self.add_basket_button = ttk.Button(buy_frame_info, text="Tilføj til kurv", command=self.add_basket) #'Tilføj til kurv' knappen
        self.add_basket_button.pack(side=tk.RIGHT, padx=1)
        self.buy_button = ttk.Button(buy_frame_info, text='Køb', command=self.buy) #Købsknappen
        self.buy_button.pack(side=tk.RIGHT, padx=1)
        
        # Treeview information
        self.can = tk.Canvas(top_frame)
        self.bog_information = ttk.Label(top_frame, text="Titel: \nForfatter: \nÅrstal: \nRating: \nCount: \nPris: ")
        self.bog_information.grid(column=0, row=0)

        # Treeview booklist
        self.db_view = ttk.Treeview(data_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
        self.db_view.bind("<ButtonRelease-1>", self.on_book_selected)
        self.db_view.heading("#1", text="Titel")
        self.db_view.heading("#2", text="Forfatter")
        self.db_view.heading("#3", text="Årstal")
        self.db_view.heading("#4", text="Rating")
        self.db_view.heading("#5", text="ID")
        self.db_view.heading("#6", text="Count")
        self.db_view.heading("#7", text="Pris")
        self.db_view.column("#3", width=50)
        self.db_view.column("#4", width=50)
        self.db_view.column("#5", width=50)
        self.db_view.column("#6", width=50)
        self.db_view.column("#7", width=50)
        self.db_view["displaycolumns"]=("column1", "column2", "column3", "column4", "column5", "column6", "column7")
        db_scrollbar = ttk.Scrollbar(data_frame, command=self.db_view.yview, orient=tk.VERTICAL)
        db_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.db_view.configure(yscrollcommand=db_scrollbar.set)
        self.db_view.pack(side = tk.TOP, fill=tk.BOTH)

        # Treeview buy (GUI-elementer af indkøbskurven)
        self.buy_view = ttk.Treeview(buy_frame_list, column=("column1", "column2", "column3", "column4"), show='headings')
        #self.buy_view.bind("<ButtonRelease-1>", self.on_book_selected)
        self.buy_view.heading("#1", text="ID")
        self.buy_view.heading("#2", text="Titel")
        self.buy_view.heading("#3", text="Count")
        self.buy_view.heading("#4", text="Pris")
        self.buy_view.column("#1", width=50)
        self.buy_view.column("#3", width=50)
        self.buy_view.column("#4", width=50)
        self.buy_view["displaycolumns"]=("column1", "column2", "column3", "column4")
        db_scrollbar = ttk.Scrollbar(buy_frame_list, command=self.buy_view.yview, orient=tk.VERTICAL)
        db_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.buy_view.configure(yscrollcommand=db_scrollbar.set)
        self.buy_view.pack(side=tk.TOP, pady=1, fill=tk.BOTH)
        self.label_samlet_pris = ttk.Label(buy_frame_info, text="Samlet pris: 0 kr.")
        self.label_samlet_pris.pack(side=tk.BOTTOM)


        #create image label
        self.imageWidget = tk.Label(root, image=None)
        self.imageWidget.pack()

        ####################################################################
        #items = ["Titel", "Forfatter", "Årstal", "Rating", "ID", "Count"]
        #x = 0
        #for x in items: 
        #    n += 1
        #    self.db_view.heading(("#", n), text=x)
        #####################################################################

root = tk.Tk()
root.geometry("800x600")
app = Book_gui(root)
app.master.title('Bøger')
app.mainloop()