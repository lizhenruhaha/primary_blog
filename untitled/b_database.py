from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://名:密码@127.0.0.1:3306/数据库名'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='fregtrf'

db=SQLAlchemy(app)

class Blog(db.Model):
    __tablename__='blogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(100))
    content=db.Column(db.String(1000))
    blog_message_id=db.Column(db.Integer,db.ForeignKey('blog_message.id'))

    def __init__(self,title,content,blog_message_id):
        self.title=title
        self.content=content
        self.blog_message_id=blog_message_id

    # def __repr__(self):
    #     return 'Blog  %s %s %s'% self.author

class Blog_people(db.Model):
    __tablename__ = 'blog_message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namea=db.Column(db.String(16), unique=True)
    password = db.Column(db.String(20), unique=True)
    titles=db.relation('Blog',backref='blog_messages')

    def __init__(self,namea,password):
        self.namea=namea
        self.password=password

    def __repr__(self):
        return 'Blog_people %s' % self.namea




# db.drop_all()
# db.create_all()
# one=Blog('论python的强大之处','王源','目前还在学习之中,还要在时间中来总结其有用之处')
# two=Blog('论Java的强大之处','不知道','目前还在学习之中,还要在时间中来总结其有用之处,等我来解答啊')
# db.session.add(two)
# db.session.commit()
# one=Blog_people(namea='王源',password='2001724')
# two=Blog_people(namea='刘星',password='28889')
# one=Blog(title='论人类的重要性',content='不知道还在学习中呢,这要以后才能知道',blog_message_id=1)
# two=Blog(title='论Java的重要性',content='不知道还在学习中呢,这要以后才能知道,有待讨论',blog_message_id=2)
# db.session.add(one)
# db.session.commit()

# Blog.query.filter_by(id=1).delete()
# db.session.commit()
