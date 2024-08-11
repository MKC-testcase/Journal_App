# This file centralizes the function in the model, controller, and view
import controller.Journal.daily_jrn as journal_app


if __name__ == "__main__":
    run = journal_app.JournalEntry()
    # opening the Journal
    run.open_journal()
    # archiving the journal entry
    run.archive_entry()
