from flask import jsonify, Blueprint, url_for
from flask_restful import Resource, Api, reqparse, inputs, \
    fields, marshal, marshal_with, abort
import models

todo_fields = {'id': fields.Integer,
               'name': fields.String,
               'created_at': fields.DateTime,
               'completed': fields.Boolean
               }


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='Todo name is required',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        todo_list = [marshal(todo, todo_fields)
                     for todo in models.Todo.select()]
        return todo_list

    def post(self):
        args = self.reqparse.parse_args()
        models.Todo.create(**args)
        todo_list = [marshal(todo, todo_fields)
                     for todo in models.Todo.select()]
        return todo_list


def get_todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id==todo_id)
    except models.Todo.DoesNotExist:
        abort(404, message='Todo id {} does not exist'.format(todo_id))
    else:
        return todo


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='Todo name is required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            help='Todo completed is not required',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        return get_todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id==id)
        query.execute()
        return (get_todo_or_404(id),
                200,
                {'Location': url_for('resources.todos.todo', id=id)})

    @marshal_with(todo_fields)
    def delete(self, id):
        query = models.Todo.delete().where(models.Todo.id==id)
        query.execute()
        return ('',
                204)


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(TodoList,
                 '/api/v1/todos',
                 endpoint='todos'
                 )
api.add_resource(Todo,
                 '/api/v1/todos/<int:id>',
                 endpoint='todo'
                 )
