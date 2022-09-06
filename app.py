import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    data = get_weather_results(zip_code, get_api_key())
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    choices = recommend(temp)
    phrase = choices[0]
    outerwear = choices[1]
    top = choices[2]
    bottoms = choices[3]
    shoes = choices[4]
    return render_template('results.html', location=location, temp=temp, feels_like=feels_like, weather=weather,
                           phrase=phrase, outerwear=outerwear, top=top, bottoms=bottoms, shoes=shoes)

def recommend(temp):
    phrase, outerwear, top, bottoms, shoes = "", "", "", "", ""
    temp = float(temp)
    if(temp > 85):
        phrase = "It's hot outside!"
        outerwear = "None, however if you're going somewhere cold, a light hoodie or cardigan."
        top = "A short sleeve t-shirt. Graphic and oversized tees are great in the summer/spring!"
        bottoms = "I'd prefer shorts. However, lightweight linen pants would also work."
        shoes = "Nowadays I like to wear sneakers/low-top boots with crew socks with shorts."
    elif(65 < temp <= 87):
        phrase = "It's cooling down or heating up! Perfect fall/spring temperatures!"
        outerwear = "If it's warmer, either nothing or a lightweight jacket will suffice. If it's colder, a medium" \
                    "-weight hoodie or cardigan will be nice."
        top = "Wear a 3/4 or long-sleeve t-shirt if you aren't wearing outerwear, otherwise, a graphic tee to layer" \
              "with the outerwear."
        bottoms = "Perfect jeans weather! Bust out your favorite pair of denim, or alternatively, cargo pants."
        shoes = "A nice pair of sneakers or boots that won't make your feet sweat too much are perfect."
    elif(temp <= 65):
        phrase = "It's cold out!"
        outerwear = "Depending on specific temperatures, either a medium-weight jacket or a warm puffer will do."
        top = "Choose graphic tee to layer with or a thermal to keep you warm if its really chilly."
        bottoms = "Go with a pair of jeans or a nice pair of wide-leg trousers."
        shoes = "Boot season! Slap on your favorite pair of boots, no matter if they're combat or cowboy."

    return [phrase, outerwear, top, bottoms, shoes]


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
    api_url="http://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

if __name__ == '__main__':
    app.run()