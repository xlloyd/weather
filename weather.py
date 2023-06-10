import tkinter as tk
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
import pytz
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import os


def get_aqi_description(aqi):
    try:
        aqi = int(aqi)  # Convert the string to an integer
    except ValueError:
        return "N/A"  # Return a default value if the conversion fails

    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Mod-Unhealthy"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

root = tk.Tk()
root.title("EcoWeather: Promoting Climate-conscious Living.")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Background Image
background_path = os.path.join(os.getcwd(), "background.png")
background_image = PhotoImage(file=background_path)
canvas = tk.Canvas(root, width=900, height=500)
canvas.pack()
canvas.create_image(0, 0, anchor=NW, image=background_image)


# Function to update the time label
def update_time():
    current_time1 = datetime.now().strftime("%I:%M %p")
    canvas.itemconfigure(time_label, text=current_time1)
    root.after(1000, update_time)  # Update every 1 second (1000 milliseconds)

# Get the current date
current_date = datetime.now().strftime("%B %d, %Y")
date_label = canvas.create_text(700, 30, text="your current date & time: " + current_date, font=("Arial", 12, "bold"), fill="white")

# Get the initial time
current_time = datetime.now().strftime("%I:%M %p")
time_label = canvas.create_text(797, 50, text=current_time, font=("Arial", 12, "bold"), fill="white")

# Start updating the time label
update_time()


def get_weather(event=None):
    try:
        city = textfield.get()

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)

        if not location:
            messagebox.showerror("Weather App", "Invalid city name entered. Please try again.")
            return

        #timezone
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        canvas.itemconfig(clock, text=current_time, font=("poppins", 13, 'bold'), fill="white")
        canvas.itemconfig(name, text="CURRENT WEATHER", font=("poppins", 15, 'bold'), fill="#ee666d")

        # weather
        weather_api = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=87d4249734d3257a7fcde087dbc7de78"
        weather_json_data = requests.get(weather_api).json()

        if 'weather' not in weather_json_data or 'main' not in weather_json_data:
            messagebox.showerror("Weather App", "check your spelling or the city you entered is not defined or valid. please try again.")
            return

        condition = weather_json_data['weather'][0]['main']
        description = weather_json_data['weather'][0]['description']
        temp = int(weather_json_data['main']['temp'] - 273.15)
        pressure = weather_json_data['main']['pressure']
        humidity = weather_json_data['main']['humidity']
        wind = weather_json_data['wind']['speed']

        canvas.itemconfig(time_val, text=f"{temp}°")
        canvas.itemconfig(clock_val, text=f"{condition} | FEELS LIKE {temp}°")

        canvas.itemconfig(wind_val, text=wind)
        canvas.itemconfig(humid_val, text=humidity)
        canvas.itemconfig(description_val, text=description)
        canvas.itemconfig(pressure_val, text=pressure)

        # AQI
        aqi_api = "https://api.waqi.info/feed/" + city + "/?token=97150e542c69fcd580e0b9e34b1f78f73236f622"  # Replace with your AQICN API token
        aqi_data = requests.get(aqi_api).json()

        if 'data' in aqi_data and 'aqi' in aqi_data['data']:
            aqi = aqi_data['data']['aqi']
            aqi_description = get_aqi_description(aqi)
            canvas.itemconfig(label5, text="AQI")
            canvas.itemconfig(aqi_value, text=aqi_description)
        else:
            canvas.itemconfig(label5, text="AQI")
            canvas.itemconfig(aqi_value, text="N/A")

        # weather forecast for additional day
        forecast_api = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=87d4249734d3257a7fcde087dbc7de78"
        forecast_json_data = requests.get(forecast_api).json()

        if 'list' not in forecast_json_data:
            messagebox.showerror("Weather App", "Forecast data not available.")
            return

        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_date = tomorrow.strftime("%Y-%m-%d")

        # Find the forecast data for tomorrow
        for forecast in forecast_json_data['list']:
            forecast_date = forecast['dt_txt'].split()[0]
            if forecast_date == tomorrow_date:
                day2_temp_value = int(forecast['main']['temp'] - 273.15)
                day2_condition_value = forecast['weather'][0]['main']
                break
        else:
            messagebox.showerror("Weather App", "Forecast data not available for tomorrow.")
            return

        # Update the canvas with the additional day's forecast
        canvas.itemconfig(day2_temp, text=f"{day2_temp_value}°")
        canvas.itemconfig(day2_condition, text=f"{day2_condition_value}")
        canvas.itemconfig(day2_label, text="TOMORROW'S FORECAST")

    except requests.exceptions.RequestException:
        messagebox.showerror("Weather App", "An error occurred while making the request. Please check your internet "
                                            "connection.")
    except KeyError:
        messagebox.showerror("Weather App", "Invalid response from the weather API.")
    except Exception as e:
        messagebox.showerror("Weather App", "An error occurred while fetching weather data: " + str(e))


