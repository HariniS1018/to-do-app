from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey

app = Flask(__name__)
api = Api(app)
DB_URL = "postgresql://postgres:postgreSQL@localhost:5432/praticedb"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.app_context().push()

db = SQLAlchemy(app)

class TodoModel(db.Model):
    id = Column(Integer, primary_key=True)
    Task = Column(String(200))
    Summary = Column(String(500))

# db.create_all()



task_post_args = reqparse.RequestParser()
task_post_args.add_argument("Task", type=str, help="Task is required", required=True)
task_post_args.add_argument("Summary", type=str, help="Summary is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("Task", type=str)
task_put_args.add_argument("Summary", type=str)

resource_fields= {
   'id': fields.Integer,
   'Task': fields.String,
   'Summary': fields.String
}

class ToDoList(Resource):
   def get(self):
    tasks = TodoModel.query.all()
    todos = {}
    for task in tasks:
        todos[task.id] = {"Task": task.Task, "Summary": task.Summary}
    return todos

class ToDo(Resource):
   @marshal_with(resource_fields)
   def get(self,todo_id):
    task = TodoModel.query.filter_by(id=todo_id).first()
    if not task:
        abort(404, message="Could not find such task")
    return task
   
   @marshal_with(resource_fields)
   def post(self,todo_id):
      args = task_post_args.parse_args()
      task = TodoModel.query.filter_by(id=todo_id).first()
      if task:
         abort(409, message="Task already exsits")
      todo = TodoModel(id=todo_id,Task = args["Task"],Summary = args["Summary"])
      db.session.add(todo)
      db.session.commit()
      return todo, 201
   
   @marshal_with(resource_fields)
   def put(self,todo_id):
      args = task_put_args.parse_args()
      task = TodoModel(id=todo_id,Task = args["Task"],Summary = args["Summary"])
      if not task:
         abort(404, message = "Task doesn't exist, cannot update")
      if args["Task"]:
         task.Task = args["Task"]
      if args["Summary"]:
         task.Summary = args["Summary"]
      return task
   
   def delete(self, todo_id):
      args = task_put_args.parse_args()
      task = TodoModel(id=todo_id,Task = args["Task"],Summary = args["Summary"])
      db.session.delete(task)
      return 'Todo Deleted', 204

api.add_resource(ToDo,'/todos/<int:todo_id>')
api.add_resource(ToDoList,'/todos')

if __name__ == '__main__':
   app.run(port=5000,debug=True)