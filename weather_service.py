import httpx
from typing import Dict
from config import Config
import json # Ensure json is imported for error handling


class WeatherServiceError(Exception):
    """Custom exception for weather service errors."""
    pass


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.BASE_URL
        self.timeout = Config.TIMEOUT

    def _handle_api_response(self, response: httpx.Response, city: str, is_forecast: bool):
        """Helper to check and process the HTTP response."""
        
        # Successful response (200 OK)
        if response.status_code == 200:
            return response.json()

        # Handle API Errors
        try:
            data = response.json()
            error_message = data.get("message", f"Error fetching data: HTTP {response.status_code}")
        except json.JSONDecodeError:
             error_message = f"API returned non-JSON error (HTTP {response.status_code})"
             
        endpoint_type = "Forecast" if is_forecast else "Current Weather"

        if response.status_code == 400:
            raise WeatherServiceError(f"{endpoint_type} Error (400): Bad Request. {error_message}")
        
        elif response.status_code == 404:
            raise WeatherServiceError(
                f"{endpoint_type} Error (404): City '{city}' not found. Please check the spelling."
            )
        elif response.status_code == 401:
            raise WeatherServiceError(
                f"{endpoint_type} Error (401): Invalid API key. Please check your configuration."
            )
        elif response.status_code >= 500:
            raise WeatherServiceError(
                f"{endpoint_type} Error (5xx): Service unavailable. {error_message}"
            )
        else:
            raise WeatherServiceError(
                f"{endpoint_type} Error ({response.status_code}): {error_message}"
            )

    
    async def get_weather(self, city: str) -> Dict:
        """Fetch current weather data for a given city."""
        if not city:
            raise WeatherServiceError("City name cannot be empty")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": Config.API_UNITS,
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
                
                return self._handle_api_response(response, city, is_forecast=False)
                
        except httpx.TimeoutException:
            raise WeatherServiceError(
                "Request timed out. Please check your internet connection."
            )
        except httpx.NetworkError:
            raise WeatherServiceError(
                "Network error. Please check your internet connection."
            )
        except Exception as e:
            if isinstance(e, WeatherServiceError):
                raise
            raise WeatherServiceError(f"An unexpected error occurred during weather fetch: {str(e)}")
    
    async def get_forecast(self, city: str) -> Dict:
        """Fetch 5-day forecast data for a given city."""
        if not city:
            raise WeatherServiceError("City name cannot be empty")
        
        # Build forecast URL (different endpoint)
        forecast_url = self.base_url.replace("/weather", "/forecast")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": Config.API_UNITS,
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(forecast_url, params=params)
                
                return self._handle_api_response(response, city, is_forecast=True)
                
        except httpx.TimeoutException:
            raise WeatherServiceError(
                "Request timed out. Please check your internet connection."
            )
        except httpx.NetworkError:
            raise WeatherServiceError(
                "Network error. Please check your internet connection."
            )
        except Exception as e:
            if isinstance(e, WeatherServiceError):
                raise
            raise WeatherServiceError(f"An unexpected error occurred during forecast fetch: {str(e)}")