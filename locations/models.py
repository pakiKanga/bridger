from MeetupPoint import db
import datetime

class UserLocation(db.Model):
    location_id = db.Column(db.String(13), primary_key=True)
    location_name = db.Column(db.String(150))
    session_id = db.Column(db.String(13), db.ForeignKey('user_session.session_id'), default=None)
    # longitude = db.Column(db.String(30))
    # latitude = db.Column(db.String(30))

    def __init__(self, location_id, session_id, curr_address):
        self.location_id = location_id
        self.session_id = session_id
        self.location_name = curr_address

    def __str__(self):
        return self.session_id

    def __repr__(self):
        return '<Application %r>' % self.session_id
    


        
        
 
