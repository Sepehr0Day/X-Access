import getpass
def GETuser():
    try:
        username = getpass.getuser()
        return {'username': username}
    except Exception as e:
        print(f"Error getting username: {str(e)}")
        return {'username': 'unknown'}