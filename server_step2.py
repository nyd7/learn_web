from flask import Flask
from weather import weather_by_city

app = Flask(__name__)


@app.route("/")
def first_foo():
    weather = weather_by_city('Petersburg,Russia')

    if weather:
        weather_text = f'''
        Сейчас {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}
        '''
    else:
        weather_text = 'Сервис погоды временно недоступен'

    return f"""
    <html>
        <head>
            <title>Прогноз погоды</title>
        </head>
        <body>
            <h1>{weather_text}</h1>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
