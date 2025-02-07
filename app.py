from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Hàm tìm kiếm sản phẩm dựa trên CAS
def query_products_by_cas(cas_list):
    results = []
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(cas_list))
        query = f"""
            SELECT Name, Code, CAS, Brand, Size, Ship, Price, Note
            FROM products
            WHERE CAS IN ({placeholders}) AND Brand IN ('Phụ lục I', 'Phụ lục II', 'CẤM NHẬP')
        """
        cursor.execute(query, cas_list)
        rows = cursor.fetchall()

    for row in rows:
        Name, Code, CAS, Brand, Size, Ship, Price, Note = row
        results.append({
            "Name": Name,
            "Code": Code,
            "CAS": CAS,
            "Brand": Brand,
            "Size": Size,
            "Ship": Ship,
            "Price": Price,
            "Note": Note,
        })
    return results

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    cas_list = data.get('cas', [])
    if not isinstance(cas_list, list) or len(cas_list) > 500:
        return jsonify({"error": "Invalid input"}), 400

    results = query_products_by_cas(cas_list)
    return jsonify({"results": results})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
