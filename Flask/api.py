from flask import Flask,jsonify, request

app = Flask(__name__)

items = [
    {'id': 1, 'name': 'Item 1', 'price':10.99},
    {'id': 2, 'name': 'Item 2', 'price':20.99},
    {'id': 3, 'name': 'Item 3', 'price':30.99}
]

@app.route('/')
def home():
    return "Welcome to The Home Page"
#retrive the data
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)
#Retrive Specific Item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):  
    item=next((item for item in items if item['id'] == item_id), None)
    return jsonify(item)
#Post the data
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        'id': len(items) + 1,
        'name': data['name'],
        'price': data['price']
    }
    items.append(new_item)
    return jsonify(new_item), 201



if __name__ == '__main__':
    app.run(debug=True)