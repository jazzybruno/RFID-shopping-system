import sqlite3
import pygame
import serial
from flask import jsonify, request
import time

products = {
    1: {"name": "laptop", "price": 1000, "points": 50},
    2: {"name": "smartphone", "price": 800, "points": 40},
    3: {"name": "headphones", "price": 100, "points": 5},
    4: {"name": "pizza", "price": 10, "points": 2},
    5: {"name": "hamburger", "price": 5, "points": 5},
    6: {"name": "ice cream", "price": 3, "points": 1},
    7: {"name": "t-shirt", "price": 20, "points": 10},
    8: {"name": "jeans", "price": 50, "points": 6},
    9: {"name": "shoes", "price": 80, "points": 5},
}


def get_product(product_id):
    product_details = products.get(product_id)

    return product_details


def play_audio(option):
    pygame.init()

    mp3_file = "audio/"

    if option == "menu":
        mp3_file += "menu.mp3"
    elif option == "purchased":
        mp3_file += "purchased.mp3"
    elif option == "topup":
        mp3_file += "topup.mp3"

    # Set the desired volume (optional)
    volume = 0.8  # Value between 0.0 and 1.0

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(mp3_file)

    # Set the volume
    pygame.mixer.music.set_volume(volume)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait for the MP3 to finish playing (optional)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Quit pygame
    pygame.quit()


class Card:
    def __init__(self, cursor: sqlite3.Cursor, card_id):
        self.balance = 0
        self.points = 0
        self.cursor = cursor
        self.card_id = card_id

        cursor.execute("SELECT * FROM cards where id = ?", (card_id,))
        card_info = cursor.fetchone()

        if not card_info:
            cursor.execute("INSERT INTO cards VALUES (?, ?, ?)", (self.card_id, 0, 0))
            print("The card is not registered so it is now registered with 0$ and 0 points")

        else:
            _id, amount, points = card_info
            self.balance = amount
            self.points = points

    def display(self):
        print("\n\nCARD INFORMATION:")
        print("__________________")
        print(f"UID: {self.card_id}")
        print(f"Balance: {self.balance}")
        print(f"Points: {self.points}\n\n")
        return {
            "uid": self.card_id,
            "balance": self.balance,
            "points": self.points
        }

    def buy(self, product):
        amount = product["price"]
        points = product["points"]

        if self.balance > amount:
            product_id = product["id"]
            cursor = self.cursor
            cursor.execute("UPDATE cards SET amount=?, points=? where id=?",
                           (self.balance - amount, self.points + points, self.card_id))
            cursor.execute("INSERT INTO transactions (card, amount, points, product) VALUES(?, ?, ?, ?)",
                           (self.card_id, amount, points, product_id))
            self.balance -= amount
            self.points += points
            print(f"Purchase successful. Remaining balance: {self.balance}")
            return True
        else:
            print("Insufficient balance. Please top up.")
            return False

    def top_up(self, amount):
        initialBalance = self.balance
        cursor = self.cursor
        cursor.execute("UPDATE cards SET amount=? WHERE id=?", (self.balance + amount, self.card_id))
        cursor.execute("INSERT INTO topups (card, amount) VALUES (?, ?)", (self.card_id, amount))
        self.balance += amount
        print(f"Top-up successful. Current balance: {self.balance}")
        return self.balance - initialBalance


def apiEndpoint(product):
    global card
    conn = sqlite3.connect('db.db')

    card1 = ("ba6cc043", 500, 0)
    card2 = ("daafdc73", 500, 0)

    timestamp = time.time()

    conn.execute('''CREATE TABLE IF NOT EXISTS cards (
              id STRING PRIMARY KEY,
              amount REAL,
              points INTEGER
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              card STRING,
              amount REAL,
              points INTEGER,
              product INTEGER
            );''')
    conn.execute('''CREATE TABLE IF NOT EXISTS topups (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              card STRING,
              amount REAL
            );''')
    conn.commit()

    # insert

    # conn.execute("INSERT INTO cards VALUES (?, ?, ?)", card1)
    # conn.execute("INSERT INTO cards VALUES (?, ?, ?)", card2)

    # conn.commit()

    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM cards")

    # Fetch all rows from the result
    # rows = cursor.fetchall()

    # Process the fetched data
    # for row in rows:
    #     card_id, amount, points = row
    #     print(f"Card ID: {card_id}, Amount: {amount}, Points: {points}")

    ser = serial.Serial('COM7', 9600)

    # read data from serial
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(line)

        if "uid" in line:
            card_id = line.split(':')[1]
            card = Card(cursor=cursor, card_id=card_id)
            conn.commit()

            isbought = card.buy(product=product)
            if (isbought):
                print("It was bought")
                returnedObject = card.display()
                conn.close()
                play_audio("purchased")
                return jsonify(
                    {'success': True, 'message': returnedObject})
            else:
                conn.close()
                return jsonify({'success': False, 'message': 'Product Payment was unsuccessful', 'cards': ''})


def topUpEndpoint(amount):
    global card
    conn = sqlite3.connect('db.db')

    card1 = ("ba6cc043", 500, 0)
    card2 = ("daafdc73", 500, 0)

    timestamp = time.time()

    conn.execute('''CREATE TABLE IF NOT EXISTS cards (
              id STRING PRIMARY KEY,
              amount REAL,
              points INTEGER
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              card STRING,
              amount REAL,
              points INTEGER,
              product INTEGER
            );''')
    conn.execute('''CREATE TABLE IF NOT EXISTS topups (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              card STRING,
              amount REAL
            );''')
    conn.commit()

    # insert

    # conn.execute("INSERT INTO cards VALUES (?, ?, ?)", card1)
    # conn.execute("INSERT INTO cards VALUES (?, ?, ?)", card2)

    # conn.commit()

    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM cards")

    # Fetch all rows from the result
    # rows = cursor.fetchall()

    # Process the fetched data
    # for row in rows:
    #     card_id, amount, points = row
    #     print(f"Card ID: {card_id}, Amount: {amount}, Points: {points}")

    ser = serial.Serial('COM7', 9600)

    # read data from serial
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(line)

        if "uid" in line:
            card_id = line.split(':')[1]
            card = Card(cursor=cursor, card_id=card_id)
            conn.commit()
            amountNew = card.top_up(amount)
            if(amountNew == amount):
                print("Success in topping up card")
                conn.close()
                play_audio("topup")
                return jsonify(
                    {'success': True, 'message': "Success in topping up card"})
            else:
                print("Failed to top up the card")
                conn.close()
                return jsonify({'success': False, 'message': 'Card Top Up Failed'})
