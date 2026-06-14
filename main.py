import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description="Скрипт для генерации сайта с винами")
parser.add_argument(
    "--filepath", 
    default="wine.xlsx", 
    help="Путь к файлу Excel с данными о винах"
)
args = parser.parse_args()


def get_year_string(age):
    if age % 10 == 1 and age % 100 != 11:
        return "год"
    elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
        return "года"
    else:
        return "лет"


founded_year = 1920
current_year = datetime.datetime.now().year
age = current_year - founded_year
winery_age_text = f"{age} {get_year_string(age)}"

excel_data = pd.read_excel(args.filepath, keep_default_na=False)
excel_data.columns = excel_data.columns.str.strip()
wines = excel_data.to_dict(orient="records")

grouped_wines = defaultdict(list)
for wine in wines:
    category = wine.get("Категория", "Без категории")
    grouped_wines[category].append(wine)


feedbacks = [
    {
        "photo": "assets/person_1.jpg",
        "text": "Если бы вино Киндзмараули вдруг стало мужчиной, то это был бы средних лет (35-40 лет) аристократичный мужчина, в белой дорогой рубашке и брюках, хорошей обуви, статный, знающий чего он хочет, успешный, но имеющий в своей душе такие струны, с которыми может быть созвучна истинная женская трепетность и беззащитность. Он может быть незаметен, он не бросается в глаза, но от того, что он есть, все вокруг становится на свои места.",
        "author": "Марина Ли"
    },
    {
        "photo": "assets/person_2.jpg",
        "text": "Вино столовое полусладкое белое Кокур - неплохое вино, молодое, невыдержанное. Особенности технологии его производства и дают, очевидно, такой вкус. Вкус - довольно простой, несложный, но приятный. Невыдержанное вино в чем-то близко к молодому виноградному соку. Пьется легко, вкус приятно- округлый, нежный.",
        "author": "Михаил Яковлев"
    },
    {
        "photo": "assets/person_3.jpg",
        "text": "Вина Шардоне хорошо подходят к нейтральным по остроте мясным, рыбным блюдам, блюдам из птицы, сырам и фруктам (яблоко, апельсин и груша). Вино мне понравилось, голова на утро от него не болела. Рекомендую.",
        "author": "Андрей Власов"
    }
]


env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)
template = env.get_template("template.html")

rendered_page = template.render(wines=grouped_wines, winery_age=winery_age_text, feedbacks=feedbacks)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()