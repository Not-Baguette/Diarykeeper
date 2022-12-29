import authcheck
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import diary_main as dm


def verification():
    """
    Verification window via tkinter
    """
    def toggle_pw():
        """
        Toggle password visibility
        """
        if password_input["show"] == "*":
            password_input["show"] = ""
        else:
            password_input["show"] = "*"

    def create_acc():
        """
        Create a new account and append it to the database
        """
        # check if either of the fields are empty
        if username_input.get() == "" or password_input.get() == "":
            error_label["text"] = "Please fill in both fields"
        # check if the username is already taken (Put this above the password check for better UX)
        elif authcheck.name_check(username_input.get()):
            error_label["text"] = "Username already taken"
        # check if the account already exists
        elif authcheck.authenticate(username_input.get(), password_input.get()):
            error_label["text"] = "Account already exists"
        else:
            # create the account
            error_label["text"] = "Account created, Please log-in"
            authcheck.create_account(username_input.get(), password_input.get())

    def login():
        """
        Login to the account
        """
        global state, account
        # check if either of the fields are empty
        if username_input.get() == "" or password_input.get() == "":
            error_label["text"] = "Please fill in both fields"
        # check if the account exists
        elif authcheck.authenticate(username_input.get(), password_input.get()):
            error_label["text"] = "Login successful"
            # close the window
            state, account = True, username_input.get() + password_input.get()  # it's a "id" per se
            root.destroy()
        else:
            error_label["text"] = "Invalid username or password"

    # Create the main window
    root = tk.Tk()
    root.title("Log In")

    # Set the window size
    root.geometry("300x200")
    root.resizable(False, False)

    font_name = "Open Sans"
    username_label = tk.Label(root, text="Username:", font=(font_name, 12))
    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_input = tk.Entry(root, font=("Arial", 12))
    username_input.grid(row=0, column=1, pady=5)

    password_label = tk.Label(root, text="Password:", font=(font_name, 12))
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_input = tk.Entry(root, show="*", font=(font_name, 12))
    password_input.grid(row=1, column=1, pady=5)

    error_label = tk.Label(root, text="", font=(font_name, 10))
    error_label.grid(row=2, column=0, columnspan=2, pady=5)

    login_button = tk.Button(root, text="Log-in", font=(font_name, 10), command=login)
    login_button.grid(row=3, column=0, pady=5)

    create_account_button = tk.Button(root, text="Create Account", font=(font_name, 10), command=create_acc)
    create_account_button.grid(row=3, column=1, pady=5)

    password_vis_button = tk.Button(root, text="Toggle password", font=(font_name, 10), command=toggle_pw)
    password_vis_button.grid(row=4, column=0, columnspan=2, pady=5)
    root.mainloop()


def diary_root():
    global file_path
    """
    Diary window via tkinter
    """
    def save_file(*args):
        """
        Save the diary by getting the text from the text widget and then save
        """

        window_txt = text_widget.get("1.0", "end-1c")
        dm.save_diary(file_path, account, window_txt)

    def open_file():
        global file_path
        """
        Open the file via the user account. This prevents using static file, also solves a security
        and portability issues
        """
        file_path = fd.askopenfilename(title="Select diary file", filetypes=[("Diary files", "*.dry")])
        file_path = fr"{file_path}"
        window_txt = dm.open_diary(file_path, account)
        # Insert the text into the text widget but first clear it
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", window_txt)
        root.title(f"Diary - {file_path}")
        root.update()

    def change_pw():
        pass

    def delete_acc():
        pass

    def open_log():
        pass

    def on_close():
        """
        Make sure the user wants to close the window
        """
        result = mb.askyesno("Quit", "Are you sure you want to quit? Have you saved your file yet?")
        if result:
            root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Diary")

    # Set the window size
    root.geometry("600x400")
    root.resizable(False, False)

    # Create the menu
    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_close)
    menu.add_cascade(label="File", menu=file_menu)

    settings_menu = tk.Menu(menu, tearoff=0)
    settings_menu.add_command(label="Change password", command=change_pw)
    settings_menu.add_command(label="Delete Account", command=delete_acc)
    settings_menu.add_separator()
    settings_menu.add_command(label="Delete Account", command=open_log)
    menu.add_cascade(label="Logs", menu=settings_menu)

    # Create the text widget
    text_widget = tk.Text(root, font=("Arial", 12))
    text_widget.pack(expand=True, fill="both")
    root.bind("<Control-s>", save_file)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    # check if "database_db.db" exists, if not it will create it
    authcheck.check_db()
    file_path = None

    account, state = None, False
    verification()
    if state is False or account is None:  # Incase the user closes the window
        print("Not logged in")
    elif state and account:  # why account? just to make sure incase someone tinkered with the variable somehow
        diary_root()
