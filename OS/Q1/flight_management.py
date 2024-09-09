#Code for flight_management system by GANESAN P V CCE23008

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import random

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="passing_clouds_123",
    database="flight_management"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("1920x1080")

        # Load the background image
        self.bg_image = Image.open("../pythonProject4/airline_background2.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label for the background image
        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for the login form (transparent background)
        self.login_frame = Frame(self.root, bg='white', bd=5, relief=RIDGE)
        self.login_frame.place(x=250, y=150, width=300, height=300)  # Positioning in front of the image

        # Create username label and entry
        self.username_label = Label(self.login_frame, text="Username", font=("Arial", 14), bg='white')
        self.username_label.place(x=30, y=40)

        self.username_entry = Entry(self.login_frame, font=("Arial", 12))
        self.username_entry.place(x=30, y=80, width=240)

        # Create password label and entry
        self.password_label = Label(self.login_frame, text="Password", font=("Arial", 14), bg='white')
        self.password_label.place(x=30, y=120)

        self.password_entry = Entry(self.login_frame, font=("Arial", 12), show="*")
        self.password_entry.place(x=30, y=160, width=240)

        # Create a login button
        self.login_button = Button(self.login_frame, text="Login", font=("Arial", 14), command=self.login)
        self.login_button.place(x=100, y=220)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate user credentials
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            self.root.destroy()  # Close the login window
            flight_management_root = Tk()
            app = FlightManagementSystem(flight_management_root)
            flight_management_root.mainloop()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")



class FlightManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Management System")
        self.root.geometry("1920x1080")
        self.root.configure(bg="midnight blue")

        # Create a notebook with tabs for available flights and booked flights
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        self.available_flights_tab = ttk.Frame(notebook, padding=10)
        self.booked_flights_tab = ttk.Frame(notebook, padding=10)
        self.search_flights_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.available_flights_tab, text="Available Flights")
        notebook.add(self.booked_flights_tab, text="Booked Flights")
        notebook.add(self.search_flights_tab, text="Search Flights")
        # Create a dictionary to store the available seats for each flight
        self.available_seats = {}

        # Initialize the available seats for each flight
        cursor.execute("SELECT flight_number FROM available_flights")
        flights = cursor.fetchall()
        for flight in flights:
            flight_number = flight[0]
            # Generate a random number of available seats between 10 and 200
            available_seats = random.randint(10, 200)
            self.available_seats[flight_number] = available_seats

        # Create a treeview to display available flights
        self.available_flights_tree = ttk.Treeview(self.available_flights_tab, columns=(
        "flight_number", "start_location", "destination", "price", "departure_time", "arrival_time"), show="headings")
        self.available_flights_tree.pack(fill=tk.BOTH, expand=True)

        self.available_flights_tree.heading("flight_number", text="Flight Number")
        self.available_flights_tree.heading("start_location", text="Start Location")
        self.available_flights_tree.heading("destination", text="Destination")
        self.available_flights_tree.heading("price", text="Price")
        self.available_flights_tree.heading("departure_time", text="Departure Time")
        self.available_flights_tree.heading("arrival_time", text="Arrival Time")

        self.available_flights_tree.column("flight_number", width=120, anchor=tk.W)
        self.available_flights_tree.column("start_location", width=150, anchor=tk.W)
        self.available_flights_tree.column("destination", width=150, anchor=tk.W)
        self.available_flights_tree.column("price", width=80, anchor=tk.W)
        self.available_flights_tree.column("departure_time", width=150, anchor=tk.W)
        self.available_flights_tree.column("arrival_time", width=150, anchor=tk.W)

        # Create a form to book a flight below the available flights treeview
        self.booking_form_frame = ttk.Frame(self.available_flights_tab, padding=10)
        self.booking_form_frame.pack(fill=tk.BOTH, expand=True)

        self.user_name_label = ttk.Label(self.booking_form_frame, text="Passenger Name:", font=("Arial", 12))
        self.user_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.user_name_entry = ttk.Entry(self.booking_form_frame, font=("Arial", 12))
        self.user_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        self.flight_number_label = ttk.Label(self.booking_form_frame, text="Flight Number:", font=("Arial", 12))
        self.flight_number_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.flight_number_entry = ttk.Entry(self.booking_form_frame, font=("Arial", 12))
        self.flight_number_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        self.book_button = ttk.Button(self.booking_form_frame, text="Book Flight", command=self.book_flight)
        self.book_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        # Create a treeview to display booked flights
        self.booked_flights_tree = ttk.Treeview(self.booked_flights_tab, columns=("booking_id", "user_name", "flight_number","booking_date", "price"), show="headings")
        self.booked_flights_tree.pack(fill=tk.BOTH, expand=True)

        self.booked_flights_tree.heading("booking_id", text="Booking ID")
        self.booked_flights_tree.heading("user_name", text="User Name")
        self.booked_flights_tree.heading("flight_number", text="Flight Number")
        self.booked_flights_tree.heading("booking_date", text="Booking Date")
        self.booked_flights_tree.heading("price", text="Price")

        self.booked_flights_tree.column("booking_id", width=100, anchor=tk.W)
        self.booked_flights_tree.column("user_name", width=150, anchor=tk.W)
        self.booked_flights_tree.column("flight_number", width=120, anchor=tk.W)
        self.booked_flights_tree.column("booking_date", width=150, anchor=tk.W)
        self.booked_flights_tree.column("price", width=80, anchor=tk.W)

        # Style for the buttons
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="black", padding=6)
        style.map("Accent.TButton", background=[('active', '#333333')])

        # Create a context menu for the booked flights treeview
        self.create_context_menu()

        # Create a button to display available seats
        self.display_available_seats_button = ttk.Button(self.root, text="Display Available Seats",
                                                         command=self.display_available_seats)
        self.display_available_seats_button.pack(side=tk.BOTTOM, pady=10)

        # Create a search form to search flights
        self.search_form_frame = ttk.Frame(self.search_flights_tab, padding=10)
        self.search_form_frame.pack(fill=tk.BOTH, expand=True)

        self.search_label = ttk.Label(self.search_form_frame, text="Search Flights:", font=("Arial", 12))
        self.search_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.search_entry = ttk.Entry(self.search_form_frame, font=("Arial", 12))
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        self.search_button = ttk.Button(self.search_form_frame, text="Search", command=self.search_flights)
        self.search_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        # Create a treeview to display search results
        self.search_results_tree = ttk.Treeview(self.search_flights_tab, columns=(
            "flight_number", "start_location", "destination", "price", "departure_time", "arrival_time"),
                                                show="headings")
        self.search_results_tree.pack(fill=tk.BOTH, expand=True)

        self.search_results_tree.heading("flight_number", text="Flight Number")
        self.search_results_tree.heading("start_location", text="Start Location")
        self.search_results_tree.heading("destination", text="Destination")
        self.search_results_tree.heading("price", text="Price")
        self.search_results_tree.heading("departure_time", text="Departure Time")
        self.search_results_tree.heading("arrival_time", text="Arrival Time")

        self.search_results_tree.column("flight_number", width=120, anchor=tk.W)
        self.search_results_tree.column("start_location", width=150, anchor=tk.W)
        self.search_results_tree.column("destination", width=150, anchor=tk.W)
        self.search_results_tree.column("price", width=80, anchor=tk.W)
        self.search_results_tree.column("departure_time", width=150, anchor=tk.W)
        self.search_results_tree.column("arrival_time", width=150, anchor=tk.W)

        # Update the treeviews initially
        self.update_treeviews()

    def update_treeviews(self):
        # Clear the treeviews
        self.available_flights_tree.delete(*self.available_flights_tree.get_children())
        self.booked_flights_tree.delete(*self.booked_flights_tree.get_children())
        self.search_results_tree.delete(*self.search_results_tree.get_children())

        # Query the available flights table
        cursor.execute("SELECT * FROM available_flights")
        available_flights = cursor.fetchall()

        # Insert the available flights into the treeview
        for flight in available_flights:
            self.available_flights_tree.insert("", tk.END, values=flight)

        # Query the booked flights table
        cursor.execute("SELECT * FROM booked_flights")
        booked_flights = cursor.fetchall()

        # Insert the booked flights into the treeview
        for flight in booked_flights:
            self.booked_flights_tree.insert("", tk.END, values=flight)
            # Update the available seats for each flight
            cursor.execute("SELECT flight_number FROM available_flights")
            flights = cursor.fetchall()
            for flight in flights:
                flight_number = flight[0]
                # Update the available seats for the flight
                available_seats = self.available_seats[flight_number]
                cursor.execute("UPDATE available_flights SET available_seats = %s WHERE flight_number = %s",
                               (available_seats, flight_number))
                db.commit()

    def book_flight(self):
        # Get the user name and flight number from the form
        user_name = self.user_name_entry.get()
        flight_number = self.flight_number_entry.get()

        # Check if the flight number is valid and available
        cursor.execute("SELECT * FROM available_flights WHERE flight_number = %s", (flight_number,))
        flight = cursor.fetchone()

        if flight:
            flight_price = flight[3]  # Assuming price is the 4th column (index 3)

            # Check if the flight is already booked by this user
            cursor.execute("SELECT * FROM booked_flights WHERE flight_number = %s AND user_name = %s",
                           (flight_number, user_name))
            existing_booking = cursor.fetchone()

            if not existing_booking:
                # Ask for confirmation before booking the flight
                confirmation = messagebox.askyesno("Book Flight",
                                                   f"Are you sure you want to book flight {flight_number} for ${flight_price}?")
                if confirmation:
                    # Book the flight by adding an entry to
                    cursor.execute(
                        "INSERT INTO booked_flights (user_name, flight_number, price, booking_date) VALUES (%s, %s, %s, NOW())",
                        (user_name, flight_number, flight_price))
                    db.commit()
                    # Update the treeviews
                    self.update_treeviews()
                    messagebox.showinfo("Booking Information", "Flight booked successfully.")
                else:
                    messagebox.showinfo("Booking Information", "Booking cancelled.")
            else:
                # Show message box if the user has already booked the flight
                messagebox.showinfo("Booking Information", "You have already booked this flight.")
        else:
            messagebox.showerror("Error", "Invalid flight number")

        # Check if there are available seats for the flight
        flight_number = self.flight_number_entry.get()
        available_seats = self.available_seats[flight_number]
        if available_seats > 0:
            # Book the flight

            # Update the available seats for the flight
            self.available_seats[flight_number] -= 1
            cursor.execute("UPDATE available_flights SET available_seats = %s WHERE flight_number = %s",
                           (self.available_seats[flight_number], flight_number))
            db.commit()
        else:
            messagebox.showerror("Error", "No available seats for this flight")

    def display_available_seats(self):
        # Create a new window to display the available seats
        available_seats_window = Toplevel(self.root)
        available_seats_window.title("Available Seats")

        # Create a treeview to display the available seats
        available_seats_tree = ttk.Treeview(available_seats_window, columns=("flight_number", "available_seats"),
                                            show="headings")
        available_seats_tree.pack(fill=BOTH, expand=True)

        available_seats_tree.heading("flight_number", text="Flight Number")
        available_seats_tree.heading("available_seats", text="Available Seats")

        # Insert the available seats into the treeview
        for flight_number, available_seats in self.available_seats.items():
            available_seats_tree.insert("", END, values=(flight_number, available_seats))

    def cancel_selected_flight(self):
        # Get the selected item from the booked flights treeview
        selected_item = self.booked_flights_tree.selection()

        if selected_item:
            # Get the booking ID from the selected item
            item_values = self.booked_flights_tree.item(selected_item)['values']
            booking_id = item_values[0]  # Assuming the booking_id is the first column

            # Check if the booking exists
            cursor.execute("SELECT * FROM booked_flights WHERE booking_id = %s", (booking_id,))
            booking = cursor.fetchone()

            if booking:
                # Ask for confirmation before cancelling the flight
                confirmation = messagebox.askyesno("Cancel Flight",
                                                   f"Are you sure you want to cancel booking {booking_id}?")
                if confirmation:
                    # Remove the flight from booked_flights table
                    cursor.execute("DELETE FROM booked_flights WHERE booking_id = %s", (booking_id,))
                    db.commit()

                    # Update the treeviews
                    self.update_treeviews()
                    messagebox.showinfo("Cancellation Information", "Flight cancelled successfully.")
                else:
                    messagebox.showinfo("Cancellation Information", "Cancellation cancelled.")
            else:
                messagebox.showerror("Error", "Invalid booking ID")
        else:
            messagebox.showwarning("Warning", "No flight selected")

    def create_context_menu(self):
        self.context_menu = Menu(self.booked_flights_tab, tearoff=0)
        self.context_menu.add_command(label="Cancel Flight", command=self.cancel_selected_flight)

        self.booked_flights_tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        # Check if an item is selected before showing the context menu
        if self.booked_flights_tree.selection():
            self.context_menu.post(event.x_root, event.y_root)

    def search_flights(self):
        flag=0
        # Get the search query from the form
        search_query = self.search_entry.get()

        # Clear the search results treeview
        self.search_results_tree.delete(*self.search_results_tree.get_children())

        # Query the available flights table with DISTINCT to remove duplicates
        cursor.execute(
            "SELECT DISTINCT * FROM available_flights WHERE flight_number LIKE %s OR start_location LIKE %s OR destination LIKE %s",
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))

        # Fetch the unique search results
        search_results = cursor.fetchall()

        # Insert the search results into the treeview
        # Display the available seats for each flight in the search results
        # Loop through each flight in the search_results
        for flight in search_results:
            flight_number = flight[0]

            # Use .get() to safely retrieve available seats, handling missing flight numbers gracefully
            available_seats = self.available_seats.get(flight_number, "N/A")

            # Insert the flight details into the tree view
            self.search_results_tree.insert("", "end", values=(
                flight[0], flight[1], flight[2], flight[3], flight[4], flight[5], available_seats))
            flag=1

        if flag==0:
            messagebox.showwarning("Warning", "No flight with such number detected")

    def display_available_seats(self):
        # Display the available seats for each flight
        seats_info = "\n".join([f"Flight {flight}: {seats} seats available" for flight, seats in self.available_seats.items()])
        messagebox.showinfo("Available Seats", seats_info)

if __name__ == "__main__":
    root = Tk()
    login_app = LoginPage(root)
    root.mainloop()

