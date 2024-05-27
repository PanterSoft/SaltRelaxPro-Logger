import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import os
import time

# Function to fetch data from the URL
def fetch_data():
    try:
        # Send a GET request to the website
        url = "http://192.168.178.185"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <tr> elements
        table_rows = soup.find_all("tr")

        # Extract the data from <td> elements within each <tr> for desired columns
        data_list = []
        for row in table_rows:
            table_data = row.find_all("td")
            column_name = table_data[0].get_text()
            if column_name in ["Temperature", "ORP", "pH"]:
                value = table_data[1].get_text()
                value = value.split(" ")[0]  # Remove the unit part
                data_list.append(value)

        return data_list

    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the HTTP request
        print(f"Error: {e}")
        return None
    except Exception as e:
        # Handle other exceptions that may occur during parsing or data extraction
        print(f"An unexpected error occurred: {e}")
        return None

# File path variable
csv_path = "/home/nicomattes/Dokumente/SaltRelaxPro-Logger/Data"

# Track previous data and timestamp
previous_data = None
previous_day = None
csv_file = None

# Run the loop continuously
while True:

    current_day = date.today().strftime("%Y%m%d")

    # Check if a new day has started
    if current_day != previous_day:
        # Close the previous file if it exists
        if csv_file is not None:
            csv_file.close()

        # Create a new CSV file for the new day or append to an existing one
        csv_filename = f"{csv_path}/{current_day}.csv"

        if os.path.exists(csv_filename):
            # File for the current day already exists, open in append mode
            csv_file = open(csv_filename, "a", newline="")
        else:
            # File for the current day does not exist, create a new one
            csv_file = open(csv_filename, "w", newline="")

        writer = csv.writer(csv_file)

        # If the file is newly created, write the header row
        if os.path.getsize(csv_filename) == 0:
            writer.writerow(["Time", "Temperature", "ORP", "pH"])

        # Update the previous day
        previous_day = current_day


    # Fetch the data
    data = fetch_data()
    if data is not None:
        current_timestamp = datetime.now().strftime("%H:%M:%S")

        # Check if the data has changed
        if data != previous_data:
            # Write the data to the CSV file
            writer.writerow([current_timestamp] + data)
            csv_file.flush()  # Flush the buffer to ensure data is written immediately

            print("Data has been updated in", csv_filename)

            # Update the previous data
            previous_data = data

    else:
        print("Failed to fetch data.")
    # Delay before the next iteration
    time.sleep(5)  # Delay for 60 seconds (adjust as needed)
