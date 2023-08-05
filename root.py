from customtkinter import *
import os
from random import *

#the window
window = CTk()
window.title("Notener")
start_width = 650
window.geometry(f"{start_width}x400")
amount_of_notes = 0

notespath = 'Notes\\'

# Check whether the specified path exists or not
isExist = os.path.exists(notespath)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(notespath)
   print("Successfully created notes folder!")


file_data = {}

#store all existing/created widgets
widgets = []


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

#load all notes at start
def load():
    global amount_of_notes
    global NewNoteFrame

    for file_name_without_extension, content in file_data.items():
        if amount_of_notes <= 3:
            y_value = 0.1412 + (0.24 * amount_of_notes)
            x_value = 0.51
        elif amount_of_notes >= 4:
            y_value = 0.1412 + (0.24 * amount_of_notes) - 0.96
            x_value = 0.83
        
        NewTitle = file_name_without_extension
        NewDescription = content
        NewNoteFrame = CTkFrame(window)
        NewNoteFrame.place(relx=x_value, rely=y_value, relwidth=0.29, relheight= 0.23, anchor="center")

        NewNoteDescription = CTkTextbox(NewNoteFrame, fg_color="transparent", padx=5, pady=5, height=75, activate_scrollbars=False, wrap="word")
        NewNoteDescription.place(relx=0.5, rely=0.6, anchor="center")
        NewNoteDescription.insert("0.0", f"{NewDescription}")
        NewNoteDescription.configure(state="disabled")

        NewNoteTitle = CTkLabel(NewNoteFrame, text=NewTitle, font=("Outfit", 20, "bold"))
        NewNoteTitle.place(relx=0.5, rely=0.15, anchor="center")
        
        NewNoteDescScrollBar = CTkScrollbar(NewNoteFrame, height=0.01)
        NewNoteDescription.configure(yscrollcommand=NewNoteDescScrollBar.set)

        widgets.append(NewNoteFrame)

        amount_of_notes += 1

load()

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
        if amount_of_notes <= 3:
            y_value = 0.1412 + (0.24 * amount_of_notes)
            x_value = 0.51
        elif amount_of_notes >= 4:
            y_value = 0.1412 + (0.24 * amount_of_notes) - 0.96
            x_value = 0.83
        
        NewNoteFrame = CTkFrame(window)
        NewNoteFrame.place(relx=x_value, rely=y_value, relwidth=0.29, relheight= 0.23, anchor="center")

        NewNoteDescription = CTkTextbox(NewNoteFrame, fg_color="transparent", padx=5, pady=5, height=75, activate_scrollbars=False, wrap="word")
        NewNoteDescription.place(relx=0.5, rely=0.6, anchor="center")
        NewNoteDescription.insert("0.0", f"{NewDescription}")
        NewNoteDescription.configure(state="disabled")

        NewNoteTitle = CTkLabel(NewNoteFrame, text=NewTitle, font=("Outfit", 20, "bold"))
        NewNoteTitle.place(relx=0.5, rely=0.15, anchor="center")
        
        NewNoteDescScrollBar = CTkScrollbar(NewNoteFrame, height=0.01)
        NewNoteDescription.configure(yscrollcommand=NewNoteDescScrollBar.set)

        with open(notespath + f'{NewTitle}.txt', "w") as my_file:
            my_file.write(NewDescription)
        ContentEntry.destroy()
        TitleEntry.destroy()
        Button1.configure(text="Create New Note", command=open_creating_settings, fg_color="#1c94ff", hover_color="#0059a8", text_color="#000000")
        Button1.place(relx=0.18, rely=0.45)
        Button2.place(relx=0.18, rely=0.55)

        widgets.append(NewNoteFrame)

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

    Button1.configure(text="Save Note", command=save_new_note1, fg_color="#00ff6c", hover_color="#21a95a", text_color="#003014")
    Button1.place(relx=0.18, rely=0.57)
    Button2.place(relx=0.18, rely=0.67)
    #locals() ["TitleEntry"+ str(amount_of_notes + 1)] = CTkEntry(window)
    #int(New_Name).place(relx=0.18, rely=0.2, relwidth=0.3, relheight= 0.08, anchor="center")
    #print(New_Name)

def remove():
    for NewNoteFrame in widgets:
        NewNoteFrame.destroy()

def delete_all_notes():
    global amount_of_notes
    for f in os.listdir(notespath):
        os.remove(os.path.join(notespath, f))
    remove()
    amount_of_notes = 0


#entitites
Button1 = CTkButton(window, text="Create New Note", command=open_creating_settings, fg_color="#40d0ff", hover_color="#00a6ff", text_color="#00194e", font=("Outfit", 20, "bold"), corner_radius=15)
Button2 = CTkButton(window, text="Delete All", command=delete_all_notes, fg_color="#ff3c3c", hover_color="#ff0f0f", text_color="#150505", font=("Outfit", 20, "bold"), corner_radius=15)
Button2.place(relx=0.18, rely=0.6, relwidth=0.3, anchor="center")
Label1 = CTkLabel(window, text="Press")
Label2 = CTkLabel(window, text="Press")

#place entities
Button1.place(relx=0.18, rely=0.45, relwidth=0.3, relheight= 0.08, anchor="center")
Button2.place(relx=0.18, rely=0.55, relwidth=0.3, relheight= 0.08,  anchor="center")

#run
window.mainloop()
