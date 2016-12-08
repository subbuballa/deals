from flask import Flask, url_for
import scrape

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'welcome'


@app.route('/deals')
def deals_daily():
    return scrape.get_json_data()


@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

if __name__ == '__main__':
    app.run()
