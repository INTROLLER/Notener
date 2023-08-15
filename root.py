#Notener 1.9.5

from customtkinter import *
import os
from random import *
from PIL import Image


#the window
window = CTk()
window.title("Notener")
window.geometry("700x450")
amount_of_notes = 0
set_appearance_mode("dark")
window.resizable(False,False)

notespath = 'Notes\\'

window.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, minsize=45)
window.grid_rowconfigure((0, 9), weight=1, minsize=25)
window.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, minsize=70)

# Check whether the specified path exists or not
DoesExist = os.path.exists(notespath)
if not DoesExist:
   # Create a new directory because it does not exist
   os.makedirs(notespath)
   print("Successfully created missing notes folder!")


file_data = {}

#store all existing/created stuff
widgets = []
titles = []
SeparateElements = []
notes_title_data = []
notes_content_data = []

SearchEntry = CTkEntry(window, width=195, height=36, placeholder_text="Search...")

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
    icon_names = ["delete icon", "create icon", "save icon", "rename icon", "edit icon", "cancel icon", "search icon"]
    global resized_icons
    resized_icons = {}

    for name in icon_names:
        icon = Image.open(f"{name}.png")
        new_size = (22, 22)
        resized_icon = CTkImage(light_image = icon, dark_image = icon, size=new_size)
        resized_icons[name] = resized_icon

#load all notes at start
def load():
    global amount_of_notes
    global NewNoteFrame
    global WidgetFrame

    WidgetFrame = CTkScrollableFrame(window, fg_color="transparent", width=413, height=400)
    WidgetFrame.grid(row=1, column=4, rowspan=9, columnspan=7)

    buttons = ["NewNoteDeleteButton", "NewNoteEditButton"]
    labels = ["NewNoteDescription", "NewNoteTitle"]

    search_query = SearchEntry.get().lower()

    for file_name_without_extension, content in file_data.items():
        
        NewTitle = file_name_without_extension
        NewDescription = content

        if search_query and search_query not in NewTitle.lower():
            continue

        NewNoteFrame = CTkFrame(WidgetFrame, height=100, width=410)
        NewNoteFrame.grid(row=amount_of_notes, column=1, pady=3)

        NewNoteFrame.grid_rowconfigure((0, 1, 2), weight=1, minsize=50)
        NewNoteFrame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, minsize=82)

        for label in labels:
            if label == "NewNoteTitle":
                text_=NewTitle
                font_=("Outfit", 21, "bold")
                text_color_="#e1ff5c"
                row_=0
                column_=0
                pady_=3
                columnspan_=5

            elif label == "NewNoteDescription":
                text_=NewDescription
                font_=("Outfit", 15, "bold")
                text_color_=None
                row_=1
                column_=0
                pady_=3
                columnspan_=5
                NewNoteDescription=label

            label1 = CTkLabel(NewNoteFrame,
                                        text=text_,
                                        font=font_,
                                        text_color=text_color_,
                                        wraplength=400,
                                        justify="center")
            label1.grid(row=row_, column=column_, pady=pady_, columnspan=columnspan_)

            if label == "NewNoteTitle":
                titles.append(label1)
                NewNoteTitle = label1
            else:
                NewNoteDescription = label1

        ActionsBackground = CTkFrame(NewNoteFrame, fg_color="#3f3f3f", height=20)
        ActionsBackground.grid(row=2, column=0, columnspan=5, sticky="nesw")

        for button in buttons:
            if button == "NewNoteDeleteButton":
                image_= resized_icons["delete icon"]
                command_ = lambda t=NewNoteTitle,f=NewNoteFrame: delete_note(f, t)
                fg_color_= "#ff3c3c"
                hover_color_= "#ec1a1a"
                row_ = 2
                column_ = 3
                padx_ = 8
            
            elif button == "NewNoteEditButton":
                image_= resized_icons["edit icon"]
                command_ = lambda f=NewNoteTitle, c=NewNoteDescription: edit_note(f, c)
                fg_color_= "#59c8ff"
                hover_color_= "#129fe5"
                row_ = 2
                column_ = 1
                padx_ = 8
                
            button = CTkButton(NewNoteFrame,
                                text="",
                                image=image_,
                                command=command_,
                                fg_color=fg_color_,
                                hover_color=hover_color_,
                                text_color="#00194e",
                                bg_color="#3f3f3f",
                                border_width=0,
                                corner_radius=150,
                                height=10,
                                width=10)
            button.grid(row=row_, column=column_, padx=padx_)

            notes_title_data.append((NewTitle, NewNoteFrame))
            notes_content_data.append((NewDescription, NewNoteFrame))
            SeparateElements.extend([button])

        SeparateElements.extend([ActionsBackground])

        widgets.append(NewNoteFrame)

        amount_of_notes += 1

        sort_notes("Alphabetical A-Z")

