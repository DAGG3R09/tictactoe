from dao.session import get_session


def authenticate_user(token):
    
    if not token:
        return False

    session = get_session(token)
    if session:
        return True
    else:
        return False