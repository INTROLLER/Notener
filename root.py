from customtkinter import *
import os
from random import *

#the window
window = CTk()
window.title("Notener")
window.geometry("700x450")
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
    global WidgetFrame
    row_state = 0

    WidgetFrame = CTkScrollableFrame(window)
    WidgetFrame.place(relx=0.675, rely=0.5, anchor="center", relwidth=0.625, relheight=0.95)

    for file_name_without_extension, content in file_data.items():
        
        NewTitle = file_name_without_extension
        NewDescription = content
        NewNoteFrame = CTkFrame(WidgetFrame, fg_color="#252525", height=100, width=410)
        NewNoteFrame.grid(row=row_state, column=1, pady=3)

        NewNoteDescription = CTkTextbox(NewNoteFrame, fg_color="transparent", padx=5, pady=5, width=410, height=75, activate_scrollbars=False, wrap="word")
        NewNoteDescription.place(relx=0.5, rely=0.6, anchor="center")
        NewNoteDescription.insert("0.0", f"{NewDescription}")
        NewNoteDescription.configure(state="disabled")

        NewNoteTitle = CTkLabel(NewNoteFrame, text=NewTitle, font=("Outfit", 20, "bold"))
        NewNoteTitle.place(relx=0.5, rely=0.15, anchor="center")
        
        NewNoteDescScrollBar = CTkScrollbar(NewNoteFrame, height=0.01)
        NewNoteDescription.configure(yscrollcommand=NewNoteDescScrollBar.set)

        widgets.append(NewNoteFrame)

        row_state = row_state + 1

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
        NewNoteFrame = CTkFrame(WidgetFrame, fg_color="#252525", height=100, width=410)
        NewNoteFrame.grid(row=amount_of_notes, column=1, pady=3)

        NewNoteDescription = CTkTextbox(NewNoteFrame, fg_color="transparent", padx=5, pady=5, width=410, height=75, activate_scrollbars=False, wrap="word")
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
        Button1.configure(text="Create New Note", command=open_creating_settings, fg_color="#40d0ff", hover_color="#00a6ff", text_color="#00194e")
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

    Button1.configure(text="Save Note", command=save_new_note1, fg_color="#1cff5a", hover_color="#00d139", text_color="#031a0d")
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
Button2 = CTkButton(window, text="Delete All", command=delete_all_notes, fg_color="#ff3c3c", hover_color="#d60e0e", text_color="#150505", font=("Outfit", 20, "bold"), corner_radius=15)
Button2.place(relx=0.18, rely=0.6, relwidth=0.3, anchor="center")
Label1 = CTkLabel(window, text="Press")
Label2 = CTkLabel(window, text="Press")

#TestLabel = CTkFrame(WidgetFrame, fg_color="#ffffff", height=10)
#TestLabel.grid(row=0, column=0)
#TestLabel2 = CTkFrame(WidgetFrame, fg_color="#ffffff", height=10)
#TestLabel2.grid(row=1, column=0)

#place entities
Button1.place(relx=0.18, rely=0.45, relwidth=0.3, relheight= 0.08, anchor="center")
Button2.place(relx=0.18, rely=0.55, relwidth=0.3, relheight= 0.08,  anchor="center")

#run
window.mainloop()