#commands
def save_new_note1():
    global amount_of_notes
    global NewNoteFrame

    buttons = ["NewNoteDeleteButton", "NewNoteEditButton"]
    labels = ["NewNoteDescription", "NewNoteTitle"]

    NewTitle = TitleEntry.get()
    NewDescription = ContentEntry.get()
    if NewTitle == "":
        print("Please type in the note title!")
    elif NewDescription == "":
        print("Please type in the note!")
    else:

        NewNoteFrame = CTkFrame(WidgetFrame, height=100, width=410)
        NewNoteFrame.grid(row=amount_of_notes, column=1, pady=3)

        NewNoteFrame.grid_rowconfigure((0, 1, 2), weight=1, minsize=50)
        NewNoteFrame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, minsize=82)

        for label in labels:
            if label == "NewNoteTitle":
                text_=NewTitle
                font_=("Outfit", 21, "bold")
                text_color_="#e1ff5c"
                row_=0
                column_=0
                pady_=3
                columnspan_=5
                NewNoteTitle = label

            elif label == "NewNoteDescription":
                text_=NewDescription
                font_=("Outfit", 15, "bold")
                text_color_=None
                row_=1
                column_=0
                pady_=3
                columnspan_=5
                NewNoteDescription=label

            label1 = CTkLabel(NewNoteFrame,
                                        text=text_,
                                        font=font_,
                                        text_color=text_color_,
                                        wraplength=400,
                                        justify="center")
            label1.grid(row=row_, column=column_, pady=pady_, columnspan=columnspan_)

            if label == "NewNoteTitle":
                titles.append(label1)
                NewNoteTitle = label1
            else:
                NewNoteDescription = label1

        ActionsBackground = CTkFrame(NewNoteFrame, fg_color="#3f3f3f", height=20)
        ActionsBackground.grid(row=2, column=0, columnspan=5, sticky="nesw")

        for button in buttons:
            if button == "NewNoteDeleteButton":
                image_= resized_icons["delete icon"]
                command_ = lambda t=NewNoteTitle,f=NewNoteFrame: delete_note(f, t)
                fg_color_= "#ff3c3c"
                hover_color_= "#ec1a1a"
                row_ = 2
                column_ = 3
                padx_ = 8
            
            elif button == "NewNoteEditButton":
                image_= resized_icons["edit icon"]
                command_ = lambda f=NewNoteTitle, c=NewNoteDescription: edit_note(f, c)
                fg_color_= "#59c8ff"
                hover_color_= "#129fe5"
                row_ = 2
                column_ = 1
                padx_ = 8
                
            button = CTkButton(NewNoteFrame,
                                text="",
                                image=image_,
                                command=command_,
                                fg_color=fg_color_,
                                hover_color=hover_color_,
                                text_color="#00194e",
                                bg_color="#3f3f3f",
                                border_width=0,
                                corner_radius=150,
                                height=10,
                                width=10)
            button.grid(row=row_, column=column_, padx=padx_)

            notes_title_data.append((NewTitle, NewNoteFrame))
            notes_content_data.append((NewDescription, NewNoteFrame))

            SeparateElements.extend([button])

        with open(notespath + f'{NewTitle}.txt', "w") as my_file:
            my_file.write(NewDescription)

        with open(notespath + f'{NewTitle}.txt', 'r') as file:
            file_content = file.read()
            file_data[NewTitle] = file_content
            
        ContentEntry.destroy()
        TitleEntry.destroy()
        CreateNoteButton.configure(text="Create Note", image=resized_icons["create icon"], command=open_creating_settings, fg_color="#40d0ff", hover_color="#00a6ff", text_color="#00194e")
        CreateNoteButton.place(relx=0.18, rely=0.45)
        DeleteAllButton.place(relx=0.18, rely=0.55)

        widgets.append(NewNoteFrame)
        SeparateElements.extend([ActionsBackground])

        sort_notes(SortingDropdown.get())


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

    CreateNoteButton.configure(text="Save Note", image=resized_icons["save icon"], command=save_new_note1, fg_color="#1cff5a", hover_color="#00d139", text_color="#000000")
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
        set_mode = "light"
        set_background_color = "#c5c5c5"
        set_text_color = "#00716f"

    elif Current_mode == "on":
        set_mode = "dark"
        set_background_color = "#3f3f3f"
        set_text_color = "#e1ff5c"

    set_appearance_mode(f"{set_mode}")
    for NewNoteTitle in titles:
        NewNoteTitle.configure(text_color=f"{set_text_color}")

    for key in SeparateElements:
        if isinstance(key, CTkFrame):
            key.configure(fg_color=f"{set_background_color}")
        else:
            key.configure(bg_color=f"{set_background_color}")

