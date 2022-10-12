import json
from pydoc import describe

from flask import request

from . import create_app, database
from .models import Accounts, Logs, Reasons, db

app = create_app()


@app.route('/<table>', methods=['GET'])
def fetch(table):
    all_data = []
    
    if table == "log":
        data = database.get_all(Logs)
        for log in data:
            new_log = {
                "id": log.id,
                "acc_id": log.acc_id,
                "amount": log.amount,
                "reason": log.reason_id
            }
            all_data.append(new_log)

    elif table == "account":
        data = database.get_all(Accounts)
        for acc in data:
            new_acc = {
                "id": acc.id,
                "name": acc.name,
                "age": acc.age,
                "value": acc.value,
                "start_date": acc.start_date,
                "end_date": acc.end_date
            }
            all_data.append(new_acc)

    elif table == "reason":
        data = database.get_all(Reasons)
        all_reasons = []
        for reason in data:
            new_reason = {
                "id": reason.id,
                "reason": reason.reason
            }
            all_data.append(new_reason)
    
    else:
        return 404
        
    return json.dumps(all_data, default=str), 200


@app.route('/add/<table>', methods=['POST'])
def add(table):
    data = request.json
    if table == "log":
        if Accounts.query.filter_by(id=data["acc_id"]).first() is None or Reasons.query.filter_by(id=data["reason_id"]).first() is None:
            return "No reason / account with this id", 404
        acc_id = data['acc_id']
        amount = data['amount']
        reason_id = data['reason_id']

        database.add_instance(Logs, acc_id=acc_id, amount=amount, reason_id=reason_id)

    elif table == "account":
        name = data['name']
        age = data['age']
        value = 0
        start_date = data['start_date']
        end_date = data['end_date']

        database.add_instance(Accounts, name=name, age=age, value=value, start_date=start_date, end_date=end_date)
    
    elif table == "reason":
        reason = data['reason']

        database.add_instance(Reasons, reason=reason)

    else:
        return 404

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
