import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("400x300")

        self.contacts_file = "con_details_manager.json"
        self.load_contacts()

        # Create and place widgets
        self.listbox = tk.Listbox(root)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(root, text="Edit Contact", command=self.edit_contact)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.view_button = tk.Button(root, text="View Contact", command=self.view_contact)
        self.view_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.refresh_listbox()

    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'r') as file:
                self.contacts = json.load(file)
        else:
            self.contacts = {}

    def save_contacts(self):
        with open(self.contacts_file, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for name in self.contacts:
            self.listbox.insert(tk.END, name)

    def add_contact(self):
        name = simpledialog.askstring("Add Contact", "Enter name:")
        if name:
            if name in self.contacts:
                messagebox.showerror("Error", "Contact already exists.")
                return

            phone = simpledialog.askinteger("Add Contact", "Enter phone number:")
            email = simpledialog.askstring("Add Contact", "Enter email address:")
            self.contacts[name] = {"phone": phone, "email": email}            
            self.save_contacts()
            self.refresh_listbox()

    def edit_contact(self):
        selected_contact = self.listbox.get(tk.ACTIVE)
        if selected_contact and selected_contact != "Contacts are empty":
            new_name = simpledialog.askstring("Edit Contact", "Edit name:", initialvalue=selected_contact)
            if new_name:
                if new_name != selected_contact and new_name in self.contacts:
                    messagebox.showerror("Error", "Another contact with this name already exists.")
                    return

                phone = simpledialog.askinteger("Edit Contact", "Edit phone number:", initialvalue=self.contacts[selected_contact]["phone"])
                email = simpledialog.askstring("Edit Contact", "Edit email address:", initialvalue=self.contacts[selected_contact]["email"])
                del self.contacts[selected_contact]
                self.contacts[new_name] = {"phone": phone, "email": email}
                self.save_contacts()
                self.refresh_listbox()

    def delete_contact(self):
        selected_contact = self.listbox.get(tk.ACTIVE)
        if selected_contact and selected_contact != "Contacts are empty":
            confirm = messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {selected_contact}?")
            if confirm:
                del self.contacts[selected_contact]
                self.save_contacts()
                self.refresh_listbox()

    def view_contact(self):
        selected_contact = self.listbox.get(tk.ACTIVE)
        if selected_contact and selected_contact != "Contacts are empty":
            contact = self.contacts[selected_contact]
            messagebox.showinfo("View Contact", f"Name: {selected_contact}\nPhone: {contact['phone']}\nEmail: {contact['email']}")

# Create the main window and start the contact management system
root = tk.Tk()
app = ContactManager(root)
root.mainloop()
