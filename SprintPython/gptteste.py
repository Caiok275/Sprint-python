Doctors = {
    "Dr. Alice Smith": {
        "type of exam": "Cardiology",
        "available hours": ["09:00", "10:00", "11:00"],
        "room number": 101,
        "contact": "alice.smith@hospital.com",
        "is_available": True
    },
    "Dr. John Doe": {
        "type of exam": "Dermatology",
        "available hours": ["13:00", "14:00", "15:00"],
        "room number": 202,
        "contact": "john.doe@hospital.com",
        "is_available": True
    }
}

# Function to display available doctors
def display_doctors():
    print("\n--- Available Doctors ---")
    for name, info in Doctors.items():
        status = "Available" if info["is_available"] else "Unavailable"
        print(f"\nDoctor: {name} ({status})")
        for key, value in info.items():
            if key != "is_available":
                print(f"  {key}: {value}")

# Function to let user select a doctor and a time
def book_exam():
    name = input("\nEnter the doctor's name: ").strip()
    if name not in Doctors:
        print("Doctor not found.")
        return

    doctor = Doctors[name]

    if not doctor["is_available"]:
        print(f"{name} is currently unavailable for booking.")
        return

    if not doctor["available hours"]:
        print(f"{name} has no available hours left.")
        doctor["is_available"] = False
        return

    print(f"\nAvailable hours for {name}: {doctor['available hours']}")
    selected_time = input("Enter a time to book (e.g., 10:00): ").strip()

    if selected_time in doctor["available hours"]:
        doctor["available hours"].remove(selected_time)
        print(f"Booked {selected_time} with {name}.")
        if not doctor["available hours"]:
            doctor["is_available"] = False
            print(f"{name} is now marked as unavailable.")
    else:
        print("Invalid time selected.")

# Main loop
if __name__ == "__main__":
    while True:
        display_doctors()
        book_exam()
        more = input("\nDo you want to book another exam? (yes/no): ").strip().lower()
        if more != "yes":
            break

    print("\nFinal doctor statuses:")
    display_doctors()