def delete_note(NewNoteFrame, file_name):
    NewNoteFrame.destroy()
    note_name = file_name.cget("text")
    file_to_remove = ('Notes\\' + note_name + '.txt')
    os.remove(file_to_remove)

def edit_note(file_name, file_content):
    def destroy_edit_window():
        edit_window.destroy()
    def save_changes():
        new_name = rename_entry.get()
        new_content = edit_content_entry.get()
        with open((notespath + file_name.cget("text") + ".txt"), "w") as f:
            f.write(new_content)
        os.rename((notespath + file_name.cget("text") + ".txt"), (notespath + new_name + ".txt"))
        file_name.configure(text=new_name)
        file_content.configure(text=new_content)
        edit_window.destroy()

    edit_window = CTkToplevel(window)
    edit_window.title("Edit Note")
    edit_window.geometry("350x150")
    edit_window.attributes('-topmost', 'true')

    rename_entry = CTkEntry(edit_window, width=315, height=35, placeholder_text="Rename your note")
    rename_entry.insert(0, file_name.cget("text"))
    edit_content_entry = CTkEntry(edit_window, width=315, height=35, placeholder_text="Edit your note content")
    edit_content_entry.insert(0, file_content.cget("text"))
    save_button = CTkButton(edit_window, text="Save", fg_color="#1cff5a", hover_color="#00d139", text_color="#000000", font=("Outfit", 20, "bold"), command=save_changes, image=resized_icons["save icon"])
    cancel_button = CTkButton(edit_window, text="Cancel", fg_color="#ff3c3c", hover_color="#ec1a1a", text_color="#000000", font=("Outfit", 20, "bold"), command=destroy_edit_window, image=resized_icons["cancel icon"])

    edit_window.rowconfigure((0, 1, 2), weight=1, minsize=50)
    edit_window.columnconfigure((0, 1), weight=1, minsize=82)
    rename_entry.grid(row=0, column=0, columnspan=2)
    edit_content_entry.grid(row=1, column=0, columnspan=2)
    save_button.grid(row=2, column=0)
    cancel_button.grid(row=2, column=1)

