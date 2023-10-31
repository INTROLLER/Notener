#Notener 2.2

from customtkinter import *
import os
from random import *
from PIL import Image
from cryptography.fernet import Fernet
import bcrypt


#the window
window = CTk()
window.title("Notener")
window.geometry("700x450")
amount_of_notes = 0
set_appearance_mode("dark")
window.resizable(False,False)

notespath = 'Notes\\'

KeyExist = os.path.exists('keyfile.key')

def save_key_to_file(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)

def load_key_from_file(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

if not KeyExist:
    encryption_key = Fernet.generate_key()
    save_key_to_file(encryption_key, 'keyfile.key')
else:
    print("")
# Load the key from the file
loaded_key = load_key_from_file('keyfile.key')

# Use the loaded key for encryption and decryption
cipher_suite = Fernet(loaded_key)

window.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29), weight=1, minsize=15)
window.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29), weight=1, minsize=23.33)

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

SearchEntry = CTkEntry(window, width=225, height=36, placeholder_text="Search...")

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
    global WidgetFrame

    WidgetFrame = CTkScrollableFrame(window, fg_color="#202020", width=413, height=400)
    WidgetFrame.grid(row=3, column=10, rowspan=26, columnspan=20)

    buttons = ["NewNoteDeleteButton", "NewNoteEditButton"]
    labels = ["NewNoteDescription", "NewNoteTitle"]

    search_query = SearchEntry.get().lower()

    for file_name, content in file_data.items():
        
        NewTitle = file_name
        NewDescription = content

        if search_query and search_query not in NewTitle.lower():
            continue

        with open(file_path, 'rb') as file:
            encrypted_content = file.read()
            decrypted_content = cipher_suite.decrypt(encrypted_content).decode()
            file_data[file_name] = decrypted_content
            NewDescription = decrypted_content

        NewNoteFrame = CTkFrame(WidgetFrame, height=100, width=410, bg_color="transparent")
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

        ActionsBackground = CTkFrame(NewNoteFrame, fg_color="#3f3f3f", height=20, bg_color="transparent")
        ActionsBackground.grid(row=2, column=0, columnspan=5, sticky="nesw")

        NewNoteDeleteButton = CTkButton(NewNoteFrame,
                            text="",
                            image=resized_icons["delete icon"],
                            command = lambda t=NewNoteTitle,f=NewNoteFrame,c=NewNoteDescription, a=ActionsBackground: delete_note(t, f, c, a),
                            fg_color="#ff3c3c",
                            hover_color="#ec1a1a",
                            text_color="#00194e",
                            bg_color="#3f3f3f",
                            border_width=0,
                            corner_radius=150,
                            height=10,
                            width=10)
        NewNoteDeleteButton.grid(row=2, column=3, padx=8)

        NewNoteEditButton = CTkButton(NewNoteFrame,
                            text="",
                            image= resized_icons["edit icon"],
                            command = lambda f=NewNoteTitle, c=NewNoteDescription: edit_note(f, c),
                            fg_color= "#59c8ff",
                            hover_color= "#129fe5",
                            text_color="#00194e",
                            bg_color="#3f3f3f",
                            border_width=0,
                            corner_radius=150,
                            height=10,
                            width=10)
        NewNoteEditButton.grid(row=2, column=1, padx=8)

        NewNoteDeleteButton.configure(command=lambda t=NewNoteTitle,f=NewNoteFrame,c=NewNoteDescription, b1=NewNoteDeleteButton, b2=NewNoteEditButton, a=ActionsBackground: delete_note(t, f, c, b1, b2, a))

        notes_title_data.append((NewTitle, NewNoteFrame))
        notes_content_data.append((NewDescription, NewNoteFrame))

        SeparateElements.extend([NewNoteDeleteButton, NewNoteEditButton])

        SeparateElements.extend([ActionsBackground])

        widgets.append(NewNoteFrame)

        amount_of_notes += 1

        sort_notes("A-Z Order")

#commands
def save_new_note1():
    global amount_of_notes
    global NewNoteFrame
    global get_the_button
    global button2_holder
    global NewNoteEditButton

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

        NewNoteDeleteButton = CTkButton(NewNoteFrame,
                            text="",
                            image=resized_icons["delete icon"],
                            command = lambda t=NewNoteTitle,f=NewNoteFrame,c=NewNoteDescription, a=ActionsBackground: delete_note(t, f, c, a),
                            fg_color="#ff3c3c",
                            hover_color="#ec1a1a",
                            text_color="#00194e",
                            bg_color="#3f3f3f",
                            border_width=0,
                            corner_radius=150,
                            height=10,
                            width=10)
        NewNoteDeleteButton.grid(row=2, column=3, padx=8)

        NewNoteEditButton = CTkButton(NewNoteFrame,
                            text="",
                            image= resized_icons["edit icon"],
                            command = lambda f=NewNoteTitle, c=NewNoteDescription: edit_note(f, c),
                            fg_color= "#59c8ff",
                            hover_color= "#129fe5",
                            text_color="#00194e",
                            bg_color="#3f3f3f",
                            border_width=0,
                            corner_radius=150,
                            height=10,
                            width=10)
        NewNoteEditButton.grid(row=2, column=1, padx=8)

        NewNoteDeleteButton.configure(command=lambda t=NewNoteTitle,f=NewNoteFrame,c=NewNoteDescription, b1=NewNoteDeleteButton, b2=NewNoteEditButton, a=ActionsBackground: delete_note(t, f, c, b1, b2, a))

        notes_title_data.append((NewTitle, NewNoteFrame))
        notes_content_data.append((NewDescription, NewNoteFrame))

        SeparateElements.extend([NewNoteDeleteButton, NewNoteEditButton])

        encrypted_content = cipher_suite.encrypt(NewDescription.encode())
        with open(notespath + f'{NewTitle}.txt', "wb") as my_file:
            my_file.write(encrypted_content)

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
        switch_appearance_mode()

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

    lists = [widgets, titles, SeparateElements, notes_title_data, notes_content_data]
    for lst in lists:
        lst.clear()

    amount_of_notes = 0

