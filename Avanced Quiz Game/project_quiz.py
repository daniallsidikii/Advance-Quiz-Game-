import mysql.connector
from tkinter import *
from customtkinter import *
from tkinter import messagebox, Tk, Frame, Label, Toplevel, Label
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Database configuration
mydb_config = {
    "host": "localhost",
    "user": "root",
    "password": "here", # here write your password
    "database": "name"  # here wite your database name 
}

# Register function to insert user data into the database
def register():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    email = entry_email.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    confirm_password = entry_confirm_password.get().strip()
    # Basic validations
    if not name or not age or not email or not username or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required.")
        return
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    # Connect to the database and insert the user data
    try:
        mydb = mysql.connector.connect(**mydb_config)
        cursor = mydb.cursor()
        # Check if username already exists
        cursor.execute("SELECT * FROM register WHERE username = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists.")
            return
        # Insert user data into the "register" table
        cursor.execute(
            "INSERT INTO register (name, age, email, username, password) VALUES (%s, %s, %s, %s, %s)",
            (name, age, email, username, password))
        mydb.commit()
        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()  # Close the register window
        open_login_page()  # Open the login page
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

# Login function to verify user credentials from the database
def login():
    username = entry_login_username.get().strip()
    password = entry_login_password.get().strip()

    try:
        mydb = mysql.connector.connect(**mydb_config)
        cursor = mydb.cursor()
        
        # Check if the username and password match
        cursor.execute("SELECT * FROM register WHERE username = %s AND password = %s", (username, password))
        if cursor.fetchone():
            login_window.destroy()  # Close the login window
            open_welcome_page()  # Open the welcome page
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

