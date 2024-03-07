from heart_prob import app
from heart_prob import db,app




from heart_prob import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol


@login_manager.user_loader
def load_user(id):
    return registration.query.get(int(id))

user_test=db.Table('user_test',
             db.Column('user_id',db.Integer,db.ForeignKey('registration.id')),
             db.Column('test_id',db.Integer,db.ForeignKey('test.id')))


tec_test=db.Table('tec_test',
             db.Column('tec_id',db.Integer,db.ForeignKey('registration.id')),
             db.Column('test_id',db.Integer,db.ForeignKey('test.id')))



user_query=db.Table('user_query',
             db.Column('user_id',db.Integer,db.ForeignKey('registration.id')),
             db.Column('query_id',db.Integer,db.ForeignKey('qresponses.id')))



doc_query=db.Table('doc_query',
             db.Column('doc_id',db.Integer,db.ForeignKey('registration.id')),
             db.Column('query_id',db.Integer,db.ForeignKey('qresponses.id')))



user_buk=db.Table('user_buk',
             db.Column('user_id',db.Integer,db.ForeignKey('registration.id')),
             db.Column('buk_id',db.Integer,db.ForeignKey('bookdoctor.id')))


doc_buk=db.Table('doc_buk',
             db.Column('doc_id',db.Integer,db.ForeignKey('registration.id')),
             db.Column('buk_id',db.Integer,db.ForeignKey('bookdoctor.id')))



class registration(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    lid=db.Column(db.String(80))
    name = db.Column(db.String(80))
    address= db.Column(db.String (80))
    age= db.Column(db.String (80))
    gender= db.Column(db.String (80))
    email= db.Column(db.String(80))
    number= db.Column(db.String (10))
    password = db.Column(db.String(80))
    usertype = db.Column(db.String(80))
    Specialisation=db.Column(db.String(80))
    Qualification=db.Column(db.String(80)) 
    Image=db.Column(db.String(80))
    def __repr__(self):
        return self.id

class contact(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) 
    email= db.Column(db.String(80))
    number= db.Column(db.String (10))
    text= db.Column(db.String (80))


class Qresponses(db.Model, UserMixin):

 
    id=db.Column(db.Integer, primary_key=True)
    uid= db.relationship('registration',secondary=user_query,backref='ques')
    did= db.relationship('registration',secondary=doc_query,backref='queries')
    que= db.Column(db.String (80))
    response= db.Column(db.String (80),default="null")

    def __repr__(self):
        return self.id


class BookDoctor(db.Model, UserMixin):
    __tablename__='bookdoctor'

 
    id=db.Column(db.Integer, primary_key=True)
    uid= db.relationship('registration',secondary=user_buk,backref='buks')
    did= db.relationship('registration',secondary=doc_buk,backref='books')
    date= db.Column(db.String (80))
    time= db.Column(db.String (80))
    status=db.Column(db.String (80),default="null")

    def __repr__(self):
        return self.id

class Test(db.Model, UserMixin):
 
    id=db.Column(db.Integer, primary_key=True)
    uid=db.relationship('registration',secondary=user_test,backref='tests')
    lid=db.relationship('registration',secondary=tec_test,backref='tes')
    date= db.Column(db.String (10))
    time= db.Column(db.String (80))
    thal= db.Column(db.String (80))
    cp= db.Column(db.String(80))
    trestbps= db.Column(db.String (10))
    chol = db.Column(db.String(80))
    fbs = db.Column(db.String(80))
    restecg=db.Column(db.String(80))
    thalach=db.Column(db.String(80)) 
    exang=db.Column(db.String(80))
    oldpeak=db.Column(db.String(80))
    slope=db.Column(db.String(80))
    ca=db.Column(db.String(80))
    pred=db.Column(db.String(80))
    test_type=db.Column(db.String(80))

    def __repr__(self):
        return self.id





    
    
    


    
    



 





