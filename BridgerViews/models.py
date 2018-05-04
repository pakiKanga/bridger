from bridger import db

# Creating a model for applications
class UserSession(db.Model):
    session_id = db.Column(db.String(13), primary_key=True, default=None)
    date_created = db.Column(db.DateTime)
    no_users = db.Column(db.Integer)


    def __init__(self, unique_id, curr_date):
        self.session_id = unique_id
        self.no_users = 0
        self.date_submitted = curr_date
    def __str__(self):
        return self.session_id

    def __repr__(self):
        return '<Application %r>' % self.session_id
    


        
        
 