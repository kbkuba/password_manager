from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    password_list = []

    [password_list.append(choice(LETTERS)) for _ in range(randint(8, 10))]
    [password_list.append(choice(SYMBOLS)) for _ in range(randint(2, 4))]
    [password_list.append(choice(NUMBERS)) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(str(char) for char in password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}\n"
                                                              f"Password: {password}\nIs it okay to save?")

        if is_ok:
            try:
                with open("passwords.json", "r") as passwords:
                    # Reading old data
                    data = json.load(passwords)
            except FileNotFoundError:
                with open("passwords.json", "w") as passwords:
                    json.dump(new_data, passwords, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("passwords.json", "w") as passwords:
                    # passwords.write(f"{website} | {email} | {password}\n")
                    # Saving updated data
                    json.dump(data, passwords, indent=4)
            finally:
                website_entry.delete(0, "end")
                password_entry.delete(0, "end")


# ---------------------------- Find Password ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("passwords.json", "r") as passwords:
            data = json.load(passwords)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops!", message="No data file found.")
    else:
        if website in data:
            saved_email = data[f"{website}"]["email"]
            saved_password = data[f"{website}"]["password"]
            messagebox.showinfo(title=f"{website}", message=f"Email: {saved_email}\nPassword: {saved_password}")
        else:
            messagebox.showinfo(title="Oops!", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=36)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "your_e-mail@mail.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

gen_pass_button = Button(text="Generate Password", width=11, command=password_generator)
gen_pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=11, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
