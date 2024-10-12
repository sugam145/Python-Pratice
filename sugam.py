import json
import random
import mysql.connector
from datetime import datetime
import uuid
import hashlib

# Load intents from JSON file
with open('intents.json') as file:
    intents = json.load(file)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your MySQL password
    database="roomsewa"
)
cursor = conn.cursor(buffered=True)  # Use a buffered cursor

# Function to hash the password using SHA-1
def hash_password(password):
    return hashlib.sha1(password.encode()).hexdigest()

# Function to get guest ID based on username and password
def get_guest_id(username, password):
    if not username or not password:
        return None
    hashed_password = hash_password(password)
    cursor.execute("SELECT GUESTID FROM tblguest WHERE G_UNAME = %s AND G_PASS = %s", (username, hashed_password))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to get room details from tblroom
def get_room_details(room_number):
    query = "SELECT ROOMID, ROOMDESC, PRICE, AMENITIES, NUMPERSON FROM tblroom WHERE ROOMNUM = %s"
    cursor.execute(query, (room_number,))
    return cursor.fetchone()

# Function to list available rooms
def list_available_rooms():
    cursor.execute("SELECT ROOMNUM, ROOMDESC, PRICE FROM tblroom")
    rooms = cursor.fetchall()
    room_list = []
    for room in rooms:
        room_num, room_desc, price = room
        room_list.append(f"Room {room_num}: {room_desc}, Price: {price}")
    return room_list

# Function to check if a room is available
def is_room_available(room_id, check_in, check_out):
    query = """
    SELECT * FROM tblreservation
    WHERE ROOMID = %s
    AND STATUS = 'Confirmed'
    AND (
        (ARRIVAL <= %s AND DEPARTURE >= %s) OR
        (ARRIVAL <= %s AND DEPARTURE >= %s) OR
        (ARRIVAL >= %s AND DEPARTURE <= %s)
    )
    """
    cursor.execute(query, (room_id, check_in, check_in, check_out, check_out, check_in, check_out))
    result = cursor.fetchall()  # Fetch all results to ensure the result set is cleared
    return len(result) == 0

# Function to book a room
def book_room(room_id, guest_id, check_in, check_out, price, purpose):
    if is_room_available(room_id, check_in, check_out):
        confirmation_code = str(uuid.uuid4())[:8]  # Generate a short unique confirmation code
        cursor.execute("""
            INSERT INTO tblreservation (CONFIRMATIONCODE, TRANSDATE, ROOMID, ARRIVAL, DEPARTURE, RPRICE, GUESTID, PRORPOSE, STATUS, BOOKDATE)
            VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, 'Confirmed', NOW())
        """, (confirmation_code, room_id, check_in, check_out, price, guest_id, purpose))
        conn.commit()
        return confirmation_code
    else:
        return None

# Function to handle booking cancellation
def cancel_booking(confirmation_code):
    cursor.execute("UPDATE tblreservation SET STATUS = 'Cancelled' WHERE CONFIRMATIONCODE = %s", (confirmation_code,))
    if cursor.rowcount > 0:
        conn.commit()
        return "Your booking has been successfully cancelled."
    else:
        return "Confirmation code not found. Please check the code and try again."

# Function to parse and validate dates
def parse_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj
    except ValueError:
        return None

# Function to handle booking
def handle_booking(context):
    username = context.get('username')
    password = context.get('password')
    
    if not username or not password:
        return "Please provide both username and password to proceed with booking."

    guest_id = get_guest_id(username, password)
    if not guest_id:
        return "Unable to proceed with booking without a valid guest ID."

    room_number = context.get('room_number')
    check_in = context.get('check_in')
    check_out = context.get('check_out')
    purpose = context.get('purpose', 'Leisure')

    room_details = get_room_details(room_number)
    if room_details:
        room_id, room_desc, price, amenities, num_person = room_details
        print(f"Chatbot: Room Details - Description: {room_desc}, Price: {price}, Amenities: {amenities}, Capacity: {num_person} persons")
        
        confirmation_code = book_room(room_id, guest_id, check_in, check_out, price, purpose)
        if confirmation_code:
            return f"Room {room_number} has been successfully booked from {check_in} to {check_out}. Your confirmation code is {confirmation_code}."
        else:
            return f"Sorry, room {room_number} is not available from {check_in} to {check_out}. Please choose different dates."
    else:
        return f"Room {room_number} does not exist. Please check the room number and try again."

# Main chatbot function
def chatbot():
    context = {}
    print("Chatbot: Hello! How can I assist you today?")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        # Handle states based on context
        if context.get("state") == "credentials":
            if not context.get("username"):
                context["username"] = user_input
                print("Chatbot: Please enter your password.")
            elif not context.get("password"):
                context["password"] = user_input
                guest_id = get_guest_id(context["username"], context["password"])
                if guest_id:
                    context["guest_id"] = guest_id  # Store guest ID in context
                    print("Chatbot: Guest ID retrieved. You can now proceed with booking.")
                    context["state"] = "booking"  # Change state to booking
                else:
                    print("Chatbot: Unable to proceed without a valid guest ID.")
                    context = {}  # Reset context after error
            continue
        
        if context.get("state") == "booking":
            if not context.get("check_in"):
                check_in = parse_date(user_input)
                if check_in:
                    context["check_in"] = check_in.strftime("%Y-%m-%d")
                    print("Chatbot: Thank you! Now, please provide the check-out date.")
                else:
                    print("Chatbot: Please enter a valid check-in date in the format YYYY-MM-DD.")
            elif not context.get("check_out"):
                check_out = parse_date(user_input)
                if check_out and check_out > parse_date(context["check_in"]):
                    context["check_out"] = check_out.strftime("%Y-%m-%d")
                    print("Chatbot: Please select a room from the following list:")
                    rooms = list_available_rooms()
                    for room in rooms:
                        print(f"Chatbot: {room}")
                else:
                    print("Chatbot: Please enter a valid check-out date that is after the check-in date.")
            elif not context.get("room_number"):
                # Clean up input to remove any extraneous characters
                try:
                    room_number = int(user_input)
                    context["room_number"] = room_number
                    print("Chatbot: What is the purpose of your stay? (e.g., Leisure, Business)")
                except ValueError:
                    print("Chatbot: Please enter a valid room number.")
            elif not context.get("purpose"):
                context["purpose"] = user_input
                response = handle_booking(context)
                print(f"Chatbot: {response}")
                context = {}  # Reset context after booking
            continue
        
        if context.get("state") == "cancellation":
            response = cancel_booking(user_input)
            print(f"Chatbot: {response}")
            context = {}  # Reset context after cancellation
            continue
        
        # Predict the intent
        intent_found = False
        user_input_lower = user_input.lower()  # Normalize input
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() in user_input_lower:
                    response = random.choice(intent['responses'])
                    context["state"] = intent.get("context", None)
                    if context["state"] == "credentials":
                        print("Chatbot: Please enter your username.")
                    elif context["state"] == "booking":
                        print("Chatbot: Please provide the check-in date.")
                    elif context["state"] == "cancellation":
                        print("Chatbot: Please provide your confirmation code to cancel your booking.")
                    else:
                        print(f"Chatbot: {response}")
                    intent_found = True
                    break
            if intent_found:
                break
        if not intent_found:
            print("Chatbot: I'm sorry, I didn't understand that. Can you please clarify?")

# Run the chatbot
chatbot()

# Close the database connection when done
cursor.close()
conn.close()
