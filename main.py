import requests
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import csv
from dotenv import dotenv_values


config = dotenv_values()


base_url = 'https://www.kogan.com'

api_key = config.get('API_KEY')

session = requests.Session()

CSV_file_name = 'Sample'


def get_html(base_url: str):
    response = session.get(
    url='https://proxy.scrapeops.io/v1/',
    
    params={
        'api_key': api_key,
        'url': base_url, 
    },
    )

    content = HTMLParser(response.text)
    return content


def parse_attribute_error(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


def export_to_csv(products: list):
    field_names = ['Name', 'Image_link', 'Product_link', 'Price', 'Sales']
    with open(f'{CSV_file_name}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(products)

        
def parse_product_info(html):
    products = html.css('div._3dbuB._2TkM7._1tVxb.tVqMg')

    for product in products:
        name = parse_attribute_error(product, 'h2._1A_Xq')
        image = product.css_first('img._1Xm_H').attributes['src']
        product_link = urljoin(base_url, product.css_first('a._3w8sH').attributes['href'])
        price = parse_attribute_error(product, 'div._2AQgf').replace('$', '')
        sales = parse_attribute_error(product, 'span.palette-pill-text')

        product_details = {
            'Name': name,
            'Image_link': image,
            'Product_link': product_link,
            'Price': price,
            'Sales': sales
        }

        yield product_details


def main():
    all_products = []
    for x in range(1, 20):
        kogan_url = f'https://www.kogan.com/au/shop/category/mens-accessories-hats-38030/?page={x}'

        html_content = get_html(kogan_url)
        print(f'Getting info from page {x}...')

        product_info = parse_product_info(html_content)

        for product in product_info:
            all_products.append(product)

    export_to_csv(all_products)
    print('All done!')


if __name__ == '__main__':
    main()