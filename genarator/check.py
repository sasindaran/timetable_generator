import tkinter as tk
import sqlite3

def open_staff_layout():
    staff_layout = tk.Toplevel(root)
    staff_layout.title("Staff Management")

    def add_staff():
        staff_name = staff_name_entry.get()
        if staff_name:
            cursor.execute('INSERT INTO staff (name) VALUES (?)', (staff_name,))
            conn.commit()
            staff_name_entry.delete(0, tk.END)
            display_staff()

    def display_staff():
        staff_list.delete(0, tk.END)
        cursor.execute('SELECT * FROM staff')
        for row in cursor.fetchall():
            staff_list.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}")

    def edit_staff():
        selected_item = staff_list.curselection()[0]
        selected_item = staff_list.get(selected_item)
        staff_id, staff_name = selected_item.split(", ")
        staff_id = staff_id.split(": ")[1]
        staff_name = staff_name.split(": ")[1]
        staff_name_entry.delete(0, tk.END)
        staff_name_entry.insert(0, staff_name)
        staff_id_entry.delete(0, tk.END)
        staff_id_entry.insert(0, staff_id)

    def update_staff():
        selected_item = staff_list.curselection()[0]
        selected_item = staff_list.get(selected_item)
        old_staff_id, old_staff_name = selected_item.split(", ")
        old_staff_id = old_staff_id.split(": ")[1]
        old_staff_name = old_staff_name.split(": ")[1]
        new_staff_name = staff_name_entry.get()
        cursor.execute('UPDATE staff SET name = ? WHERE id = ?', (new_staff_name, old_staff_id))
        conn.commit()
        staff_name_entry.delete(0, tk.END)
        staff_id_entry.delete(0, tk.END)
        display_staff()

    def delete_staff():
        selected_item = staff_list.curselection()[0]
        selected_item = staff_list.get(selected_item)
        staff_id, staff_name = selected_item.split(", ")
        staff_id = staff_id.split(": ")[1]
        staff_name = staff_name.split(": ")[1]
        cursor.execute('DELETE FROM staff WHERE id = ?', (staff_id,))
        conn.commit()
        display_staff()

    staff_name_label = tk.Label(staff_layout, text='Staff Name')
    staff_name_label.pack()
    staff_name_entry = tk.Entry(staff_layout)
    staff_name_entry.pack()

    staff_id_label = tk.Label(staff_layout, text='Staff ID')
    staff_id_label.pack()
    staff_id_entry = tk.Entry(staff_layout)
    staff_id_entry.pack()

    add_staff_button = tk.Button(staff_layout, text='Add Staff', command=add_staff)
    add_staff_button.pack()

    staff_list = tk.Listbox(staff_layout, selectmode=tk.SINGLE)
    staff_list.pack()

    view_button = tk.Button(staff_layout, text='View Staff', command=display_staff)
    view_button.pack()

    edit_button = tk.Button(staff_layout, text='Edit Staff', command=edit_staff)
    edit_button.pack()

    update_button = tk.Button(staff_layout, text='Update Staff', command=update_staff)
    update_button.pack()

    delete_button = tk.Button(staff_layout, text='Delete Staff', command=delete_staff)
    delete_button.pack()

# Create a SQLite database and a table to store staff data
conn = sqlite3.connect('school.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')
conn.commit()

# Create the main application window
root = tk.Tk()
root.title('School Management')

# Create and pack widgets
add_staff_button = tk.Button(root, text='Add Staff', command=open_staff_layout)
add_staff_button.pack()

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()
