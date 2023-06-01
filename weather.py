import tkinter as tk
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
import pytz
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import os


class EcoWeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EcoWeather: Promoting Climate-conscious Living.")
        self.root.geometry("900x500+300+200")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=900, height=500)
        self.canvas.pack()
        self.background_path = os.path.join(os.getcwd(), "background.png")
        self.background_image = PhotoImage(file=self.background_path)
        self.canvas.create_image(0, 0, anchor=NW, image=self.background_image)

        self.current_date = datetime.now().strftime("%B %d, %Y")
        self.date_label = self.canvas.create_text(800, 30, text=self.current_date, font=("Arial", 15, "bold"),
                                                  fill="white")

        self.textfield = tk.Entry(self.root, justify="center", width=17, font=("poppins", 25, "bold"),
                                  bg=self.canvas["bg"], border=0, fg="black")
        self.textfield.place(x=50, y=40)
        self.textfield.focus()
        self.textfield.bind("<Return>", self.get_weather)  # Bind Enter key to get_weather function

        self.search_icon_path = os.path.join(os.getcwd(), "search_icon.png")
        self.search_icon = PhotoImage(file=self.search_icon_path)
        self.myimage_icon = Button(image=self.search_icon, borderwidth=0, cursor="hand2", bg="black",
                                   command=self.get_weather)
        self.myimage_icon.place(x=380, y=30)

        self.logo_image_path = os.path.join(os.getcwd(), "logo.png")
        self.logo_image = PhotoImage(file=self.logo_image_path)
        self.logo = self.canvas.create_image(140, 100, anchor=NW, image=self.logo_image)

        self.frame_image_path = os.path.join(os.getcwd(), "box.png")
        self.frame_image = PhotoImage(file=self.frame_image_path)
        self.frame_myimage = self.canvas.create_image(50, 380, anchor=NW, image=self.frame_image)

        self.name = self.canvas.create_text(140, 120, text="", font=("arial", 15, "bold"), fill="white")
        self.clock = self.canvas.create_text(130, 150, text="", font=("Helvetica", 20), fill="white")

        self.label1 = self.canvas.create_text(130, 410, text="WIND", font=("Helvetica", 15, 'bold'), fill="white")
        self.label2 = self.canvas.create_text(270, 410, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fill="white")
        self.label3 = self.canvas.create_text(470, 410, text="DESCRIPTION", font=("Helvetica", 15, 'bold'),
                                              fill="white")
        self.label4 = self.canvas.create_text(690, 410, text="PRESSURE", font=("Helvetica", 15, 'bold'), fill="white")

        self.t = self.canvas.create_text(530, 200, text="", font=("arial", 90, 'bold'), fill="#ee666d")
        self.c = self.canvas.create_text(530, 280, text="", font=("arial", 15, 'bold'), fill="white")

        self.w = self.canvas.create_text(130, 445, text="...", font=("arial", 20, "bold"), fill="white")
        self.h = self.canvas.create_text(260, 445, text="...", font=("arial", 20, "bold"), fill="white")
        self.d = self.canvas.create_text(465, 445, text="...", font=("arial", 20, "bold"), fill="white")
        self.p = self.canvas.create_text(670, 445, text="...", font=("arial", 20, "bold"), fill="white")

        self.day2_temp = self.canvas.create_text(727, 220, text="", font=("poppins", 60, 'bold'), fill="#ee666d")
        self.day2_condition = self.canvas.create_text(708, 280, text="", font=("poppins", 15, 'bold'), fill="white")
        self.day2_label = self.canvas.create_text(720, 160, text="", font=("poppins", 9, 'bold'), fill="white")

        self.root.mainloop()

    def get_weather(self, event=None):
        try:
            city = self.textfield.get()

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
            self.canvas.itemconfig(self.clock, text=current_time)
            self.canvas.itemconfig(self.name, text="CURRENT WEATHER")

            # weather
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

            self.canvas.itemconfig(self.t, text=f"{temp}°")
            self.canvas.itemconfig(self.c, text=f"{condition} | FEELS LIKE {temp}°")

            self.canvas.itemconfig(self.w, text=wind)
            self.canvas.itemconfig(self.h, text=humidity)
            self.canvas.itemconfig(self.d, text=description)
            self.canvas.itemconfig(self.p, text=pressure)

            # weather forecast for additional day
            api_forecast = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid" \
                                                                                         "=87d4249734d3257a7fcde087dbc7de78"
            json_data_forecast = requests.get(api_forecast).json()

            if 'list' not in json_data_forecast:
                messagebox.showerror("Weather App", "Forecast data not available.")
                return

            # Get tomorrow's date
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_date = tomorrow.strftime("%Y-%m-%d")

            # Find the forecast data for tomorrow
            for forecast in json_data_forecast['list']:
                forecast_date = forecast['dt_txt'].split()[0]
                if forecast_date == tomorrow_date:
                    day2_temp_value = int(forecast['main']['temp'] - 273.15)
                    day2_condition_value = forecast['weather'][0]['main']
                    break
            else:
                messagebox.showerror("Weather App", "Forecast data not available for tomorrow.")
                return

            # Update the canvas with the additional day's forecast
            self.canvas.itemconfig(self.day2_temp, text=f"{day2_temp_value}°")
            self.canvas.itemconfig(self.day2_condition, text=f"{day2_condition_value}")
            self.canvas.itemconfig(self.day2_label, text="TOMORROW'S FORECAST")

        except requests.exceptions.RequestException:
            messagebox.showerror("Weather App", "An error occurred while making the request. Please check your internet"
                                                "connection.")
        except KeyError:
            messagebox.showerror("Weather App", "Invalid response from the weather API.")
        except Exception as e:
            messagebox.showerror("Weather App", "An error occurred while fetching weather data: " + str(e))


app = EcoWeatherApp()
