import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Configuration
    API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    BASE_URL = os.getenv(
        "OPENWEATHER_BASE_URL", 
        "https://api.openweathermap.org/data/2.5/weather"
    )
    
    # App Configuration
    APP_TITLE = "Weather App"
    APP_WIDTH = 400
    APP_HEIGHT = 600
    
    # API Settings
    # Store the unit used for API calls (Metric for client-side conversion)
    API_UNITS = "metric" 
    TIMEOUT = 10 
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.API_KEY:
            # This raises an error if the key is missing.
            raise ValueError(
                "OPENWEATHER_API_KEY not found. "
                "Please create a .env file with your API key to ensure accurate weather data."
            )
        return True

# Validate on import
Config.validate()