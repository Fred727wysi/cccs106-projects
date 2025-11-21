# Main file for the Weather App using Flet
# Contains the WeatherApp class that handles the UI and app logic
# Fetches weather data via WeatherService and shows it in a simple interface
# Supports Celsius/Fahrenheit toggle and search history
# Dependencies: flet, json, pathlib, datetime, collections
import flet as ft
import json
from pathlib import Path
import datetime
from collections import defaultdict

from weather_service import WeatherService
from config import Config


class WeatherApp:
    """Main Weather Application class."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        # self.current_unit tracks the displayed unit ('metric' or 'imperial')
        self.current_unit = "metric" 
        # API fetches in metric, store these base values
        self.current_temp_c = None
        self.current_feels_like_c = None
        self.forecast_data = None # Store raw, metric forecast data
        self.weather_container = None
        self.forecast_container = None
        self.setup_page()
        self.build_ui()

    def setup_page(self):
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()
        self.page.animate_theme_mode = True
        self.page.theme_animation_duration = 500

    def build_ui(self):
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )

        # City input
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search_async,
        )

        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search_async,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        )

        # Search history dropdown
        self.history_dropdown = ft.Dropdown(
            label="Recent Searches",
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=self.on_history_select,
            width=300
        )

        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
        )

        # Unit toggle
        self.unit_button = ft.ElevatedButton(
            "°C",
            tooltip="Toggle temperature unit",
            on_click=self.toggle_units,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        )

        # Weather container (for current weather)
        self.weather_container = ft.Container(
            visible=False,
            border_radius=10,
            padding=20,
            animate_opacity=300,
        )

        # Forecast container (will hold both summary cards and tabs/expanders)
        self.forecast_container = ft.Container(
            visible=False,
            padding=10,
            animate_opacity=300,
        )

        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
        )

        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)

        # Main scrollable column
        self.main_column = ft.Column(
            [
                ft.Row([self.title, ft.Row([self.theme_button, self.unit_button])],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.city_input,
                self.search_button,
                self.history_dropdown,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.loading,
                self.error_message,
                self.weather_container,
                self.forecast_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            scroll="auto",
            expand=True
        )

        self.page.add(self.main_column)

    def c_to_f(self, temp_c):
        """Converts Celsius to Fahrenheit."""
        return (temp_c * 9/5) + 32

    def f_to_c(self, temp_f):
        """Converts Fahrenheit to Celsius."""
        return (temp_f - 32) * 5/9

    async def on_search_async(self, e):
        await self.get_weather()

    async def on_history_select(self, e):
        if self.history_dropdown.value:
            self.city_input.value = self.history_dropdown.value
            self.page.update()
            await self.get_weather()

    async def get_weather(self):
        city = self.city_input.value.strip()
        if not city:
            self.show_error("Please enter a city name")
            return

        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.page.update()

        try:
            # Current weather
            weather_data = await self.weather_service.get_weather(city)
            # Forecast (Data will be in metric as per weather_service.py config)
            self.forecast_data = await self.weather_service.get_forecast(city)

            # Store base metric values
            self.current_temp_c = weather_data.get("main", {}).get("temp", 0)
            self.current_feels_like_c = weather_data.get("main", {}).get("feels_like", 0)

            # Ensure unit is set to C (API standard) before display
            self.current_unit = "metric"
            self.unit_button.text = "°C"

            # Save to history
            self.add_to_history(city)
            self.update_history_dropdown()

            # Display weather (uses current_temp_c, but handles conversion in display)
            await self.display_weather(weather_data)
            # Await the initial forecast display
            await self.display_forecast(self.forecast_data) 

        except Exception as e:
            self.show_error(str(e))
        finally:
            self.loading.visible = False
            self.page.update()

    def get_weather_visuals(self, description: str):
        desc = description.lower()
        if "clear" in desc:
            return "☀", "#FFEE88"
        if "cloud" in desc or "broken" in desc or "scattered" in desc:
            return "☁", "#C9D6DF"
        if "rain" in desc:
            return "🌧", "#90C4F7"
        if "thunder" in desc:
            return "⛈", "#735D78"
        if "snow" in desc:
            return "❄", "#D8F3FF"
        if "mist" in desc or "fog" in desc:
            return "🌫", "#E0E0E0"
        return "🌡", "#F5F5F5"

    async def display_weather(self, data: dict):
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)

        # Determine visual cues
        emoji, light_bg_color = self.get_weather_visuals(description)

        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.bgcolor = light_bg_color
            self.weather_container.bgcolor = ft.Colors.BLUE_50
        else:
            self.page.bgcolor = None  
            self.weather_container.bgcolor = ft.Colors.GREY_900
        
        # Get displayed temps using the current unit
        temp_to_display = self.current_temp_c
        feels_to_display = self.current_feels_like_c
        unit_symbol = "°C"
        
        if self.current_unit == "imperial":
            temp_to_display = self.c_to_f(temp_to_display)
            feels_to_display = self.c_to_f(feels_to_display)
            unit_symbol = "°F"

        self.weather_container.content = ft.Column(
            [
                ft.Text(f"{city_name}, {country}", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Text(f"{emoji} {description}", size=20, italic=True)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                # TEMP CONTROL (Index 2)
                ft.Text(f"{temp_to_display:.1f}{unit_symbol}", size=48, weight=ft.FontWeight.BOLD),
                # FEELS LIKE CONTROL (Index 3)
                ft.Text(f"Feels like {feels_to_display:.1f}{unit_symbol}", size=16),
                ft.Row(
                    [
                        self.create_info_card(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%"),
                        self.create_info_card(ft.Icons.AIR, "Wind Speed", f"{wind_speed} m/s")
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                )
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.weather_container.visible = True
        self.weather_container.update()

    async def display_forecast(self, data: dict):
        """
        Aggregates min/max temp and condition across all 3-hour intervals for each day.
        """
        forecast_list = data.get("list", [])
        
        # Dictionary to hold aggregated daily data: {date: [data_points]}
        daily_forecasts = defaultdict(list)
        
        # 1. Aggregate all 3-hour data points by date
        for item in forecast_list:
            dt_txt = item.get("dt_txt", "")
            if not dt_txt:
                continue
            
            # Use only the date part (YYYY-MM-DD)
            date_str = dt_txt.split(" ")[0]
            daily_forecasts[date_str].append(item)
            
        # 2. Process and summarize daily data
        summary_items = []
        # Get the forecast for the next 5 days, starting from the day *after* today's first forecast
        sorted_dates = sorted(daily_forecasts.keys())[1:6] 
        
        for date_str in sorted_dates:
            day_points = daily_forecasts[date_str]
            if not day_points:
                continue
                
            # Initialize with extreme values
            min_temp = float('inf')
            max_temp = float('-inf')
            
            # Get the date object
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                date_obj = None
                
            # Use the data point closest to noon (12:00:00) for the primary icon/description
            midday_point = day_points[len(day_points) // 2]
            description = midday_point.get("weather", [{}])[0].get("description", "").title()
            icon_code = midday_point.get("weather", [{}])[0].get("icon", "01d")

            # Find the true min/max temperatures for the day from all data points
            for point in day_points:
                temp_min = point.get("main", {}).get("temp_min", 0)
                temp_max = point.get("main", {}).get("temp_max", 0)
                
                # Check for absolute min (low)
                if temp_min < min_temp:
                    min_temp = temp_min
                # Check for absolute max (high)
                if temp_max > max_temp:
                    max_temp = temp_max
            
            # Store the aggregated daily summary (temps are in Celsius)
            summary_items.append({
                'date_obj': date_obj,
                'min_temp_c': min_temp,
                'max_temp_c': max_temp,
                'description': description,
                'icon_code': icon_code
            })

        # 3. Build summary cards (Unit conversion logic applied here)
        summary_cards = []
        unit_symbol = "°F" if self.current_unit == "imperial" else "°C"

        for item in summary_items:
            date_obj = item['date_obj']
            
            weekday_short = date_obj.strftime("%a") if date_obj else "Day"

            # **UNIT CONVERSION for display**
            min_temp_c = item['min_temp_c']
            max_temp_c = item['max_temp_c']
            
            if self.current_unit == "imperial":
                temp_min_display = self.c_to_f(min_temp_c)
                temp_max_display = self.c_to_f(max_temp_c)
            else:
                temp_min_display = min_temp_c
                temp_max_display = max_temp_c

            emoji, _ = self.get_weather_visuals(item['description'])

            # highlight weekends
            is_weekend = date_obj and date_obj.weekday() in (5, 6)

            # Theme-aware colors
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                card_bg = "#FFF7F7" if is_weekend else ft.Colors.WHITE
            else:
                card_bg = ft.Colors.GREY_800 if is_weekend else ft.Colors.BLACK54 

            # SUMMARY CARD 
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(weekday_short, size=12, weight=ft.FontWeight.BOLD),
                        ft.Image(src=f"https://openweathermap.org/img/wn/{item['icon_code']}@2x.png", width=60, height=60),
                        ft.Text(f"{emoji} {item['description']}", size=11, text_align=ft.TextAlign.CENTER),
                        # DISPLAY CONVERTED TEMPS
                        ft.Text(f"{temp_min_display:.0f}{unit_symbol} / {temp_max_display:.0f}{unit_symbol}", size=12),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6
                ),
                bgcolor=card_bg,
                border_radius=10,
                padding=10,
                width=110,
                height=170,
                shadow=ft.BoxShadow(blur_radius=6, spread_radius=0, offset=ft.Offset(0, 2))
            )
            summary_cards.append(card)

        # 4. Final composition
        if not summary_cards:
            self.forecast_container.content = ft.Column(
                [
                    ft.Text("No forecast data available.", size=14)
                ]
            )
        else:
            summary_row = ft.Row(summary_cards, scroll="auto", spacing=10, alignment=ft.MainAxisAlignment.START)
            self.forecast_container.content = ft.Column(
                [
                    ft.Text("5-Day Forecast", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    summary_row,
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            
        self.forecast_container.visible = True
        self.forecast_container.update() 
        
    def create_info_card(self, icon, label, value):
        # Theme-aware colors
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            card_bg = ft.Colors.WHITE
            icon_color = ft.Colors.BLUE_700
            value_color = ft.Colors.BLUE_900
        else:
            card_bg = ft.Colors.BLACK54
            icon_color = ft.Colors.BLUE_400
            value_color = ft.Colors.BLUE_200
            
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=28, color=icon_color),
                    ft.Text(label, size=12),
                    ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=value_color)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6
            ),
            bgcolor=card_bg,
            border_radius=10,
            padding=10,
            width=140,
            height=90
        )

    def show_error(self, msg: str):
        self.error_message.value = f"❌ {msg}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.page.update()

    def toggle_units(self, e):
        # Check if weather data is loaded
        if self.current_temp_c is None:
            return

        # 1. Toggle the internal state
        if self.current_unit == "metric":
            self.current_unit = "imperial"
            self.unit_button.text = "°F"
        else:
            self.current_unit = "metric"
            self.unit_button.text = "°C"

        # 2. Trigger the asynchronous display update via run_task
        self.page.run_task(self.update_display)

    async def update_display(self):
        """Updates both current weather and forecast asynchronously."""
        if not self.weather_container.content:
            return
        
        unit_symbol = "°F" if self.current_unit == "imperial" else "°C"
        
        # Current Weather Update Logic
        temp_to_display = self.current_temp_c
        feels_to_display = self.current_feels_like_c
        
        if self.current_unit == "imperial":
            temp_to_display = self.c_to_f(temp_to_display)
            feels_to_display = self.c_to_f(feels_to_display)
            
        # Re-apply weather container theme based on current theme mode
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            description_text = self.weather_container.content.controls[1].controls[1].value
            description = description_text.split(" ", 1)[-1].strip() 
            _, light_bg_color = self.get_weather_visuals(description)

            self.page.bgcolor = light_bg_color
            self.weather_container.bgcolor = ft.Colors.BLUE_50
        else:
            self.page.bgcolor = None 
            self.weather_container.bgcolor = ft.Colors.GREY_900

        # Update current temp/feels like text values
        self.weather_container.content.controls[2].value = f"{temp_to_display:.1f}{unit_symbol}"
        self.weather_container.content.controls[3].value = f"Feels like {feels_to_display:.1f}{unit_symbol}"
        
        # Forecast Update Logic
        if self.forecast_data:
            # AWAIT the forecast display since update_display is now async
            await self.display_forecast(self.forecast_data) 

        # 3. Update the controls and page (page.update is synchronous in Flet)
        self.page.update()

    def toggle_theme(self, e):
        # 1. Update the theme mode immediately
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        
        # 2. Rerender all components (colors, forecast, etc.) using update_display 
        if self.weather_container.visible:
             # Run the new async update_display
             self.page.run_task(self.update_display)
        else:
            # Only update the page to show the theme change if no weather data is present
            self.page.update()

    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.search_history, f)

    def add_to_history(self, city: str):
        city = city.strip().title()
        if city in self.search_history:
             self.search_history.remove(city)
        
        self.search_history.insert(0, city)
        self.search_history = self.search_history[:10]
        self.save_history()

    def update_history_dropdown(self):
        self.history_dropdown.options = [ft.dropdown.Option(c) for c in self.search_history]
        self.page.update()


def main(page: ft.Page):
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)