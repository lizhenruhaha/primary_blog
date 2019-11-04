from b_database import Blog,Blog_people,db,app
from flask import Flask,flash,render_template,request,redirect,url_for,session,escape
from sqlalchemy import and_
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://名:密码@127.0.0.1:3306/数据库名'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='xdfcgyuhijokpl'

@app.route('/blog/<author_id>')
def select(author_id):
    author=Blog_people.query.get(author_id)
    return  render_template('b_select.html',message=author)

@app.route('/index')
def index():
    # 查询出注册过的人
    index_message=Blog_people.query.all()
    # 把名字session复值给word
    word = escape(session['str_word'])
    return render_template('a_index.html',content=index_message,word=word)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login_c.html')
    else:
        name=request.form['namea']
        password=request.form['password']
        judge=Blog_people.query.filter(and_(Blog_people.namea==name,Blog_people.password==password)).first()
        if judge:
            id=judge.id
            name=judge.namea
            session['num']=id
            session['str_word']=name
            return redirect(url_for('index'))
        else:
            return render_template('login_c.html')

@app.route('/newblog',methods=['GET','POST'])
def newblog():
    if request.method=='GET':
        return render_template('new_d.html')
    else:
        title = request.form['title']
        content = request.form['content']
        num = escape(session['num'])
        if title=='' or content=='':
            flash('输入不能为空,请规范书写')
        else:
            try:
                new = Blog(title=title, content=content, blog_message_id=num)
                db.session.add(new)
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                print(e)
                db.session.rollback()
    return render_template('new_d.html')

@app.route('/personal')
def personal():
    num = escape(session['num'])
    author = Blog_people.query.get(num)
    return  render_template('personal_e.html',message=author)

@app.route('/delblog/<title_id>')
def delete(title_id):
    try:
        Blog.query.filter_by(id=title_id).delete()
        db.session.commit()
        return redirect(url_for('personal'))
    except Exception as e:
        print(e)
        db.session.rollback()
    num = escape(session['num'])
    author = Blog_people.query.get(num)
    return  render_template('personal_e.html',message=author)

@app.route('/editblog/<title_id>',methods=['GET','POST'])
def edit(title_id):
    if request.method=='GET':
        return render_template('edit_f.html', title_id=title_id)
    else:
        tit=request.form['title_a']
        cont=request.form['content_a']
        total=Blog.query.filter_by(id=title_id).first()
        try:
            total.title=tit
            total.content=cont
            db.session.commit()
            return redirect(url_for('personal'))
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('edit_f.html',title_id=title_id)

@app.route('/register_g',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register_g.html')
    else:
        name=request.form['name']
        password1=request.form['password1']
        password2=request.form['password2']
        if password1==password2:
            try:
                new=Blog_people(namea=name,password=password2)
                db.session.add(new)
                db.session.commit()
                # 把注册的名字和id弄session  全局的
                session['str_word']=name
                peo=Blog_people.query.filter(and_(Blog_people.namea==name,Blog_people.password==password1)).first()
                num=peo.id
                session['num']=num
                # 注册成功后重定向到第一个页面
                return redirect(url_for('index'))
            except Exception as e:
                print(e)
                db.session.rollback()
        else:
            return render_template('register_g.html')
    return render_template('register_g.html')
if __name__=='__main__':
    app.run()