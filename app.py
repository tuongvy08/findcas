from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import sqlite3
import os
import json
from middleware_access import register_ip_access_control  # IP + phân quyền

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Kích hoạt kiểm soát IP & quyền truy cập
register_ip_access_control(app, base_path='/home/deploy/myapps')

# Đường dẫn database
DB_PATH = '/home/deploy/myapps/shared_data/products.db'

# Hàm tìm kiếm sản phẩm dựa trên CAS
def query_products_by_cas(cas_list):
    results = []
    with sqlite3.connect(DB_PATH) as conn:
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

# Đăng nhập phân quyền
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'Truong@2004':
            session['authenticated'] = True
            session['role'] = 'manager'
            return redirect(url_for('home'))
        elif password == 'Truong@123':
            session['authenticated'] = True
            session['role'] = 'staff'
            return redirect(url_for('home'))
        else:
            return "Sai mật khẩu!", 403
    return render_template('login.html')

@app.route('/search', methods=['POST'])
def search():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    data = request.json
    cas_list = data.get('cas', [])
    if not isinstance(cas_list, list) or len(cas_list) > 500:
        return jsonify({"error": "Invalid input"}), 400

    results = query_products_by_cas(cas_list)
    return jsonify({"results": results})

@app.route('/')
def home():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