def sort_notes(choice):
    if choice == "Alphabetical A-Z":
        # Sort the notes_data based on titles and recreate WidgetFrames in sorted order
        sorted_notes_data = sorted(notes_title_data, key=lambda x: x[0].lower())
        for index, (title, frame) in enumerate(sorted_notes_data):
            frame.grid(row=index, column=1, pady=3)  # Re-grid frames in sorted order

    elif choice == "Alphabetical Z-A":
        # Sort the notes_data based on titles and recreate WidgetFrames in sorted order
        sorted_notes_data = sorted(notes_title_data, key=lambda x: x[0].lower(), reverse=True)
        for index, (title, frame) in enumerate(sorted_notes_data):
            frame.grid(row=index, column=1, pady=3)  # Re-grid frames in sorted order

    elif choice == "Note length (Asc)":
        # Sort the notes_data based on title length and recreate WidgetFrames in sorted order
        sorted_notes_data = sorted(notes_content_data, key=lambda x: len(x[0]))
        for index, (title, frame) in enumerate(sorted_notes_data):
            frame.grid(row=index, column=1, pady=3)  # Re-grid frames in sorted order

    elif choice == "Note length (Desc)":
        # Sort the notes_data based on title length and recreate WidgetFrames in sorted order
        sorted_notes_data = sorted(notes_content_data, key=lambda x: len(x[0]), reverse=True)
        for index, (title, frame) in enumerate(sorted_notes_data):
            frame.grid(row=index, column=1, pady=3)  # Re-grid frames in sorted order

    elif choice == "Title length (Asc)":
        # Sort the notes_data based on title length and recreate WidgetFrames in sorted order
        sorted_notes_data = sorted(notes_title_data, key=lambda x: len(x[0]))
        for index, (title, frame) in enumerate(sorted_notes_data):
            frame.grid(row=index, column=1, pady=3)  # Re-grid frames in sorted order

    elif choice == "Title length (Desc)":
        # Sort the notes_data based on title length and recreate WidgetFrames in sorted order
        sorted_notes_data = sorted(notes_title_data, key=lambda x: len(x[0]), reverse=True)
        for index, (title, frame) in enumerate(sorted_notes_data):
            frame.grid(row=index, column=1, pady=3)  # Re-grid frames in sorted order

def search_notes():
    global amount_of_notes
    search_query = SearchEntry.get().lower()
    buttons = ["NewNoteDeleteButton", "NewNoteEditButton"]
    labels = ["NewNoteDescription", "NewNoteTitle"]

    remove()
    widgets.clear()
    [list.clear() for list in (widgets, SeparateElements, notes_content_data, notes_title_data)]
    amount_of_notes = 0

    for file_name_without_extension, content in file_data.items():
        NewTitle = file_name_without_extension
        NewDescription = content

        if search_query and search_query not in NewTitle.lower():
            continue
        
        NewNoteFrame = CTkFrame(WidgetFrame, height=100, width=410)
        NewNoteFrame.grid(row=amount_of_notes, column=1, pady=3)

        NewNoteFrame.grid_rowconfigure((0, 1, 2), weight=1, minsize=50)
        NewNoteFrame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, minsize=82)

        amount_of_notes += 1

        for label in labels:
            if label == "NewNoteTitle":
                text_=NewTitle
                font_=("Outfit", 21, "bold")
                text_color_="#e1ff5c"
                row_=0
                column_=0
                pady_=3
                columnspan_=5
                NewNoteTitle = label

            elif label == "NewNoteDescription":
                text_=NewDescription
                font_=("Outfit", 15, "bold")
                text_color_=None
                row_=1
                column_=0
                pady_=3
                columnspan_=5
                NewNoteDescription=label

            label1 = CTkLabel(NewNoteFrame,
                                        text=text_,
                                        font=font_,
                                        text_color=text_color_,
                                        wraplength=400,
                                        justify="center")
            label1.grid(row=row_, column=column_, pady=pady_, columnspan=columnspan_)

            if label == "NewNoteTitle":
                titles.append(label1)
                NewNoteTitle = label1
            else:
                NewNoteDescription = label1

        ActionsBackground = CTkFrame(NewNoteFrame, fg_color="#3f3f3f", height=20)
        ActionsBackground.grid(row=2, column=0, columnspan=5, sticky="nesw")

        for button in buttons:
            if button == "NewNoteDeleteButton":
                image_= resized_icons["delete icon"]
                command_ = lambda t=NewNoteTitle,f=NewNoteFrame: delete_note(f, t)
                fg_color_= "#ff3c3c"
                hover_color_= "#ec1a1a"
                row_ = 2
                column_ = 3
                padx_ = 8
            
            elif button == "NewNoteEditButton":
                image_= resized_icons["edit icon"]
                command_ = lambda f=NewNoteTitle, c=NewNoteDescription: edit_note(f, c)
                fg_color_= "#59c8ff"
                hover_color_= "#129fe5"
                row_ = 2
                column_ = 1
                padx_ = 8
                
            button = CTkButton(NewNoteFrame,
                                text="",
                                image=image_,
                                command=command_,
                                fg_color=fg_color_,
                                hover_color=hover_color_,
                                text_color="#00194e",
                                bg_color="#3f3f3f",
                                border_width=0,
                                corner_radius=150,
                                height=10,
                                width=10)
            button.grid(row=row_, column=column_, padx=padx_)

            notes_title_data.append((NewTitle, NewNoteFrame))
            notes_content_data.append((NewDescription, NewNoteFrame))

            SeparateElements.extend([button])
        widgets.append(NewNoteFrame)
        SeparateElements.extend([ActionsBackground])
    sort_notes(SortingDropdown.get())

