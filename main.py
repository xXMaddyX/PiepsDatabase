import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs import dialogs
import sqlite3 as sql
import tkinter as tk
import threading
import re

#Main Window Functions
class Main(ttk.Window):
    def __init__(self, *args, **kwargs):
        ttk.Window.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.title("Piep´s DB")
        self.place_window_center()
#-------------------------------------------------------------------------------------------------------------------------------------------------------

        #Custom Font
        self.my_fond = ttk.font.Font(size="16")
#-------------------------------------------------------------------------------------------------------------------------------------------------------

        #Button and label Packs
        self.header = ttk.Label(self, background="grey", foreground="black")
        self.header.pack(side="top", fill="x")

        self.header_text = ttk.Label(self.header, text="Piep´s Datenbank", foreground="black", background="grey", font=self.my_fond, justify='center')
        self.header_text.pack()

        self.button_frame = ttk.Labelframe(self, text="Datenbank Funktionen", border=20)
        self.button_frame.pack(side="left", anchor="nw", fill="y", padx=5, pady=5)

        self.create_db_button = ttk.Button(self.button_frame, width=30, text="Datenbank Erstellen", command=self.call_table_creator)
        self.create_db_button.pack(side="top")

        self.load_db_button = ttk.Button(self.button_frame, width=30, text="Datenbank Laden", command=self.ask_on_db_load)
        self.load_db_button.pack(side="top", pady=5)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #Threads for Toplevels
    def ask_on_db_load(self):
        self.db_load = threading.Thread(target=LoadDb)
        self.db_load.start()

    def call_table_creator(self):
            self.table_thread = threading.Thread(target=Table_create)
            self.table_thread.start()
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    #Thoast Messages (ERROS AND Succsesses)
    def toast_call_data_ok(self):
        toast = ToastNotification(
            title="Daten Übertragen",
            message="Daten wurden erfolgreich Übertragen",
            duration=3000,
            bootstyle="success",
            alert = True
            )
        toast.show_toast()

    def toast_call_data_error(self):
        toast = ToastNotification(
            title="Fehler",
            message="Bitte beachte die eingabe Parameter, oder Daten schon vorhanden",
            duration=3000,
            bootstyle="danger",
            alert = True
            )
        toast.show_toast()
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_table_data(self):
        pass
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Create Database and Table Window
class Table_create(ttk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.geometry("300x350")
        self.maxsize(300, 350)
        self.minsize(300, 350)
        self.title("Table Erstellen")
        self.place_window_center()
#-------------------------------------------------------------------------------------------------------------------------------------------------------

        #Buttons and Entrys of Table Create Window
        self.head_info_label = ttk.Label(self, text="Datanbank und Table Erstellen", foreground="black", background="grey", width=50, anchor="n")
        self.head_info_label.grid(columnspan=5)

        self.input_database_name_lable = ttk.Label(self, text="Datenbank Datei Name", padding="10")
        self.input_database_name_lable.grid(row=1, column=0)
        self.input_database_name_entry = ttk.Entry(self, bootstyle="danger")
        self.input_database_name_entry.grid(row=1, column=1)

        self.input_table_name_entry_label = ttk.Label(self, text="Table Name", padding="10")
        self.input_table_name_entry_label.grid(row=2, column=0, ipady=10)
        self.input_table_name_entry = ttk.Entry(self, bootstyle="Danger")
        self.input_table_name_entry.grid(row=2, column=1, padx=5)
        
        self.input_item_spalte1_label = ttk.Label(self, text="Spalte1", padding="10")
        self.input_item_spalte1_label.grid(row=3, column=0)
        self.input_table_spalte1_entry = ttk.Entry(self, bootstyle="primary")
        self.input_table_spalte1_entry.grid(row=3, column=1, padx=5)

        self.input_item_spalte2_label = ttk.Label(self, text="Spalte2", padding="10")
        self.input_item_spalte2_label.grid(row=4, column=0)
        self.input_table_spalte2_entry = ttk.Entry(self, bootstyle="primary")
        self.input_table_spalte2_entry.grid(row=4, column=1, padx=5)

        self.input_item_spalte3_label = ttk.Label(self, text="Spalte3", padding="10")
        self.input_item_spalte3_label.grid(row=5, column=0)
        self.input_table_spalte3_entry = ttk.Entry(self, bootstyle="primary")
        self.input_table_spalte3_entry.grid(row=5, column=1, padx=5)

        self.input_item_spalte4_label = ttk.Label(self, text="Spalte4", padding="10")
        self.input_item_spalte4_label.grid(row=6, column=0)
        self.input_table_spalte4_entry = ttk.Entry(self, bootstyle="primary")
        self.input_table_spalte4_entry.grid(row=6, column=1, padx=5)


        self.ok_button = ttk.Button(self, text="Erstellen", width="18", command=self.ok_button_get_data)
        self.ok_button.grid(row=7, column=1, pady=35)

        self.cancel_button = ttk.Button(self, text="Abbrechen", width="18", command=self.close_table_popup)
        self.cancel_button.grid(row=7, column=0)
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    def close_table_popup(self):
        app.table_thread.join()
        result = app.table_thread.is_alive()
        print(result)
        self.destroy()

    def ok_button_get_data(self):
        self.db_file_name = self.input_database_name_entry.get()
        self.table_data = self.input_table_name_entry.get()
        self.spalte1_data = self.input_table_spalte1_entry.get()
        self.spalte2_data = self.input_table_spalte2_entry.get()
        self.spalte3_data = self.input_table_spalte3_entry.get()
        self.spalte4_data = self.input_table_spalte4_entry.get()
        self.tab_data = self.spalte1_data, self.spalte2_data, self.spalte3_data, self.spalte4_data
        self.con = sql.connect(f'{self.db_file_name}.db')
        self.cur = self.con.cursor()
        self.set_table_data(self.table_data, self.tab_data)

    #Check for Valid Entry
    def is_valid_entry(self, data):
        return re.match("^[a-zA-Z][a-zA-Z0-9_]*$", data)

        
    def set_table_data(self, table_name, tab_data):
        if not self.is_valid_entry(table_name) or not all(self.is_valid_entry(column) for column in tab_data):
            return

        a, b, c, d = tab_data
        print(a,b,c,d)
        try:
            self.cur.execute(f"CREATE TABLE {table_name}({a}, {b}, {c}, {d})")
            app.toast_call_data_ok()
        except:
            app.toast_call_data_error()
        self.con.commit()
        self.con.close()
        self.destroy()
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Database Load Popup
class LoadDb(ttk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.geometry("250x170")
        self.maxsize(250, 170)
        self.minsize(250, 170)
        self.title("Load DB")
        self.place_window_center()
#-------------------------------------------------------------------------------------------------------------------------------------------------------

        #Buttons and Entrys
        self.load_db_window = ttk.Labelframe(self, text="Datenbank Name eintragen")
        self.load_db_window.pack(side="top", fill="both", padx=5, pady=5)

        self.input_database_name_entry = ttk.Entry(self.load_db_window, bootstyle="danger", width=30)
        self.input_database_name_entry.pack(side="top", pady=20, )

        self.ok_button = ttk.Button(self.load_db_window, text="Bestätigen", command=self.get_db_data)
        self.ok_button.pack(anchor="center", fill="y", pady=20)
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_db_data(self):
        app.db_load.join()
        app.db_load.is_alive()
        self.destroy()
#-------------------------------------------------------------------------------------------------------------------------------------------------------


#Main Function 
if __name__ == "__main__":
    app = Main(themename="superhero")
    app.mainloop()