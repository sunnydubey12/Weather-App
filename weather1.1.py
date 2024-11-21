import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QTime


def get_weather():
    city = city_input.text().strip()
    if not city:
        QMessageBox.warning(window, "Input Error", "Please enter a city name")
        return

    try:
        api_key = "5c26f0cbb8304103607097485586a2be"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            QMessageBox.warning(window, "Error", data.get("message", "City not found"))
        else:
            
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"].capitalize()
            icon_code = data["weather"][0]["icon"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            visibility = data.get("visibility", 0) / 1000  # Convert to kilometers

            # Update labels with the fetched data
            temperature_label.setText(f"Temperature: {temp}°C")
            weather_label.setText(weather)
            humidity_label.setText(f"Humidity: {humidity}%")
            wind_label.setText(f"Wind Speed: {wind_speed} m/s")
            pressure_label.setText(f"Air Pressure: {pressure} hPa")
            visibility_label.setText(f"Visibility: {visibility} km")

            # Update weather icon
            update_weather_icon(icon_code)

            # Fetch UV index
            lon, lat = data["coord"]["lon"], data["coord"]["lat"]
            get_uv_index(lon, lat)

    except Exception as e:
        QMessageBox.critical(window, "Error", f"Failed to retrieve weather: {str(e)}")

# Function to get UV index using a second API request
def get_uv_index(lon, lat):
    try:
        api_key ="5c26f0cbb8304103607097485586a2be"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        uv_label.setText(f"UV Index: {data['value']}")
    except Exception as e:
        uv_label.setText("UV Index: N/A")

# Function to update weather icon
def update_weather_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    pixmap = QPixmap()
    pixmap.loadFromData(requests.get(icon_url).content)
    weather_icon.setPixmap(pixmap)

# Function to update time every second
def update_time():
    current_time = QTime.currentTime().toString('hh:mm:ss AP')
    time_label.setText(current_time)


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Weather Forecast")
window.setFixedSize(400, 500)

# Layout and Widgets
layout = QGridLayout()

# Time label
time_label = QLabel()
layout.addWidget(time_label, 0, 0, 1, 2)  # Span 2 columns

# City input and button
city_input = QLineEdit()
city_input.setPlaceholderText("Enter city name...")
layout.addWidget(city_input, 1, 0, 1, 2)  # Span 2 columns

get_weather_button = QPushButton("Get Weather")
get_weather_button.clicked.connect(get_weather)
layout.addWidget(get_weather_button, 2, 0, 1, 2)  # Span 2 columns

# Weather data labels (organized in grid)
temperature_label = QLabel("Temperature: ")
layout.addWidget(temperature_label, 3, 0)

weather_label = QLabel("Weather: ")
layout.addWidget(weather_label, 3, 1)

humidity_label = QLabel("Humidity: ")
layout.addWidget(humidity_label, 4, 0)

wind_label = QLabel("Wind Speed: ")
layout.addWidget(wind_label, 4, 1)

pressure_label = QLabel("Air Pressure: ")
layout.addWidget(pressure_label, 5, 0)

visibility_label = QLabel("Visibility: ")
layout.addWidget(visibility_label, 5, 1)

uv_label = QLabel("UV Index: ")
layout.addWidget(uv_label, 6, 0, 1, 2)  # Span 2 columns

# Weather icon
weather_icon = QLabel()
layout.addWidget(weather_icon, 7, 0, 1, 2)  # Span 2 columns

# Set layout and show the window
window.setLayout(layout)

# Update time every second
timer = QTimer()
timer.timeout.connect(update_time)
timer.start(1000)

update_time()  # Initial time update

window.show()
sys.exit(app.exec_())
