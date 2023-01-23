from cinema_seat import Seat
import sqlite3

import random
import string
import sys
from fpdf import FPDF


class User:

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):

        boole, balance = card.validate(seat.get_price())
        if boole:
            if seat.is_free():
                seat.occupy(seat.seat_id)
                final_balance = balance - seat.get_price()
                connection = sqlite3.connect(Card.database)
                connection.execute("""
                UPDATE "Card" SET "balance"= ? WHERE "holder" = ? """,
                                   [final_balance, card.holder])
                connection.commit()
                connection.close()

                return True

        else:
            print('Unsuficient credential or balance!')


class Card:

    database = 'banking.db'

    def __init__(self, typ, number, cvc, holder):
        self.typ = typ
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        connection = sqlite3.connect(Card.database)
        cursor = connection.cursor()
        #TODO: change holder to some unique identificator like card number
        cursor.execute("""
        SELECT "number", "cvc", "holder", "balance" FROM "Card" WHERE "holder" = ?""",
                       [self.holder])

        fetched = cursor.fetchone()
        connection.close()

        counter = 0
        try:
            # fetched[0] = card_number, fetched[1] = cvc, fetched[2] = holder
            if self.number == int(fetched[0]):
                counter += 1
            if self.cvc == int(fetched[1]):
                counter += 1
            if self.holder == fetched[2]:
                counter += 1
        except TypeError as typ:
            print(typ)
            print('Invalid credentials')
            sys.exit()

        res_balance = fetched[3]
        if counter == 3 and fetched[3] >= price:
            return True, res_balance
        else:
            return False, res_balance


class Ticket:

    def __init__(self, user, price, seat):
        self.id = ''.join(random.choices(string.ascii_letters, k=8))
        self.user = user
        self.price = price
        self.seat = seat

    def to_pdf(self, pathh):
        pdf_file = FPDF(orientation='P', unit='pt', format='A4')
        pdf_file.add_page()

        pdf_file.set_font(family='Times', size=36, style='B')
        pdf_file.cell(w=0, h=100, txt='Your Digital Ticket', border=1, align='C', ln=1)
        pdf_file.set_font(family='Times', size=18, style='B')
        pdf_file.cell(w=150, h=40, txt='Name:', border=1, align='L')
        pdf_file.set_font(family='Times', size=18)
        pdf_file.cell(w=0, h=40, txt=f'{self.user}', border=1, align='L', ln=1)
        pdf_file.set_font(family='Times', size=18, style='B')
        pdf_file.cell(w=150, h=40, txt='Ticket ID:', border=1, align='L', )
        pdf_file.set_font(family='Times', size=18)
        pdf_file.cell(w=0, h=40, txt=f'{self.id}', border=1, align='L', ln=1)
        pdf_file.set_font(family='Times', size=18, style='B')
        pdf_file.cell(w=150, h=40, txt='Price:', border=1, align='L')
        pdf_file.set_font(family='Times', size=18)
        pdf_file.cell(w=0, h=40, txt=f'{self.price}', border=1, align='L', ln=1)
        pdf_file.set_font(family='Times', size=18, style='B')
        pdf_file.cell(w=150, h=40, txt='Seat Number:', border=1, align='L')
        pdf_file.set_font(family='Times', size=18)
        pdf_file.cell(w=0, h=40, txt=f'{self.seat}', border=1, align='L', ln=1)

        pdf_file.output(pathh)


# default parameters! for faster checking
# your_name = 'John Kafko'  # -> set up to be anything and will be displayed in pdf file
# pref_seat = 'B2'  # -> mandatory.. checking if pref_seat has value 0 which is free
# card_type = 'cikosina'  # -> set up just for information.. nothing is doing with that info later
# card_number = 12345678  # -> mandatory.. checking if card number valid with user from database
# card_cvc = 123  # -> same as card number
# card_hold_name = 'John Smith'  # -> same as card cvc


# other option is from input parameters from the user
your_name = input("Your full name: ")
pref_seat = input("Prefered seat number: ")
card_type = input("Your card type: ")
card_number = int(input("Your card number: "))
card_cvc = int(input("Your card cvc: "))
card_hold_name= input("Card holder name: ")


# Logic of the code below:
moj_seat = Seat(pref_seat)
ja_user = User(your_name)
ja_karta = Card(card_type, card_number, card_cvc, card_hold_name)

if ja_user.buy(moj_seat, ja_karta):
    Ticket(ja_user.name, moj_seat.get_price(), moj_seat.seat_id).to_pdf('skusame_spolu.pdf')
