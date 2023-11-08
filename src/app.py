from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src', 'templates')

app = Flask(__name__, template_folder = template_dir)


#rutas de la aplicación
@app.route("/")
def index():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    # convertir result a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for result in results:
        insertObject.append(dict(zip(columnNames, result)))
    cursor.close

    return render_template("index.html", data=insertObject)


# save user
@app.route("/user", methods=["POST"])
def user():
    username = request.form["username"]
    name = request.form["name"]
    password = request.form["password"]
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    
    return redirect(url_for("index"))


# edit user
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form["username"]
    name = request.form["name"]
    password = request.form["password"]
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    
    return redirect(url_for("index"))


# delete user
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)