def switch_appearance_mode():
    Current_mode = ModeSwitch_var.get()

    if Current_mode == "off":
        set_mode = "light"
        set_background_color = "#a4a4a4"
        set_text_color = "#00716f"
        set_scrolling_case_color = "#e1e1e1"
        search_button_fg_color = "#ababab"
        search_button_hover_color = "#929292"
        main_frame_fg_color = "#cfcfcf"

    elif Current_mode == "on":
        set_mode = "dark"
        set_background_color = "#3f3f3f"
        set_text_color = "#e1ff5c"
        set_scrolling_case_color = "#202020"
        search_button_fg_color = "#d6d6d6"
        search_button_hover_color = "#9b9b9b"
        main_frame_fg_color = "#2a2a2a"


    set_appearance_mode(f"{set_mode}")

    for MainNoteFrame in widgets:
        MainNoteFrame.configure(fg_color=f"{main_frame_fg_color}")

    for NewNoteTitle in titles:
        NewNoteTitle.configure(text_color=f"{set_text_color}")

    for key in SeparateElements:
        if isinstance(key, CTkFrame):
            key.configure(fg_color=f"{set_background_color}")
        else:
            key.configure(bg_color=f"{set_background_color}")

    WidgetFrame.configure(fg_color=f"{set_scrolling_case_color}")
    SearchButton.configure(fg_color=f"{search_button_fg_color}", hover_color=f"{search_button_hover_color}")


def edit_note(file_name, file_content):
    def destroy_edit_window():
        edit_window.destroy()
    def save_changes():
        new_name = rename_entry.get()
        new_content = edit_content_entry.get()
        encrypted_content = cipher_suite.encrypt(new_content.encode())
        with open((notespath + file_name.cget("text") + ".txt"), "wb") as f:
            f.write(encrypted_content)
        os.rename((notespath + file_name.cget("text") + ".txt"), (notespath + new_name + ".txt"))
        file_name.configure(text=new_name)
        file_content.configure(text=new_content)
        edit_window.destroy()

    edit_window = CTkToplevel(window)
    edit_window.title("Edit Note")
    edit_window.geometry("350x150")
    edit_window.attributes('-topmost', 'true')
    edit_window.resizable(False,False)
    
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

def delete_note(file_name, NewNoteFrame, file_content, button1, button2, actionsbackground):
    global amount_of_notes
    global notes_title_data
    global notes_content_data
    global titles
    global SeparateElements
    global widgets

    NewNoteFrame.destroy()
    note_name = file_name.cget("text")
    file_to_remove = ('Notes\\' + note_name + '.txt')
    os.remove(file_to_remove)
    amount_of_notes -= 1

    notes_title_data = [(title, frame) for title, frame in notes_title_data if title != file_name.cget("text")]
    notes_content_data = [(content, frame) for content, frame in notes_content_data if content != file_content.cget("text")]
    titles = [title for title in titles if title !=file_name]
    SeparateElements = [button for button in SeparateElements if button != button1]
    SeparateElements = [button for button in SeparateElements if button != button2]
    SeparateElements = [frame for frame in SeparateElements if frame != actionsbackground]
    widgets = [frame for frame in widgets if frame != NewNoteFrame]

def sort_notes(choice):
    if choice == "A-Z Order":
        sorted_notes_data = sorted(notes_title_data, key=lambda x: x[0].lower())

    elif choice == "Z-A Order":
        sorted_notes_data = sorted(notes_title_data, key=lambda x: x[0].lower(), reverse=True)

    elif choice == "Note Length ↑":
        sorted_notes_data = sorted(notes_content_data, key=lambda x: len(x[0]))

    elif choice == "Note Length ↓":
        sorted_notes_data = sorted(notes_content_data, key=lambda x: len(x[0]), reverse=True)

    elif choice == "Title Length ↑":
        sorted_notes_data = sorted(notes_title_data, key=lambda x: len(x[0]))

    elif choice == "Title Length ↓":
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
    [list.clear() for list in (widgets, SeparateElements, notes_content_data, notes_title_data, titles)]
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
    switch_appearance_mode()

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
                                font=("Outfit", 16, "bold"),
                                dropdown_font=("Outfit", 14, "bold"),
                                text_color="#000000" ,
                                dropdown_hover_color="#00a6ff",
                                width=1, height=30,
                                dynamic_resizing=True,
                                values=["A-Z Order", "Z-A Order", "Note Length ↑", "Note Length ↓", "Title Length ↑", "Title Length ↓"],
                                command=sort_notes)
SortingDropdown.configure(width=1)
SortingDropdown.grid(row=0, column=23, rowspan=3, columnspan=7, pady=7, padx=5)

SearchEntry.grid(row=0, column=8, rowspan=3, columnspan=15, pady=7, padx=5)
SearchButton = CTkButton(window, text="", image=resized_icons["search icon"], command=search_notes, fg_color="#d6d6d6", hover_color="#9b9b9b", text_color="#000000", font=("Outfit", 15, "bold"))
SearchButton.grid(row=0, column=21, rowspan=3, columnspan=2, pady=7, padx=5)

#place entities
CreateNoteButton.place(relx=0.18, rely=0.45, relwidth=0.3, relheight=0.08, anchor="center")
DeleteAllButton.place(relx=0.18, rely=0.55, relwidth=0.3, relheight=0.08,  anchor="center")

#run
window.mainloop()
