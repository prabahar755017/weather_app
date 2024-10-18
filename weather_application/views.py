from django.shortcuts import render
import json  # To convert JSON data into Python dictionary
import urllib.request  # To make HTTP requests

def index(request):
    if request.method == 'POST':
        city = request.POST['city']  # Get the city name from the form

        # Replace 'your_api_key_here' with your actual API key
        API_KEY = ''

        # Construct the API URL
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

        try:
            # Make the request and read the response
            source = urllib.request.urlopen(url).read()
            
            # Convert the response from JSON to a dictionary
            list_of_data = json.loads(source)

            # Extract the required data
            data = {
                "city": city,
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": f"{list_of_data['main']['temp']} °C",
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "weather": str(list_of_data['weather'][0]['description']),
            }
        except urllib.error.HTTPError as e:
            data = {"error": f"Unable to fetch data. HTTP Error: {e}"}
            print(data)
        except KeyError:
            data = {"error": "Invalid city name or API response."}
            print(data)
    else:
        data = {}
        print(data)

    # Render the template with the data
    return render(request, "weather/index.html", {"data": data})
