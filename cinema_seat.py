import sqlite3


class Seat:

    database = 'cinema.db'

    def __init__(self, seat_id: str):
        self.seat_id = seat_id
        # self.price = self.get_price()

    def get_price(self):
        connection = sqlite3.connect(Seat.database)
        cursor = connection.cursor()
        query = cursor.execute("""
        SELECT "price" FROM "Seat" WHERE "seat_id" = ? """,
                       [self.seat_id])
        fetching = query.fetchone()[0]
        connection.close()

        return fetching

    def get_availability(self):
        connection = sqlite3.connect(Seat.database)
        cursor = connection.cursor()
        query = cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id" = ? """,
        [self.seat_id])
        fetching = query.fetchone()[0]
        connection.close()

        return fetching

    def is_free(self):
        result = self.get_availability()

        if result == 1:
            print('seat is NOT available')
            return 0
        elif result == 0:
            # print('seat is not available!!')
            return 1

    def occupy(self, param):
        if self.is_free():
            connection = sqlite3.connect(Seat.database)
            connection.execute("""
            UPDATE "Seat" SET "taken"=1 WHERE "seat_id" = ? """,
                                   [param])
            connection.commit()
            connection.close()



# first_seat = Seat('A1')
# print(first_seat.seat_id)
# print(first_seat.get_price())
# print(first_seat.get_availability())
# print(first_seat.is_free())
# first_seat.occupy('A1')
