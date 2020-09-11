from flask import Flask, render_template, request
import json, os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    cast = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(50),)



@app.route("/")
def index():
    db = Movies.query.all()
    return render_template("index.html",movies=db) 


@app.route("/new-movie", methods=['POST', 'GET'])
def new_movie():

    if request.method == 'GET':
        return render_template("new_movie.html")
    else:
        # fetch movie details from request


        m = Movies()
        m.title = request.form['title']            
        m.budget = request.form['budget']            
        m.cast = request.form['cast']            
        m.year = request.form['year']    


        db.session.add(m)        
        db.session.commit()        

        return render_template(
            "new_movie.html",
            success = f"Movie '{m.title}' was seccessfully added."
        )
@app.route("/edit/<string:title>", methods=['POST', 'GET'])
def edit_movies(title):
    m = Movies.query.filter_by(title=title).first()
    if request.method == 'GET':
        return render_template("edit.html", movie=m)
    else:
        m.title = request.form['title']
        m.year = request.form['year']
        m.budget = request.form['budget']
        m.cast = request.form['cast']

        db.session.commit()

        return render_template(
            "edit.html",
         movie=m,
         msg=f"{movie.title} successfully update"
        )

@app.route("/search")   
def search():
    q = request.args.get("q")
    results = Movies.query.filter(Movies.title.contains(q)).all()
    return render_template("search.html", results = results, q=q)

@app.route("/delete/<int:id>", methods = ['POST','GET'])
def delete_movie(id):
    m = Movies.query.get(id)

    if m is None:
        return render_template("error.html")

    if request.method == "GET":
        return render_template("delete.html", movie=m)

    else:
                 
            db.session.delete(m)
            db.session.commit()
            return redirect("/")

     
        























# @app.route("/")
# def index():
#     movies = {}

#     if os.path.exists("movies.json"):
#         with open("movies.json") as movies_file:
#             movies = json.load(movies_file)

#     else:
#         with open("movies.json", "w") as f:
#             f.write("[]")
            
#         new_movie = [{
#             "title": "Prison Break",
#             "year": 2005,
#             "budget":"USD 700m",
#             "cast": "people"
#         }]
#         movies = new_movie

#     return render_template("index.html", movies=movies) 




# @app.route("/new-movie",methods=['POST','GET'])
# def new_movie():

#     if request.method == 'GET':
#         return render_template("new_movie.html")
#     else:
#         new_movie = {}
#         new_movie["title"] = request.form['title']
#         new_movie['year'] = request.form['year']
#         new_movie['budget'] = request.form['budget']
#         new_movie['cast'] = request.form['cast']

#         with open("movies.json", "w") as f:
#             json.dump(new_movie,f)

#         return render_template(
#             "new_movie.html",
#             success = f"Movie'{new_movie['title']}' was successful added."
#             )

            