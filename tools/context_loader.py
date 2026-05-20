import json

def load_company_context():
    with open("company_context.json","r") as file:
        data = json.load(file)

    return data