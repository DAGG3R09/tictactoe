from dao.session import get_session
from dao.user import get_user_by_id


def authenticate_user(token):
    
    if not token:
        return False

    session = get_session(token)
    if session:
        return True
    else:
        return False