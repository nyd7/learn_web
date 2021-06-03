from flask import Flask, render_template
from weather import weather_by_city

app = Flask(__name__)


@app.route("/")
def first_foo():
    page_title = 'Прогноз погоды'
    weather = weather_by_city('Petersburg,Russia')

    if weather:
        weather_text = f"""
        Сейчас {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}
        """
    else:
        weather_text = 'Сервис погоды временно недоступен'

    return render_template('index.html', weather_text=weather_text, page_title=page_title)


if __name__ == "__main__":
    app.run(debug=True)