load_icons()
load()

#entitites
CreateNoteButton = CTkButton(window, text="Create Note", image=resized_icons["create icon"], command=open_creating_settings, fg_color="#40d0ff", hover_color="#00a6ff", text_color="#000000", font=("Outfit", 20, "bold"), corner_radius=15)
DeleteAllButton = CTkButton(window, text="Delete All", image=resized_icons["delete icon"], command=delete_all_notes, fg_color="#ff3c3c", hover_color="#ec1a1a", text_color="#000000", font=("Outfit", 20, "bold"), corner_radius=15)
Label1 = CTkLabel(window, text="Press")
Label2 = CTkLabel(window, text="Press")
ModeSwitch_var = StringVar(value="on")
ModeSwitch = CTkSwitch(window, text="Darkmode", command=switch_appearance_mode, variable=ModeSwitch_var, onvalue="on", offvalue="off", corner_radius=100)
ModeSwitch.place(relx=0.1, rely=0.95, anchor="center")
SortingDropdown = CTkOptionMenu(window,
                                fg_color="#40d0ff",
                                button_color="#40d0ff",
                                button_hover_color="#00a6ff",
                                dropdown_fg_color="#40d0ff",
                                dropdown_text_color="#000000",
                                font=("Outfit", 11, "bold"),
                                dropdown_font=("Outfit", 14, "bold"),
                                text_color="#000000" ,
                                dropdown_hover_color="#00a6ff",
                                width=1, height=30,
                                dynamic_resizing=True,
                                values=["Alphabetical A-Z", "Alphabetical Z-A", "Note length (Asc)", "Note length (Desc)", "Title length (Asc)", "Title length (Desc)"],
                                command=sort_notes)
SortingDropdown.configure(width=1)
SortingDropdown.grid(row=0, column=8, columnspan=2, pady=7, padx=5)

SearchEntry.grid(row=0, column=4, rowspan=1,columnspan=3, pady=7, padx=5)
SearchButton = CTkButton(window, text="", image=resized_icons["search icon"], command=search_notes, fg_color="#d6d6d6", hover_color="#9b9b9b", text_color="#000000", font=("Outfit", 15, "bold"))
SearchButton.grid(row=0, column=7, rowspan=1,columnspan=1, pady=7, padx=5)

#place entities
CreateNoteButton.place(relx=0.18, rely=0.45, relwidth=0.3, relheight=0.08, anchor="center")
DeleteAllButton.place(relx=0.18, rely=0.55, relwidth=0.3, relheight=0.08,  anchor="center")

#run
window.mainloop()
