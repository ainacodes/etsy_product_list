from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from scraper import scrape_etsy

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_url = request.form['searchTerm']
        filepath = scrape_etsy(input_url)

        col = ['name of item', 'price (RM)', 'number of downloads', 'item URL']
        product_data = pd.read_csv(filepath, names=col, skiprows=1)

        return render_template('index.html', table=product_data.to_html(), filename=filepath)

    return render_template('index.html', table=None, filename=None)


@app.route('/download_csv/<filename>')
def download_csv(filename):
    filepath = f'./results/{filename}'
    return redirect(url_for('static', filename=f'results/{filename}'))


if __name__ == '__main__':
    app.run(debug=True)
