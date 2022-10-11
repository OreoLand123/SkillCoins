import json
from pydoc import describe

from flask import request

from . import create_app, database
from .models import Cats

app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    cats = database.get_all(Cats)
    all_cats = []
    for cat in cats:
        new_cat = {
            "id": cat.id,
            "name": cat.name,
            "age": cat.age,
            "breed": cat.breed,
            "describe": cat.describe,
            "img_url": cat.img_url
        }

        all_cats.append(new_cat)
    return json.dumps(all_cats), 200


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    name = data['name']
    age = data['age']
    breed = data['breed']
    describe = data['describe']
    img_url = data['img_url']

    database.add_instance(Cats, name=name, age=age, breed=breed, describe=describe, img_url=img_url)
    return json.dumps("Added"), 200


@app.route('/remove/<id>', methods=['DELETE'])
def remove(id):
    database.delete_instance(Cats, id=id)
    return json.dumps("Deleted"), 200


@app.route('/edit/<id>', methods=['PATCH'])
def edit(id):
    data = request.get_json()
    new_price = data['price']
    database.edit_instance(Cats, id=id, price=new_price)
    return json.dumps("Edited"), 200
