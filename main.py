import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import authcheck
import diary_main as dm
import open_log as ol


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
        elif len(password_input.get()) < 8:
            error_label["text"] = "Password must be at least 8 characters"
        elif len(username_input.get()) > 10:
            error_label["text"] = "Username must be less than 10 characters"
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
        global state, key, acc_id
        # check if either of the fields are empty
        if username_input.get() == "" or password_input.get() == "":
            error_label["text"] = "Please fill in both fields"
        # check if the account exists
        elif authcheck.authenticate(username_input.get(), password_input.get()):
            error_label["text"] = "Login successful"
            # close the window
            state = True
            key = authcheck.get_id(username_input.get()) + username_input.get()
            acc_id = authcheck.get_id(username_input.get())
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
    username_input = tk.Entry(root, font=(font_name, 12))
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

    def save_file(*args):  # NOQA
        """
        Save the diary by getting the text from the text widget and then save
        """

        window_txt = text_widget.get("1.0", "end-1c")
        if dm.save_diary(file_path, key, window_txt) is False:
            mb.showerror("Error", "Could not save the file, you might be trying to save to a file that is not your own")

    def open_file():
        global file_path
        """
        Open the file via the user account. The unique id makes it so that the user can only access their own files.
        """
        file_path = fd.askopenfilename(title="Select diary file", filetypes=[("Diary files", "*.dry")])
        file_path = fr"{file_path}"
        window_txt = dm.open_diary(file_path, key)
        # Insert the text into the text widget but first clear it
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", window_txt)
        root.title(f"Diary - {file_path}")
        root.update()

    def change_pw():
        """
        Make a sub-window asking the user for their username, old password, new password,
        and then confirm the new password
        """

        def change_pw_internal():
            """
            Change the password
            """
            if authcheck.authenticate(username_input.get(), old_password_input.get()):
                if username_input.get() == "" or new_password_input.get() == "" or confirm_password_input.get() == "" \
                        or old_password_input.get() == "":
                    mb.showerror("Error", "Please input the fields correctly.")
                # check if the username is already taken (Put this above the password check for better UX)
                elif len(new_password_input.get()) < 8:
                    mb.showerror("Error", "Password must be at least 8 characters")
                elif new_password_input.get() == confirm_password_input.get():
                    authcheck.change_password(username_input.get(), old_password_input.get(), new_password_input.get())
                    mb.showinfo("Success", "Password changed successfully")
                    root2.destroy()
                else:
                    mb.showerror("Error", "Passwords do not match")
            else:
                mb.showerror("Error", "Invalid username or password")

        # Create the main window
        root2 = tk.Toplevel(root)
        root2.title("Change Password")

        # Set the window size
        root2.geometry("400x200")
        root2.resizable(False, False)

        font_name = "Open Sans"
        username_label = tk.Label(root2, text="Username:", font=(font_name, 12))
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_input = tk.Entry(root2, font=(font_name, 12))
        username_input.grid(row=0, column=1, pady=5)

        old_password_label = tk.Label(root2, text="Old Password:", font=(font_name, 12))
        old_password_label.grid(row=1, column=0, padx=10, pady=5)
        old_password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        old_password_input.grid(row=1, column=1, pady=5)

        new_password_label = tk.Label(root2, text="New Password:", font=(font_name, 12))
        new_password_label.grid(row=2, column=0, padx=10, pady=5)
        new_password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        new_password_input.grid(row=2, column=1, pady=5)

        confirm_password_label = tk.Label(root2, text="Confirm Password:", font=(font_name, 12))
        confirm_password_label.grid(row=3, column=0, padx=10, pady=5)
        confirm_password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        confirm_password_input.grid(row=3, column=1, pady=5)

        change_pw_button = tk.Button(root2, text="Change Password", font=(font_name, 10), command=change_pw_internal)
        change_pw_button.grid(row=4, column=0, columnspan=2, pady=5)

    def delete_acc():
        """
        prompt the user for their username and password and then delete the account
        """

        def delete_acc_internal():
            """
            Delete the account
            """
            delete_state = authcheck.delete_account(username_input.get(), password_input.get())
            if delete_state is True:
                mb.showinfo("Success", "Account deleted successfully")
                root.destroy()
            else:
                mb.showerror("Error", "Invalid username or password")

        # Create the main window
        root2 = tk.Toplevel(root)
        root2.title("Delete Account")

        # Set the window size
        root2.geometry("310x140")
        root2.resizable(False, False)

        font_name = "Open Sans"
        username_label = tk.Label(root2, text="Username:", font=(font_name, 12))
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_input = tk.Entry(root2, font=(font_name, 12))
        username_input.grid(row=0, column=1, pady=5)

        password_label = tk.Label(root2, text="Password:", font=(font_name, 12))
        password_label.grid(row=1, column=0, padx=10, pady=5)
        password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        password_input.grid(row=1, column=1, pady=5)

        delete_acc_button = tk.Button(root2, text="Delete Account", font=(font_name, 10), command=delete_acc_internal)
        delete_acc_button.grid(row=2, column=0, columnspan=2, pady=15)

    def open_log():
        class Table:
            def __init__(self, window, lst):
                self.lst = lst
                self.total_rows = len(lst)
                self.total_columns = len(lst[0])
                self.window = window
                self.e = None

            def create(self):
                # code for creating table
                for i in range(self.total_rows):
                    for j in range(self.total_columns):
                        print(self.lst[i][j])
                        self.e = tk.Entry(self.window, width=20, fg="black",
                                          font=("Open Sans", 16, "bold"))
                        self.e.grid(row=i, column=j)
                        self.e.insert(tk.END, self.lst[i][j])

        def access_log(account_name, account_password):
            if authcheck.authenticate(account_name, account_password) is False:
                mb.showerror("Error", "Invalid username or password")
                return None
            elif authcheck.authenticate(account_name, account_password) is True:
                data = ol.access_read(authcheck.get_id(account_name))
                print(data)
                root2 = tk.Toplevel(root)
                root2.title("Log")
                t = Table(root2, data)
                t.create()
                root2.mainloop()

        # create root window
        root_ask = tk.Toplevel(root)
        ol.check_db_log()  # check and creates the log file if it doesn't exist
        root_ask.title("Log")
        # Set the window size
        root_ask.geometry("310x140")
        root_ask.resizable(False, False)

        font_name = "Open Sans"
        username_label = tk.Label(root_ask, text="Username:", font=(font_name, 12))
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_input = tk.Entry(root_ask, font=(font_name, 12))
        username_input.grid(row=0, column=1, pady=5)

        password_label = tk.Label(root_ask, text="Password:", font=(font_name, 12))
        password_label.grid(row=1, column=0, padx=10, pady=5)
        password_input = tk.Entry(root_ask, show="*", font=(font_name, 12))
        password_input.grid(row=1, column=1, pady=5)

        access_button = tk.Button(root_ask, text="Access account log", font=(font_name, 10), command=lambda: access_log(
            username_input.get(), password_input.get()))
        access_button.grid(row=2, column=0, columnspan=2, pady=15)

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
    settings_menu.add_command(label="Open logs", command=open_log)
    menu.add_cascade(label="Settings", menu=settings_menu)

    # Create the text widget
    text_widget = tk.Text(root, font=("Open Sans", 12))
    text_widget.pack(expand=True, fill="both")
    root.bind("<Control-s>", save_file)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    # check if "database_db.db" exists, if not it will create it
    authcheck.check_db()
    file_path = None

    key, state, acc_id = None, False, None
    verification()
    if state is False or key is None:  # Incase the user closes the window
        quit()
    elif state and key:  # why account? just to make sure incase someone tinkered with the variable somehow
        ol.access_write(acc_id)
        diary_root()
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import authcheck
import diary_main as dm
import open_log as ol


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
        elif len(password_input.get()) < 8:
            error_label["text"] = "Password must be at least 8 characters"
        elif len(username_input.get()) > 10:
            error_label["text"] = "Username must be less than 10 characters"
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
        global state, key, acc_id
        # check if either of the fields are empty
        if username_input.get() == "" or password_input.get() == "":
            error_label["text"] = "Please fill in both fields"
        # check if the account exists
        elif authcheck.authenticate(username_input.get(), password_input.get()):
            error_label["text"] = "Login successful"
            # close the window
            state = True
            key = authcheck.get_id(username_input.get()) + username_input.get()
            acc_id = authcheck.get_id(username_input.get())
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
    username_input = tk.Entry(root, font=(font_name, 12))
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

    def save_file(*args):  # NOQA
        """
        Save the diary by getting the text from the text widget and then save
        """

        window_txt = text_widget.get("1.0", "end-1c")
        if dm.save_diary(file_path, key, window_txt) is False:
            mb.showerror("Error", "Could not save the file, you might be trying to save to a file that is not your own")

    def open_file():
        global file_path
        """
        Open the file via the user account. The unique id makes it so that the user can only access their own files.
        """
        file_path = fd.askopenfilename(title="Select diary file", filetypes=[("Diary files", "*.dry")])
        file_path = fr"{file_path}"
        window_txt = dm.open_diary(file_path, key)
        # Insert the text into the text widget but first clear it
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", window_txt)
        root.title(f"Diary - {file_path}")
        root.update()

    def change_pw():
        """
        Make a sub-window asking the user for their username, old password, new password,
        and then confirm the new password
        """

        def change_pw_internal():
            """
            Change the password
            """
            if authcheck.authenticate(username_input.get(), old_password_input.get()):
                if username_input.get() == "" or new_password_input.get() == "" or confirm_password_input.get() == "" \
                        or old_password_input.get() == "":
                    mb.showerror("Error", "Please input the fields correctly.")
                # check if the username is already taken (Put this above the password check for better UX)
                elif len(new_password_input.get()) < 8:
                    mb.showerror("Error", "Password must be at least 8 characters")
                elif new_password_input.get() == confirm_password_input.get():
                    authcheck.change_password(username_input.get(), old_password_input.get(), new_password_input.get())
                    mb.showinfo("Success", "Password changed successfully")
                    root2.destroy()
                else:
                    mb.showerror("Error", "Passwords do not match")
            else:
                mb.showerror("Error", "Invalid username or password")

        # Create the main window
        root2 = tk.Toplevel(root)
        root2.title("Change Password")

        # Set the window size
        root2.geometry("400x200")
        root2.resizable(False, False)

        font_name = "Open Sans"
        username_label = tk.Label(root2, text="Username:", font=(font_name, 12))
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_input = tk.Entry(root2, font=(font_name, 12))
        username_input.grid(row=0, column=1, pady=5)

        old_password_label = tk.Label(root2, text="Old Password:", font=(font_name, 12))
        old_password_label.grid(row=1, column=0, padx=10, pady=5)
        old_password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        old_password_input.grid(row=1, column=1, pady=5)

        new_password_label = tk.Label(root2, text="New Password:", font=(font_name, 12))
        new_password_label.grid(row=2, column=0, padx=10, pady=5)
        new_password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        new_password_input.grid(row=2, column=1, pady=5)

        confirm_password_label = tk.Label(root2, text="Confirm Password:", font=(font_name, 12))
        confirm_password_label.grid(row=3, column=0, padx=10, pady=5)
        confirm_password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        confirm_password_input.grid(row=3, column=1, pady=5)

        change_pw_button = tk.Button(root2, text="Change Password", font=(font_name, 10), command=change_pw_internal)
        change_pw_button.grid(row=4, column=0, columnspan=2, pady=5)

    def delete_acc():
        """
        prompt the user for their username and password and then delete the account
        """

        def delete_acc_internal():
            """
            Delete the account
            """
            delete_state = authcheck.delete_account(username_input.get(), password_input.get())
            if delete_state is True:
                mb.showinfo("Success", "Account deleted successfully")
                root.destroy()
            else:
                mb.showerror("Error", "Invalid username or password")

        # Create the main window
        root2 = tk.Toplevel(root)
        root2.title("Delete Account")

        # Set the window size
        root2.geometry("310x140")
        root2.resizable(False, False)

        font_name = "Open Sans"
        username_label = tk.Label(root2, text="Username:", font=(font_name, 12))
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_input = tk.Entry(root2, font=(font_name, 12))
        username_input.grid(row=0, column=1, pady=5)

        password_label = tk.Label(root2, text="Password:", font=(font_name, 12))
        password_label.grid(row=1, column=0, padx=10, pady=5)
        password_input = tk.Entry(root2, show="*", font=(font_name, 12))
        password_input.grid(row=1, column=1, pady=5)

        delete_acc_button = tk.Button(root2, text="Delete Account", font=(font_name, 10), command=delete_acc_internal)
        delete_acc_button.grid(row=2, column=0, columnspan=2, pady=15)

    def open_log():
        class Table:
            def __init__(self, window, lst):
                self.lst = lst
                self.total_rows = len(lst)
                self.total_columns = len(lst[0])
                self.window = window
                self.e = None

            def create(self):
                # code for creating table
                for i in range(self.total_rows):
                    for j in range(self.total_columns):
                        print(self.lst[i][j])
                        self.e = tk.Entry(self.window, width=20, fg="black",
                                          font=("Open Sans", 16, "bold"))
                        self.e.grid(row=i, column=j)
                        self.e.insert(tk.END, self.lst[i][j])

        def access_log(account_name, account_password):
            if authcheck.authenticate(account_name, account_password) is False:
                mb.showerror("Error", "Invalid username or password")
                return None
            elif authcheck.authenticate(account_name, account_password) is True:
                data = ol.access_read(authcheck.get_id(account_name))
                print(data)
                root2 = tk.Toplevel(root)
                root2.title("Log")
                t = Table(root2, data)
                t.create()
                root2.mainloop()

        # create root window
        root_ask = tk.Toplevel(root)
        ol.check_db_log()  # check and creates the log file if it doesn't exist
        root_ask.title("Log")
        # Set the window size
        root_ask.geometry("310x140")
        root_ask.resizable(False, False)

        font_name = "Open Sans"
        username_label = tk.Label(root_ask, text="Username:", font=(font_name, 12))
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_input = tk.Entry(root_ask, font=(font_name, 12))
        username_input.grid(row=0, column=1, pady=5)

        password_label = tk.Label(root_ask, text="Password:", font=(font_name, 12))
        password_label.grid(row=1, column=0, padx=10, pady=5)
        password_input = tk.Entry(root_ask, show="*", font=(font_name, 12))
        password_input.grid(row=1, column=1, pady=5)

        access_button = tk.Button(root_ask, text="Access account log", font=(font_name, 10), command=lambda: access_log(
            username_input.get(), password_input.get()))
        access_button.grid(row=2, column=0, columnspan=2, pady=15)

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
    settings_menu.add_command(label="Open logs", command=open_log)
    menu.add_cascade(label="Settings", menu=settings_menu)

    # Create the text widget
    text_widget = tk.Text(root, font=("Open Sans", 12))
    text_widget.pack(expand=True, fill="both")
    root.bind("<Control-s>", save_file)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    # check if "database_db.db" exists, if not it will create it
    authcheck.check_db()
    file_path = None

    key, state, acc_id = None, False, None
    verification()
    if state is False or key is None:  # Incase the user closes the window
        quit()
    elif state and key:  # why account? just to make sure incase someone tinkered with the variable somehow
        ol.access_write(acc_id)
        diary_root()
