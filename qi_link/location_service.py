"""
Location Service - Real-World Environmental Data
=================================================

Fetches real-time location, weather, and environmental data
using free APIs (no API keys required).
"""

import json
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error


@dataclass
class LocationData:
    """Geographic location information."""
    city: str
    region: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    ip_address: str


@dataclass
class WeatherData:
    """Current weather conditions."""
    temperature_celsius: float
    feels_like_celsius: float
    humidity_percent: int
    wind_speed_kmh: float
    wind_direction_degrees: int
    weather_condition: str
    is_day: bool


@dataclass
class CompassData:
    """Compass/orientation data."""
    direction_degrees: float
    cardinal_direction: str
    chinese_direction: str
    element: str  # Associated element in Feng Shui


class LocationService:
    """
    Service for fetching real-world location and environmental data.
    
    Uses free APIs that don't require API keys:
    - ip-api.com for geolocation
    - Open-Meteo for weather data
    """
    
    CARDINAL_DIRECTIONS = [
        ("N", "North", "北", "water"),
        ("NE", "Northeast", "東北", "earth"),
        ("E", "East", "東", "wood"),
        ("SE", "Southeast", "東南", "wood"),
        ("S", "South", "南", "fire"),
        ("SW", "Southwest", "西南", "earth"),
        ("W", "West", "西", "metal"),
        ("NW", "Northwest", "西北", "metal"),
    ]
    
    def __init__(self):
        self._cached_location: Optional[LocationData] = None
        self._cached_weather: Optional[WeatherData] = None
        self._cache_time: float = 0
        self._cache_duration: float = 300  # 5 minutes
    
    def get_location(self) -> Optional[LocationData]:
        """
        Get current location based on IP address.
        
        Returns:
            LocationData or None if fetch fails.
        """
        if self._cached_location and (time.time() - self._cache_time) < self._cache_duration:
            return self._cached_location
        
        try:
            url = "http://ip-api.com/json/?fields=status,city,regionName,country,lat,lon,timezone,query"
            req = urllib.request.Request(url, headers={"User-Agent": "Qi-Link/1.0"})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                if data.get("status") == "success":
                    self._cached_location = LocationData(
                        city=data.get("city", "Unknown"),
                        region=data.get("regionName", "Unknown"),
                        country=data.get("country", "Unknown"),
                        latitude=data.get("lat", 0.0),
                        longitude=data.get("lon", 0.0),
                        timezone=data.get("timezone", "UTC"),
                        ip_address=data.get("query", "0.0.0.0"),
                    )
                    self._cache_time = time.time()
                    return self._cached_location
                    
        except (urllib.error.URLError, json.JSONDecodeError, Exception):
            pass
        
        return self._get_fallback_location()
    
    def get_weather(self, location: Optional[LocationData] = None) -> Optional[WeatherData]:
        """
        Get current weather for location.
        
        Uses Open-Meteo API (free, no key required).
        
        Args:
            location: LocationData or None to auto-detect.
            
        Returns:
            WeatherData or None if fetch fails.
        """
        if location is None:
            location = self.get_location()
        
        if location is None:
            return self._get_fallback_weather()
        
        try:
            # Open-Meteo API
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={location.latitude}&longitude={location.longitude}"
                f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
                f"weather_code,wind_speed_10m,wind_direction_10m,is_day"
                f"&timezone=auto"
            )
            
            req = urllib.request.Request(url, headers={"User-Agent": "Qi-Link/1.0"})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                current = data.get("current", {})
                
                weather_code = current.get("weather_code", 0)
                condition = self._weather_code_to_condition(weather_code)
                
                self._cached_weather = WeatherData(
                    temperature_celsius=current.get("temperature_2m", 20.0),
                    feels_like_celsius=current.get("apparent_temperature", 20.0),
                    humidity_percent=int(current.get("relative_humidity_2m", 50)),
                    wind_speed_kmh=current.get("wind_speed_10m", 0.0),
                    wind_direction_degrees=int(current.get("wind_direction_10m", 0)),
                    weather_condition=condition,
                    is_day=bool(current.get("is_day", 1)),
                )
                return self._cached_weather
                
        except (urllib.error.URLError, json.JSONDecodeError, Exception):
            pass
        
        return self._get_fallback_weather()
    
    def get_compass_direction(self, degrees: Optional[float] = None) -> CompassData:
        """
        Convert degrees to compass direction with Feng Shui associations.
        
        Desktop devices cannot detect compass direction, so this can be:
        - Manual input (degrees provided)
        - Derived from wind direction (weather data)
        - Time-based calculation (solar position approximation)
        
        Args:
            degrees: Direction in degrees (0-360), or None for auto.
            
        Returns:
            CompassData with direction info.
        """
        if degrees is None:
            # Try to get from wind direction if weather is cached
            if self._cached_weather:
                degrees = float(self._cached_weather.wind_direction_degrees)
            else:
                # Fallback: Use time-based pseudo-direction
                # Maps hour to direction (sun position approximation)
                hour = datetime.now().hour
                degrees = (hour * 15) % 360  # 15 degrees per hour
        
        # Normalize to 0-360
        degrees = degrees % 360
        
        # Find cardinal direction (8 directions, 45 degrees each)
        index = int((degrees + 22.5) / 45) % 8
        abbrev, name, chinese, element = self.CARDINAL_DIRECTIONS[index]
        
        return CompassData(
            direction_degrees=degrees,
            cardinal_direction=name,
            chinese_direction=chinese,
            element=element,
        )
    
    def _weather_code_to_condition(self, code: int) -> str:
        """Convert WMO weather code to human-readable condition."""
        conditions = {
            0: "Clear",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing Rime Fog",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Dense Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Slight Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            77: "Snow Grains",
            80: "Slight Rain Showers",
            81: "Moderate Rain Showers",
            82: "Violent Rain Showers",
            85: "Slight Snow Showers",
            86: "Heavy Snow Showers",
            95: "Thunderstorm",
            96: "Thunderstorm with Slight Hail",
            99: "Thunderstorm with Heavy Hail",
        }
        return conditions.get(code, "Unknown")
    
    def _get_fallback_location(self) -> LocationData:
        """Return fallback location when API fails."""
        return LocationData(
            city="Unknown",
            region="Unknown",
            country="Unknown",
            latitude=0.0,
            longitude=0.0,
            timezone="UTC",
            ip_address="0.0.0.0",
        )
    
    def _get_fallback_weather(self) -> WeatherData:
        """Return fallback weather when API fails."""
        hour = datetime.now().hour
        # Simulate temperature based on time of day
        base_temp = 20.0
        time_variance = 5.0 * (1 - abs(hour - 14) / 12)  # Peak at 2 PM
        
        return WeatherData(
            temperature_celsius=round(base_temp + time_variance, 1),
            feels_like_celsius=round(base_temp + time_variance, 1),
            humidity_percent=50,
            wind_speed_kmh=10.0,
            wind_direction_degrees=180,
            weather_condition="Unknown (Offline)",
            is_day=6 <= hour <= 18,
        )
    
    def get_all_environmental_data(self) -> dict:
        """
        Fetch all environmental data in one call.
        
        Returns:
            dict with location, weather, and compass data.
        """
        location = self.get_location()
        weather = self.get_weather(location)
        compass = self.get_compass_direction()
        
        return {
            "location": location,
            "weather": weather,
            "compass": compass,
        }

