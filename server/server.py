import json

from flask import Flask, request, render_template
from flask.ext.cache import Cache

app = Flask(__name__,
            static_folder='../static/dist',
            template_folder='../static')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


raw_stats = {
        "errors_last_3days": [
            {
                "count": 2,
                "code": 502
            },
            {
                "count": 720,
                "code": 599
            },
            {
                "count": 1780,
                "code": None
            }
        ],
        "errors_yesterday": [
            {
                "count": 615,
                "code": None
            },
            {
                "count": 305,
                "code": 599
            }
        ],
        "errors_last_hour": [],
        "data": [
            {
                "bookings_current_last_3days": 7556,
                "timeout_yesterday": 0.217542189065684,
                "zeroes_yesterday": 5.03052033295241,
                "avg_price_yesterday": 9447.87135852322,
                "clicks_current_last_hour": 428,
                "avg_price_last_hour": 10243.0263157895,
                "zeroes_last_hour": None,
                "mobile_pessimizer": 0.000999999974737875,
                "bookings_current_last_hour": 32,
                "searches_current_last_3days": 4445192,
                "bookings_previous_last_hour": 98,
                "str_yesterday": 14.9289099526066,
                "errors_yesterday": 0.376232384954177,
                "ctr_last_hour": 0.640574721245229,
                "gate_id": 20,
                "ctr_yesterday": 1.06052388326287,
                "searches_current_yesterday": 2188541,
                "bookings_previous_last_3days": 8647,
                "zeroes_last_3days": 5.55262854787825,
                "clicks_previous_last_hour": 784,
                "timeout_last_3days": 0.122851836321131,
                "errors_last_3days": 0.143953287057117,
                "bookings_previous_yesterday": 3641,
                "searches_previous_yesterday": 2050500,
                "searches_previous_last_hour": 88385,
                "str_last_hour": None,
                "clicks_previous_yesterday": 23364,
                "avg_price_last_3days": 10694.8964067661,
                "searches_current_last_hour": 66815,
                "web_pessimizer": 100.0,
                "ctr_last_3days": 1.12946752356254,
                "clicks_previous_last_3days": 60505,
                "str_last_3days": 15.0496942657398,
                "timeout_last_hour": None,
                "clicks_current_last_3days": 50207,
                "bookings_current_yesterday": 3465,
                "searches_previous_last_3days": 6118984,
                "errors_last_hour": None,
                "clicks_current_yesterday": 23210
            }
        ]
    }


@cache.cached(timeout=600)
def get_stats():
    """A helper function that computes the values required on the client side based on raw stats
    The values are calculated for four possible choices: ['last_hour', 'today', 'yesterday', 'last_3days']
    It is cached in our case, because the statistics does not change
    :param keyword - str - one of ['last_hour', 'today', 'yesterday', 'last_3days']
    :return dict()
    лучше, если она вернет словарик, для каждого дня, а функкия? вызываемся с фронта будет передавать key word,
    и забирать значение
    """

    data = raw_stats.get('data')[0]
    res = dict()
    for keyword in ['last_hour', 'today', 'yesterday', 'last_3days']:
        tmp = dict(
            top_statistics={x: dict(
                name=x.capitalize(),
                average=round(data.get(f'{x}_last_3days', 0) / 3, 2),
                value=round(data.get(f'{x}_{keyword}', 0), 2) if data.get(f'{x}_{keyword}') else 0
                                   ) for x in ['timeout', 'errors', 'zeroes']},
            top_errors=get_errors(keyword))
        content = dict(
            searches=dict(
                # mobile traffic
                param1=round(data.get("mobile_pessimizer", 0), 2) if data.get("mobile_pessimizer") else 0,
                # web traffic
                param2=round(data.get("web_pessimizer", 0), 2) if data.get("mobile_pessimizer") else 0,
            ),
            clicks=dict(
                # ctr
                param1=round(data.get(f"ctr_{keyword}", 0), 2) if data.get(f"ctr_{keyword}") else 0,
                param2=None
            ),
            bookings=dict(
                # str
                param1=round(data.get(f"str_{keyword}", 0), 2) if data.get(f"str_{keyword}") else 0,
                # avg_check
                param2=round(data.get(f"avg_price_{keyword}", 0), 2) if data.get(f"avg_price_{keyword}") else 0
            )
        )
        for key in ['searches', 'clicks', 'bookings']:
            content[key]['current'] = round(data.get(f'{key}_current_{keyword}', 0), 2)
            content[key]['previous'] = round(data.get(f'{key}_previous_{keyword}', 0), 2)
            # добавить процент изменений по Searches, Clicks, Bookings
            diff = round((content[key]['current'] - content[key]['previous']) / content[key]['previous'], 2) \
                if content[key]['previous'] != 0 else 0
            content[key]['diff'] = f'+{diff}' if diff > 0 else diff
        tmp['content'] = content
        res[keyword] = tmp

    return res


def get_errors(keyword):
    """ A helper function to process errors
    :param keyword - str - one of ['last_hour', 'today', 'yesterday', 'last_3days']
    :return dict list
    """
    errors = []
    for el in raw_stats:
        if el.endswith(f'_{keyword}'):

            total_count = 0
            for key in raw_stats[el]:
                tmp = dict()
                tmp['code'] = 'Other' if key['code'] is None else f'Error {key["code"]:}'
                tmp['count'] = key['count']
                errors.append(tmp)
                total_count = total_count + key['count']

        i = 0
        for error in errors:
            if i > 3:
                i = 0
            error['width'] = f'{int((error["count"] / total_count) * 100)}%'
            i = i + 1

    return errors


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data")
def get_data():
    """Return a random book out of the list"""
    keyword = request.args.get('keyword')
    res = get_stats().get(keyword)

    return json.dumps(res)


if __name__ == "__main__":
    app.run()
