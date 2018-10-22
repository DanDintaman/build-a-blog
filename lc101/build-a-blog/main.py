from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Smokey0!@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key='key+894984'
db = SQLAlchemy(app)

class Blog(db.Model):    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body




#newpost

@app.route('/', methods=['POST', 'GET'])
def newpost():

    title_error = ""
    body_error = ""


    blogs = Blog.query.all()
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title_error="required field"

        if not body:
            body_error="required field"

        if not title or not body:
            return render_template('newpost.html', blogs=blogs, title_error=title_error, body_error=body_error)

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        new_blog_id = new_blog.id
        return redirect('/blog?id={0}'.format(new_blog.id))

    return render_template('newpost.html', blogs=blogs)

#blog

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id=request.args.get('id')
    blog_id_int=int(blog_id)
    blog = Blog.query.filter_by(id=blog_id_int).first()
    if blog:
        return render_template('blog.html', blog=blog)
    else:
        return 'Not Found'


if __name__ == '__main__':
    app.run()