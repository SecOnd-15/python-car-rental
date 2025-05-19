

class Session():
    session_id = None
    session_name = None
    session_email = None
    session_role = None

    @staticmethod
    def NewSession(id, name, email, role):
        Session.session_id = id
        Session.session_name = name
        Session.session_email = email
        Session.session_role = role
        print("ADDED")

  

    @staticmethod
    def ClearSession():
        Session.session_id = None
        Session.session_name = None
        Session.session_email = None
        Session.session_role = None
