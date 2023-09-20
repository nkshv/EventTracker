import calendar
import datetime
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import os, csv



def create_csv_file(filename):
    if not os.path.isfile(filename): ###CHECKS AND CREATES CSV FILE TO UPDATE THE DATA
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["day", "month", "year"])

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def create_event(filename):
    root = tk.Tk()
    root.title("Event tracker")

    root.geometry('450x500+650+250')

    # Create the Calendar widget
    cal = Calendar(root, year=current_year, month=current_month, selectmode='day', showothermonthdays=False, weekendbackground="#F5F5F5", firstweekday='sunday')
    cal.pack(fill="both", expand=True)

    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)
        date_format = "%Y-%m-%d"
        for row in csv_reader:
            print(row[0])
            date = f"{row[2]}-{row[1]}-{row[0]}"
            date_object = datetime.datetime.strptime(date, date_format)
            cal.calevent_create(date_object, "", "")  # Create event (changes day color)

    root.mainloop()



def pick_a_date(filename):    #USER CHOOSES A DATE THROUGH GUI
    def add_event():
        selected_date = cal.get_date()
        data = [selected_date.day, selected_date.month, selected_date.year]
        #day = selected_date.day
        #month = selected_date.month
        #year = selected_date.year
        
        with open(filename, mode="a", newline="") as file:
            print("File_name =", filename)

            writer = csv.writer(file)
            writer.writerow(data)


        print("Selected date:", selected_date)

    date_window = tk.Toplevel(root)
    date_window.title("Choose Date")
    date_window.geometry('500x550+650+250')
    date_window.configure(bg='gray')



    cal = DateEntry(date_window, width=15, background='darkblue',
                    foreground='white', borderwidth=3, year=current_year)
    cal.pack(padx=10, pady=10)

    print_button = tk.Button(date_window, text="Add an Event", command=add_event)
    print_button.pack(padx=10, pady=10)

current_date = datetime.datetime.now()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day

print(current_date)

root = tk.Tk()
root.title("Calendar Project")
root.geometry('500x550+650+250')
root.attributes("-alpha", 0.95)

root.configure(bg='gray') 

def edit_file(file_name):
    # NEEDS WORK
    print("Editing file:", file_name)
    #root.destroy() ###???

    #show_calendar()
    pick_a_date(file_name)

def show_calendar():
    cal = Calendar(year=current_year, month=current_month, selectmode='day', showothermonthdays=False, weekendbackground = "#F5F5F5", firstweekday='sunday')
    cal.calevent_create(current_date, "", "") # CREATES EVENT (CHANGES DAY COLOR)
    cal.pack(fill="both", expand=True)


def create_calendar():
    def get_user_input():
        user_input = entry.get()
        result_label.config(text=f"You entered: {user_input}")

        filename = user_input + '_cl.csv'
        create_csv_file(filename)

        # Close the pop-up window after creating the calendar
        create_window.destroy()

    # Create a new pop-up window for calendar creation
    create_window = tk.Toplevel(root)
    create_window.title("Create Calendar")

    create_window.geometry('500x550+650+250') 

    label = tk.Label(create_window, text="Calendar's name:")
    label.pack()

    entry = tk.Entry(create_window)
    entry.pack()

    submit_button = tk.Button(create_window, text="Submit", command=get_user_input)
    submit_button.pack()

    result_label = tk.Label(create_window, text="")
    result_label.pack()

label_frames = []
def select_a_calendar():
    for label_frame in label_frames:
        label_frame.destroy()
    
    current_directory = os.getcwd()

    all_files = os.listdir(current_directory)
    matching_files = [file for file in all_files if file.endswith("_cl.csv")]

    for file_name in matching_files:
        file_path = os.path.join(current_directory, file_name)
        print("Found:", file_name[0:-7])

        frame = tk.Frame(root)
        frame.pack(side=tk.TOP)
        label_frames.append(frame) 

        label = tk.Label(frame, text= file_name[0:-7] + '  ', font=("Arial", 11, "bold"))
        label.pack(side=tk.LEFT, anchor="center", pady=(10,0))

        delete_button = tk.Button(frame, text=" Delete", command=lambda name=file_name: delete_file(name))
        delete_button.pack(side=tk.RIGHT, padx=5, pady=3)

        edit_button = tk.Button(frame, text="Edit  ", command=lambda name=file_name: edit_file(name))
        edit_button.pack(side=tk.RIGHT, pady=3)

        open_button = tk.Button(frame, text="Open ", command= lambda name=file_name: create_event(name))
        open_button.pack(side=tk.RIGHT, pady=3, padx=5)


create = tk.Button(root, text="Create a new Calendar", command=create_calendar, highlightcolor='red')
create.pack(pady=10)
select = tk.Button(root, text="Show Calendars", command=select_a_calendar)
select.pack()

create.configure(padx=20, pady=10)
select.configure(padx=20, pady=10)


root.mainloop()


#create_event('leitura_cl.csv')
