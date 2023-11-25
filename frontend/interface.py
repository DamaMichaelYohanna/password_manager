__author__ = 'Dama Michael Yohanna'
__version__ = '1.0.0'
"""
    Password manager program
    writing purely in python
    using tkinter module for UI
    and sqlite3 for database.

    Version: 1.0
    Credit:
        Dama Michael Yohanna
    Dependency:
        # Open Cv to be implemented for login using face detection
        Pmw
    Modules:
        os module
        sys module
        webbrowser module
        tkinter module

"""
# standard library import
import os
import tkinter as tk
from tkinter import ttk, Frame
from tkinter import messagebox as mbox
import webbrowser

# external library import
import Pmw

from database_manager import UserDatabase
from password_utility import PasswordManager


class MasterFrame(Frame):
    def __init__(self, parent):
        # initialize the password utility class and set to global variable
        self.password_util = PasswordManager()
        # initialize the inherited Frame class
        Frame.__init__(self, parent, bg='red')
        # set a global frame inheriting from tk.Tk
        self.parent = parent
        # Set title for main window
        self.parent.bank_name('Password Manager')
        # make window un resizable
        self.parent.resizable(0, 0)
        # initialize balloon class fo help text
        # Pmw.initialise()
        self.balloon = Pmw.Balloon(self.parent)
        # --------------------------------------------------------------
        self.result = None
        self.user_id = None  # hold user id in case for db transaction
        # # --------------------------------------------------------------------
        self.logo = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                    'assets',
                                                    'head3.png')
                                  )
        self.logo = self.logo.subsample(4, 4)
        self.gen_pass = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                        'assets',
                                                        'lock1.png'))
        self.gen_pass = self.gen_pass.subsample(3, 3)
        self.save_pass = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                         'assets', 'lock2.png'))
        self.save_pass = self.save_pass.subsample(3, 3)
        self.retrieve_spass = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                              'assets', 'lock3.png'))
        self.retrieve_spass = self.retrieve_spass.subsample(3, 3)
        self.retrieve_all_pass = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'lock4.png'))
        self.retrieve_all_pass = self.retrieve_all_pass.subsample(3, 3)
        # # --------------------------------------------------------------------
        self.site_logo = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'site.png'))
        self.site_logo = self.site_logo.subsample(4, 4)
        self.user_logo = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'user.png'))
        self.user_logo = self.user_logo.subsample(3, 4)
        self.pass_logo = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                         'assets', 'pass.png'))
        self.pass_logo = self.pass_logo.subsample(4, 4)
        self.retrieve = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'retrieve.png'))
        self.retrieve = self.retrieve.subsample(3, 3)
        self.all_pass = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'all_pass.png'))
        self.all_pass = self.all_pass.subsample(3, 3)
        self.delete_logo = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'delete.png'))
        self.delete_logo = self.delete_logo.subsample(5, 5)
        self.view_logo = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                         'assets', 'view.png'))
        self.view_logo = self.view_logo.subsample(8, 8)
        self.edit_logo = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                         'assets', 'edit.png'))
        self.edit_logo = self.edit_logo.subsample(8, 8)
        self.web_logo = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                        'assets', 'web.png'))
        self.web_logo = self.web_logo.subsample(2, 2)
        self.copy_image = tk.PhotoImage(
            file=os.path.join(os.getcwd(),
                              'assets', 'paste.png'))
        self.copy_image = self.copy_image.subsample(7, 7)
        # -----------------------------------------------------
        self.my_pix = tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                      'assets', 'me.png'))
        self.my_pix = self.my_pix.subsample(3, 3)
        self.legacy_logo = tk.PhotoImage(
            file=os.path.join(os.getcwd(), 'assets', 'legacy_logo.png')
        )
        self.legacy_logo = self.legacy_logo.subsample(3, 3)

        # call the login method after initialization.
        self.login()

    def create_credentail(self):
        """ method to handle interface for creating credentials"""

        def go_back():
            """function to close the current window"""
            # destroy the frame to close the window
            create_cred_frame.destroy()

        def validate_credentials():
            """valid date input and save if valid"""
            user = username.get()  # get the usename
            pass1 = password.get()  # get the first password
            pass2 = password_confirm.get()  # get the password confirmation

            # check if field are empty, then show error message
            if pass1 == '' or user == '' or pass2 == '':
                mbox.showerror('Error', "A field can't be empty")
            # check if the two password mismatch, then show an error message
            elif pass2 != pass1:
                password1_var.set('')
                password2_var.set('')
                mbox.showerror('Error', "Password mismatched!")
            # if receive data are valid then call the password saver method
            else:
                # call the 'save_login' method from the UserDatabase class
                # to save the password, grab the return value which is False if
                # no error or True if  an error occurred and store in user var
                user = UserDatabase().save_login_details(user, pass1)
                if not user:  # if no error show success message
                    mbox.showinfo('Success', 'Account created Successfully!')
                    create_cred_frame.destroy()  # destroy the current window
                    self.login()  # call the login method
                else:  # if error occurred, show error message
                    password1_var.set('')
                    password2_var.set('')
                    username_var.set('')
                    mbox.showerror('Save Failed', 'User name already exist!')

        # create a big frame for create credentials page
        create_cred_frame = tk.Frame(self.parent)
        create_cred_frame.grid(row=1, column=0)
        create_cred_frame['padx'] = 20  # set some horizontal padding
        create_cred_frame['pady'] = 10  # set some vertical padding
        create_cred_frame['bg'] = 'white'  # set the background color
        create_cred_frame['bd'] = 2  # set some border
        # display the passwordmanager logo
        logo = tk.Label(create_cred_frame, image=self.logo,
                        bg='white', pady=0, padx=6)
        logo.grid(row=0, column=0)
        # draw a horizontal line using separator widget
        sep = ttk.Separator(create_cred_frame)
        sep.grid(sticky='we', row=1, column=0, )
        # -------------------------------------
        # show some descriptions
        label_frame = tk.LabelFrame(create_cred_frame,
                                    text="Create Credentials", bg='white')
        label_frame.grid(row=3, padx=10, pady=15)
        # ----------------------------------------
        # description for username and the username entry field
        username_label = tk.Label(label_frame, text='Username', bg='white')
        username_label.grid(pady=15, padx=15)
        username_var = tk.StringVar()
        username = tk.Entry(label_frame, textvariable=username_var,
                            width=25, bg='#f5f5f5', relief='flat')
        username.grid(pady=10, ipady=5)
        self.balloon.bind(username, 'Your Desire Username', )
        # description for password and password confirmation as well the
        # their respective input fields
        password_label = tk.Label(label_frame, text='Password', bg='white')
        password_label.grid(padx=15)
        password1_var = tk.StringVar()
        password = tk.Entry(label_frame, width=25, show='*', bg='#f5f5f5',
                            textvariable=password1_var, relief='flat')
        password.grid(pady=8, ipady=5, padx=15)
        username.focus()  # give focus to the input area
        self.balloon.bind(password, 'Your Desired Password', )
        password_confirm_label = tk.Label(label_frame,
                                          text='Password Again', bg='white')
        password_confirm_label.grid(padx=15)
        password2_var = tk.StringVar()
        password_confirm = tk.Entry(label_frame, width=25, show='*',
                                    textvariable=password2_var, bg='#f5f5f5',
                                    relief='flat')
        password_confirm.grid(pady=8, ipady=5, padx=15)
        self.balloon.bind(password_confirm, 'Enter Password Again', )
        # draw a horizontal line
        sep1 = ttk.Separator(create_cred_frame)
        sep1.grid(sticky='we', column=0, )
        # create a small internal frame to hold the submit
        # button and the back button
        small_frame = Frame(create_cred_frame)
        small_frame.grid(pady=5, padx=5)
        # submit button goes here
        submit = tk.Button(small_frame,
                           text='Create', width=17, bg='azure',
                           command=validate_credentials, )
        submit.grid(padx=10, pady=5)
        # back butto goes here
        back_button = tk.Button(small_frame, text='Back', bg='white',
                                command=go_back)
        back_button.grid(row=0, column=1, sticky='we', pady=5, padx=15)
        # end of the create credential page. next is the login page
        # ===============================================================================

    def login(self):
        """ method to display the login page"""

        def show_or_hide_password():
            if not hide_var.get():
                password['show'] = '*'
            else:
                password['show'] = ''

        def validate_credentials():
            """function to validate user input"""
            user = username.get()  # get username
            pass_ = password.get()  # get password
            if pass_ == '' or user == '':  # check if fields are not empty
                mbox.showerror('Error', "A field can't be empty")
            else:
                # login the user and save the user id which is the
                # return value into the 'user' variable
                user = UserDatabase().login(user, pass_)  # grab the return id
                if user:  # id if was return
                    self.user_id = user  # set user id to be global
                    # show success message
                    mbox.showinfo('Success', 'Login successful')
                    # destroy the login page
                    login_frame.destroy()
                    # launch the home page
                    self.home_page()
                else:  # if id was not returned
                    # show error message
                    password_var.set('')
                    mbox.showerror(
                        'Failed',
                        'Login Failed! Check credentials and try again.'
                    )

        # create a big frame for the login page
        login_frame = tk.Frame(self.parent)
        login_frame.grid(row=1, column=0)
        login_frame['padx'] = 20  # set some horizontal padding
        login_frame['pady'] = 40  # set some vertical padding
        login_frame['bg'] = 'white'  # set background color as well
        login_frame['bd'] = 2  # set border of two pixels
        # display the 'password manager' logo
        logo = tk.Label(login_frame, image=self.logo, bg='white', pady=0, padx=6)
        logo.grid(row=0, column=0)
        # draw a horizontal line
        sep = ttk.Separator(login_frame)
        sep.grid(sticky='we', row=1, column=0, )
        # show some description using the label frame which provide border
        # -------------------------------------
        label_frame = tk.LabelFrame(login_frame,
                                    text="Login Credentials", bg='white')
        label_frame.grid(row=3, padx=10, pady=15)
        # ----------------------------------------
        # label for username and the username entry field
        username_label = tk.Label(label_frame, text='Username', bg='white')
        username_label.grid(pady=5, padx=15)
        username = tk.Entry(label_frame,
                            width=25, bg='#f5f5f5', relief='flat')
        username.grid(pady=10, ipady=5)
        username.focus()  # give focus to the input area
        # label for username and the username input field
        password_label = tk.Label(label_frame, text='Password', bg='white')
        password_label.grid(padx=15)
        password_var = tk.StringVar()
        hide_var = tk.IntVar(value=0)
        password = tk.Entry(label_frame, width=25, bg='#f5f5f5', relief='flat',
                            textvariable=password_var, show='*')
        password.grid(pady=5, ipady=5)
        small_frame = tk.Frame(label_frame, bg='white')
        small_frame.grid()
        text = tk.Label(small_frame, text='Show Password', bg='white', width=20)
        text.grid(row=0, column=0, padx=10)
        check = tk.Checkbutton(small_frame, variable=hide_var, onvalue=1,
                               offvalue=0, command=show_or_hide_password)
        check.grid(row=0, column=1, padx=10)
        # the submit button goes here
        submit = tk.Button(label_frame,
                           text='Login', width=25, bg='pink',
                           command=validate_credentials, )
        submit.grid(padx=10, pady=15)
        # create a small frame to hold the description and button for
        # creating new credentials.
        small_frame = Frame(login_frame)
        small_frame.grid()
        # description goes here
        create_new_credential = tk.Label(small_frame,
                                         text='Create New Credentials', )
        create_new_credential.grid(row=0, column=0,
                                   sticky='we', pady=5, padx=15)
        # button goes here
        create_new_credential = tk.Button(small_frame,
                                          text='Here', bg='white',
                                          command=self.create_credentail
                                          )
        create_new_credential.grid(row=0, column=1,
                                   sticky='we', pady=5, padx=15)
        # end of the login page
        # ==========================================================

    def home_page(self):
        """ the method to display the home page"""
        # create a tk menu widget
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)
        # create sub menus
        submenu1 = tk.Menu(menu)
        menu.add_cascade(label='File', menu=submenu1)
        submenu1.add_command(label='Delete My Account')
        submenu1.add_separator()  # add a seperator (horizontal line)
        submenu1.add_command(label='Clear My Records',
                             command=self.password_util.delete_all_records)
        submenu1.add_separator()  # add a seperator (horizontal line)
        submenu1.add_command(label='Quit',
                             command=self.close_program)
        # create another sub menu
        submenu2 = tk.Menu(menu)
        menu.add_cascade(label='Help', menu=submenu2)
        submenu2.add_command(label='About Us', command=self.about_page)
        submenu2.add_command(label='Developer', command=self.developer_page)
        # create a big frame for the home page display
        first_frame = tk.Frame(self.parent, bg='azure')
        first_frame.grid(row=1, column=0, )
        first_frame['pady'] = 10  # set some horizontal padding
        first_frame['padx'] = 4  # set some vertical padding
        # display the 'password manager logo
        logo = tk.Label(first_frame, image=self.logo,
                        bg='azure', pady=0, padx=6)
        logo.grid(row=0, column=0, columnspan=2)
        # display logo
        generate_pass_icon = tk.Label(first_frame, image=self.gen_pass,
                                      bg='azure', width=55, )
        generate_pass_icon.grid(row=1, column=0, pady=15, ipady=5, )
        # display button for generating new password
        generate_pass_button = tk.Button(
            first_frame, text='Generate New Password', relief='raised',
            pady=6, compound='left', width=26, bg='azure', cursor='hand2',
            command=self.generate_password_page
        )
        generate_pass_button.grid(row=1, column=1, pady=10, padx=10, ipady=13)
        # -----------------------------------------------------------
        # display logo for save new password
        save_pass_icon = tk.Label(first_frame, image=self.save_pass,
                                  bg='azure', width=55, )
        save_pass_icon.grid(row=2, column=0, pady=15, ipady=5, padx=10)
        # the save new password button goes here
        save_pass_button = tk.Button(first_frame, text='Save New Credentials',
                                     relief='raised', pady=5, compound='left',
                                     width=26, bg='azure', cursor='hand2',
                                     command=self.save_or_edit_password_page)
        save_pass_button.grid(row=2, column=1, pady=10, padx=10, ipady=13)

        # ---------------------------------------------------------------
        # retrieve  single password logo
        retrieve_spass_icon = tk.Label(first_frame, image=self.retrieve_spass,
                                       bg='azure', width=55, )
        retrieve_spass_icon.grid(row=3, column=0, pady=15, ipady=5, padx=10)
        # retrieve single password button
        retrieve_spass_button = tk.Button(
            first_frame, text='Retrieve Single Credential', relief='raised',
            pady=10, width=26, bg='azure', cursor='hand2',
            command=self.retrieve_single_password
        )
        retrieve_spass_button.grid(row=3, column=1, pady=10, padx=10, ipady=13)
        # -----------------------------------------------------
        # retrieve all password logo goes here
        retrieve_all_pass_icon = tk.Label(first_frame,
                                          image=self.retrieve_all_pass,
                                          bg='azure', width=50, )
        retrieve_all_pass_icon.grid(row=4, column=0, pady=15, ipady=5, )
        # retrieve all password button goes here
        retrieve_all_pass_button = tk.Button(
            first_frame,
            text='Retrieve All Saved Password',
            compound='left', width=26,
            bg='azure', cursor='hand2',
            command=self.retrieve_all_password_page)
        retrieve_all_pass_button.grid(row=4, column=1,
                                      pady=10, padx=10, ipady=13)

    def generate_password_page(self):
        """function for displaying the newly
            generated password
        """
        # call the password generator method from the password util class and
        # save the generated password in a variable for reference
        generated_password = self.password_util.return_generated_password()

        def close_generated_pass_page():
            """function to close the generate password window"""
            decoration_frame.destroy()  # destroy the frame

        def call_save_method():
            """function to call the """
            self.save_or_edit_password_page(input_password=generated_password)

        def copy_to_clipboard():
            """function to copy the generated password to clipboard"""
            self.parent.clipboard_clear()  # clearing the clip board
            self.parent.clipboard_append(f'{generated_password}')  # copied
            self.parent.update()  # store in clipboard for use outside program
            mbox.showinfo('Success', 'Password successfully copied to clipboard')

        # big frame for the generate password page
        decoration_frame = tk.Frame(self.parent, width=50, bg='white')  #
        decoration_frame.grid(row=1, column=0, )  # positioning the frame
        description = tk.Label(decoration_frame,
                               text='Your Generated Password Is',
                               font='consalas 14',
                               bg='white', fg='red')  # show description
        description.grid(ipadx=20, ipady=15, padx=15, pady=25)  # position
        # create an inner frame to hold the password text
        inner_frame = tk.Frame(decoration_frame, bg='white', )
        inner_frame.grid()  # position the frame
        password_label = tk.Label(inner_frame,
                                  bg='white', width=20,
                                  text=f'{generated_password}',
                                  font='consalas 14', )  # the password text
        password_label.grid(ipadx=10, ipady=15, padx=25, pady=25)  # position
        # create a frame to hold the copy & save button
        buttons_frame = tk.Frame(decoration_frame, bg='white')
        buttons_frame.grid()  # position the button
        copy_button = tk.Button(buttons_frame,
                                text='Copy to clipboard',
                                command=copy_to_clipboard)  # button for copy
        copy_button.grid(row=0, column=0, ipadx=1, ipady=5, padx=15, pady=10)
        save_button = tk.Button(buttons_frame,
                                bg='powderblue', text='Save password',
                                command=call_save_method)  # button for saving
        save_button.grid(row=0, column=1, ipadx=1, ipady=5, padx=15, pady=10)
        back_button = tk.Button(decoration_frame,
                                width=29, bg='pink', text='Go Back',
                                command=close_generated_pass_page
                                )
        back_button.grid(ipadx=10, ipady=10, padx=15, pady=15)

    def save_or_edit_password_page(
            self, pk=None, input_site_name=None,
            input_username=None, input_password=None, ):
        """function to display the save password window. can also
        be use to update existing credentials."""

        def close_save_password_page():
            """function to close this window"""
            decoration_frame.destroy()  # destroy the frame

        def validate_inputs():

            key = v.get()  # get key (sign whether to encrypt password or not
            site = sitename.get()  # get web site name
            user = username.get()  # get username
            pass_ = password.get()  # get password
            # check if all input are supplied
            if pass_ != '' and user != '' and site != '':
                # check if primary key for existing record is given, then call
                # update method instead of saving new record
                if pk:
                    # call update method here
                    self.password_util.refresh_btn(pk, site_name=site,
                                                   username=user,
                                                   password=pass_,
                                                   owner=self.user_id,
                                                   encrypt=key, )
                    # show success message
                    mbox.showinfo('Success', 'Credential updated successfully!')
                    decoration_frame.destroy()  # destroy the frame
                else:
                    # call save new password method
                    self.password_util.save_new_password(site,
                                                         username=user,
                                                         password=pass_,
                                                         owner=self.user_id,
                                                         encrypt=key)
                    # show success message
                    mbox.showinfo('Success', 'Credential saved successfully!')
                    # close window by destroying the frame
                    decoration_frame.destroy()
            else:
                # show error if fields are not all filled
                mbox.showwarning('Error', 'A Field can not be empty', )

        # create a big frame for this window
        decoration_frame = tk.Frame(self.parent, width=50, bg='white')  #
        decoration_frame.grid(row=1, column=0, )  # positioning the frame
        # create an inner frame
        inner_frame = tk.Frame(decoration_frame, bg='white')
        inner_frame.grid()
        # create a from to hold the check box and description
        frame_for_checkbox = tk.Frame(inner_frame, bg='white')
        frame_for_checkbox.grid()
        # description goes here
        description = tk.Label(frame_for_checkbox, text='Encrypt Password',
                               bg='white', width=32, )
        description.grid(row=0, column=0, ipady=10, sticky='w')
        v = tk.IntVar(value=1)  # variable to hold the state of check button
        # check button for encrypting password goes here
        check_button = tk.Checkbutton(frame_for_checkbox, bg='azure',
                                      variable=v, onvalue=1,
                                      offvalue=0)  # check box
        check_button.grid(row=0, column=1, padx=15)  # add separator
        # add a balloon description to widget
        self.balloon.bind(check_button, 'Untick to save password raw.')
        # draw horizontal line
        sep1 = ttk.Separator(inner_frame)
        sep1.grid()
        # ----------------------------------------------------
        # site name logo, label and input goes here
        site_name_frame = tk.Frame(inner_frame, bg='white')
        site_name_frame.grid(sticky='w', ipadx=20, padx=29)
        sitename_logo = tk.Label(site_name_frame,
                                 image=self.site_logo, bg='white')
        sitename_logo.grid(pady=5, padx=25, row=0, column=0, sticky='w')
        sitename_label = tk.Label(site_name_frame, text='Site name', compound='right',
                                  bg='white')
        sitename_label.grid(pady=5, padx=25, row=0, column=1)
        site_name_var = tk.StringVar(value=input_site_name)
        sitename = tk.Entry(inner_frame, textvariable=site_name_var,
                            width=25, bg='#f5f5f5', relief='flat')
        sitename.grid(pady=10, ipady=5)
        sitename.focus()
        # ---------------------------------------------------
        # username logo, label and input goes here
        username_frame = tk.Frame(inner_frame, bg='white')
        username_frame.grid(sticky='w', ipadx=20, padx=29)
        username_logo = tk.Label(username_frame,
                                 image=self.user_logo, bg='white')
        username_logo.grid(pady=5, padx=15, row=0, column=0)
        username_label = tk.Label(username_frame, text='Username', bg='white')
        username_var = tk.StringVar(value=input_username)
        username_label.grid(pady=5, padx=25, row=0, column=1)
        username = tk.Entry(inner_frame, textvariable=username_var,
                            width=25, bg='#f5f5f5', relief='flat')
        username.grid(pady=10, ipady=5)
        # --------------------------------------------------------
        # password logo, label and input area goes here
        password_frame = tk.Frame(inner_frame, bg='white')
        password_frame.grid(sticky='w', ipadx=20, padx=29)
        password_logo = tk.Label(password_frame,
                                 image=self.pass_logo, bg='white')
        password_logo.grid(pady=5, padx=25, row=0, column=0, sticky='e')
        password_label = tk.Label(password_frame, text='Password', bg='white', )
        password_label.grid(padx=25, row=0, column=1)
        password_var = tk.StringVar(value=input_password)
        password = tk.Entry(inner_frame, textvariable=password_var, width=25, bg='#f5f5f5', relief='flat')
        password.grid(pady=15, ipady=5)
        # --------------------------------------------------------------
        # update/save button and back button goes here
        buttons_frame = tk.Frame(decoration_frame, bg='white')
        buttons_frame.grid()
        if pk:  # set the button text base on the current state: update/save
            button_text = 'Update record'
        else:
            button_text = 'Save Credential'
            # save/update button goes here
        submit_button = tk.Button(buttons_frame,
                                  text=button_text,
                                  command=validate_inputs)  # button for copy
        submit_button.grid(row=0, column=0, ipadx=1, ipady=5, padx=15, pady=10)
        # back button goes here
        back_button = tk.Button(buttons_frame,
                                bg='azure', text='Go back',
                                command=close_save_password_page)  # button for saving
        back_button.grid(row=0, column=1, ipadx=1, ipady=5, padx=15, pady=10)

    # end of the save/update password page
    # =======================================================================

    def retrieve_single_password(self):
        """function retrieve and display a single
        credential given the site name
        """

        def close_retrieve_password_page():
            """close the current window"""
            decoration_frame.destroy()  # destroy frame
            self.result = None  # set result to None

        def copy_to_clipboard(key):
            """function to copy username or password to clipboard"""
            if key == 'username':
                self.parent.clipboard_clear()  # clearing the clip board
                self.parent.clipboard_append(f'{self.result[2]}')  # copied
                self.parent.update()  # store in clipboard for use outside program
                mbox.showinfo('Success', 'Username has been copied to clipboard')
            else:
                self.parent.clipboard_clear()  # clearing the clip board
                self.parent.clipboard_append(f'{self.result[3]}')  # copied
                self.parent.update()  # store in clipboard for use outside program
                mbox.showinfo('Success', 'Password has been copied to clipboard')

        def validate_inputs():
            """function to validate user input"""
            site_name = site_name_input.get()  # grab site name
            if site_name:
                # search record for given site name
                self.result = self.password_util.retrieve_single_password(
                    site_name, self.user_id
                )
                decoration_frame.destroy()  # destroy window
                self.retrieve_single_password()  # rebuild window with updated data
            else:
                # show error if field is empty
                mbox.showwarning('Error', 'Field can not be empty', )

        # big frame for the retrieve single password window
        decoration_frame = tk.Frame(self.parent, bg='white')  # frame
        decoration_frame.grid(row=1, column=0, ipady=0)  # positioning the frame
        # create an inner frame
        inner_frame = tk.Frame(decoration_frame, bg='white')
        inner_frame.grid(padx=0)
        # display an icon
        site_name_icon = tk.Label(inner_frame, image=self.retrieve, bg='white')
        site_name_icon.grid(row=0, column=0, padx=20, )
        # display a description
        site_name_label = tk.Label(inner_frame, width=24,
                                   text='Enter Site Name', bg='azure',
                                   font='helvetica 14')
        site_name_label.grid(ipady=15, row=0, column=1)
        # ----------------------------------------
        # draw horizontal line
        sep = ttk.Separator(decoration_frame, )
        sep.grid(sticky='we', row=1, column=0, columnspan=2)
        # site name input area goes here
        site_name_input = tk.Entry(decoration_frame, font='helvetica 12',
                                   width=25, bg='#f8f8f8', relief='flat')
        site_name_input.grid(ipady=6, ipadx=3, pady=15)
        # create frame for submit button and back button
        buttons_frame = tk.Frame(decoration_frame, bg='white')
        site_name_input.focus()  # give th input field focus
        buttons_frame.grid(pady=5)  # position the button
        # submit button goes here
        submit_button = tk.Button(buttons_frame,
                                  text='Proceed', width=15,
                                  command=validate_inputs)  # button for copy
        submit_button.grid(row=0, column=0, ipady=5, padx=15, pady=10)
        # back button goes here
        back_button = tk.Button(buttons_frame,
                                bg='azure', text='Back',
                                command=close_retrieve_password_page)  # button for saving
        back_button.grid(row=0, column=1, ipadx=1, ipady=5, padx=15, pady=10)
        # draw horizontal line
        sep = ttk.Separator(decoration_frame, )
        sep.grid(sticky='we', column=0, columnspan=2)
        # if there exist a record for a given site name, add details below
        if self.result:
            # create another frame
            info_frame = tk.Frame(decoration_frame, bg='white')
            info_frame.grid(sticky='w')
            # display site name here
            site_name_label = tk.Label(info_frame, text='Site name:', bg='white')
            site_name_label.grid(row=0, column=0, ipadx=10, ipady=10)
            site_name_field = tk.Label(info_frame, text=f"{self.result[1]}",
                                       bg='white')
            site_name_field.grid(row=0, column=1, ipadx=10, ipady=10, sticky='w')
            # ------------------------------------------------------
            # display username here
            username_label = tk.Label(info_frame, text='Username:',
                                      bg='white')
            username_label.grid(row=1, column=0, ipadx=10, ipady=10)
            username_field = tk.Label(info_frame, text=f"{self.result[2]}",
                                      bg='white')
            username_field.grid(row=1, column=1, ipadx=10,
                                ipady=10, sticky='w')
            copy_username = tk.Button(
                info_frame, image=self.copy_image, bg='white', relief='flat',
                command=lambda key='username': copy_to_clipboard(key))
            copy_username.grid(row=1, column=2)
            self.balloon.bind(copy_username, 'Copy  username to clipboard')
            # ----------------------------------------------------
            # display password here
            password_label = tk.Label(info_frame, text='Password:',
                                      bg='white')
            password_label.grid(row=2, column=0, ipadx=10, ipady=10)
            password_field = tk.Label(info_frame, text=f"{self.result[3][:15]}",
                                      bg='white')
            password_field.grid(row=2, column=1, ipadx=10,
                                ipady=10, sticky='w')
            copy_password = tk.Button(
                info_frame, image=self.copy_image, bg='white', relief='flat',
                command=lambda key='password': copy_to_clipboard(key))
            copy_password.grid(row=2, column=2)
            self.balloon.bind(copy_password, 'Copy  password to clipboard')
            # draw horizontal line
            sep = ttk.Separator(decoration_frame, )
            sep.grid(sticky='we', column=0, columnspan=2)
            # ----------------------------------------------------------
            # create a small frame to hold the delete, edit, and launch buttons
            buttons_frame = tk.Frame(decoration_frame, bg='white')
            buttons_frame.grid(pady=5, sticky='w')
            # delete button goes here
            delete_button = tk.Button(
                buttons_frame, image=self.delete_logo, bg='white',
                relief='flat', bd=0,
                command=lambda pk=self.result[0]: self.confirm_delete(pk))
            delete_button.grid(row=0, column=0, ipadx=1,
                               ipady=5, padx=5, pady=10)
            self.balloon.bind(delete_button, 'Delete record')
            edit_button = tk.Button(
                buttons_frame, image=self.edit_logo,
                bg='white', relief='flat', bd=0,
                command=lambda pk=self.result[0],
                               site_name=self.result[1],
                               username=self.result[2],
                               password=self.result[3]:
                self.save_or_edit_password_page(
                    pk, site_name, username, password
                ))  # button for saving
            edit_button.grid(row=0, column=1, ipady=5, padx=5, pady=10)
            self.balloon.bind(edit_button, 'Update record')
            # add a view button
            view_button = tk.Button(
                buttons_frame, image=self.view_logo,
                bg='white', relief='flat', bd=0,
                command=lambda pk=self.result[0],
                               site_name=self.result[1],
                               username=self.result[2],
                               password=self.result[3]: self.view_and_edit_page(
                    pk, site_name, username, password
                ))
            view_button.grid(row=0, column=2, padx=2, ipadx=1, ipady=3, pady=10)
            self.balloon.bind(view_button, 'View Details')
            # add launch button for familiar website

            familiar_site = ['facebook', 'instagram', 'twitter', 'github', 'whatsapp']
            if self.result[1] in familiar_site:
                lunch_button = tk.Button(buttons_frame,
                                         bg='azure', text='launch site',
                                         command=self.lunch_site)  # button for saving
                lunch_button.grid(row=0, column=3, ipadx=1, ipady=3, padx=5, pady=5)
                self.balloon.bind(lunch_button, 'Launch website in browser')
        # if no record available, display empty space
        else:
            space = tk.Label(decoration_frame, bg='white')
            space.grid(pady=60, ipady=20)
        # end of the retrieve single password page
        # =============================================================

    def retrieve_all_password_page(self):
        """function retrieve and display all
         password for the logged in user
         """

        def close_retrieve_all_password_page():
            """function to close this window"""
            decoration_frame.destroy()  # destroy the frame

        # grab all the credentials in the database for the logged in user.
        records = self.password_util.retrieve_all_password(self.user_id)
        # create a frame to hold the window
        decoration_frame = tk.Frame(self.parent, bg='white')  # frame
        decoration_frame.grid(row=1, column=0, ipady=0)  # positioning the frame
        # create another internal frame
        inner_frame = tk.Frame(decoration_frame, bg='white')
        inner_frame.grid(padx=0)
        # display an icon
        site_name_icon = tk.Label(inner_frame, image=self.all_pass, bg='white')
        site_name_icon.grid(row=0, column=0, padx=20, )
        # display some description
        site_name_label = tk.Label(inner_frame, width=20,
                                   text='All Saved Credentials', bg='azure',
                                   font='helvetica 14')
        site_name_label.grid(ipady=15, row=0, column=1)
        # display a back button
        back_button = tk.Button(inner_frame,
                                bg='azure', text='Back', relief='flat',
                                command=close_retrieve_all_password_page)  # button for saving
        back_button.grid(row=0, column=2, ipadx=1, ipady=14, pady=0)
        # ----------------------------------------
        # draw a horizontal line
        sep = ttk.Separator(decoration_frame, )
        sep.grid(sticky='we', row=1, column=0, columnspan=2)
        # create another frame to hold the table headers
        header_frame = tk.Frame(decoration_frame, bg='azure')
        header_frame.grid(sticky='w')
        # display the table headers i.e sitename, username, and actions
        site_name_label = tk.Label(header_frame, text='Site name', bg='azure')
        site_name_label.grid(row=0, column=0, ipadx=10, ipady=10)
        username_label = tk.Label(header_frame, text='Username', bg='azure',
                                  width=15)
        username_label.grid(row=0, column=1, ipadx=10, ipady=10)
        action_label = tk.Label(header_frame, text='Options', bg='azure',
                                width=10)
        action_label.grid(row=0, column=3, ipadx=3, ipady=10)
        # draw a horizontal line
        sep = ttk.Separator(decoration_frame, )
        sep.grid(sticky='we', row=3, column=0, columnspan=2)
        # ------------------------------------------------------
        # create a scrollable frame from the Pmw module to display the
        # retrieved the password
        sf = Pmw.ScrolledFrame(decoration_frame, labelpos='n',
                               hscrollmode='none',
                               vscrollmode='static',
                               usehullsize=1, hull_width=405, hull_height=296)
        sf.grid(pady=3, )
        content_frame = sf.interior()  # make a reference to the interior part
        # create a for loop from the retrieved record while populating the data
        # i use the enumerate function to grab the index which is use to grid
        # the widget while in the for loop
        for index, record in enumerate(records):
            if len(record[1]) > 9:  # slice the site name if too long
                site_name = f"{record[1][:10]}..."
            else:
                site_name = record[1]  # else leave it un touch
            # display site name here
            site_name_field = tk.Label(content_frame, text=site_name,
                                       bg='white', width=10)
            site_name_field.grid(row=index, column=0, ipadx=1, ipady=10, sticky='w')
            if len(record[2]) > 10:  # slice the username if too long > 10
                username = f"{record[2][:10]}..."
            else:
                username = record[2]  # else leave it un touch
            # display username here
            username_field = tk.Label(content_frame, text=username,
                                      bg='white', width=13)
            username_field.grid(row=index, column=1, ipadx=10, ipady=10, )
            # ----------------------------------------------------
            # create a frame to hold the action buttons
            action_frame = tk.Frame(content_frame, bg='white')
            action_frame.grid(row=index, column=2, )
            # first is the delete button
            delete_button = tk.Button(
                action_frame, image=self.delete_logo,
                bg='white', width=8, relief='flat', bd=0,
                command=lambda pk=record[0]: self.confirm_delete(pk)
            )
            delete_button.grid(row=0, column=0, ipadx=12, ipady=6, )
            # show a tooltip
            self.balloon.bind(delete_button, 'Delete credentials')
            # display a launch button if the site is a familiar one
            familiar_site = ['facebook', 'instagram', 'twitter', 'github',
                             'whatsapp']
            if record[1] in familiar_site:
                launch_button = tk.Button(action_frame, image=self.web_logo,
                                          bg='white', width=8, relief='flat',
                                          command=self.lunch_site, bd=0)
                launch_button.grid(row=0, column=1, ipadx=11, ipady=5, )
                self.balloon.bind(launch_button, 'Launch web site on browser')
            else:
                # if site not familiar, remove launch button and display space
                empty_space = tk.Label(action_frame, bg='white', width=2)
                empty_space.grid(row=0, column=1, padx=5)
            # next is th view button
            view_button = tk.Button(
                action_frame, image=self.view_logo,
                bg='white', width=8, relief='flat', bd=0,
                command=lambda pk=record[0],
                               site_name=record[1],
                               username=record[2],
                               password=record[3]: self.view_and_edit_page(
                    pk, site_name, username, password
                ))
            view_button.grid(row=0, column=2, ipadx=12, ipady=6, )
            self.balloon.bind(view_button, 'View record in detail')
        # ----------------------------------------------------------

    def view_and_edit_page(self, pk, site_name_, username_, password_):
        """the function provide the page to view password information
        and a switch to toggle edit mode.
        """
        self.edit = False  # condition for either editing or just display

        def close_this_page():
            """function to destroy this window"""
            decoration_frame.destroy()  # destroy the frame

        def change_mode():
            """function to change mode: edit or display"""
            if self.edit:
                self.edit = False
            else:
                self.edit = True
                # call the edit page method
                self.save_or_edit_password_page(pk, site_name_,
                                                username_, password_)
            decoration_frame.destroy()  # destroy the frame to close the page

        # create frame to hold this window
        decoration_frame = tk.Frame(self.parent, width=50, bg='white')  #
        decoration_frame.grid(row=1, column=0, )  # positioning the frame
        # create frame for check button
        frame_for_checkbox = tk.Frame(decoration_frame, bg='white')
        frame_for_checkbox.grid()
        # display a back button
        back_button = tk.Button(frame_for_checkbox,
                                bg='azure', text='Back', width=5,
                                command=close_this_page)  # button for saving
        back_button.grid(row=0, column=0, ipadx=1, ipady=5, pady=10)
        # create an int variable to hold state of check box
        check_value = tk.IntVar(value=0)
        # dynamic header base on the value of check button
        if check_value:
            place_holder = tk.StringVar(value='Toggle Edit Mode')
        else:
            place_holder = tk.StringVar(value='Toggle View Mode')
        # add a description here
        description = tk.Label(frame_for_checkbox, textvariable=place_holder,
                               bg='white', width=20, )
        description.grid(row=0, column=1, ipady=10, sticky='w')
        # the check button for switch goes here
        check_button = tk.Checkbutton(frame_for_checkbox, bg='azure',
                                      variable=check_value, onvalue=1,
                                      offvalue=0, command=change_mode)  # check box
        check_button.grid(row=0, column=2, padx=15)  # add separator
        self.balloon.bind(check_button, 'Switch to Edit mode')
        # draw a horizontal line
        sep1 = ttk.Separator(decoration_frame)
        sep1.grid(sticky='we', row=3, column=0, columnspan=2)
        # create another frame
        inner_frame = tk.Frame(decoration_frame, bg='white')  # create a frame
        inner_frame.grid()
        # show some description
        description = tk.Label(inner_frame, text='Password View Mode',
                               bg='azure', width=32, font='helvetica 14')
        description.grid(row=0, column=0, ipady=10, sticky='w')
        # ----------------------------------------------------
        # site logo, label and display goes here
        site_name_frame = tk.Frame(inner_frame, bg='white')
        site_name_frame.grid(sticky='w', ipadx=20, padx=29)
        sitename_logo = tk.Label(site_name_frame,
                                 image=self.site_logo, bg='white')
        sitename_logo.grid(pady=5, padx=25, row=0, column=0, sticky='w')
        sitename_label = tk.Label(site_name_frame, text='Site name', compound='right',
                                  bg='white')
        sitename_label.grid(pady=5, padx=25, row=0, column=1)
        sitename = tk.Label(inner_frame, text=site_name_,
                            width=25, bg='#f5f5f5', relief='flat')
        sitename.grid(pady=10, ipady=5)
        # ---------------------------------------------------
        # username logo, label and display goes here
        username_frame = tk.Frame(inner_frame, bg='white')
        username_frame.grid(sticky='w', ipadx=20, padx=29)
        username_logo = tk.Label(username_frame,
                                 image=self.user_logo, bg='white')
        username_logo.grid(pady=5, padx=15, row=0, column=0)
        username_label = tk.Label(username_frame, text='Username', bg='white', )
        username_label.grid(pady=5, padx=25, row=0, column=1)
        username = tk.Label(inner_frame, text=username_,
                            width=25, bg='#f5f5f5', relief='flat')
        username.grid(pady=10, ipady=5)
        # --------------------------------------------------------
        # password logo, label and display goes here
        password_frame = tk.Frame(inner_frame, bg='white')
        password_frame.grid(sticky='w', ipadx=20, padx=29)
        password_logo = tk.Label(password_frame,
                                 image=self.pass_logo, bg='white')
        password_logo.grid(pady=5, padx=25, row=0, column=0, sticky='e')
        password_label = tk.Label(password_frame, text='Password', bg='white', )
        password_label.grid(padx=25, row=0, column=1)
        password = tk.Label(inner_frame, text=password_, width=25,
                            bg='#f5f5f5', relief='flat')
        password.grid(pady=15, ipady=5)

    # end of this view
    # ======================================================
    # extral functionalities goes here

    def confirm_delete(self, pk):
        """method to confirm and initiate delete query"""
        if mbox.askyesno('Confirm Delete',
                         'Are you sure you want to delete the credentials?'):
            self.password_util.delete_single_record(pk)
            mbox.showinfo('Success', 'Credential have been deleted successfully')

    def close_program(self):
        """method to close the program"""
        if mbox.askokcancel('warning', 'Do want to close the program?'):
            exit()
        else:
            pass

    def lunch_site(self):
        """function to launch web browser to any of the below web site"""
        site_name = self.result[1]  # grab site name from the result
        if site_name == 'facebook':
            webbrowser.open('www.facebook.com')
        elif site_name == 'twitter':
            webbrowser.open('www.twitter.com')
        elif site_name == 'whatsapp':
            webbrowser.open('www.whatsapp.com')
        elif site_name == 'instagram':
            webbrowser.open('www.instagram.com')
        elif site_name == 'github':
            webbrowser.open('www.github.com')

    def about_page(self):
        """function for displaying help"""

        def destroy_about_page():
            """function for closing this window
            """
            about_frame.destroy()
            # bt4['state']='active'

        # -------------------------------------------------------


        about_frame = tk.Frame(self.parent, bg='white')
        about_frame.grid(row=1, column=0)
        about_frame['bd'] = 2
        # notebook = Pmw.NoteBook(about_frame,)
        # page_one = notebook.add('About Us')
        # page_two = notebook.add('Developer')
        #
        # notebook.grid(padx=5, pady=5)
        small_frame = tk.Frame(about_frame, bg='azure')
        small_frame.grid()
        btn = tk.Button(small_frame, text='Back', width=5, relief='ridge',
                        bg='azure', command=destroy_about_page, )
        btn.grid(row=0, column=0, )
        header = tk.Label(small_frame, text='Password Manager', width=20,
                          font='matura 15', bg='azure')
        header.grid(row=0, column=1, padx=4)
        sep = ttk.Separator(about_frame, )
        sep.grid(sticky='we', row=1, column=0, columnspan=2)
        version_label = tk.Label(about_frame, bg='white',
                                 text='Version Number')
        version_label.grid()
        version = tk.Label(about_frame, bg='white', font='matura 14',
                           text=f'v{__version__}')
        version.grid()
        # -------------------------------------------------------
        # second help
        sep = ttk.Separator(about_frame, )
        sep.grid(sticky='we', columnspan=2)
        # designer = tk.Label(about_frame, text='Developer', relief='flat',
        #                     bg='white', pady=5, compound='left', width=33, )
        # designer.grid()
        org_logo = tk.Label(about_frame, image=self.legacy_logo, bg='white', )
        org_logo.grid()
        sep = ttk.Separator(about_frame, )
        sep.grid(sticky='we', column=0, columnspan=2)
        fb_and_email_frame = tk.Frame(about_frame)
        fb_and_email_frame.grid(pady=10)
        fb_logo = tk.Label(fb_and_email_frame, image=self.delete_logo,
                           bg='white',)
        fb_logo.grid(row=0, column=0)
        fb = tk.Label(fb_and_email_frame, text='Legacy Technology',
                            relief='flat', bg='white', pady=5, compound='left', )
        fb.grid(row=0, column=1)
        youtube_logo = tk.Label(fb_and_email_frame, image=self.edit_logo,
                              bg='white', )
        youtube_logo.grid(row=0, column=2)
        youtube = tk.Label(fb_and_email_frame, text='Legacy Technology',
                            relief='flat', bg='white', pady=5, compound='left', )
        youtube.grid(row=0, column=3)
        email_frame = tk.Frame(about_frame)
        email_frame.grid()
        email_logo = tk.Label(email_frame, image=self.edit_logo,
                              bg='white', )
        email_logo.grid(row=0, column=2)
        email = tk.Label(email_frame, text='Legacytechnology1@gmail.com',
                         relief='flat', bg='white', pady=5, compound='left', )
        email.grid(row=0, column=3)
        sep = ttk.Separator(about_frame, )
        sep.grid(sticky='we', column=0, columnspan=2)
        # ---------------------------------------------

    def developer_page(self):
        """function for displaying the developer page"""

        def destroy_cre():
            """function for destroying the contributor
                frame after displaying the contributor
                section.
            """
            credit_frame.destroy()

        # --------------------------------------------------------------------

        credit_frame = tk.Frame(self.parent, bg='white')
        credit_frame.grid(row=1, column=0)
        small_frame = tk.Frame(credit_frame, bg='azure')
        small_frame.grid(columnspan=2, row=0, column=0,)
        btn = tk.Button(small_frame, text='Back', width=5, relief='ridge',
                        bg='azure', command=destroy_cre, )
        btn.grid(row=0, column=0, )
        header = tk.Label(small_frame, text='Meet Developer', width=20,
                          font='matura 15', bg='azure')
        header.grid(row=0, column=1, padx=4)
        image = tk.Label(credit_frame, image=self.my_pix)
        image.grid(row=1, column=0, pady=21)
        info_frame = tk.Frame(credit_frame, bg='white')
        info_frame.grid(row=1, column=1)
        name = tk.Label(info_frame, text='Dama Michael Y', bg='white')
        name.grid(row=0, column=0, pady=2, ipady=5, )
        sep = ttk.Separator(info_frame, )
        sep.grid(sticky='we', row=1, column=0, columnspan=2)
        rank = tk.Label(info_frame, text='Legacy Technology', bg='white',)
        rank.grid(row=2, column=0, pady=2, ipady=5, )
        sep = ttk.Separator(info_frame, )
        sep.grid(sticky='we', row=3, column=0, columnspan=2)
        phone = tk.Label(info_frame, text='08160535033', bg='white',)
        phone.grid(row=4, column=0, pady=2, ipady=5, )

        copy_right = tk.Label(credit_frame,
                              text='@ 2021 Legacy Technology',
                              font='matura 14', bg='azure', width=27 )
        copy_right.grid(ipady=7, ipadx=3, columnspan=2)

        # --------------------------------------------------------------------


def main():
    root = tk.Tk()
    MasterFrame(root)
    root.configure(bg='white')
    root.mainloop()


if __name__ == '__main__':
    main()
