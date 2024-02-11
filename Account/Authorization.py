from json.decoder import JSONDecodeError
import secrets, string, json

def KeyAuthorization():
    string_length = secrets.randbelow(50) + 50
    random_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(string_length))
    return random_string

def loadAuthorization():
    try:
        with open('credentials/Authorization.json', 'r') as file:
            data = json.load(file)
            return data.get('Authorization', None)
    except FileNotFoundError:
        return None, None
    except JSONDecodeError:
        return None, None
    
def SaveAuthorization(Authorization):
    data = {'Authorization':Authorization}
    with open('credentials/Authorization.json', 'w') as file:
        json.dump(data, file)
    return Authorization  

def ChangeAuthorization(AuthorizationNew):
    AuthorizationBef = loadAuthorization()
    if AuthorizationBef != "":
        SaveAuthorization(AuthorizationNew)
        return True
    else:
        return False
