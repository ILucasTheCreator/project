from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_location():
    ip_address = request.remote_addr
    if ip_address == '127.0.0.1':
        ip_address = '72.229.28.185'
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        'ip': ip_address,
        'city': response.get('city'),
        'region': response.get('region'),
        'country': response.get('country_name')
    }
    return jsonify(location_data)

API_KEY = '5e005e60e5e8bbae8839485f8be45859'
def backround_info(weather_id):
        backround_image = ''
        backround_color = ''
        if weather_id == "01d":
            backround_image = 'sunnyday.webm'
            backround_color = '#569cd4'
        elif weather_id == "01n":
            backround_image = 'clearnight.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "02d":
            backround_image = 'few-cloud-day.webm'
            backround_color = '#569cd4'
        elif weather_id == "02n":
            backround_image = 'cloudynight.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "03d":
            backround_image = 'scattered-day.webm'
            backround_color = '#73a1d0'
        elif weather_id == "03n":
            backround_image = 'scattered-night.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "04d":
            backround_image = 'nigcloudy.webm'
            backround_color = '#a6b1ba'
        elif weather_id == "04n":
            backround_image = 'nigcloudy.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "09d":
            backround_image = 'sunny-rain.webm'
            backround_color = '#73a1d0'
        elif weather_id == "09n":
            backround_image = 'moon-peeking-rain.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "10d":
            backround_image = 'heavy-rains.webm'
            backround_color = '#a6b1ba'
        elif weather_id == "10n":
            backround_image = 'heavy-rains.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "11d":
            backround_image = 'thunderstorm.webm'
            backround_color = '#a6b1ba'
        elif weather_id == "11n":
            backround_image = 'thunderstorm.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "13d":
            backround_image = 'snow.webm'
            backround_color = '#a6b1ba'
        elif weather_id == "13n":
            backround_image = 'snow.webm'
            backround_color = '#3f3e3e'
        elif weather_id == "50d":
            backround_image = 'mist.webm'
            backround_color = '#a6b1ba'    
        elif weather_id == "50n":
            backround_image = 'mist.webm'
            backround_color = '#3f3e3e'
        else:
            backround_image = 'default.jpg'
        # Add more conditions for other weather icons as needed
        return backround_image, backround_color
    
@app.route('/', methods=['GET', 'POST'])
def index():
    user_location = get_location().get_json()
    user_city = user_location['city']
    if not user_city:
        user_city = 'Hong Kong'

    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            user_url = f'http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid=5e005e60e5e8bbae8839485f8be45859&units=imperial'
            user_weather_info = requests.get(user_url)
            if user_weather_info.status_code == 200:
                data = user_weather_info.json()
                city_name = data['name'] + ',' + data['sys']['country']
                description = data['weather'][0]['description']
                tempeture = round(data['main']['temp'])
                temp_min = round(data['main']['temp_min'])
                temp_max = round(data['main']['temp_max'])
                feels_like = round(data['main']['feels_like'])
                backround_image, backround_color = backround_info(data['weather'][0]['icon'])
                if not backround_image or not backround_color:
                    backround_image = 'snow.webm'
                    backround_color = '#ffffff'
                return render_template('index.html', error="please enter a city" , city_name=city_name, description=description,
                                       tempeture=tempeture, temp_min=temp_min, temp_max=temp_max,
                                       feels_like=feels_like , backround_image=backround_image,
                                       backround_color=backround_color)
        else:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5e005e60e5e8bbae8839485f8be45859&units=imperial'
            weather_info = requests.get(url)
            if weather_info.status_code == 200:
                data = weather_info.json()
                if 'country' not in data['sys']:
                    city_name = data['name']
                else:
                    city_name = data['name'] + ',' + data['sys']['country']
                description = data['weather'][0]['description']
                tempeture = round(data['main']['temp'])
                temp_min =round(data['main']['temp_min'])
                temp_max = round(data['main']['temp_max'])
                feels_like = round(data['main']['feels_like'])
                backround_image, backround_color = backround_info(data['weather'][0]['icon'])
                if not backround_image or not backround_color:
                    backround_image = 'snow.webm'
                    backround_color = '#ffffff'
                return render_template('index.html', city_name=city_name, description=description,
                                   tempeture=tempeture, temp_min=temp_min, temp_max=temp_max,
                                   feels_like=feels_like , backround_image=backround_image,
                                   backround_color=backround_color)
            else:
                user_url = f'http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid=5e005e60e5e8bbae8839485f8be45859&units=imperial'
                user_weather_info = requests.get(user_url)
                if user_weather_info.status_code == 200:
                    data = user_weather_info.json()
                    city_name = data['name'] + ',' + data['sys']['country']
                    description = data['weather'][0]['description']
                    tempeture = round(data['main']['temp'])
                    temp_min = round(data['main']['temp_min'])
                    temp_max = round(data['main']['temp_max'])
                    feels_like = round(data['main']['feels_like'])
                    backround_image, backround_color = backround_info(data['weather'][0]['icon'])
                    if not backround_image or not backround_color:
                        backround_image = 'snow.webm'
                        backround_color = '#ffffff'
                    return render_template('index.html', error="city not found,please try again" , city_name=city_name, description=description,
                                       tempeture=tempeture, temp_min=temp_min, temp_max=temp_max,
                                       feels_like=feels_like , backround_image=backround_image,
                                       backround_color=backround_color)
    else:
        user_url = f'http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid=5e005e60e5e8bbae8839485f8be45859&units=imperial'
        user_weather_info = requests.get(user_url)
        if user_weather_info.status_code == 200:
            data = user_weather_info.json()
            city_name = data['name'] + ',' + data['sys']['country']
            description = data['weather'][0]['description']
            tempeture = round(data['main']['temp'])
            temp_min = round(data['main']['temp_min'])
            temp_max = round(data['main']['temp_max'])
            feels_like = round(data['main']['feels_like'])
            backround_image, backround_color = backround_info(data['weather'][0]['icon'])
            if not backround_image or not backround_color:
                backround_image = 'snow.webm'
                backround_color = '#ffffff'
            return render_template('index.html', city_name=city_name, description=description,
                                       tempeture=tempeture, temp_min=temp_min, temp_max=temp_max,
                                       feels_like=feels_like , backround_image=backround_image,
                                       backround_color=backround_color)

if __name__ == '__main__':
    app.run(debug=True)
