from tkinter import *
import string
import random
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- SAVE PASSWORD ------------------------------- #
def clearing_entries():
    website_entry.delete(0, "end")
    password_label_entry.delete(0, "end")


def saving_password():
    websitename = website_entry.get()
    useremail = email_or_username_entry.get()
    userpassword = password_label_entry.get()
    data_entry = {
        websitename: {
            "email": useremail,
            "password": userpassword,
        }
    }

    if len(userpassword) == 0 or len(useremail) == 0 or len(websitename) == 0:
        messagebox.showinfo(title="Oops!", message="Please fill all the fields.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(data_entry, file, indent=4)

        else:
            data.update(data_entry)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            clearing_entries()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# this password generation
# mechanism is complete of my own thought of approaching this process. The passwords generated using this function
# were tested using password strength checker websites, and they turned out to be very strong.
def password_generation(entry_widget):
    entry_widget.delete(0, "end")
    all_case_alphabets = list(string.ascii_letters)
    numbers_for_password = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    symbols = ['!', '@', '#', '$', '%', '&', '*']
    generated_password = []
    for i in range(16):
        random_entry = random.randint(0, 6)
        if random_entry == 1 or random_entry == 4 or random_entry == 0:
            random_alphabet_number = random.randint(0, 51)
            random_alphabet = all_case_alphabets[random_alphabet_number]
            generated_password.append(random_alphabet)
        elif random_entry == 5 or random_entry == 3:
            random_number_no = random.randint(0, 9)
            random_number = numbers_for_password[random_number_no]
            generated_password.append(random_number)
        elif random_entry == 2 or random_entry == 6:
            random_symbol_number = random.randint(0, 6)
            random_symbol = symbols[random_symbol_number]
            generated_password.append(random_symbol)

    generated_password_string = ''.join(map(str, generated_password))
    entry_widget.insert(0, f"{generated_password_string}")
    pyperclip.copy(generated_password_string)


# ---------------------------- SEARCHING MECHANISM ------------------------------- #
def search(webname):
    websitename = webname.get()
    with open("data.json", "r") as file:
        data = json.load(file)
        try:
            retrieved_info = data[websitename]
        except KeyError:
            messagebox.showinfo(title="Oops!", message="The website is not listed")
        else:
            messagebox.showinfo(title="Info Found", message=f"Email: {retrieved_info['email']}\n"
                                                            f"Password : {retrieved_info['password']}")
            pyperclip.copy(retrieved_info['password'])
        finally:
            clearing_entries()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# setting up the canvas
canvas = Canvas(height=200, width=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

# setting up the labels needed
website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

email_or_username_label = Label(text="Email/Username: ")
email_or_username_label.grid(column=0, row=2)

password_label = Label(width=21, text="Password: ")
password_label.grid(column=0, row=3)

# setting up the Entries
website_entry = Entry()
website_entry.grid(column=1, row=1, columnspan=2, sticky='EW')
website_entry.focus()

email_or_username_entry = Entry()
email_or_username_entry.grid(column=1, row=2, sticky='EW')
email_or_username_entry.insert(0, "sumitbajiraopatil@gmail.com")

password_label_entry = Entry()
password_label_entry.grid(column=1, row=3, sticky='EW')

# setting up the buttons
generate_password_button = Button(text="Generate Password", command=lambda: password_generation(password_label_entry))
generate_password_button.grid(column=2, row=3, sticky='EW')

add_button = Button(text="Add", width=36, command=saving_password)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=lambda: search(website_entry))
search_button.grid(column=2, row=1, sticky='EW')

window.mainloop()
