#Notener 1.3

from customtkinter import *
import os
from random import *
from tkinter import PhotoImage
from PIL import Image, ImageTk


#the window
window = CTk()
window.title("Notener")
window.geometry("700x450")
amount_of_notes = 0
set_appearance_mode("dark")

notespath = 'Notes\\'

# Check whether the specified path exists or not
DoesExist = os.path.exists(notespath)
if not DoesExist:
   # Create a new directory because it does not exist
   os.makedirs(notespath)
   print("Successfully created missing notes folder!")


file_data = {}

#store all existing/created widgets
widgets = []
titles = []


# Iterate over all files in the folder
for filename in os.listdir(notespath):
    file_path = os.path.join(notespath, filename)
        
    # Check if the path points to a file (not a directory)
    if os.path.isfile(file_path):
        if filename.endswith('.txt'):
            file_name_without_extension = os.path.splitext(filename)[0]
            print(f"Processing file: {file_path}")
            
        with open(file_path, 'r') as file:
            file_content = file.read()
            file_data[file_name_without_extension] = file_content

for filename, content in file_data.items():
    print(f"File: {filename}")
    print(f"Content: {content}")
    print()

def load_icons():
    global resized_delete_icon
    global resized_create_icon
    global resized_save_icon

    delete_icon = Image.open("delete icon.png")
    create_icon = Image.open("create icon.png")
    save_icon = Image.open("save icon.png")
    new_size = (22, 22)
    resized_delete_icon = delete_icon.resize(new_size, Image.Resampling.LANCZOS)
    resized_delete_icon = ImageTk.PhotoImage(resized_delete_icon)
    #resized_delete_icons.append(resized_delete_icon)

    resized_create_icon = create_icon.resize(new_size, Image.Resampling.LANCZOS)
    resized_create_icon = ImageTk.PhotoImage(resized_create_icon)
    #resized_create_icons.append(resized_create_icon)

    resized_save_icon = save_icon.resize(new_size, Image.Resampling.LANCZOS)
    resized_save_icon = ImageTk.PhotoImage(resized_save_icon)
    #resized_save_icons.append(resized_save_icon)

#load all notes at start
def load():
    global amount_of_notes
    global NewNoteFrame
    global WidgetFrame
    row_state = 0

    WidgetFrame = CTkScrollableFrame(window, fg_color="transparent")
    WidgetFrame.place(relx=0.675, rely=0.5, anchor="center", relwidth=0.625, relheight=0.95)

    for file_name_without_extension, content in file_data.items():
        
        NewTitle = file_name_without_extension
        NewDescription = content
        #NewNoteFrame = CTkFrame(WidgetFrame, fg_color="#252525", height=100, width=410)
        NewNoteFrame = CTkFrame(WidgetFrame, height=100, width=410)
        NewNoteFrame.grid(row=row_state, column=1, pady=3)

        NewNoteFrame.grid_rowconfigure(0, weight=1, minsize=50)
        NewNoteFrame.grid_rowconfigure(1, weight=1, minsize=50)
        NewNoteFrame.grid_columnconfigure(0, weight=1, minsize=360)
        NewNoteFrame.grid_columnconfigure(1, weight=1, minsize=50)

        NewNoteDescription = CTkLabel(NewNoteFrame, text=NewDescription, font=("Outfit", 15, "bold"), wraplength=400, justify="center")
        NewNoteDescription.grid(row=1, column=0, pady=3)

        NewNoteTitle = CTkLabel(NewNoteFrame, text=NewTitle, font=("Outfit", 21, "bold"), text_color="#e1ff5c", wraplength=348, justify="center")
        NewNoteTitle.grid(row=0, column=0, pady=5, padx=7)

        NewNoteDeleteButton = CTkButton(NewNoteFrame, text="", image=resized_delete_icon, command=lambda t=NewNoteTitle,f=NewNoteFrame: delete_note(f, t), fg_color="#ff3c3c", hover_color="#ec1a1a", text_color="#00194e", corner_radius=150, height=10, width=10)
        NewNoteDeleteButton.grid(row=0, column=1, pady=3, padx=8)

        widgets.append(NewNoteFrame)
        titles.append(NewNoteTitle)

        row_state = row_state + 1

        amount_of_notes += 1

