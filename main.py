from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/users'
# mysql://username:password@host:port/database_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model): #Muscle Memory
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(400), nullable=False)
    
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def users_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("user/list.html", users=users)
    
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method=="POST":
        user = User(
            title=request.form['title'],
            description=request.form['description']
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("index"))
    return render_template("user/add.html")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if request.method == "POST":
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            return "User not found", 404

    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if request.method=="POST":
        user=User.query.get(id)
        if user:
            new_title = request.form["new_title"]
            new_description = request.form["new_description"]
            if new_title:
                user.title = new_title
            if new_description:
                user.description = new_description
                
            db.session.commit()
            return redirect(url_for('index'))
        
        else:
            return "User not found", 404
        
    return redirect(url_for("index"))
        
    
    
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
    