# Register Page
def open_register_page():
    global register_window, entry_name, entry_age, entry_email, entry_username, entry_password, entry_confirm_password
    
    # Create the register window
    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.configure(bg="#536493")
    width, height = 1000, 650
    c_x, c_y = root.winfo_screenwidth() // 2 - width // 2, root.winfo_screenheight() // 2 - height // 2
    register_window.geometry(f"{width}x{height}+{c_x}+{c_y}")

    # Add the image
    image_path = "helloo.png"  # Replace with the path to your image
    img = Image.open(image_path)
    ctk_image = CTkImage(light_image=img, dark_image=img, size=(360, 320))  # Adjust size as needed
    # Display the image in a CTkLabel
    label = CTkLabel(register_window, image=ctk_image, text="")  # Set `text` to "" to avoid overlap
    label.place(x=-20, y=300)

    image_path = "wel.png"  # Replace with the path to your image
    img = Image.open(image_path)
    ctk_image = CTkImage(light_image=img, dark_image=img, size=(225, 300))  # Adjust size as needed
    # Display the image in a CTkLabel
    label = CTkLabel(register_window, image=ctk_image, text="")  # Set `text` to "" to avoid overlap
    label.place(x=700, y=100)

    entry_name = CTkEntry(register_window, placeholder_text="Enter your Name ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40, width=270)
    entry_name.place(x=380, y=60)

    entry_age = CTkEntry(register_window, placeholder_text="Enter your Age ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40, width=270)
    entry_age.place(x=380, y=140)

    entry_email = CTkEntry(register_window, placeholder_text="Enter your Email ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40, width=270)
    entry_email.place(x=380, y=220)

    entry_username = CTkEntry(register_window,placeholder_text="Create Username ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40, width=270 )
    entry_username.place(x=380, y=300)

    entry_password = CTkEntry(register_window, placeholder_text="Create Password ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40, width=270)
    entry_password.place(x=380, y=380)

    entry_confirm_password = CTkEntry(register_window, placeholder_text="Confirm Password ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40, width=270)
    entry_confirm_password.place(x=380, y=460)

    Label(register_window, text="Name:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 12)).place(x=380, y=35)
    Label(register_window, text="Age:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 12)).place(x=380, y=115)
    Label(register_window, text="Email:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 12)).place(x=380, y=195)
    Label(register_window, text="Username:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 12)).place(x=380, y=275)
    Label(register_window, text="Password:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 12)).place(x=380, y=355)
    Label(register_window, text="Confirm Password:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 12)).place(x=380, y=435)
    # Register Button
    register_button = CTkButton(register_window, corner_radius=30, text="REGISTER", font=("Times New Roman", 18), border_color="black",border_width=2, text_color="BLACK", fg_color="#CBDCEB", hover_color="#608BC1",command=register, height=50, width=150)
    register_button.place(x=509, y=540)
    
    # Login Button
    log_button = CTkButton(register_window, corner_radius=30, text="LOGIN", font=("Times New Roman", 18), border_color="black",border_width=2, text_color="BLACK", fg_color="#CBDCEB", hover_color="#608BC1", command=open_login_page, height=50, width=150)
    log_button.place(x=348, y=540)

# Get the next question number
def get_next_question_number(table_name):

    try:
        mydb = mysql.connector.connect(**mydb_config)
        cursor = mydb.cursor()

        # Get the current table structure
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in cursor.fetchall()]

        # Find the last question number
        question_numbers = [
            int(col[4:]) for col in columns if col.startswith("ques") and col[4:].isdigit()
        ]
        next_question_number = max(question_numbers) + 1 if question_numbers else 1

        # Check if the columns for the next question exist
        ques_col = f"ques{next_question_number}"
        option_a_col = f"option{next_question_number}_a"
        option_b_col = f"option{next_question_number}_b"
        option_c_col = f"option{next_question_number}_c"
        correct_answer_col = f"correct_answer{next_question_number}"

        if ques_col not in columns:
            # Add the missing columns to the table
            alter_query = f"""
            ALTER TABLE {table_name}
            ADD COLUMN {ques_col} VARCHAR(255),
            ADD COLUMN {option_a_col} VARCHAR(255),
            ADD COLUMN {option_b_col} VARCHAR(255),
            ADD COLUMN {option_c_col} VARCHAR(255),
            ADD COLUMN {correct_answer_col} VARCHAR(255)
            """
            cursor.execute(alter_query)
            mydb.commit()
        return next_question_number
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def delete_question():
    subject = subject_var.get().lower()
    level = level_var.get()
    table_name = f"{subject}_level_{level}"
    question_number = question_number_entry.get().strip()

    if not question_number.isdigit():
        messagebox.showerror("Error", "Please enter a valid question number.")
        return

    ques_col = f"ques{question_number}"
    option_a_col = f"option{question_number}_a"
    option_b_col = f"option{question_number}_b"
    option_c_col = f"option{question_number}_c"
    correct_answer_col = f"correct_answer{question_number}"

    try:
        mydb = mysql.connector.connect(**mydb_config)
        cursor = mydb.cursor()

        # Drop the columns associated with the question
        query = f"""
        ALTER TABLE {table_name}
        DROP COLUMN {ques_col},
        DROP COLUMN {option_a_col},
        DROP COLUMN {option_b_col},
        DROP COLUMN {option_c_col},
        DROP COLUMN {correct_answer_col}
        """
        cursor.execute(query)
        mydb.commit()
        messagebox.showinfo("Success", f"Question {question_number} and its columns deleted from {table_name}!")
        # Reset the fields after deletion (optional)
        reset_fields()
        add_ques()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return  # Exit if an error occurs, don't continue


def submit_question():
    subject = subject_var.get().lower()
    level = level_var.get()
    table_name = f"{subject}_level_{level}"
    question = question_entry.get().strip()
    option1 = option1_entry.get().strip()
    option2 = option2_entry.get().strip()
    option3 = option3_entry.get().strip()
    correct_answer = correct_answer_entry.get().strip().lower()

    if not all([question, option1, option2, option3, correct_answer]) or correct_answer not in "abc":
        messagebox.showerror("Error", "Please fill all fields and enter a valid correct answer (a, b, or c).")
        return

    next_question_number = get_next_question_number(table_name)
    if not next_question_number:
        return

    ques_col = f"ques{next_question_number}"
    option_a_col = f"option{next_question_number}_a"
    option_b_col = f"option{next_question_number}_b"
    option_c_col = f"option{next_question_number}_c"
    correct_answer_col = f"correct_answer{next_question_number}"

    try:
        mydb = mysql.connector.connect(**mydb_config)
        cursor = mydb.cursor()

        query = f"""
        UPDATE {table_name}
        SET 
            {ques_col} = %s,
            {option_a_col} = %s,
            {option_b_col} = %s,
            {option_c_col} = %s,
            {correct_answer_col} = %s
        WHERE id = 1
        """
        cursor.execute(query, (question, option1, option2, option3, correct_answer))
        mydb.commit()
        messagebox.showinfo("Success", f"Question added to {table_name} as {ques_col}!")

        # Reset fields after submission
        reset_fields()
        add_ques()


    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return  # Exit if an error occurs, don't continue

# Reset input fields (called after submit or delete)
def reset_fields():
    question_number_entry.delete(0, END)
    question_entry.delete(0, END)
    option1_entry.delete(0, END)
    option2_entry.delete(0, END)
    option3_entry.delete(0, END)
    correct_answer_entry.delete(0, END)

# Add question GUI

def add_ques():
    global subject_var, level_var, question_entry, option1_entry, option2_entry, option3_entry, correct_answer_entry, question_number_entry, current_frame
    
    admin_ques_window = Toplevel(root)
    admin_ques_window.title("Add Questions")
    admin_ques_window.configure(bg="#577B8D")
    width, height = 1000, 650
    admin_ques_window.geometry(f"{width}x{height}+{root.winfo_screenwidth() // 2 - width // 2}+{root.winfo_screenheight() // 2 - height // 2}")

    # Load the GIF image using Pillow
    gif_image = Image.open("GIF_pic.gif")  # Replace with the path to your GIF image

    # Create a list to store the frames
    frames = []

    # Extract frames from the GIF using Pillow
    for frame in range(gif_image.n_frames):
        gif_image.seek(frame)  # Move to the current frame
        frame_image = gif_image.copy()  # Copy the frame
        frame_image = frame_image.resize((345, 245))
        frames.append(ImageTk.PhotoImage(frame_image))  # Convert to PhotoImage and add to the list

    # Create a label to display the GIF
    image_label = Label(admin_ques_window, bg="#577B8D")  # Use tk.Label
    image_label.place(x=260, y=12)   # Adjust position as needed

    # Global variable for the current frame
    current_frame = 0

    # Function to update the frame to create animation effect
    def update_frame():
        global current_frame  # Declare current_frame as global
        image_label.configure(image=frames[current_frame])  # Update the image
        current_frame = (current_frame + 1) % len(frames)  # Loop through frames
        image_label.after(100, update_frame)  # Update every 100 ms for smooth animation

    # Start the animation
    update_frame()

    subject_mapping = {
        "Biology": "bio",
        "Chemistry": "chem",
        "Physics": "phy",
        "English": "eng"
    }

    # Subject label and optionMenu
    subject_var = StringVar(value="Select")  # Default value
    Label(admin_ques_window, text="Subject:", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 15)).place(x=830, y=280)
    option_menu = CTkOptionMenu(admin_ques_window, 
                                    variable=subject_var, 
                                    values=list(subject_mapping.values()),
                                    height=37, 
                                    width=150,
                                    fg_color="#f0f0f0",  # Background color of the dropdown
                                    text_color="#333333",  # Text color of the selected option
                                    dropdown_fg_color="#EDDFE0",  # Background color of the dropdown menu
                                    dropdown_text_color="black",  # Text color in the dropdown menu
                                    button_color="#FF6500",  # Button background color
                                    button_hover_color="#FFAD60",  # Button hover color
                                    dropdown_hover_color="#B7B7B7",
                                    font=("Times New Roman", 15))  # Custom font for the text
    option_menu.place(x=800, y=320)

    # Level Label and OptionMenu
    level_var = StringVar(value="Select")  # Default value
    Label(admin_ques_window, text="Level:", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 15)).place(x=680, y=280)
    option_menu = CTkOptionMenu(admin_ques_window, 
                                    variable=level_var, 
                                    values=["1", "2", "3"],
                                    height=37, 
                                    width=150,
                                    fg_color="#f0f0f0",  # Background color of the dropdown
                                    text_color="#333333",  # Text color of the selected option
                                    dropdown_fg_color="#EDDFE0",  # Background color of the dropdown menu
                                    dropdown_text_color="black",  # Text color in the dropdown menu
                                    button_color="#FF6500",  # Button background color
                                    button_hover_color="#FFAD60",  # Button hover color
                                    dropdown_hover_color="#B7B7B7",
                                    font=("Times New Roman", 15))  # Custom font for the text
    option_menu.place(x=630, y=320)
    
    Label(admin_ques_window, text=" Write Question", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 18)).place(x=130, y=254)
    question_entry = CTkEntry(admin_ques_window, placeholder_text="Enter Question ", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 15), height=40, width=270)
    question_entry.place(x=300, y=250)

    Label(admin_ques_window, text="Option A", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 18)).place(x=195, y=304)
    option1_entry = CTkEntry(admin_ques_window, placeholder_text="Enter Option A", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 15), height=40, width=270)
    option1_entry.place(x=300, y=300)

    Label(admin_ques_window, text="Option B", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 18)).place(x=195, y=354)
    option2_entry = CTkEntry(admin_ques_window, placeholder_text="Enter Option B", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 15), height=40, width=270)
    option2_entry.place(x=300, y=350)

    Label(admin_ques_window, text="Option C", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 18)).place(x=195, y=404)
    option3_entry = CTkEntry(admin_ques_window, placeholder_text="Enter Option C", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 15), height=40 , width=270)
    option3_entry.place(x=300, y=400)

    Label(admin_ques_window, text="Correct Answer ( A, B, C )", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 18)).place(x=22, y=454)
    correct_answer_entry = CTkEntry(admin_ques_window, placeholder_text="Enter Correct Answer", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10,font=("Times New Roman", 18), height=40 ,width=270)
    correct_answer_entry.place(x=300, y=450)

    Label(admin_ques_window, text="Delete Question ( No. )", fg="#F5EFFF", bg="#577B8D", font=("Times New Roman", 18)).place(x=62, y=504)
    question_number_entry = CTkEntry(admin_ques_window, placeholder_text="Enter Question no. to be deleted", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10, font=("Times New Roman", 18), height=40 ,width=270)
    question_number_entry.place(x=300, y=500)
    
    # Add the image
    image_path = "admin_panel.png"  # Replace with the path to your image
    img = Image.open(image_path)
    ctk_image = CTkImage(light_image=img, dark_image=img, size=(260, 200))  # Adjust size as needed

    # Display the image in a CTkLabel
    label = CTkLabel(admin_ques_window, image=ctk_image, text="")  # Set `text` to "" to avoid overlap
    label.place(x=725, y=30)

    login_button = CTkButton(
        admin_ques_window,
        text="ADD",
        font=("Time New Roman", 18),
        text_color="BLACK",
        fg_color="#CBDCEB",
        hover_color="#608BC1",
        border_color="black",
        border_width=2,
        corner_radius=10,
        command=submit_question,
        height=40,
        width=115
    )
    login_button.place(x=200, y=570)

    login_button = CTkButton(
        admin_ques_window,
        text="DELETE",
        font=("Time New Roman", 18),
        text_color="BLACK",
        fg_color="#CBDCEB",
        hover_color="#608BC1",
        border_color="black",
        border_width=2,
        corner_radius=10,
        command=delete_question,
        height=40,
        width=115
    )
    login_button.place(x=350, y=570)

    login_button = CTkButton(
        admin_ques_window,
        text="EXIT",
        font=("Time New Roman", 18),
        text_color="BLACK",
        fg_color="#CBDCEB",
        hover_color="#608BC1",
        border_color="black",
        border_width=2,
        corner_radius=10,
        command=admin_ques_window.destroy,
        height=40,
        width=115
    )
    login_button.place(x=500, y=570)

