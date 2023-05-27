from flask import Flask, request
from flask_restful import Resource, Api
import requests
import os

# this is a great comment!
# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
app.app_context().push()

# For GET request to http://localhost:5000/

# https://sensors-1.onrender.com
endpoint_1 = os.environ.get("ENDPOINT_1")
# https://sensors-2.onrender.com
endpoint_2 = os.environ.get("ENDPOINT_2")

class GetSensor(Resource):
    def get(self):
        res_api_1 = requests.get(f'{endpoint_1}/health')
        res_api_2 = requests.get(f'{endpoint_2}/health')
        if res_api_1.status_code == 200:
            return requests.get(endpoint_1).json()
        elif res_api_2.status_code == 200:
            return requests.get(endpoint_2).json()
        else:
            return {"error": "Service Not Available"}, 503

# For Post request to http://localhost:5000/add


class AddSensor(Resource):
    def post(self):

        if request.is_json:
            res_api_1 = requests.get(f'{endpoint_1}/health')
            res_api_2 = requests.get(f'{endpoint_2}/health')
            if res_api_1.status_code == 200:
                res = requests.post(f'{endpoint_1}/add', json=request.json)
                return res.json()
            elif res_api_2.status_code == 200:
                res = requests.post(f'{endpoint_2}/add', json=request.json)
                return res.json()
            else:
                return {"error": "Service Not Available"}, 503
        else:
            return {'error': 'Request must be JSON'}, 400


# For put request to http://localhost:5000/update/?


class UpdateSensor(Resource):
    def put(self, id):
        if request.is_json:
            res_api_1 = requests.get(f'{endpoint_1}/health')
            res_api_2 = requests.get(f'{endpoint_2}/health')
            if res_api_1.status_code == 200:
                res = requests.put(f'{endpoint_1}/update/' + str(id), json=request.json)
                return res.json()
            elif res_api_2.status_code == 200:
                res = requests.put(f'{endpoint_2}/update/' + str(id), json=request.json)
                return res.json()
            else:
                return {"error": "Service Not Available"}, 503
        else:
            return {'error': 'Request must be JSON'}, 400

# For delete request to http://localhost:5000/delete/?


class DeleteSensor(Resource):
    def delete(self, id):
        res_api_1 = requests.get(f'{endpoint_1}/health')
        res_api_2 = requests.get(f'{endpoint_2}/health')
        if res_api_1.status_code == 200:
            res = requests.delete(f'{endpoint_1}/delete/' + str(id))
            return res.json()
        elif res_api_2.status_code == 200:
            res = requests.delete(f'{endpoint_2}/delete/' + str(id))
            return res.json()
        else:
            return {"error": "Service Not Available"}, 503


class GetHealth(Resource):
    def get(self):
        return {"status": 'UP'}, 200


api.add_resource(GetSensor, '/')
api.add_resource(AddSensor, '/add')
api.add_resource(UpdateSensor, '/update/<int:id>')
api.add_resource(DeleteSensor, '/delete/<int:id>')
api.add_resource(GetHealth, '/health')

if __name__ == '__main__':
    app.run(debug=True)
