from flask import Flask, render_template
from weather import weather_by_city

app = Flask(__name__)


@app.route("/")
def first_foo():
    page_title = 'Новости Python'
    weather = weather_by_city('Petersburg,Russia')
    return render_template('index.html', weather=weather, page_title=page_title)


if __name__ == "__main__":
    app.run(debug=True)
