import unittest
from urllib import request
import json
from app import app
from models import Todo, User
from peewee import SqliteDatabase


MODELS = [Todo, User]
test_db = SqliteDatabase(':memory:')


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def testGetTodos(self):
        response = self.app.get('/api/v1/todos')
        self.assertEqual(response.status, '200 OK')
    
    def testPostPutDelete(self):
        payload = {"name": "clean the horse"}

        response = self.app.post('/api/v1/todos',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        self.assertEqual(response.status, '200 OK')
        self.assertIn('clean the horse', response.data.decode('utf-8'))
        
        returned_json_data = json.loads(response.data)
        for todo in returned_json_data:
            if todo['name'] == 'clean the horse':
                test_todo_id = todo['id']

        payload = {"id": test_todo_id, 
                   "name": "clean the norse", 
                   "completed": "false"}

        response = self.app.put('/api/v1/todos/{}'.format(test_todo_id),
                                data=json.dumps(payload),
                                content_type='application/json')

        self.assertEqual(response.status, '200 OK')
        self.assertIn('clean the norse', response.data.decode('utf-8'))

        response = self.app.delete('/api/v1/todos/{}'.format(test_todo_id),
                                   data=None,
                                   content_type='application/json')
        
        self.assertEqual(response.status, '204 NO CONTENT')
        self.assertEqual(b'', response.data)
        
        response = self.app.get('/api/v1/todos')
        self.assertNotIn('clean the norse', response.data.decode('utf-8'))


class TestViews(unittest.TestCase):

    def testGetTodos(self):
        get_data = request.urlopen('http://127.0.0.1:8000/api/v1/todos')
        self.assertEqual(get_data.status, 200)
        self.assertNotEqual(get_data.length, 0)

    def testPostPutDelete(self):
        test_todo_id = 0
        url = 'http://127.0.0.1:8000/api/v1/todos'
        payload = {"name": "clean the horse"}
        headers = {'content-type': 'application/json'}

        test_post = request.Request(url,
                                    data=json.dumps(payload).encode('utf-8'),
                                    headers=headers)
        test_post_response = request.urlopen(test_post)

        self.assertEqual(test_post_response.status, 200)

        returned_data = test_post_response.read()
        self.assertIn('clean the horse', returned_data.decode('utf-8'))

        returned_json_data = json.loads(returned_data)
        for todo in returned_json_data:
            if todo['name'] == 'clean the horse':
                test_todo_id = todo['id']

        ### Test PUT ###

        url = 'http://127.0.0.1:8000/api/v1/todos/{}'.format(
            str(test_todo_id))

        payload = {"id": test_todo_id,
                   "name": "walk the frog",
                   "completed": "false"}

        test_put = request.Request(url,
                                   data=json.dumps(payload).encode('utf-8'),
                                   headers=headers,
                                   method='PUT')
        test_put_response = request.urlopen(test_put)

        self.assertEqual(test_put_response.status, 200)

        returned_data = test_put_response.read()

        self.assertIn('walk the frog', returned_data.decode('utf-8'))

        ### Test DELETE ###

        test_delete = request.Request(url,
                                      headers=headers,
                                      method='DELETE')

        test_delete_response = request.urlopen(test_delete)

        returned_data = test_delete_response.read()

        self.assertEqual(test_delete_response.status, 204)
        self.assertEqual(returned_data, b'')


class TestModels(unittest.TestCase):

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)
    
    def testNewTodo(self):
        test_todo = Todo.create(name='Eat a hotdog')        
        self.assertEqual(1, test_todo.id)

        test_todos = Todo.select()
        self.assertEqual(test_todos.__len__(), 1)
    
    def testUpdateTodo(self):
        test_todo = Todo.create(name='Eat a hotdog')        
        test_todo.name = 'Hotdog Eats You'
        
        self.assertEqual('Hotdog Eats You', test_todo.name)
        
    def testDeleteTodo(self):
        test_todo = Todo.create(name='Eat a hotdog') 

        delete_todo = Todo.delete().where(Todo.id==1)
        delete_todo.execute()
        
        self.assertEqual(0, Todo.select().__len__())

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()


if __name__ == '__main__':
    unittest.main()
