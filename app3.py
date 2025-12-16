from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

todos = { 
         1: {"Task": "Wake up", "Summary":"To be fresh"},
         2: {"Task": "Do Yoga", "Summary":"To be fit"},
         3: {"Task": "Read book", "Summary":"To enjoy peace"}
        }

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("Task", type=str, help="Task is required", required=True)
task_post_args.add_argument("Summary", type=str, help="Summary is required", required=True)

class ToDo(Resource):
   def get(self,todo_id):
      return todos[todo_id]
   
   def post(self,todo_id):
      args = task_post_args.parse_args()
      if todo_id in todos:
         abort(409, "Task is already taken")
      todos[todo_id] = {"Task": args["Task"],"Summary":args["Summary"]}
      return todos[todo_id]

class ToDoList(Resource):
   def get(self):
      return todos

api.add_resource(ToDo,'/todos/<int:todo_id>')
api.add_resource(ToDoList,'/todos')

if __name__ == '__main__':
   app.run(port=5000,debug=True)