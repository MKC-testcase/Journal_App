import tkinter as tk
from tkinter import ttk
import re
import controller.Journal.daily_jrn as djr


class JournalApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # Setting up the entire journal GUI
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # message saved in self.insert
        self.insert = ""
        # self.parent becomes the tkinter frame that is provided from outside the class
        self.parent = parent

        # GUI DESIGN BELOW
        # Creating the tab system to separate read and write functions
        tab_control = ttk.Notebook(self.parent)
        # Creating the tabs
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)

        #adding created frames to separate tabs
        tab_control.add(self.tab1, text='Write')
        tab_control.add(self.tab2, text='Read')
        # packing and filling the tabs
        tab_control.pack(expand=1, fill="both")

        # tab1, assigning GUI elements to tab1
        self.intro = tk.Label(master=self.tab1, text="Enter Journal Entry Below (300 characters only)")
        self.textbox = tk.Text(master=self.tab1)
        # adding 2 label to indicate word and character counts
        self.word_count_label = tk.Label(master=self.tab1)
        self.char_count_label = tk.Label(master=self.tab1)
        # button element with command element to submit journal entry to database
        self.enter_entry = tk.Button(master=self.tab1, text="Enter Database", height=3, width=55,
                                     command=self.submit_event)
        # button element with command to exit GUI without adding to Journal
        self.close_app = tk.Button(master=self.tab1, text="Exit", height=3, width=55, command=self.close_window)
        # textbox with key-event that updates work and character counts
        self.textbox.bind('<Key>', self.update_character_count)

        # packing created elements
        self.intro.pack()
        self.textbox.pack(fill="both")
        self.word_count_label.pack(side='top')
        self.char_count_label.pack(side='top')
        self.enter_entry.pack(side='left', fill="both")
        self.close_app.pack(side='right', fill="both")

        # tab2, assigning GUI elements to tab2
        self.read_message = tk.Label(master=self.tab2, text="click on a date to read the entry")
        # major elements created (listbox, contents)
        self.date_listbox = tk.Listbox(master=self.tab2)
        self.contents = tk.Text(master=self.tab2)
        # creating the scrollbar
        self.scrollbar = tk.Scrollbar(master=self.tab2)

        # packing GUI elements
        self.read_message.pack()
        self.contents.pack(side='left', fill='both')
        self.scrollbar.pack(side='right', fill='both')

        # bind listbox via Selecting Listbox Element event to fill textbox with journal entry
        self.date_listbox.bind('<<ListboxSelect>>', self.populate_content)
        self.date_listbox.pack(side='right', fill='both')
        # populates the listbox with dates found in the Journal Entry
        self.populate_scrollbar()

        # attaching the scroll bar to the listbox
        self.date_listbox.config(yscrollcommand=self.scrollbar.set)
        # setting the yview of the listbox to the listbox
        self.scrollbar.config(command= self.date_listbox.yview)

    def update_character_count(self, event):
        """Reads and updates the labels for the word and char count labels"""
        words = self.textbox.get(1.0, "end-1c")
        num_chars = len(words)
        num_words = len(re.findall("\w+", words))
        self.word_count_label.config(text=f"Words: {num_words}")
        self.char_count_label.config(text=f"Characters: {num_chars}")
        return

    # maybe figure out whether I can just insert the item in the main loop so we don't need to exit to enter the entry
    def submit_event(self):
        """Assigns the text value to the insert, so it can be accessed outside the mainloop of the GUI"""
        self.insert = self.textbox.get(1.0, "end-1c")
        self.close_window()

    def close_window(self):
        """Closes the GUI window"""
        self.parent.destroy()

    def send_text(self):
        """Returns the extracted values"""
        return self.insert

    # Functions past this point are used to populate the listbox used to read the journal entries
    def populate_scrollbar(self):
        """ Populates the scroll bar with dates collected from the Journal database """
        journal_data = djr.JournalEntry()
        date_list = journal_data.list_archive()

        for ele in date_list:
            curr_date = ele[0].strftime("%Y-%m-%d")
            self.date_listbox.insert('end', curr_date)

    def populate_content(self, virtual_event):
        """ Takes the current date in from listbox selection and returns the content to the textbox """
        # virtual_event is a dummy variable
        print(virtual_event)
        selected = self.date_listbox.curselection()
        # need to trim the selected element from the listbox
        print(selected)
        if selected == ():
            return
        journal = djr.JournalEntry()
        content_text = journal.get_content(self.date_listbox.get(selected[0]))
        #try:
        self.contents.delete("1.0", tk.END)
        #except tk.TclError as e:
        #    print(e)
        self.contents.insert(tk.INSERT, content_text)

if __name__ == "__main__":
    root = tk.Tk()
    temp = JournalApplication(root)
    root.mainloop()
    print(temp.send_text())
