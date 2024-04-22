import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def get_weather(city_name):
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        pollution_data = get_pollution(city_name)

        weather = {
            "city": city_name,
            "temperature": main_data["temp"],
            "humidity": main_data["humidity"],
            "description": weather_data["description"],
            "icon": weather_data["icon"],
            "pollution": pollution_data
        }
        return weather
    else:
        return None

def get_pollution(city_name):
    api_key = "YOUR_OPENAQ_API_KEY"
    base_url = "https://api.openaq.org/v1/latest?"
    complete_url = f"{base_url}city={city_name}&parameter=pm25&limit=1&order_by=lastUpdated&sort=desc&format=json"
    response = requests.get(complete_url)
    data = response.json()

    if "results" in data and data["results"]:
        pollution_data = data["results"][0]["measurements"][0]["value"]
        return pollution_data
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        weather = get_weather(city)

    return render_template("index.html", weather=weather)

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

if __name__ == "__main__":
    app.run(debug=True)
