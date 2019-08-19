import json
from user import User

class Users:
    def __init__(self, filepath):
        self.filepath = filepath
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.filepath,'r') as f:
                users = json.load(f)
                result = []
                for user in users:
                    lUser = User(user['id'],user['name'],user['wow_name'],user['dkp'])
                    result.append(lUser)
                return result
        except(IOError,IndexError):
            print('Failed to load user data.')

    def save_users(self):
        with open(self.filepath,'w') as f:
            nusers = []
            for user in self.users:
                user_dict = user.__dict__
                nusers.append(user_dict)
            json.dump(nusers,f)

    def add_user(self,id,name,wow_name,dkp=50):
        new_user = User(id,name,wow_name,dkp)
        self.users.append(new_user)
        self.save_users()
        return self

    
    def find_user(self,authorid):
        '''
        Takes ctx.author.id as a string as input, wraps it in mention syntax to check against database
        And returns the user if the user was found, false otherwise.
        '''
        if str(authorid)[:2] == '<@':
            authorid = str(authorid)[2:-1]
        found = False
        for user in self.users:
            if user.id == ('<@'+str(authorid)+'>'):
                found = True
                break
        if found:
            return user
        else:
            return False
            