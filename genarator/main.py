import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import csv

conn = sqlite3.connect('staff_courses.db')
cursor = conn.cursor()

def create_staff_table(staff_name):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{staff_name}" (
            id INTEGER PRIMARY KEY,
            course TEXT,
            type TEXT,
            branch TEXT,
            year TEXT
        )
    ''')
    conn.commit()

def add_staff():
    staff_name = staff_name_entry.get()
    if staff_name.strip():
        cursor.execute('INSERT INTO staff (name) VALUES (?)', (staff_name,))
        conn.commit()
        staff_name_entry.delete(0, tk.END)
        update_staff_list()

def delete_staff():
    selected_staff = staff_listbox.get(tk.ACTIVE)
    if selected_staff:
        cursor.execute(f'DELETE FROM staff WHERE name = ?', (selected_staff,))
        conn.commit()
        cursor.execute(f'DROP TABLE IF EXISTS "{selected_staff}"')
        conn.commit()
        update_staff_list()
        clear_course_list()

def add_course():
    selected_staff = staff_listbox.get(tk.ACTIVE)
    course_name = course_entry.get()
    course_type = course_type_var.get()
    branch_name = branch_var.get()
    year_name = year_var.get()
    if selected_staff and course_name.strip() and branch_name and year_name:
        create_staff_table(selected_staff)
        cursor.execute(f'INSERT INTO "{selected_staff}" (course, type, branch, year) VALUES (?, ?, ?, ?)', (course_name, course_type, branch_name, year_name))
        conn.commit()
        course_entry.delete(0, tk.END)
        update_course_list(selected_staff)
        update_course_details_grid(selected_staff)

def delete_course():
    selected_staff = staff_listbox.get(tk.ACTIVE)
    selected_course = course_listbox.get(tk.ACTIVE)
    if selected_staff and selected_course:
        cursor.execute(f'DELETE FROM "{selected_staff}" WHERE course = ?', (selected_course,))
        conn.commit()
        update_course_list(selected_staff)
        update_course_details_grid(selected_staff)

def export_csv():
    with open('staff_courses.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Number", "Staff Name", "Courses", "Course Type", "Branch", "Year"])
        cursor.execute('SELECT name FROM staff')
        number = 1
        for staff_row in cursor.fetchall():
            staff_name = staff_row[0]
            cursor.execute(f'SELECT course, type, branch, year FROM "{staff_name}"')
            for course_row in cursor.fetchall():
                course_name = course_row[0]
                course_type = course_row[1]
                branch_name = course_row[2]
                year_name = course_row[3]
                writer.writerow([number, staff_name, course_name, course_type, branch_name, year_name])
                number += 1

def update_staff_list():
    staff_listbox.delete(0, tk.END)
    cursor.execute('SELECT name FROM staff')
    for row in cursor.fetchall():
        staff_listbox.insert(tk.END, row[0])

def update_course_list(staff_name):
    course_listbox.delete(0, tk.END)
    create_staff_table(staff_name)
    cursor.execute(f'SELECT course, type, branch, year FROM "{staff_name}"')
    for row in cursor.fetchall():
        course_listbox.insert(tk.END, f"{row[0]} ({row[1]}, {row[2]}, {row[3]})")

def clear_course_list():
    course_listbox.delete(0, tk.END)

def show_staff_courses(event):
    selected_staff = staff_listbox.get(tk.ACTIVE)
    if selected_staff:
        update_course_list(selected_staff)
        update_course_details_grid(selected_staff)

def update_course_details_grid(staff_name):
    clear_course_details_grid()
    create_staff_table(staff_name)
    cursor.execute(f'SELECT course, type, branch, year FROM "{staff_name}"')
    for i, row in enumerate(cursor.fetchall(), start=1):
        course_tree.insert('', 'end', values=(i, staff_name, row[0], row[1], row[2], row[3]))

def clear_course_details_grid():
    for item in course_tree.get_children():
        course_tree.delete(item)

app = tk.Tk()
app.title("Staff Management App")

staff_frame = tk.Frame(app)
staff_frame.pack(pady=10)

staff_name_label = tk.Label(staff_frame, text="Staff Name")
staff_name_label.grid(row=0, column=0)
staff_name_entry = tk.Entry(staff_frame)
staff_name_entry.grid(row=0, column=1)

add_staff_button = tk.Button(staff_frame, text="Add Staff", command=add_staff)
add_staff_button.grid(row=0, column=2)

delete_staff_button = tk.Button(staff_frame, text="Delete Staff", command=delete_staff, state=tk.DISABLED)
delete_staff_button.grid(row=0, column=3)

staff_listbox = tk.Listbox(staff_frame)
staff_listbox.grid(row=1, column=0, columnspan=4)
staff_listbox.bind('<<ListboxSelect>>', show_staff_courses)

course_frame = tk.Frame(app)
course_frame.pack(pady=10)

course_label = tk.Label(course_frame, text="Course Name")
course_label.grid(row=0, column=0)
course_entry = tk.Entry(course_frame)
course_entry.grid(row=0, column=1)

branch_label = tk.Label(course_frame, text="Branch")
branch_label.grid(row=1, column=0)
branch_options = ["MTech", "MTech net", "MCA", "MSc"]
branch_var = tk.StringVar()
branch_var.set(branch_options[0])
branch_optionmenu = tk.OptionMenu(course_frame, branch_var, *branch_options)
branch_optionmenu.grid(row=1, column=1)

year_label = tk.Label(course_frame, text="Year")
year_label.grid(row=1, column=2)
year_options = ["First Year", "Second Year"]
year_var = tk.StringVar()
year_var.set(year_options[0])
year_optionmenu = tk.OptionMenu(course_frame, year_var, *year_options)
year_optionmenu.grid(row=1, column=3)

course_type_frame = tk.Frame(course_frame)
course_type_frame.grid(row=2, column=0, columnspan=2)
course_type_var = tk.StringVar()
course_type_var.set(None)  # No default selection

hardcore_radio = tk.Radiobutton(course_type_frame, text="Hardcore", variable=course_type_var, value="Hardcore")
softcore_radio = tk.Radiobutton(course_type_frame, text="Softcore", variable=course_type_var, value="Softcore")
lab_radio = tk.Radiobutton(course_type_frame, text="Lab", variable=course_type_var, value="Lab")
skill_enhancement_radio = tk.Radiobutton(course_type_frame, text="Skill Enhancement", variable=course_type_var, value="Skill Enhancement")

hardcore_radio.grid(row=0, column=0)
softcore_radio.grid(row=0, column=1)
lab_radio.grid(row=0, column=2)
skill_enhancement_radio.grid(row=0, column=3)

add_course_button = tk.Button(course_frame, text="Add Course", command=add_course, state=tk.DISABLED)
add_course_button.grid(row=2, column=4)

delete_course_button = tk.Button(course_frame, text="Delete Course", command=delete_course, state=tk.DISABLED)
delete_course_button.grid(row=2, column=5)

course_listbox = tk.Listbox(course_frame)
course_listbox.grid(row=3, column=0, columnspan=6)

export_button = tk.Button(app, text="Export to CSV", command=export_csv)
export_button.pack(pady=10)

# Create a Treeview for displaying course details in a grid
course_tree = ttk.Treeview(app, columns=("Number", "Staff Name", "Course", "Type", "Branch", "Year"), show="headings")
course_tree.heading("Number", text="Number")
course_tree.heading("Staff Name", text="Staff Name")
course_tree.heading("Course", text="Course")
course_tree.heading("Type", text="Type")
course_tree.heading("Branch", text="Branch")
course_tree.heading("Year", text="Year")
course_tree.pack()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')
conn.commit()

update_staff_list()

app.mainloop()

conn.close()
