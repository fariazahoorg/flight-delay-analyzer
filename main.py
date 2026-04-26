import pandas as pd
import os

class Flight:
    def __init__(self, flight_num, delay):
        self.flight_num = flight_num
        self.delay = delay

    def check_severity(self):
        if self.delay > 60:
            print(f"🚨 SEVERE WARNING: Flight {self.flight_num} delayed {self.delay} minutes")
        elif self.delay > 30:
            print(f"⚠️ WARNING: Flight {self.flight_num} delayed {self.delay} minutes")
        else:
            print(f"✔ Flight {self.flight_num} is on time or minor delay")


# Load CSV
df = pd.read_csv("arrivals.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Fix delay column
df["Minutes_Delayed"] = pd.to_numeric(df["Minutes_Delayed"], errors="coerce").fillna(0).astype(int)

# Filter
delayed_flights = df[df["Minutes_Delayed"] > 30]

if not delayed_flights.empty:

    worst = delayed_flights.loc[delayed_flights["Minutes_Delayed"].idxmax()]

    flight = Flight(worst["Flight_Number"], worst["Minutes_Delayed"])
    flight.check_severity()

    new_record = pd.DataFrame([{
        "Flight_Number": worst["Flight_Number"],
        "Airline": worst["Airline"],
        "Minutes_Delayed": worst["Minutes_Delayed"]
    }])

    log_file = "severe_delays_log.csv"

    if os.path.exists(log_file):
        old = pd.read_csv(log_file)
        final = pd.concat([old, new_record], ignore_index=True)
    else:
        final = new_record

    final.to_csv(log_file, index=False)

    print("Saved successfully!")

else:
    print("No severe delays found")


