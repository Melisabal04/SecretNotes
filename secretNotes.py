from tkinter import *
from tkinter import messagebox
import base64

# Encode function (Encrypt)
def encode(key, clear_text):
    enc = []
    for i in range(len(clear_text)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear_text[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

# Decode function (Decrypt)
def decode(key, enc_text):
    dec = []
    enc_text = base64.urlsafe_b64decode(enc_text).decode()
    for i in range(len(enc_text)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc_text[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

# Save and Encrypt Notes
def save_and_encrypt_notes():
    title = title_entry.get()
    message = input_text.get("1.0", END).strip()
    master_secret = master_secret_input.get()

    if len(title) == 0 or len(message) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        message_encrypted = encode(master_secret, message)
        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f'\nTitle: {title}\nEncrypted Message: {message_encrypted}\n')
        except FileNotFoundError:
            with open("mysecret.txt", "w") as data_file:
                data_file.write(f'\nTitle: {title}\nEncrypted Message: {message_encrypted}\n')
        finally:
            title_entry.delete(0, END)
            master_secret_input.delete(0, END)
            input_text.delete("1.0", END)
            messagebox.showinfo(title="Success", message="Your note has been encrypted and saved!")

# Decrypt Notes
def decrypt_notes():
    message_encrypted = input_text.get("1.0", END).strip()
    master_secret = master_secret_input.get()

    if len(message_encrypted) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            input_text.delete("1.0", END)
            input_text.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please make sure of the encrypted information.")

# UI Setup
window = Tk()
window.title("Secret Notes")
window.config(padx=30, pady=30)


title_info_label = Label(text="Enter your title", font=("Verdana", 20, "normal"))
title_info_label.pack()

title_entry = Entry(width=30)
title_entry.pack()

input_info_label = Label(text="Enter your secret", font=("Verdana", 20, "normal"))
input_info_label.pack()

input_text = Text(width=50, height=25)
input_text.pack()

master_secret_label = Label(text="Enter master key", font=("Verdana", 20, "normal"))
master_secret_label.pack()

master_secret_input = Entry(width=30)
master_secret_input.pack()

save_button = Button(text="Save & Encrypt", command=save_and_encrypt_notes)
save_button.pack()

decrypt_button = Button(text="Decrypt", command=decrypt_notes)
decrypt_button.pack()

window.mainloop()
