from types import NoneType
import bcrypt
from email_validator import validate_email, EmailNotValidError


class Validate_user():
  def register(body_data):
    first_name = body_data['first_name']
    last_name = body_data['last_name']
    email = body_data['email']
    password = body_data['password']
    verify_password = body_data['verify_password']

    try:
      verify_email = validate_email(email)
      print('verifying Email', verify_email)
      verified_Email = verify_email['email']
      print('validated Email::',verified_Email)
      if len(first_name) < 2 or len(last_name) < 2 :
        return {'success': False, 'error_info':'NAME REQUIREMENT ERROR'}
      if password == verify_password or len(password) > 7:
        password_to_bytes = password.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed_password = bcrypt.hashpw(password_to_bytes, salt)

        return {'success': True, 'result':{'first_name': first_name, 'last_name': last_name, 'email': email, 'password': hashed_password}}
      else:
        return {'success': False, 'error_info':'Password validation failed'}
    except EmailNotValidError as err:
      return {'success': False, 'error_info': str(err)}


  def login(body_data):
    email = body_data['email']
    password = body_data['password']

    if type(password) == NoneType or len(password) < 7:
      return {'success': False, 'error_info': 'PASSWORD REQUIREMENT ERROR'}
      
    try:
      verify_email = validate_email(email)
      print('verifying Email', verify_email)
      verified_Email = verify_email['email']
      return {'success': True, 'result': {'email': verified_Email, 'password': password}}
    except EmailNotValidError as err:
      return {'success': False, 'error_info': str(err)}
