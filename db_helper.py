import mysql.connector
from dotenv import load_dotenv
import os


class DB:
    def __init__(self):
        load_dotenv()  # Load .env file

        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")

        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.conn.is_connected():
                self.mycursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetch_Source_city_names(self):
        self.mycursor.execute("""
            SELECT DISTINCT Source AS city FROM flights
            WHERE Destination IN (SELECT DISTINCT Destination FROM flights)
        """)
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_city_names(self):
        query = """
            SELECT DISTINCT Source AS city FROM flights
            WHERE Destination IN (SELECT DISTINCT Destination FROM flights)
            UNION
            SELECT DISTINCT Destination AS city FROM flights
            WHERE Source IN (SELECT DISTINCT Source FROM flights)
        """
        self.mycursor.execute(query)
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_destinations_for_source(self, source):
        self.mycursor.execute("SELECT DISTINCT Destination FROM flights WHERE Source = %s", (source,))
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_month_names(self):
        self.mycursor.execute("SELECT DISTINCT MONTHNAME(Date_of_Journey) FROM flights")
        return [item[0] for item in self.mycursor.fetchall()]

    def fetch_months_by_route(self, source=None, destination=None):
        query = "SELECT DISTINCT MONTHNAME(Date_of_Journey) FROM flights WHERE 1=1"
        params = []
        if source:
            query += " AND Source = %s"
            params.append(source)
        if destination:
            query += " AND Destination = %s"
            params.append(destination)
        self.mycursor.execute(query, tuple(params))
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_airline_names(self):
        self.mycursor.execute("SELECT DISTINCT Airline FROM flights")
        return [item[0] for item in self.mycursor.fetchall()]

    def fetch_airlines_by_route(self, source=None, destination=None):
        query = "SELECT DISTINCT Airline FROM flights WHERE 1=1"
        params = []
        if source:
            query += " AND Source = %s"
            params.append(source)
        if destination:
            query += " AND Destination = %s"
            params.append(destination)
        self.mycursor.execute(query, tuple(params))
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_all_flights(self, selected_month, airline, source, destination):
        query = """
            SELECT Airline, Route, Dep_Time, Duration, Price
            FROM flights
            WHERE 1=1
        """
        params = []
        if selected_month != 'All':
            query += " AND MONTHNAME(Date_of_Journey) = %s"
            params.append(selected_month)
        if airline != 'All':
            query += " AND Airline = %s"
            params.append(airline)
        if source != 'All':
            query += " AND Source = %s"
            params.append(source)
        if destination != 'All':
            query += " AND Destination = %s"
            params.append(destination)
        self.mycursor.execute(query, tuple(params))
        return self.mycursor.fetchall()

    def fetch_airline_frequency(self):
        self.mycursor.execute("""
            SELECT Airline, COUNT(*) FROM flights GROUP BY Airline
        """)
        data = self.mycursor.fetchall()
        return [row[0] for row in data], [row[1] for row in data]

    def busy_airport(self):
        self.mycursor.execute("""
            SELECT Source, COUNT(*) FROM (
                SELECT Source FROM flights
                UNION ALL
                SELECT Destination FROM flights
            ) t GROUP BY t.Source ORDER BY COUNT(*) DESC
        """)
        data = self.mycursor.fetchall()
        return [row[0] for row in data], [row[1] for row in data]

    def daily_frequency(self):
        self.mycursor.execute("""
            SELECT Date_of_Journey, COUNT(*) FROM flights GROUP BY Date_of_Journey
        """)
        data = self.mycursor.fetchall()
        return [row[0] for row in data], [row[1] for row in data]

    def fetch_top_routes(self):
        self.mycursor.execute("""
            SELECT Route, COUNT(*) FROM flights GROUP BY Route ORDER BY COUNT(*) DESC LIMIT 10
        """)
        data = self.mycursor.fetchall()
        return [row[0] for row in data], [row[1] for row in data]

    def fetch_average_price_by_airline(self):
        self.mycursor.execute("""
            SELECT Airline, ROUND(AVG(Price), 2) FROM flights GROUP BY Airline ORDER BY AVG(Price) DESC
        """)
        data = self.mycursor.fetchall()
        return [row[0] for row in data], [row[1] for row in data]

    def fetch_monthly_volume(self):
        self.mycursor.execute("""
            SELECT MONTHNAME(Date_of_Journey), COUNT(*) FROM flights GROUP BY MONTHNAME(Date_of_Journey)
        """)
        data = self.mycursor.fetchall()
        return [row[0] for row in data], [row[1] for row in data]

    def fetch_all_durations(self):
        self.mycursor.execute("SELECT Duration FROM flights")
        raw_durations = [item[0] for item in self.mycursor.fetchall()]
        return raw_durations

    def fetch_total_duration_by_airline(self):
        self.mycursor.execute("SELECT Airline, SUM(Duration) FROM flights GROUP BY Airline ORDER BY Airline")
        items = self.mycursor.fetchall()
        airlines = [item[0] for item in items]
        raw_durations = [item[1] for item in items]
        return airlines, raw_durations

    def fetch_cities_fly_duration(self):
        self.mycursor.execute("""
        SELECT Airline, SUM(Duration) AS TotalDuration
        FROM flights
        WHERE Source = 'Banglore'
        AND Destination = 'New Delhi'
        GROUP BY Airline
                              """)
        items = self.mycursor.fetchall()
        print(len(items))
        city1 = [item[0] for item in items]
        city2 = [item[1] for item in items]
        return city1, city2


    def fetch_airline_duration_between(self, source, destination):
        self.mycursor.execute("""
                              SELECT Airline, SUM(Duration)
                              FROM flights
                              WHERE Source = %s
                                AND Destination = %s GROUP BY Airline
                              """, (source, destination))

        data = self.mycursor.fetchall()

        city = [item[0] for item in data]
        duration = [item[1] for item in data]
        return city, duration