# Search box
search_image_path = os.path.join(os.getcwd(), "search_box.png")
search_image = PhotoImage(file=search_image_path)
image = canvas.create_image(25, 20, anchor=NW, image=search_image)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg=canvas["bg"], border=0,
                     fg="black")
textfield.place(x=50, y=40)
textfield.focus()
textfield.bind("<Return>", get_weather)  # Bind Enter key to get_weather function

search_icon_path = os.path.join(os.getcwd(), "search_icon.png")
search_icon = PhotoImage(file=search_icon_path)
image_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="black", command=get_weather)
image_icon.place(x=380, y=30)


# Logo
logo_image_path = os.path.join(os.getcwd(), "logo.png")
logo_image = PhotoImage(file=logo_image_path)
logo = canvas.create_image(140, 100, anchor=NW, image=logo_image)

# Bottom box
frame_image_path = os.path.join(os.getcwd(), "box.png")
frame_image = PhotoImage(file=frame_image_path)
frame_image = canvas.create_image(50, 380, anchor=NW, image=frame_image)

# Time
name = canvas.create_text(140, 120, text="", font=("arial", 15, "bold"), fill="white")
clock = canvas.create_text(130, 150, text="", font=("Helvetica", 20), fill="white")

# Labels
label1 = canvas.create_text(125, 410, text="WIND", font=("Helvetica", 15, 'bold'), fill="white")
label2 = canvas.create_text(245, 410, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fill="white")
label3 = canvas.create_text(405, 410, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fill="white")
label4 = canvas.create_text(565, 410, text="PRESSURE", font=("Helvetica", 15, 'bold'), fill="white")
label5 = canvas.create_text(700, 410, text="AQI", font=("Helvetica", 15, 'bold'), fill="white")

# Values
time_val = canvas.create_text(530, 200, text="", font=("arial", 90, "bold"), fill="#ee666d")
clock_val = canvas.create_text(530, 280, text="", font=("arial", 15, "bold"), fill="white")
wind_val = canvas.create_text(125, 440, text="...", font=("arial", 15, "bold"), fill="white")
humid_val = canvas.create_text(245, 440, text="...", font=("arial", 15, "bold"), fill="white")
description_val = canvas.create_text(405, 440, text="...", font=("arial", 15, "bold"), fill="white")
pressure_val = canvas.create_text(565, 440, text="...", font=("arial", 15, "bold"), fill="white")
aqi_value = canvas.create_text(697, 440, text="...", font=("Helvetica", 15, "bold"), fill="white")

# Additional day forecast
day2_label = canvas.create_text(720, 160, text="", font=("poppins", 9, "bold"), fill="white")
day2_temp = canvas.create_text(727, 220, text="", font=("poppins", 60, "bold"), fill="#ee666d")
day2_condition = canvas.create_text(708, 280, text="", font=("poppins", 15, "bold"), fill="white")

root.mainloop()
