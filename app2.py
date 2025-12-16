from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = { 
        1: {"Task": "Wake up", "Summary":"To be fresh"},
        2: {"Task": "Do Yoga", "Summary":"To be healthy"},
        3: {"Task": "Read book", "Summary":"To enjoy peace"}
        }

class ToDo(Resource):
   def get(self,todo_id):
      return todos[todo_id]

class ToDoList(Resource):
   def get(self):
      return todos

api.add_resource(ToDo,'/todos/<int:todo_id>')

if __name__ == '__main__':
   app.run(port=5000,debug=True)