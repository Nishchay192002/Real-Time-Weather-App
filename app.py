from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Replace 'your-openweathermap-api-key' with your actual OpenWeatherMap API key
OPENWEATHER_API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_weather')
def get_weather(data):
    city = data['city']
    weather_data = fetch_weather(city)
    emit('weather_response', {'city': city, 'weather_data': weather_data})

def fetch_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'
        response = requests.get(url)
        weather_data = response.json()

        if 'main' in weather_data:
            # Convert temperature from Kelvin to Celsius
            weather_data['main']['temp'] = round(weather_data['main']['temp'] - 273.15, 2)
            
        return weather_data
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    socketio.run(app, debug=True)