# admin login page
def admin_login_page():
    global admin_entry_login_username, admin_entry_login_password, userName, passw, img_label

    def admin_login():
        admin_username = userad.get().strip()  # Use .strip() to remove extra spaces
        admin_pass = userpss.get().strip()
        
        if admin_username == "Admin" and admin_pass == "123":
            add_ques()
        else:
            messagebox.showerror("Login Failed", "Please enter the correct username or password!")
            admin_login_page()

    admin_login_window = Toplevel(root)
    admin_login_window.title("Login")
    admin_login_window.configure(bg="#5C8984")
    width, height = 1000, 650
    c_x, c_y = root.winfo_screenwidth() // 2 - width // 2, root.winfo_screenheight() // 2 - height // 2
    admin_login_window.geometry(f"{width}x{height}+{c_x}+{c_y}") 
    
    userad = StringVar()
    userpss = StringVar()

    Label(admin_login_window, text="Username:", fg="#E8ECD7", bg="#5C8984", font=("Times New Roman", 15)).place(x=380, y=326)
    Label(admin_login_window, text="Password:", fg="#E8ECD7", bg="#5C8984", font=("Times New Roman", 15)).place(x=380, y=426)

    admin_entry_login_username=CTkEntry(admin_login_window, placeholder_text="Enter Username", fg_color="#D1D8C5", text_color="black", border_width=3, corner_radius=10, font=("Times New Roman", 18), height=40 , textvariable=userad, width=270)
    
    admin_entry_login_username.place(x=380, y=362)
    admin_entry_login_password=CTkEntry(admin_login_window, placeholder_text="Enter Password", textvariable=userpss, fg_color="#D1D8C5", text_color="black", border_width=3, corner_radius=10, font=("Times New Roman", 18), height=40 ,width=270, show="*")
    admin_entry_login_password.place(x=380, y=462)

    login_button = CTkButton(
        admin_login_window,
        text="LOGIN",
        font=("Time New Roman", 18),
        text_color="BLACK",
        fg_color="#CBDCEB",
        hover_color="#608BC1",
        border_color="black",
        border_width=2,
        corner_radius=10,
        command=admin_login,
        height=60,
        width=130
    )
    login_button.place(x=460, y=540)
    
    # Add the image
    image_path = "pen.png"  # Replace with the path to your image
    img = Image.open(image_path)
    ctk_image = CTkImage(light_image=img, dark_image=img, size=(355, 290))  # Adjust size as needed

    # Display the image in a CTkLabel
    label = CTkLabel(admin_login_window, image=ctk_image, text="")  # Set `text` to "" to avoid overlap
    label.place(x=320, y=40)

