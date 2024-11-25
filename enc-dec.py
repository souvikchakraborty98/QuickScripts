from cryptography.fernet import Fernet
import base64
import os
import random
import string
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key(password):
    """
    Generates a Fernet key based on the provided password.
    """
    salt = bytes('12345678910111213141516','utf-8')
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000)
    adr=kdf.derive(bytes(password, 'utf-8'))
    key = base64.urlsafe_b64encode(adr)
    f = Fernet(key)
    return f


def encrypt_file(key, input_file, output_file):
    """
    Encrypts the input file using the given key and saves the encrypted data to the output file.
    """
    try:
        with open(input_file, 'rb') as file:
            input_data = file.read()
            encrypted_data = key.encrypt(input_data)
            with open(output_file, 'wb') as output:
                output.write(encrypted_data)
        messagebox.showinfo("Encryption Successful", "File encrypted successfully.")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "Input file not found.")
    except PermissionError:
        messagebox.showerror("Permission Denied", "Unable to write to output file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while encrypting the file: {str(e)}")


def decrypt_file(key, input_file, output_file):
    """
    Decrypts the input file using the given key and saves the decrypted data to the output file.
    """
    try:
        with open(input_file, 'rb') as file:
            input_data = file.read()
            decrypted_data = key.decrypt(input_data)
            with open(output_file, 'wb') as output:
                output.write(decrypted_data)
        messagebox.showinfo("Decryption Successful", "File decrypted successfully.")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "Input file not found.")
    except PermissionError:
        messagebox.showerror("Permission Denied", "Unable to write to output file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while decrypting the file: {str(e)}")


def encrypt_button_clicked():
    """
    Event handler for encrypt button.
    """
    input_file = filedialog.askopenfilename(title="Select Input File", filetypes=[("All Files", "*.*")])
    output_file = filedialog.asksaveasfilename(title="Save Encrypted File As", defaultextension="enc",
                                               filetypes=[("Encrypted Files", "*.enc")])

    if input_file and output_file:
        password = simpledialog.askstring("Password", "Please enter the password to encrypt:")
        key = generate_key(password)
        encrypt_file(key, input_file, output_file)
        messagebox.showinfo("Password", f"The password used was: {password}. Please remember it for decryption.")


def decrypt_button_clicked():
    """
    Event handler for decrypt button.
    """
    input_file = filedialog.askopenfilename(title="Select Input File", filetypes=[("Encrypted Files", "*.enc")])
    output_file = filedialog.asksaveasfilename(title="Save Decrypted File As", defaultextension="",
                                                   filetypes=[("All Files", "*.*")])
    if input_file and output_file:
        password = simpledialog.askstring("Password", "Please enter the password to decrypt:")
        if password:
            key = generate_key(password)
            decrypt_file(key, input_file, output_file)


# Create the main window
window = tk.Tk()
window.title("File Encryption/Decryption")
window.geometry("400x200")

# Encrypt button
encrypt_button = tk.Button(window, text="Encrypt File", command=encrypt_button_clicked)
encrypt_button.pack()

# Decrypt button
decrypt_button = tk.Button(window, text="Decrypt File", command=decrypt_button_clicked)
decrypt_button.pack()

# Start the main event loop
window.mainloop()
