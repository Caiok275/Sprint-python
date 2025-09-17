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

# Function to display available doctors in a menu format
def display_doctors():
    print("\n--- Available Doctors ---")
    available_doctors = [name for name, info in Doctors.items() if info["is_available"]]
    
    if not available_doctors:
        print("No doctors available for booking.")
        return None

    for idx, name in enumerate(available_doctors, start=1):
        doctor = Doctors[name]
        status = "Available"
        print(f"{idx}. {name} ({doctor['type of exam']}) - {status}")
    
    return available_doctors

# Function to let user select a doctor and book an exam
def book_exam():
    available_doctors = display_doctors()
    if not available_doctors:
        return

    try:
        # Choose doctor
        choice = int(input("\nEnter the number of the doctor you want to book an exam with: ").strip())
        if choice < 1 or choice > len(available_doctors):
            print("Invalid choice. Please select a valid option.")
            return

        name = available_doctors[choice - 1]
        doctor = Doctors[name]

        # Choose available time
        if not doctor["available hours"]:
            print(f"{name} has no available hours left.")
            doctor["is_available"] = False
            return

        print(f"\nAvailable hours for {name}:")
        for idx, time in enumerate(doctor["available hours"], start=1):
            print(f"{idx}. {time}")

        time_choice = int(input("Enter the number of the time you want to book: ").strip())
        
        if time_choice < 1 or time_choice > len(doctor["available hours"]):
            print("Invalid time selection. Please choose a valid time slot.")
            return
        
        selected_time = doctor["available hours"][time_choice - 1]
        doctor["available hours"].remove(selected_time)
        print(f"Booked {selected_time} with {name}.")

        # If no more available hours, mark doctor as unavailable
        if not doctor["available hours"]:
            doctor["is_available"] = False
            print(f"{name} is now marked as unavailable.")
    
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Main loop
if __name__ == "__main__":
    while True:
        book_exam()
        more = input("\nDo you want to book another exam? (yes/no): ").strip().lower()
        if more != "yes":
            break

    print("\nFinal doctor statuses:")
    display_doctors()