#commands
def save_new_note1():
    global amount_of_notes
    global NewNoteFrame

    NewTitle = TitleEntry.get()
    NewDescription = ContentEntry.get()
    if NewTitle == "":
        print("Enter stuff!")
    elif NewDescription == "":
        print("Enter stuff")
    else:
        #NewNoteFrame = CTkFrame(WidgetFrame, fg_color="#252525", height=100, width=410)
        NewNoteFrame = CTkFrame(WidgetFrame, height=100, width=410)
        NewNoteFrame.grid(row=amount_of_notes, column=1, pady=3)

        NewNoteFrame.grid_rowconfigure(0, weight=1, minsize=50)
        NewNoteFrame.grid_rowconfigure(1, weight=1, minsize=50)
        NewNoteFrame.grid_columnconfigure(0, weight=1, minsize=360)
        NewNoteFrame.grid_columnconfigure(1, weight=1, minsize=50)

        NewNoteDescription = CTkLabel(NewNoteFrame, text=NewDescription, font=("Outfit", 15, "bold"), wraplength=400, justify="center")
        NewNoteDescription.grid(row=1, column=0, pady=3)

        NewNoteTitle = CTkLabel(NewNoteFrame, text=NewTitle, font=("Outfit", 21, "bold"), text_color="#e1ff5c", wraplength=348, justify="center")
        NewNoteTitle.grid(row=0, column=0, pady=5, padx=7)

        NewNoteDeleteButton = CTkButton(NewNoteFrame, text="", image=resized_delete_icon, command=lambda t=NewNoteTitle,f=NewNoteFrame: delete_note(f, t), fg_color="#ff3c3c", hover_color="#ec1a1a", text_color="#00194e", corner_radius=150, height=10, width=10)
        NewNoteDeleteButton.grid(row=0, column=1, pady=3, padx=8)

        with open(notespath + f'{NewTitle}.txt', "w") as my_file:
            my_file.write(NewDescription)
        ContentEntry.destroy()
        TitleEntry.destroy()
        CreateNoteButton.configure(text="Create Note", image=resized_create_icon, command=open_creating_settings, fg_color="#40d0ff", hover_color="#00a6ff", text_color="#00194e")
        CreateNoteButton.place(relx=0.18, rely=0.45)
        DeleteAllButton.place(relx=0.18, rely=0.55)

        widgets.append(NewNoteFrame)
        titles.append(NewNoteTitle)

def open_creating_settings():
    global amount_of_notes
    global TitleEntry
    global ContentEntry
    # Iterate directory
    amount_of_notes = sum(1 for item in os.listdir(notespath) if os.path.isfile(os.path.join(notespath, item)))
    New_Name = f"TitleEntry{str(amount_of_notes + 1)}"
    TitleEntry = CTkEntry(window,  placeholder_text="Title your note", corner_radius=15)
    TitleEntry.place(relx=0.18, rely=0.35, relwidth=0.3, relheight= 0.08, anchor="center")
    ContentEntry = CTkEntry(window,  placeholder_text="Enter desired note content", corner_radius=15)
    ContentEntry.place(relx=0.18, rely=0.45, relwidth=0.3, relheight= 0.08, anchor="center")

    CreateNoteButton.configure(text="Save Note", image=resized_save_icon, command=save_new_note1, fg_color="#1cff5a", hover_color="#00d139", text_color="#031a0d")
    CreateNoteButton.place(relx=0.18, rely=0.57)
    DeleteAllButton.place(relx=0.18, rely=0.67)

def remove():
    for NewNoteFrame in widgets:
        NewNoteFrame.destroy()

def delete_all_notes():
    global amount_of_notes
    for f in os.listdir(notespath):
        os.remove(os.path.join(notespath, f))
    remove()
    amount_of_notes = 0

def switch_appearance_mode():
    Current_mode = ModeSwitch_var.get()
    if Current_mode == "off":
        set_appearance_mode("light")
        for NewNoteTitle in titles:
            NewNoteTitle.configure(text_color="#00716f")

    elif Current_mode == "on":
        set_appearance_mode("dark")
        for NewNoteTitle in titles:
            NewNoteTitle.configure(text_color="#e1ff5c")

def delete_note(NewNoteFrame, NewNoteTitle):
    NewNoteFrame.destroy()
    note_name = NewNoteTitle.cget("text")
    file_to_remove = ('Notes\\' + note_name + '.txt')
    os.remove(file_to_remove)

load_icons()
load()

#entitites
CreateNoteButton = CTkButton(window, text="Create Note", image=resized_create_icon, command=open_creating_settings, fg_color="#40d0ff", hover_color="#00a6ff", text_color="#00194e", font=("Outfit", 20, "bold"), corner_radius=15)
DeleteAllButton = CTkButton(window, text="Delete All", image=resized_delete_icon, command=delete_all_notes, fg_color="#ff3c3c", hover_color="#ec1a1a", text_color="#150505", font=("Outfit", 20, "bold"), corner_radius=15)
Label1 = CTkLabel(window, text="Press")
Label2 = CTkLabel(window, text="Press")
ModeSwitch_var = StringVar(value="on")
ModeSwitch = CTkSwitch(window, text="Darkmode", command=switch_appearance_mode, variable=ModeSwitch_var, onvalue="on", offvalue="off", corner_radius=100)
ModeSwitch.place(relx=0.1, rely=0.95, anchor="center")

#place entities
CreateNoteButton.place(relx=0.18, rely=0.45, relwidth=0.3, relheight= 0.08, anchor="center")
DeleteAllButton.place(relx=0.18, rely=0.55, relwidth=0.3, relheight= 0.08,  anchor="center")

#run
window.mainloop()
