import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (Assuming ChromeDriver is used)
service = Service(r'C:\Users\mspre\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = 'https://globe.adsbexchange.com/?icao=3c4b35&lat=50.014&lon=8.551&zoom=13.2&showTrace=2024-07-02&leg=2&timestamp=1719925899'
driver.get(url)

# Wait for the 5x button to be clickable and click it
wait = WebDriverWait(driver, 10)
five_x_button = wait.until(EC.element_to_be_clickable((By.ID, 't5x')))
five_x_button.click()

# Allow some time for the data to update
time.sleep(0.01)

print("START")

try:
    # Initialize arrays to store data
    data = {
        'Ground Speed': [],
        'Baro. Altitude': [],
        'WGS84 Altitude': [],
        'Vert. Rate': [],
        'Track': [],
        'Pos.': [],
        'Distance': [],
        'Sel. Alt': [],
        'Sel. Head.': [],
        'Wind Speed': [],
        'Wind Direction': [],
        'Wind TAT/OAT': [],
        'True Air Speed': [],
        'Indicated Air Speed': [],
        'Barometric Altitude': [],
        'Baro. Rate': [],
        'Selected Geometric Rate': [],
        'Selected Nav QNH': [],
        'Ground Track': [],
        'True Heading': [],
        'Magnetic Heading': [],
        'Magnetic Decline': [],
        'Track Rate': [],
        'Roll': [],
        'Selected Navigational Velocity': [],
        'Selected RC': [],
        'Pos Epoch': [],
    }

    # Define a function to fetch and update the data
    def fetch_data():
        data['Ground Speed'].append(driver.find_element(By.ID, 'selected_speed1').text)
        data['Baro. Altitude'].append(driver.find_element(By.ID, 'selected_altitude1').text)
        data['WGS84 Altitude'].append(driver.find_element(By.ID, 'selected_altitude_geom1').text)
        data['Vert. Rate'].append(driver.find_element(By.ID, 'selected_vert_rate').text)
        data['Track'].append(driver.find_element(By.ID, 'selected_track1').text)
        data['Pos.'].append(driver.find_element(By.ID, 'selected_position').text)
        data['Distance'].append(driver.find_element(By.ID, 'selected_sitedist2').text)
        data['Sel. Alt'].append(driver.find_element(By.ID, 'selected_nav_altitude').text)
        data['Sel. Head.'].append(driver.find_element(By.ID, 'selected_nav_heading').text)
        data['Wind Speed'].append(driver.find_element(By.ID, 'selected_ws').text)
        data['Wind Direction'].append(driver.find_element(By.ID, 'selected_wd').text)
        data['Wind TAT/OAT'].append(driver.find_element(By.ID, 'selected_temp').text)
        data['True Air Speed'].append(driver.find_element(By.ID, 'selected_tas').text)
        data['Indicated Air Speed'].append(driver.find_element(By.ID, 'selected_ias').text)
        data['Barometric Altitude'].append(driver.find_element(By.ID, 'selected_altitude2').text)
        data['Baro. Rate'].append(driver.find_element(By.ID, 'selected_baro_rate').text)
        data['Selected Geometric Rate'].append(driver.find_element(By.ID, 'selected_geom_rate').text)
        data['Selected Nav QNH'].append(driver.find_element(By.ID, 'selected_nav_qnh').text)
        data['Ground Track'].append(driver.find_element(By.ID, 'selected_track2').text)
        data['True Heading'].append(driver.find_element(By.ID, 'selected_true_heading').text)
        data['Magnetic Heading'].append(driver.find_element(By.ID, 'selected_mag_heading').text)
        data['Magnetic Decline'].append(driver.find_element(By.ID, 'selected_mag_declination').text)
        data['Track Rate'].append(driver.find_element(By.ID, 'selected_trackrate').text)
        data['Roll'].append(driver.find_element(By.ID, 'selected_roll').text)
        data['Selected Navigational Velocity'].append(driver.find_element(By.ID, 'selected_nac_v').text)
        data['Selected RC'].append(driver.find_element(By.ID, 'selected_rc').text)
        data['Pos Epoch'].append(driver.find_element(By.ID, 'selected_pos_epoch').text)

    # Continuously update the data every half second for a certain duration
    duration = 60 * 60 * 3  # Duration in seconds
    end_time = time.time() + duration

    while time.time() < end_time:
        fetch_data()
        time.sleep(0.25)
except KeyboardInterrupt:
    print("Manually Overwritten.")

print("END")

# Print the collected data
for key, values in data.items():
    print(f'{key}: {values}')

# Close the WebDriver
driver.quit()

for key, value in data.items():
    with open(os.getcwd() + "\\" + key.replace(' ', "_").replace('.','').replace('/','') + ".txt", "w", encoding='utf-8') as key_fd:
        for datum in data[key]:
            #print(datum.encode('utf-8'))
            # \xe2\x96\xb2\xe2\x80\xaf = triangle pointing up
            datum = datum.encode('utf-8').replace(b'\xe2\x80\xaf', b' ').replace(b'\xe2\x96\xb2\xe2\x80\xaf',b'').decode('utf-8', errors='ignore')
            #print(datum)
            key_fd.write(f"{datum}\n")
    key_fd.close()
