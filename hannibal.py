import pyfiglet
from colorama import Fore
import geocoder
import folium
import requests

text = pyfiglet.figlet_format("HANNIBAL \n")
print(Fore.YELLOW + text)

# API token for ipinfo.io
API_TOKEN = "3689f8f6882585"

def get_location_from_ip(ip_address):
  try:
    return geocoder.ip(ip_address).latlng
  except geocoder.GeocoderError:
    return None

def get_ip_info(ip_address):
  url = f"https://ipinfo.io/{ip_address}/json?token={API_TOKEN}"
  response = requests.get(url)

  if response.status_code == 200:
    try:
      data = response.json()
      return {
        "ip": data.get("ip"),
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country"),
        "loc": data.get("loc"),  # Approximate latitude and longitude
        "org": data.get("org"),  # Organization name
        "postal": data.get("postal"),  # Postal code
        "timezone": data.get("timezone"),
      }
    except ValueError:
      print("Invalid JSON response received.")
  else:
    print(f"API request failed with status code: {response.status_code}")

def main():
  ip_address = input("Enter an IP address for map location: ")
  location = get_location_from_ip(ip_address)

  if location is not None:
    map = folium.Map(location=location, zoom_start=10)
    folium.Marker(location=location).add_to(map)
    map.save("map.html")
    print("Person location saved in map.html")
  else:
    print("Could not find location for IP address:", ip_address)

  # Get IP information using a separate function
  ip_info = get_ip_info(ip_address)
  if ip_info:
    print("IP information:")
    for key, value in ip_info.items():
      print(f"{key}: {value}")
  else:
    print("Failed to retrieve IP information.")

  print("Thanks for using our tool!")

if __name__ == "__main__":
  main()