def open_login_page():
    global login_window, entry_login_username, entry_login_password, image, photo

    # Create the login window
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.configure(bg="#536493")
    width, height = 1000, 650
    c_x, c_y = root.winfo_screenwidth() // 2 - width // 2, root.winfo_screenheight() // 2 - height // 2
    login_window.geometry(f"{width}x{height}+{c_x}+{c_y}")

    # Add an image to the window (logo or header)
    image = Image.open("visitor.png") 
    image = image.resize((500, 265), Image.LANCZOS)  # Resize to fit the window
    photo = ImageTk.PhotoImage(image)
    label = Label(login_window, image=photo, bg="#536493")
    label.place(x=250, y=50) # Add padding for spacing

    entry_login_username = CTkEntry(login_window, placeholder_text="Enter Username", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10, font=("Times New Roman", 18), height=40 ,width=270)
    entry_login_username.place(x=380, y=370)

    entry_login_password = CTkEntry(login_window, placeholder_text="Enter Password", fg_color="#D1D8C5", text_color="black", border_width=2, corner_radius=10, font=("Times New Roman", 18),show="*", height=40 ,width=270)
    entry_login_password.place(x=380, y=450)

    Label(login_window, text="Username:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 15)).place(x=390, y=340)
    Label(login_window, text="Password:", fg="#E8ECD7", bg="#536493", font=("Times New Roman", 15)).place(x=390, y=420)

    # Login button
    login_button = CTkButton(login_window, text="LOGIN", corner_radius=30, font=("Times New Roman", 18), text_color="BLACK", fg_color="#CBDCEB", hover_color="#608BC1", command=login, height=60, width=140)
    login_button.place(x=545, y=548)  # Position the login button
    
    # Register button
    reg_button = CTkButton(login_window, text="REGISTER", corner_radius=30, font=("Times New Roman", 18), text_color="BLACK", fg_color="#CBDCEB", hover_color="#608BC1", command=open_register_page, height=60, width=130)
    reg_button.place(x=350, y=548)  # Position the register button

# Welcome Page
def open_welcome_page():
    global chemistry, current_frame
    welcome_page = Toplevel(root)
    welcome_page.title("Welcome Page")
    welcome_page.configure(bg="#F0D290")
    width, height = 1000, 650
    c_x, c_y = root.winfo_screenwidth() // 2 - width // 2, root.winfo_screenheight() // 2 - height // 2
    welcome_page.geometry(f"{width}x{height}+{c_x}+{c_y}")

    Label(welcome_page, text="Choose your Subject ↓", bg="#DE834D", font=("Times New Roman", 16)).pack(pady=35, ipadx=40, ipady=15)

    chemistry = CTkButton(
        welcome_page, 
            text="Chemistry", 
            width=200,
            height=70,
            fg_color="#781D42",  # Text color (foreground)
            hover_color="#A3423C",  # Hover color
            font=("Times New Roman", 20), 
            corner_radius=30,
            command=chemistry_levels)
    physics = CTkButton(
        welcome_page, 
            text="Physics",            
            width=200,
            height=70,
            fg_color="#781D42",  # Text color (foreground)
            hover_color="#A3423C",  # Hover color
            font=("Times New Roman", 20),
            corner_radius=30, 
            command=physics_levels)
    bio = CTkButton(
        welcome_page, 
            text="Biology", 
            width=200,
            height=70,
            fg_color="#781D42",  # Text color (foreground)
            hover_color="#A3423C",  # Hover color
            font=("Times New Roman", 20),
            corner_radius=30,
            command=bio_levels)
    english = CTkButton(
        welcome_page, 
            text="English",     
            width=200,
            height=70,
            fg_color="#781D42",  # Text color (foreground)
            hover_color="#A3423C",  # Hover color
            font=("Times New Roman", 20),
            corner_radius=30,
            command=english_levels)

    chemistry.place(x=150, y=190)
    bio.place(x=150, y=270)
    physics.place(x=150, y=350)
    english.place(x=150, y=430)

    logout_button = CTkButton(
            welcome_page, 
            text="LOGOUT",             
            width=170,
            height=60,
            fg_color="#781D42",  # Text color (foreground)
            hover_color="#A3423C",  # Hover color
            font=("Times New Roman", 20),
            corner_radius=10,
            command=welcome_page.destroy)
    logout_button.place(x=394, y=560)

    # Load the first GIF (for the level window)
    gif_image = Image.open("level.gif")  # Replace with the path to your GIF image
    frames = []
    for frame_num in range(gif_image.n_frames):
        gif_image.seek(frame_num)  # Move to the current frame
        frame_image = gif_image.copy()  # Copy the frame
        frame_image = frame_image.resize((350, 250))
        frames.append(ImageTk.PhotoImage(frame_image))  # Convert to PhotoImage and add to the list
    image_label_1 = Label(welcome_page, bg="#F0D290")  # Use tk.Label for level window GIF
    image_label_1.place(x=530, y=200)  # Adjust position as needed
    current_frame = 0
    def update_level_window_frame():
        global current_frame  # Declare current_frame as global
        image_label_1.configure(image=frames[current_frame])  # Update the image
        current_frame = (current_frame + 1) % len(frames)  # Loop through frames
        image_label_1.after(100, update_level_window_frame)  # Update every 100 ms for smooth animation
    update_level_window_frame()

# Function to fetch questions from the database
def fetch_questions(subject, level):
    global questions, correct_answers, total_questions
    questions = []
    correct_answers = []
    try:
        conn = mysql.connector.connect(**mydb_config)
        cursor = conn.cursor(dictionary=True)
        table_name = f"{subject.lower()}_level_{level}"
        # Dynamically fetch column names from the table
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [col['Field'] for col in cursor.fetchall()]
        # Extract only the question, option, and correct answer columns
        question_columns = [col for col in columns if col.startswith('ques')]
        option_columns = [col for col in columns if col.startswith('option')]
        correct_answer_columns = [col for col in columns if col.startswith('correct_answer')]
        # Query the table
        query = f"SELECT {', '.join(question_columns + option_columns + correct_answer_columns)} FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            for i, question_col in enumerate(question_columns, start=1):
                question = row[question_col]
                if question:
                    # Extract options for this question
                    options = [
                        row[f"option{i}_a"],
                        row[f"option{i}_b"],
                        row[f"option{i}_c"],
                    ]
                    correct_answer = row[f"correct_answer{i}"]
                    questions.append((question, options, correct_answer))
                    correct_answers.append(correct_answer)

        total_questions = len(questions)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()
    return questions

# Function to calculate performance
def calculate_performance(score, total_questions):
    """
    Calculate the proportion of 'Good' and 'Bad' performance categories
    based on the score.
    """
    good_threshold = 0.5  # Define the threshold for "Good" performance
    good = score if score / total_questions >= good_threshold else 0
    bad = total_questions - good
    categories = ["Good", "Bad"]
    proportions = [good, bad]
    return categories, proportions

def display_pie_chart(score, total_questions):
    """Display a pie chart for the progress report."""
    pi_chart_window = Toplevel()
    pi_chart_window.title("Progress Report")
    pi_chart_window.configure(bg="#F0D290")

    width, height = 1000, 650  # Adjusted size for better focus on the pie chart
    c_x, c_y = root.winfo_screenwidth() // 2 - width // 2, root.winfo_screenheight() // 2 - height // 2
    pi_chart_window.geometry(f"{width}x{height}+{c_x}+{c_y}")
    
    # Get categories and proportions for the chart
    categories, proportions = calculate_performance(score, total_questions)
    # Updated dark colors for "Good" and "Bad"
    colors = ["#1B5E20", "#B71C1C"]  # Dark green for "Good", dark red for "Bad"
    # Create the pie chart figure
    fig = Figure(figsize=(4.5, 4.5), dpi=100)
    fig.patch.set_facecolor("#F0D290")  # Set the figure's background color
    ax = fig.add_subplot(111)
    ax.set_facecolor("blue")  # Set the axes background color to match the window
    wedges, texts, autotexts = ax.pie(
        proportions, 
        labels=categories, 
        autopct=lambda p: f'{p:.1f}%',  # Format percentages
        startangle=90, 
        colors=colors,
        textprops={'fontsize': 14, 'color': 'black'})  # Adjust text properties
    # Make pie chart visually appealing
    ax.set_title("Performance Analysis", fontsize=18, fontweight="bold",pad=20)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(12)
    # Attach the chart to the Tkinter window
    canvas = FigureCanvasTkAgg(fig, pi_chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=60)  # Center the pie chart within the window
    # Add a score summary below the pie chart
    Label(pi_chart_window, text=f"Your Score: {score}/{total_questions}", font=("Times New Roman", 18, "bold"), bg="#F0D290",fg="#1B5E20").pack(pady=10)

# Display a question
def display_question(frame, index):
    global user_answers, correct_answers, total_questions

    for widget in frame.winfo_children():
        widget.destroy()

    question, options, correct_answer = questions[index]

    question_number_label = Label(
        frame,
        text=f"Question {index + 1} of {total_questions}",
        bg="#E9EED9",
        font=("Arial", 14),
    )
    question_number_label.place(x=10, y=35, height=40, width=200)

    question_label = Label(
        frame,
        text=question,
        bg="#D7C0AE",
        font=("Arial", 16),
        wraplength=550
    )
    question_label.pack(fill=X, padx=10, pady=75, ipady=10)

    option_var = StringVar(value=user_answers[index] if index < len(user_answers) else "")

    y_position = 170
    for i, option in enumerate(options):
        rb = CTkRadioButton(
            frame,
            text=option,
            variable=option_var,
            value=chr(97 + i),
            font=("Arial", 16),
            fg_color="#321E1E",
            hover_color="#83764F",
            text_color="black"
        )
        rb.place(x=50, y=y_position)
        y_position += 45

    def save_answer_and_next():
        if len(user_answers) > index:
            user_answers[index] = option_var.get()
        else:
            user_answers.append(option_var.get())
        if index < total_questions - 1:
            display_question(frame, index + 1)

    if index > 0:
        CTkButton(
            frame,
            text="PREVIOUS",
            width=200,
            height=50,
            fg_color="#795458",
            hover_color="#6B8A7A",
            corner_radius=30,
            font=("Arial", 16),
            command=lambda: display_question(frame, index - 1)
        ).place(x=205, y=400)

    if index < total_questions - 1:
        CTkButton(
            frame,
            text="NEXT",
            width=200,
            height=50,
            fg_color="#795458",
            hover_color="#6B8A7A",
            corner_radius=30,
            font=("Arial", 16),
            command=save_answer_and_next
        ).place(x=455, y=400)
    
    else:
        CTkButton(
            frame,
            text="RESULT",
            width=200,
            height=50,
            fg_color="#795458",
            hover_color="#6B8A7A",
            corner_radius=30,
            font=("Arial", 16),
            command=lambda: show_result(frame)
        ).place(x=455, y=400)

def next_question(frame):
    """Move to the next question."""
    global current_question_index
    if current_question_index < len(questions) - 1:
        current_question_index += 1
        display_question(frame, current_question_index)

def previous_question(frame):
    """Go to the previous question."""
    global current_question_index
    if current_question_index > 0:
        current_question_index -= 1
        display_question(frame, current_question_index)

def create_level_window(subject, level):
    """Create the quiz window for the selected level."""
    global questions, current_question_index, user_answers, correct_answers, current_frame, frame_index

    # Reset variables for a new quiz
    current_question_index = 0
    user_answers = []
    correct_answers = []
    questions = fetch_questions(subject, level)
    if not questions:
        messagebox.showinfo("Quiz Game", "No questions available for this level.")
        return
    
    # Initialize the level window
    level_window = Toplevel()
    level_window.title(f"Quiz Game - Level {level}")
    width, height = 1000,650
    level_window.configure(bg="#9A7E6F")
    c_x = root.winfo_screenwidth() // 2 - width // 2
    c_y = root.winfo_screenheight() // 2 - height // 2
    level_window.geometry(f"{width}x{height}+{c_x}+{c_y}")

    frame = Frame(level_window,  bd=2, relief="solid", bg="#E9EED9")
    frame.place(x=70, y=120, height=500, width=850)

    # Load the first GIF (for the level window)
    gif_image = Image.open("ques_animation.gif")  # Replace with the path to your GIF image
    frames = []
    for frame_num in range(gif_image.n_frames):
        gif_image.seek(frame_num)  # Move to the current frame
        frame_image = gif_image.copy()  # Copy the frame
        frame_image = frame_image.resize((200, 100))
        frames.append(ImageTk.PhotoImage(frame_image))  # Convert to PhotoImage and add to the list
    image_label_1 = Label(level_window, bg="#9A7E6F")  # Use tk.Label for level window GIF
    image_label_1.place(x=410, y=8)  # Adjust position as needed
    current_frame = 0
    def update_level_window_frame():
        global current_frame  # Declare current_frame as global
        image_label_1.configure(image=frames[current_frame])  # Update the image
        current_frame = (current_frame + 1) % len(frames)  # Loop through frames
        image_label_1.after(100, update_level_window_frame)  # Update every 100 ms for smooth animation
    update_level_window_frame()  # Start the animation for the level window

    # Display the first question
    display_question(frame, current_question_index)

def show_result(frame):
    """Calculate and display the user's score."""
    global correct_answers
    score = sum(1 for user_answer, correct_answer in zip(user_answers, correct_answers) if user_answer == correct_answer)

    # Clear frame to show results
    for widget in frame.winfo_children():
        widget.destroy()

    result_label = Label(frame, text=f"Result\nYour total score is: {score} out of {len(questions)}", bg="#E9EED9", font=("Arial", 16))
    result_label.place(x=290, y=150)

    # Add an exit button
    exit_button = CTkButton(frame, 
            text="EXIT",
            width=200,
            height=50,
            fg_color="#795458",  # Text color (foreground)
            hover_color="#6B8A7A",  # Color when hovering over the button
            font=("Arial", 16),
            border_color="black",
            border_width=2,
            corner_radius=30,
            command=frame.master.destroy)
    exit_button.place(x=200, y=300)

    # Add an exit button
    exit_button = CTkButton(frame, 
            text="Show Progress",
            width=200,
            height=50,
            fg_color="#795458",  # Text color (foreground) 
            hover_color="#6B8A7A",  # Color when hovering over the button
            font=("Arial", 16),
            corner_radius=30,
            border_color="black",
            border_width=2,
            command=lambda: display_pie_chart(sum(1 for a, b in zip(user_answers, correct_answers) if a == b), total_questions))
    exit_button.place(x=450, y=300)

def subject_levels(subject):
    global current_frame, frames
    level_window = Tk()
    level_window.title(f"Levels of {subject.capitalize()}")
    level_window.configure(bg="#698474")
    width, height = 1000, 650
    c_x = level_window.winfo_screenwidth() // 2 - width // 2
    c_y = level_window.winfo_screenheight() // 2 - height // 2
    level_window.geometry(f"{width}x{height}+{c_x}+{c_y}")

    Label(level_window, text="Choose Level ↓", bg="#DBB5B5", font=("Times New Roman", 16)).pack(pady=50, ipadx=40, ipady=15)


    CTkButton(level_window, 
        text="EASY",          
        font=("Time New Roman", 20),
        text_color="BLACK",
        fg_color="#DCA47C",
        hover_color="#FFD3B6",
        border_color="black",
        border_width=2,
        height=70,
        corner_radius=30,
        width=200,
        command=lambda: create_level_window(subject, 1)).place(x=400, y=250)
    CTkButton(level_window, 
        text="MEDIUM",          
        font=("Time New Roman", 20),
        text_color="BLACK",
        fg_color="#DCA47C",
        hover_color="#FFD3B6",
        border_color="black",
        border_width=2,
        corner_radius=30,
        height=70,
        width=200,
        command=lambda: create_level_window(subject, 1)).place(x=400, y=350)
    CTkButton(level_window, 
        text="HARD",          
        font=("Time New Roman", 20),
        text_color="BLACK",
        fg_color="#DCA47C",
        hover_color="#FFD3B6",
        border_color="black",
        corner_radius=30,
        border_width=2,
        height=70,
        width=200,
        command=lambda: create_level_window(subject, 1)).place(x=400, y=450)
    
    level_window.mainloop()

def chemistry_levels():
    subject_levels("chem")

def physics_levels():
    subject_levels("phy")

def bio_levels():
    subject_levels("bio")

def english_levels():
    subject_levels("eng")

# Define the root window
root = Tk()
root.title("Main")
root.configure(bg="#3a506b")
width, height = 1000, 650
c_x = root.winfo_screenwidth() // 2 - width // 2
c_y = root.winfo_screenheight() // 2 - height // 2
root.geometry(f"{width}x{height}+{c_x}+{c_y}")

# Create a frame for organization
frame = Frame(root, bg="light blue")
frame.pack(fill=X, pady=20)

# Welcome label inside the frame
label = Label(frame, text="Welcome to Quiz Game", font=("Times New Roman", 20), bg="light blue")
label.pack(pady=20)

label = Label(root, text="New user", font=("Arial", 12), bg="#3a506b", fg="#FFF1DB")
label.place(x=168, y=450)
register_page_button = CTkButton(
    root, 
    text="REGISTER", 
    font=("Time New Roman", 18), 
    corner_radius=10, 
    fg_color="#76BA99", 
    text_color="BLACK", 
    hover_color="#EDDFB3", 
    command=open_register_page, height=50, width=150)
register_page_button.place(x=130, y=480)

label = Label(root, text="Registered user", font=("Arial", 12), bg="#3a506b", fg="#FFF1DB")
label.place(x=443, y=450)
login_page_button = CTkButton(
    root, 
    text="LOGIN",
    font=("Time New Roman", 18),
    corner_radius=10, 
    text_color="BLACK",
    fg_color="#76BA99", 
    hover_color="#EDDFB3" ,
    command=open_login_page, height=50, width=150)
login_page_button.place(x=430, y=480)

label = Label(root, text="Admin", font=("Arial", 12), bg="#3a506b", fg="#FFF1DB")
label.place(x=755, y=450)
login_page_button = CTkButton(
    root, 
    text="LOGIN",
    font=("Time New Roman", 18), 
    corner_radius=10, 
    text_color="BLACK",
    fg_color="#76BA99", 
    hover_color="#EDDFB3" , 
    command=admin_login_page, height=50, width=150)
login_page_button.place(x=710, y=480)

# Add the image
image_path = "quiz_intro.png"  # Replace with the path to your image
img = Image.open(image_path)
ctk_image = CTkImage(light_image=img, dark_image=img, size=(490, 280))  # Adjust size as needed

# Display the image in a CTkLabel
label = CTkLabel(root, image=ctk_image, text="")  # Set `text` to "" to avoid overlap
label.place(x=260, y=120)

root.mainloop() 
