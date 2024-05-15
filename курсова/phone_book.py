import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class ContactBookApp:
    def __init__(self, master):
        self.master = master
        master.title("Телефонний довідник")
        master.geometry("500x350")
        
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)
        
        self.label = tk.Label(self.frame, text="Вітаю! Оберіть функцію для використання:", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.style = ttk.Style()
        self.style.configure('Black.TButton', foreground='black', borderwidth=2, highlightthickness=2)
        
        self.add_button = ttk.Button(self.frame, text="Додати контакт", command=self.add_contact, style='Black.TButton')
        self.add_button.grid(row=1, column=0, pady=5, padx=10, ipadx=10, sticky="EW")
        
        self.edit_button = ttk.Button(self.frame, text="Редагувати контакт", command=self.edit_contact, style='Black.TButton')
        self.edit_button.grid(row=1, column=1, pady=5, padx=10, ipadx=10, sticky="EW")
        
        self.delete_button = ttk.Button(self.frame, text="Видалити контакт", command=self.delete_contact, style='Black.TButton')
        self.delete_button.grid(row=2, column=0, pady=5, padx=10, ipadx=10, sticky="EW")
        
        self.delete_all_button = ttk.Button(self.frame, text="Видалити всі контакти", command=self.delete_all_contacts, style='Black.TButton')
        self.delete_all_button.grid(row=2, column=1, pady=5, padx=10, ipadx=10, sticky="EW")
        
        self.search_button = ttk.Button(self.frame, text="Пошук", command=self.search_contact, style='Black.TButton')
        self.search_button.grid(row=3, column=0, pady=5, padx=10, ipadx=10, sticky="EW")
        
        self.view_button = ttk.Button(self.frame, text="Переглянути контакти", command=self.view_contacts, style='Black.TButton')
        self.view_button.grid(row=3, column=1, pady=5, padx=10, ipadx=10, sticky="EW")
        
        self.help_button = ttk.Button(self.frame, text="Довідка", command=self.display_help, style='Black.TButton')
        self.help_button.grid(row=4, column=0, columnspan=2, pady=10, ipadx=10, sticky="EW")
        
        self.quit_button = ttk.Button(self.frame, text="Вийти", command=master.quit, style='Black.TButton')
        self.quit_button.grid(row=5, column=0, columnspan=2, pady=5, ipadx=10, sticky="EW")
        
        self.footer_label = tk.Label(master, text="© 2024, Created by Deadlight, Версія: 1.0", font=("Helvetica", 10))
        self.footer_label.pack(pady=10)

    def ask_input(self, title, prompt):
        dialog = tk.Toplevel(self.master)
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.title(title)

        label = tk.Label(dialog, text=prompt, padx=20, pady=10)
        label.pack()

        entry = tk.Entry(dialog)
        entry.pack(padx=20, pady=10)
        entry.focus()

        def on_ok():
            self.master.response = entry.get()
            dialog.destroy()

        ok_button = ttk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=(0, 20))

        self.master.wait_window(dialog)
        return getattr(self.master, 'response', None)
    
    def add_contact(self):
        name = self.ask_input("Додати контакт", "Введіть ПІБ:")
        if name is not None:
            address = self.ask_input("Додати контакт", "Введіть адресу:")
            email = self.ask_input("Додати контакт", "Введіть електронну пошту:")
            mobile_phone = self.ask_input("Додати контакт", "Введіть мобільний телефон:")
            home_phone = self.ask_input("Додати контакт", "Введіть домашній телефон:")
            
            with open("contacts.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, address, email, mobile_phone, home_phone])
            
            messagebox.showinfo("Додати контакт", "Контакт успішно додано!")
    
    def edit_contact(self):
        contact_to_edit = self.ask_input("Редагувати контакт", "Введіть ПІБ контакту для редагування:")
        if contact_to_edit:
            with open("contacts.csv", "r") as file:
                reader = csv.reader(file)
                contacts = list(reader)
            
            for index, contact in enumerate(contacts):
                if contact[0] == contact_to_edit:
                    new_name = self.ask_input("Редагувати контакт", "Введіть нове ПІБ:")
                    if new_name is not None:
                        new_address = self.ask_input("Редагувати контакт", "Введіть нову адресу:")
                        new_email = self.ask_input("Редагувати контакт", "Введіть нову електронну пошту:")
                        new_mobile_phone = self.ask_input("Редагувати контакт", "Введіть новий мобільний телефон:")
                        new_home_phone = self.ask_input("Редагувати контакт", "Введіть новий домашній телефон:")
                        
                        contacts[index] = [new_name, new_address, new_email, new_mobile_phone, new_home_phone]
                        
                        with open("contacts.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(contacts)
                        
                        messagebox.showinfo("Редагувати контакт", "Контакт успішно відредаговано!")
                        return
            
            messagebox.showwarning("Редагувати контакт", "Контакт з таким ПІБ не знайдено.")
        else:
            messagebox.showwarning("Редагувати контакт", "Будь ласка, введіть ПІБ контакту.")

    def delete_contact(self):
        contact_to_delete = self.ask_input("Видалити контакт", "Введіть ПІБ контакту для видалення:")
        if contact_to_delete:
            with open("contacts.csv", "r") as file:
                reader = csv.reader(file)
                contacts = list(reader)
            
            found = False
            for contact in contacts:
                if contact[0] == contact_to_delete:
                    found = True
                    break
            
            if found:
                new_contacts = [contact for contact in contacts if contact[0] != contact_to_delete]
                
                with open("contacts.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(new_contacts)
                
                messagebox.showinfo("Видалити контакт", "Контакт успішно видалено!")
                # Оновлення відображення списку контактів
                self.view_contacts()
            else:
                messagebox.showwarning("Видалити контакт", f"Контакт з ПІБ '{contact_to_delete}' не знайдено.")
        else:
            messagebox.showwarning("Видалити контакт", "Будь ласка, введіть ПІБ контакту.")

    def delete_all_contacts(self):
        confirm = messagebox.askyesno("Видалити всі контакти", "Ви впевнені, що хочете видалити всі контакти?")
        if confirm:
            with open("contacts.csv", "w", newline="") as file:
                pass  # Просто очищаємо файл
            messagebox.showinfo("Видалити всі контакти", "Всі контакти були успішно видалені!")

    def search_contact(self):
        search_query = self.ask_input("Пошук контакту", "Введіть ПІБ або номер телефону для пошуку:")
        if search_query:
            found_contacts = []
            with open("contacts.csv", "r") as file:
                reader = csv.reader(file)
                for contact in reader:
                    if search_query.lower() in contact[0].lower() or search_query in contact[3] or search_query in contact[4]:
                        found_contacts.append(contact)
            
            if found_contacts:
                found_info = ""
                for contact in found_contacts:
                    found_info += f"ПІБ: {contact[0]}\nАдреса: {contact[1]}\nЕлектронна пошта: {contact[2]}\nМобільний телефон: {contact[3]}\nДомашній телефон: {contact[4]}\n\n"
                messagebox.showinfo("Результати пошуку", found_info)
            else:
                messagebox.showinfo("Результати пошуку", "Контактів за вашим запитом не знайдено.")
        else:
            messagebox.showwarning("Пошук контакту", "Будь ласка, введіть ПІБ або номер телефону для пошуку.")

    def view_contacts(self):
        contacts_info = ""
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            for contact in reader:
                contacts_info += f"ПІБ: {contact[0]}\nАдреса: {contact[1]}\nЕлектронна пошта: {contact[2]}\nМобільний телефон: {contact[3]}\nДомашній телефон: {contact[4]}\n\n"
        
        messagebox.showinfo("Переглянути контакти", contacts_info)
    
    def display_help(self):
        help_text = """Телефонний довідник - це програма для керування вашим списком контактів.
        
        Опції:
        - Додати контакт: Дозволяє додати новий контакт до вашого телефонного довідника.
        - Редагувати контакт: Дозволяє змінити інформацію про існуючий контакт.
        - Видалити контакт: Видаляє контакт із телефонного довідника.
        - Видалити всі контакти: Видаляє всі контакти із телефонного довідника.
        - Пошук: Шукає контакти за прізвищем або номером телефону.
        - Переглянути контакти: Показує список всіх контактів у вашому довіднику.
        - Довідка: Відображає це вікно довідки.
        - Вийти: Закриває програму.
        
        Щоб розпочати використання, виберіть потрібну опцію з меню."""
        
        messagebox.showinfo("Довідка", help_text)

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
