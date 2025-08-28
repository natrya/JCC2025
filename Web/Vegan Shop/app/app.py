from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = '{REDACTED}'

vegetables = {
    'tomat': {'name': 'Tomat Segar', 'price': 15000, 'stock': 50, 'description': 'Tomat merah segar dari kebun lokal', 'image': 'tomat.jpg'},
    'wortel': {'name': 'Wortel Organik', 'price': 12000, 'stock': 30, 'description': 'Wortel organik kaya vitamin A', 'image': 'wortel.jpg'},
    'bayam': {'name': 'Bayam Hijau', 'price': 8000, 'stock': 25, 'description': 'Bayam segar penuh zat besi', 'image': 'bayam.jpg'},
    'kangkung': {'name': 'Kangkung Air', 'price': 6000, 'stock': 40, 'description': 'Kangkung air segar untuk tumisan', 'image': 'kangkung.jpg'},
    'brokoli': {'name': 'Brokoli Premium', 'price': 20000, 'stock': 15, 'description': 'Brokoli premium kaya nutrisi', 'image': 'brokoli.jpg'}
}

def security_filter(user_input):
    blacklist = ["%", "\\", "/", "\"", "'", "`", "|", " ", "[", "]", "+", "init", "subprocess", "globlas", "config", "update", "mro", "subclasses", "class", "base", "builtins", "cycler", "joiner", "namespace", "lipsum", "subprocess"]
    
    for word in blacklist:
        if word in user_input:
            return False
    return True

def get_cart():
    """Get cart from session"""
    return session.get('cart', [])

def add_to_cart_session(item):
    """Add item to cart in session"""
    cart = get_cart()
    cart.append(item)
    session['cart'] = cart
    session.permanent = True

@app.route('/')
def home():
    cart = get_cart()
    return render_template('index.html', vegetables=vegetables, cart=cart)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()
    
    if not query:
        flash('Mohon masukkan kata kunci pencarian!', 'error')
        return redirect(url_for('home'))
    
    if not security_filter(query):
        return render_template('blocked.html', query=query)
    
    found_vegetables = {}
    for key, veggie in vegetables.items():
        if query.lower() in key or query.lower() in veggie['name'].lower():
            found_vegetables[key] = veggie
    
    if found_vegetables:
        template_msg = f"Hasil pencarian untuk '{query}': {len(found_vegetables)} sayuran ditemukan!"
    else:
        template_msg = f"Maaf, tidak ada sayuran yang cocok dengan '{query}'. Coba kata kunci lain!"
    
    search_template = '''
    <div class="result-info">
        <h3>''' + template_msg + '''</h3>
        <a href="{{ url_for('home') }}" class="btn btn-secondary">← Kembali ke Beranda</a>
    </div>
    '''

    template_content = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hasil Pencarian - Pasar Sayur Segar</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="{{ url_for('home') }}" class="logo">🥬 Pasar Sayur Segar</a>
            <div class="nav-links">
                <a href="{{ url_for('home') }}">Beranda</a>
                <a href="{{ url_for('view_cart') }}">🛒 Keranjang</a>
                <a href="{{ url_for('admin') }}">👤 Admin</a>
            </div>
        </div>
    </nav>

    <main class="main-content">
        <div class="container">
            <div class="search-header">
                <h1>🔍 Hasil Pencarian</h1>
            </div>
            
            <div class="result-info">
                ''' + render_template_string(search_template) + '''
            </div>
            
            {% if found_vegetables %}
            <div class="vegetables-grid">
                {% for key, veggie in found_vegetables.items() %}
                <div class="veggie-card">
                    <div class="veggie-image">🥕</div>
                    <h3>{{ veggie.name }}</h3>
                    <p class="veggie-description">{{ veggie.description }}</p>
                    <div class="price">Rp {{ "{:,}".format(veggie.price) }} / kg</div>
                    <div class="stock">Stok: {{ veggie.stock }} kg</div>
                    <a href="{{ url_for('add_to_cart', veggie_key=key) }}" class="btn btn-primary">Tambah ke Keranjang</a>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Pasar Sayur Segar. Sayuran segar langsung dari kebun ke meja Anda!</p>
        </div>
    </footer>
</body>
</html>'''
    
    return render_template_string(template_content, 
                                found_vegetables=found_vegetables,
                                query=query)

@app.route('/add_to_cart/<veggie_key>')
def add_to_cart(veggie_key):
    if veggie_key in vegetables:
        item = {
            'key': veggie_key,
            'name': vegetables[veggie_key]['name'],
            'price': vegetables[veggie_key]['price']
        }
        add_to_cart_session(item)
        flash(f"{vegetables[veggie_key]['name']} berhasil ditambahkan ke keranjang!", 'success')
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    cart = get_cart()
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    flash('Keranjang berhasil dikosongkan!', 'info')
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4001)
