import tkinter as tk
from tkinter import messagebox

from PIL import Image, Image
from datetime import datetime, timedelta
import pytz
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import os

# Initialize the Tkinter window
root = tk.Tk()
root.title("EcoWeather: Promoting Climate-conscious Living.")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Background Image
background_path = os.path.join(os.getcwd(), "background.png")
background_image = Image.PhotoImage(Image.open(background_path))
canvas = tk.Canvas(root, width=900, height=500)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Create a dictionary mapping weather conditions to logo image paths
logo_images = {
    "Clear": "logo_clear.png",
    "Clouds": "logo_clouds.png",
    "Rain": "logo_rain.png",
    "Snow": "logo_snow.png"
}

current_date = datetime.now().strftime("%B %d, %Y")
date_label = canvas.create_text(800, 30, text=current_date, font=("Arial", 15, "bold"), fill="white")


def update_logo(condition):
    logo_image_path = os.path.join(os.getcwd(), logo_images.get(condition, "logo.png"))
    logo_image = Image.PhotoImage(Image.open(logo_image_path))
    canvas.itemconfig(logo, image=logo_image)
    canvas.image = logo_image


def get_weather(event=None):
    try:
        city = textfield.get()

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)

        if not location:
            messagebox.showerror("Weather App", "Invalid city name entered. Please try again.")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        canvas.itemconfig(clock, text=current_time)
        canvas.itemconfig(name, text="CURRENT WEATHER")

        api = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=87d4249734d3257a7fcde087dbc7de78"

        json_data = requests.get(api).json()

        if 'weather' not in json_data or 'main' not in json_data:
            messagebox.showerror("Weather App", "Weather data not available.")
            return

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        canvas.itemconfig(t, text=f"{temp}°")
        canvas.itemconfig(c, text=f"{condition} | FEELS LIKE {temp}°")

        canvas.itemconfig(w, text=wind)
        canvas.itemconfig(h, text=humidity)
        canvas.itemconfig(d, text=description)
        canvas.itemconfig(p, text=pressure)

        api_forecast = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=87d4249734d3257a7fcde087dbc7de78"
        json_data_forecast = requests.get(api_forecast).json()

        if 'list' not in json_data_forecast:
            messagebox.showerror("Weather App", "Forecast data not available.")
            return

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_date = tomorrow.strftime("%Y-%m-%d")

        for forecast in json_data_forecast['list']:
            forecast_date = forecast['dt_txt'].split()[0]
            if forecast_date == tomorrow_date:
                day2_temp_value = int(forecast['main']['temp'] - 273.15)
                day2_condition_value = forecast['weather'][0]['main']
                break
        else:
            messagebox.showerror("Weather App", "Forecast data not available for tomorrow.")
            return

        canvas.itemconfig(day2_temp, text=f"{day2_temp_value}°")
        canvas.itemconfig(day2_condition, text=f"{day2_condition_value}")
        canvas.itemconfig(day2_label, text="TOMORROW'S FORECAST")

        update_logo(condition)

    except requests.exceptions.RequestException:
        messagebox.showerror("Weather App", "An error occurred while making the request. Please check your internet connection.")
    except KeyError:
        messagebox.showerror("Weather App", "Invalid response from the weather API.")
    except Exception as e:
        messagebox.showerror("Weather App", "An error occurred while fetching weather data: " + str(e))


# Search box
search_image_path = os.path.join(os.getcwd(), "search_box.png")
search_image = Image.PhotoImage(Image.open(search_image_path))
myimage = canvas.create_image(25, 20, anchor=tk.NW, image=search_image)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg=canvas["bg"], border=0,
                     fg="black")
textfield.place(x=50, y=40)
textfield.focus()
textfield.bind("<Return>", get_weather)

search_icon_path = os.path.join(os.getcwd(), "search_icon.png")
search_icon = Image.PhotoImage(Image.open(search_icon_path))
myimage_icon = tk.Button(image=search_icon, borderwidth=0, cursor="hand2", bg="black", command=get_weather)
myimage_icon.place(x=380, y=30)

# Logo
logo_image_path = os.path.join(os.getcwd(), "logo.png")
logo_image = Image.PhotoImage(Image.open(logo_image_path))
logo = canvas.create_image(140, 100, anchor=tk.NW, image=logo_image)

# Bottom box
frame_image_path = os.path.join(os.getcwd(), "box.png")
frame_image = Image.PhotoImage(Image.open(frame_image_path))
frame_myimage = canvas.create_image(50, 380, anchor=tk.NW, image=frame_image)

# Time
name = canvas.create_text(140, 120, text="", font=("arial", 15, "bold"), fill="white")
clock = canvas.create_text(130, 150, text="", font=("Helvetica", 20), fill="white")

# Labels
label1 = canvas.create_text(130, 410, text="WIND", font=("Helvetica", 15, 'bold'), fill="white")
label2 = canvas.create_text(270, 410, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fill="white")
label3 = canvas.create_text(470, 410, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fill="white")
label4 = canvas.create_text(690, 410, text="PRESSURE", font=("Helvetica", 15, 'bold'), fill="white")

t = canvas.create_text(530, 200, text="", font=("arial", 90, 'bold'), fill="#ee666d")
c = canvas.create_text(530, 280, text="", font=("arial", 15, 'bold'), fill="white")

w = canvas.create_text(130, 445, text="...", font=("arial", 20, "bold"), fill="white")
h = canvas.create_text(260, 445, text="...", font=("arial", 20, "bold"), fill="white")
d = canvas.create_text(465, 445, text="...", font=("arial", 20, "bold"), fill="white")
p = canvas.create_text(670, 445, text="...", font=("arial", 20, "bold"), fill="white")

# Additional day's forecast
day2_temp = canvas.create_text(727, 220, text="", font=("poppins", 60, 'bold'), fill="#ee666d")
day2_condition = canvas.create_text(708, 280, text="", font=("poppins", 15, 'bold'), fill="white")
day2_label = canvas.create_text(720, 160, text="", font=("poppins", 9, 'bold'), fill="white")

root.mainloop()
