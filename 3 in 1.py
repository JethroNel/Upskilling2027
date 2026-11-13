import random
import string
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from cryptography.fernet import Fernet

# Password Generator
def generate_password():
    length = int(length_entry.get())
    if length < 4:
        messagebox.showerror("Error", "Who would make a password with less than 4 characters??.")
        return
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(password)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    root.update()
    messagebox.showinfo("Success", "Password copied to clipboard Successfully!")

# File Encryptor
def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(file_path, password):
    try:
        key = get_key(password)
        cipher = AES.new(key, AES.MODE_CBC)
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = cipher.iv + cipher.encrypt(pad(data, AES.block_size))
        
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)
        
        messagebox.showinfo("Success", "The File encryption was a success Woop woop!!!")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")

def decrypt_file(file_path, password):
    try:
        key = get_key(password)
        
        with open(file_path, 'rb') as f:
            iv = f.read(16)
            encrypted_data = f.read()
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        output_path = file_path.replace(".enc", "")
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        messagebox.showinfo("Success", "File decryption Completed Your hand!!!")
    except ValueError:
        messagebox.showerror("Error", "Incorrect .. Pay attention!!!")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed.. You failed Turkey!!!!: {e}")

def select_file(action):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password at this time and try again!!!!!!!")
        return
    
    if action == "encrypt":
        encrypt_file(file_path, password)
    elif action == "decrypt":
        decrypt_file(file_path, password)

# Password Manager
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return key

encryption_key = load_key()
cipher = Fernet(encryption_key)
PASSWORD_FILE = "passwords.json"
MASTER_PASSWORD = "Fafit@=mc2"

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def save_password(site, username, password):
    encrypted_password = encrypt_password(password)
    data = load_passwords()
    data[site] = {"username": username, "password": encrypted_password}
    with open(PASSWORD_FILE, "w") as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Success", "Well done Mi lord, Password saved successfully!")

def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    return {}

def view_passwords():
    master_pass = simpledialog.askstring("Master Password", "Enter master password here, Your hand:", show='*')
    if master_pass == MASTER_PASSWORD:
        passwords = load_passwords()
        display_text = ""
        for site, creds in passwords.items():
            username = creds["username"]
            password = decrypt_password(creds["password"])
            display_text += f"Site: {site}\nUsername: {username}\nPassword: {password}\n\n"
        if display_text:
            messagebox.showinfo("Saved Passwords", display_text)
        else:
            messagebox.showinfo("No Passwords", "No passwords saved yet.")
    else:
        messagebox.showerror("Error", "Incorrect master password.. who are you and what do you want!??")

def add_password():
    site = simpledialog.askstring("Input", "Enter Website/App Name:")
    username = simpledialog.askstring("Input", "1. Enter Correct Username:")
    password = simpledialog.askstring("Input", "2. Enter Correct Password here:")
    if site and username and password:
        save_password(site, username, password)

# GUI Setup
root = tk.Tk()
root.title("Security Suite")
root.geometry("500x550")

tk.Label(root, text="Password Generator").pack(pady=5)
length_entry = tk.Entry(root)
length_entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate Password here", command=generate_password)
generate_btn.pack(pady=5)

password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, state='readonly', width=30)
password_entry.pack(pady=5)

copy_btn = tk.Button(root, text="Copy this password to Clipboard ??", command=copy_to_clipboard)
copy_btn.pack(pady=5)

tk.Label(root, text="File Encryptor").pack(pady=5)
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

tk.Button(root, text="Select File for Encryption", command=lambda: select_file("encrypt")).pack(pady=5)
tk.Button(root, text="Select File to Decrypt", command=lambda: select_file("decrypt")).pack(pady=5)

tk.Label(root, text="Password Manager").pack(pady=5)
tk.Button(root, text="Add Your Passwords here", command=add_password).pack(pady=5)
tk.Button(root, text="View All Passwords here", command=view_passwords).pack(pady=5)

tk.Button(root, text="Leave Now", command=root.quit).pack(pady=10)

root.mainloop()
