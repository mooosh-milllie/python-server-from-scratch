from email import message
from operator import eq
import os
import json
import bcrypt
from utils.db import Users
from http.server import BaseHTTPRequestHandler

from routes.main import routes
from utils.validate_inputs import Validate_user
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        print(os.path.splitext(self.path))
        request_extension = split_path[1]

        if request_extension == "" or request_extension == ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        elif request_extension == ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(self.path)
 
        self.respond({
            'handler': handler
        })
    def do_POST(self):
        self.sort_post()
        print('e reach here')

    def sort_post(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        body_data = json.loads(post_body)
        if self.path == '/register':
            validate_register = Validate_user.register(body_data)
            print(validate_register)
            if validate_register['success'] == True:
                validation_result = validate_register['result']
                register_user = Users.insert_user(validation_result)
                print(register_user)
                if register_user == True:
                    return self.handle_request_response({"message": "REGISTERATION SUCCESSFUL"}, 200, 'OK')
                
                return self.handle_request_response(validation_result, 400, 'Bad Request')
                
            else:
                return self.handle_request_response(validate_register, 400, 'Bad Request')

        if self.path == '/login':
            validate_login = Validate_user.login(body_data)
            if validate_login['success'] == True:
                validated_login = validate_login['result']
                get_user = Users.get_user(body_data['email'])

                print('GET USER', get_user)
                if get_user == None:
                    json_response = {"success": False, "message": "INVALID LOGIN CREDENTIALS"}
                    return self.handle_request_response(json_response, 401, 'Unauthorized')
                
                # If user is found encode client password to bytes, then compare with db password
                password_to_bytes = validated_login['password'].encode('utf-8')
                retrieved_password = get_user[4]    
                compare_passwords = bcrypt.checkpw(password_to_bytes, retrieved_password)

                if compare_passwords:
                    response_json = {"success": True, "data": {"token": "wjdjfncidmd.dididhcd,d,.djdd", "message": "LOGIN SUCESSFUL", 'name': get_user[1]}}
                    return self.handle_request_response(response_json, 200, 'OK')
                else:
                    json_response = {"success": False, "message": "INVALID LOGIN CREDENTIALS"}
                    return self.handle_request_response(json_response, 401, 'Unauthorized')

            return self.handle_request_response( validate_login, 400, 'Bad Request')



    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code == 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')

    def handle_request_response(self, json_response, response_code, server_response_message):
        response_json = json_response
        dump_response = json.dumps(response_json)
        self.send_response(response_code, message=server_response_message)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        return self.wfile.write(dump_response.encode("utf-8"))
    
    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
