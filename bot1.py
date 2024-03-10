import os
import json
from datetime import datetime

# Define the path to the contacts data file
contacts_data_file = os.path.join(os.path.dirname(__file__), "contacts.json")

# Define the dataset
users = [
    {"name": "John", "surname": "Forbes Nash Jr.", "birthday": datetime(1928, 6, 13)},
    {"name": "Andrew", "surname": "Wiles", "birthday": datetime(1953, 4, 11)},
    {"name": "Guido", "surname": "van Rossum", "birthday": datetime(1956, 1, 31)},
    {"name": "Satya", "surname": "Nadella", "birthday": datetime(1967, 8, 19)},
    {"name": "Demis", "surname": "Hassabis", "birthday": datetime(1976, 7, 27)},
]

# Initialize an empty dictionary to store contacts
contacts = {}

# Define a list of commands
commands = ["add", "change", "find", "list", "close", "exit"]

# Function to load contacts from a file
def load_contacts():
    global contacts
    if os.path.isfile(contacts_data_file):
        with open(contacts_data_file, "r") as f:
            try:
                contacts = json.load(f)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in contacts.json")
                contacts = {}
    else:
        contacts = {}
    return contacts

# Function to save contacts to a file
def save_contacts():
    with open(contacts_data_file, "w") as f:
        json.dump(contacts, f, default=str, indent=4)

# Load contacts from the data file on startup
contacts = load_contacts()

# Add initial contacts to the contacts dictionary
for user in users:
    full_name = f"{user['name'].capitalize()} {user['surname'].title()}"
    contacts[full_name] = {"birthday": user["birthday"].strftime("%d/%m/%Y"), "phone": ""}

# Error handling decorator for user input
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please provide valid input."
        except KeyError:
            return "Please enter a valid name."
        except IndexError:
            return "Incomplete command."

    return inner

# Function to add a new contact
@input_error
def add_contact():
    name = input("Enter the name of the contact: ").strip().capitalize()
    surname = input("Enter the surname of the contact: ").strip().title()
    birthday = input("Enter the birthday of the contact (DD/MM/YYYY): ")

    # Check if the entered date is valid
    try:
        datetime.strptime(birthday, "%d/%m/%Y")
    except ValueError:
        return "Invalid date format. Please enter the date in the format DD/MM/YYYY."

    phone = input("Enter the phone number of the contact: ")

    while not phone.isdigit():
        print("Phone number should contain only digits.")
        phone = input("Enter the phone number of the contact: ")

    full_name = f"{name} {surname}"
    contacts[full_name] = {"birthday": birthday, "phone": phone}
    save_contacts()
    return "Contact added."

# Function to list all contacts
@input_error
def list_contacts():
    if not contacts:
        return "No contacts found."
    else:
        contact_list = []
        for name, info in contacts.items():
            contact_list.append(f"{name}: Birthday - {info['birthday']}, Phone - {info.get('phone', 'Not available')}")
        return "\n".join(contact_list)

# Function to change the phone number of a contact
@input_error
def change_contact():
    name = input("Enter the name of the contact: ").strip().capitalize()
    surname = input("Enter the surname of the contact: ").strip().title()
    full_name = f"{name} {surname}"
    if full_name not in contacts:
        return "Contact not found."
    new_phone = input("Enter the new phone number: ")
    while not new_phone.isdigit():
        print("Phone number should contain only digits.")
        new_phone = input("Enter the new phone number: ")
    contacts[full_name]["phone"] = new_phone
    save_contacts()
    return "Phone number updated."

# Main loop of the bot
while True:
    command = input("Enter a command (add/change/find/list/close/exit): ").strip().lower()

    if command not in commands:
        print("Invalid command. Please enter a valid command.")
        continue

    if command == "add":
        print(add_contact())
    elif command == "list":
        print(list_contacts())
    elif command == "change":
        print(change_contact())
    elif command == "close" or command == "exit":
        print("Closing the bot.")
        break
