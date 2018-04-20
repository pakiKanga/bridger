from bridger import db

# Creating a model for applications
class User(db.Model):
    user_id = db.Column(db.String(13), primary_key=True, default=None)
    username = db.Column(db.String(80))


    def __init__(self, unique_id, curr_date):
        self.session_id = unique_id
        self.no_users = 0
        self.date_submitted = curr_date
    def __str__(self):
        return self.session_id

    def __repr__(self):
        return '<Application %r>' % self.session_id
    


        
        
 