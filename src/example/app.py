import json
from pydoc import describe

from flask import request

from . import create_app, database
from .models import Accounts, Logs

app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    accs = database.get_all(Accounts)
    all_accs = []
    for acc in accs:
        new_acc = {
            "id": acc.id,
            "name": acc.name,
            "age": acc.age,
            "value": acc.value,
            "start_date": acc.start_date,
            "end_date": acc.end_date
        }

        all_accs.append(new_acc)
    return json.dumps(all_accs), 200


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    acc_id = data['acc_id']
    amount = data['amount']
    reason = data['reason']

    database.add_instance(Logs, acc_id=acc_id, amount=amount, reason=reason)
    return json.dumps("Added"), 200


# @app.route('/remove/<id>', methods=['DELETE'])
# def remove(id):
#     database.delete_instance(Cats, id=id)
#     return json.dumps("Deleted"), 200


# @app.route('/edit/<id>', methods=['PATCH'])
# def edit(id):
#     data = request.get_json()
#     new_price = data['price']
#     database.edit_instance(Cats, id=id, price=new_price)
#     return json.dumps("Edited"), 200
