from flask import Flask, request, jsonify
from selectorlib import Extractor
import requests
import json
from time import sleep
from nltk.metrics import jaccard_distance


def jaccard_similarity(str1, str2):
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    similarity = 1 - jaccard_distance(set1, set2)
    return similarity

def result(title):
    data = requests.get("https://script.google.com/macros/s/AKfycbyfy36EPPINEXetgDGdIIA-HqHexrHlBg1ZPwmhssRVWst_ki-cT1wVouHCdv02q0pX/exec")
    if data.status_code == 200:
       product_list = json.loads(data.text)      
    max_similarity = 0
    best_match = None
    url = None
    amazonTitle = title
    for product in product_list:
        csv_product = product["Product"]
        csv_url = product["Link"]
        similarity = jaccard_similarity(amazonTitle, csv_product)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = csv_product
            url = csv_url

    result_dict = {
        "name": best_match,
        "url": url
    }
    json_result = json.dumps(result_dict)
    print("Amazon Title:", amazonTitle)
    print(f"Product with Highest Jaccard Similarity: {json_result} ")
    return json_result

app = Flask(__name__)

@app.route('/api/scrape', methods=['POST'])
def scrape_and_compare():
    try:
        Name = str(request.get_data())
        result_data = result(Name)
        return (result_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port = 5081)
