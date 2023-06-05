import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import time

# Function to fetch data from the URL
def fetch_data():
    # Send a GET request to the website
    url = "http://192.168.178.184" ### Adjust to your URL ###
    response = requests.get(url)

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

# File path variable
csv_path = "/home/YOUR_USERNAME/Dokumente/Data" ### Adjust your Path where the files should be stored

# File name with the day timestamp
timestamp = date.today().strftime("%Y%m%d")

# Construct the full file path
csv_filename = f"{csv_path}/{timestamp}.csv"

# Track previous data and timestamp
previous_data = None
previous_timestamp = None

# Run the loop continuously
while True:
    # Fetch the data
    data = fetch_data()
    current_timestamp = datetime.now().strftime("%H:%M:%S")

    # Check if the data has changed
    if data != previous_data:
        # Write the data to the CSV file
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row if the file is newly created
            if csvfile.tell() == 0:
                writer.writerow(["Time", "Temperature", "ORP", "pH"])

            # Append the data to the CSV file along with the timestamp
            writer.writerow([current_timestamp] + data)

        print("Data has been updated in", csv_filename)

        # Update the previous data and timestamp
        previous_data = data
        previous_timestamp = current_timestamp

    # Delay before the next iteration
    time.sleep(5)  # Delay for 5 seconds (adjust as needed)
