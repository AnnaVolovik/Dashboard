
from flask import Flask, render_template, jsonify
import json
from pprint import pprint

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_envvar('DASHBOARD_SETTINGS', silent=True)

data = Config.statistics.get('data', [])[0]

def get_errors(keyword):

    errors = []
    for el in Config.statistics:
        if el.endswith(f'_{keyword}'):

            total_count = 0
            for key in Config.statistics[el]:
                tmp = {}
                tmp['code'] = 'Other' if key['code'] is None else f'Error {key["code"]:}'
                tmp['count'] = key['count']
                errors.append(tmp)
                total_count = total_count + key['count']

        colors = ['yellow', 'violet', 'blue', 'grey-background']
        hexcolors = ['#FFCC00', '#5856D5', '#2196F3', '#A0B0B9']

        i = 0
        for error in errors:
            if i > 3:
                i = 0
            error['style'] = {"width" : f'{int((error["count"] / total_count) * 100)}%', "background-color": hexcolors[i]}
            error['color'] = colors[i]
            i = i + 1

    return errors

@app.route('/get_stats/<keyword>', methods=['GET', 'POST'])
def get_stats(keyword):

    #set the structure and default values
    stats = {
        'top_statistics': {
            'timeout': {},
            'errors': {},
            'zeroes': {}
        },
        'top_errors': get_errors(keyword),
        'searches': {
            'mobile': round(data.get("mobile_pessimizer", 0), 2) if data.get("mobile_pessimizer") else 0,
            'web': round(data.get("web_pessimizer", 0), 2) if data.get("mobile_pessimizer") else 0
        },
        'clicks': {
            'ctr': round(data.get(f"ctr_{keyword}", 0), 2) if data.get(f"ctr_{keyword}") else 0
        },
        'bookings': {
            'str': round(data.get(f"str_{keyword}", 0), 2) if data.get(f"str_{keyword}") else 0,
            'avg_check': round(data.get(f"avg_price_{keyword}", 0), 2) if data.get(f"avg_price_{keyword}") else 0
        }
    }
    for el in stats['top_statistics']:
        stats['top_statistics'][el]['name'] = el.capitalize()
        # get averages by last 3 days value
        stats['top_statistics'][el]['average'] = round(data.get(f'{el}_last_3days', 0) / 3, 2)
        stats['top_statistics'][el]['value'] = round(data.get(f'{el}_{keyword}', 0), 2) if data.get(f'{el}_{keyword}') else 0

    for key in ['searches', 'clicks', 'bookings']:
        stats[key]['current'] = round(data.get(f'{key}_current_{keyword}', 0), 2)
        stats[key]['previous'] = round(data.get(f'{key}_previous_{keyword}', 0), 2)
        # добавить процент изменений по Searches, Clicks, Bookings
        diff = round((stats[key]['current'] - stats[key]['previous']) / stats[key]['previous'], 2) if stats[key]['previous'] != 0 else 0
        stats[key]['diff'] = f'+{diff}' if diff > 0 else diff

    print(stats)

    return jsonify(stats)

@app.route('/')
def dashboard():
    stats = {}
    for key in ['last_hour', 'today', 'yesterday', 'last_3days']:
        stats[key] = json.loads(get_stats(key).data)
    pprint(stats)
    return render_template('dashboard.html', methods=['GET'], stats=stats)
