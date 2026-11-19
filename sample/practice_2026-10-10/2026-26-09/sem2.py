import json
from flask import Flask, render_template
from database.select import select_dict
from database.sql_provider import SQLProvider
from os import path

app = Flask(__name__)
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


with open('../data/db_config.json', 'r') as f:
    app.config["db_config"] = json.load(f)


@app.route('/')
def main():
    prod_param = {
        "prod_category": 2
    }
    q = provider.get('product.sql')
    result = select_dict(q, prod_param)

    print(str(result))

    return render_template('dynamic.html', prod_title = 'Продукты' , product=result)

if __name__ == '__main__':
    app.run(debug=True)