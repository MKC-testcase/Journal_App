from model.access_database import DB
import datetime as dt
import tkinter as tk
import model.use_config as uc


class JournalEntry:
    def __init__(self):
        # automatically date the journal entry
        self.date = dt.datetime.now().strftime('%Y-%m-%d')
        # 300-character message
        self.message = ""
        config_file = uc.read_database_config()
        self.server_name = config_file['server_name']
        self.database_name = config_file['database_name']
        self.username = config_file['username']
        self.password = config_file['password']

    def set_message(self, journal_entry):
        """Sets the message for the journal entry"""
        self.message = journal_entry

    def open_journal(self):
        """Opens the Journal GUI and gets the information for the journal entry"""
        # Deferring the library import to avoid circular imports
        from view.journal_GUI import JournalApplication

        root = tk.Tk()
        root.title("Journal Application")
        window = JournalApplication(root)
        root.mainloop()
        try:
            text = window.send_text()
        except tk.TclError:
            print("No Message was entered")
            text = ""
        self.set_message(text)
        return

    def archive_entry(self):
        """Sends the message to the database"""
        # Assuming the Journal table in Alexandria with permissions and logins are created
        if self.message == "" or self.message is None:
            # Fail case
            sql_statement = (f"INSERT INTO [ALexandria].[dbo].Journal ([journal_date], [entry]) "
                             f"VALUES('{self.date}', 'No Message')")
        else:
            # Success case
            sql_statement = (f"INSERT INTO [Alexandria].[dbo].Journal ([journal_date], [entry]) "
                             f"VALUES('{self.date}', '{self.message}')")

        db = DB(server_name=self.server_name, database=self.database_name, user_name=self.username,
                password=self.password)
        db.set_connection()
        db.create_cursor()
        if db.query_validation(sql_statement, 4):
            db.send_data(sql_statement)
            db.end_connection()
        else:
            print("There was a error with your message")

    def list_archive(self):
        """Queries the database for the journal table to return all dates found"""
        # lists all the dates archived in the database
        sql_statement = ("SELECT CAST([journal_date] AS DATE)"
                         "FROM [Alexandria].[dbo].[Journal]")
        db = DB(server_name=self.server_name, database=self.database_name, user_name=self.username,
                password=self.password)
        db.set_connection()
        db.create_cursor()
        date_list = db.query_data(sql_statement)
        db.end_connection()
        return date_list

    def get_content(self, date):
        """Given a date to query in the database, returns the day's journal entry"""
        # gets the content from the database that match the date from the input
        # need to make sure that date is not capable of being an avenue of sql injection attack
        sql_statement = (f"SELECT [entry] "
                         f"FROM [Alexandria].[dbo].[Journal] AS J "
                         f"WHERE J.[journal_date] = CAST(\'{date}\' AS DATETIME)")
        print(sql_statement)
        db = DB(server_name=self.server_name, database=self.database_name, user_name=self.username,
                password=self.password)
        db.set_connection()
        db.create_cursor()
        journal_contents = db.query_data(sql_statement)
        db.end_connection()
        return journal_contents


if __name__ == "__main__":
    test = JournalEntry()
    test.open_journal()
    test.archive_entry()