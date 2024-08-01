from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import CityForm
from app.models import CitySearch
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import pytz
from timezonefinder import TimezoneFinder
import requests
import psycopg2

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CityForm()
    weather = None
    forecast = None

    if form.validate_on_submit():
        city = form.city.data
        weather, forecast = get_weather(city)

        if weather:
            flash(f'Weather in {city}: {weather}')

            city_search = CitySearch.query.filter_by(city_name=city).first()
            if city_search:
                db.session.delete(city_search)
                db.session.commit()
            city_search = CitySearch(city_name=city)
            db.session.add(city_search)
            db.session.commit()

    search_history = [entry.city_name for entry in CitySearch.query.order_by(CitySearch.id.desc()).limit(3).all()]

    return render_template('index.html', form=form, weather=weather, forecast=forecast, search_history=search_history)

conn_string = "host=localhost port=5432 dbname=postgres user=postgres password=I4seeyiseey"

def get_db_connection():
    conn = psycopg2.connect(conn_string)
    return conn

@app.route('/api/cities', methods=['GET'])
def cities():
    q = request.args.get('q')
    if not q:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT name
    FROM city
    WHERE name ILIKE %s
    ORDER BY name
    LIMIT 10;
    """
    cursor.execute(query, (f'{q}%',))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    cities = [{'name': row[0]} for row in results]
    return jsonify(cities)

def get_coordinates(city):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None

def get_weather(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return None, None

    api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        weather_data = data['current_weather']
        hourly_weather = data.get('hourly', {}).get('temperature_2m', [])
        times = data.get('hourly', {}).get('time', [])

        if len(hourly_weather) > 0 and len(times) > 0:
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lat=lat, lng=lon)
            local_timezone = pytz.timezone(timezone_str) if timezone_str else pytz.utc
            current_time = datetime.now(local_timezone)

            forecast = []

            current_hour = current_time.replace(minute=0, second=0, microsecond=0)
            hours_from_now = [current_hour + timedelta(hours=i) for i in range(6)]

            for hour in hours_from_now:
                hour_str = hour.strftime('%Y-%m-%dT%H:%M')
                if hour_str in times:
                    index = times.index(hour_str)
                    temperature = hourly_weather[index]
                    forecast.append({
                        'time': hour.strftime('%H:%M'),
                        'temperature': f'{temperature}'
                    })
                else:
                    forecast.append({
                        'time': hour.strftime('%H:%M'),
                        'temperature': 'Нет данных'
                    })

            utc_time = datetime.strptime(weather_data['time'], '%Y-%m-%dT%H:%M').replace(tzinfo=pytz.utc)
            local_time = utc_time.astimezone(local_timezone)
            weather_data['time'] = local_time.strftime('%Y-%m-%d')

            return weather_data, forecast

    return None, None

@app.route('/api/history', methods=['GET'])
def history():
    history = CitySearch.query.order_by(CitySearch.id.desc()).limit(3).all()
    cities = [{'city': h.city_name} for h in history]
    return jsonify(cities)
