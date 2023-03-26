from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import os


bp = Blueprint("banco", __name__)


@bp.route("/")
def index():
    """Show all the suspects, most recent first."""
    db = get_db()
    suspects = db.execute(
        "SELECT  p.id, path_img, name_full, nickname, dn, endereco, mother, faccao, ficha "
        " FROM suspect p JOIN imagem u ON p.cpf = u.img_cpf"

    ).fetchall()

    return render_template("banco/index.html", suspects=suspects)




def get_suspect(id, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    suspect = (
        get_db()
        .execute(
            "SELECT  p.id, path_img, name_full, nickname, dn, endereco, mother, faccao, ficha "
            " FROM suspect p JOIN imagem u ON p.cpf = u.img_cpf"            
            "WHERE p.id = ?", (id,)
        )
        .fetchone()
    )

    if suspect is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and suspect["author_id"] != g.user["id"]:
        abort(403)

    return suspect



## Está sem erro agora
@bp.route("/")
@bp.route("/details", methods=["GET", "POST"])
@bp.route("/<int:id>")
def details(id):   

    
    error = None
    if not id:
        error = "ID is required."

    if error is not None:
            flash(error)
    else:
        susp = (
        get_db()
        .execute(
                "SELECT p.id, path_img, name_full, nickname,cpf, rg, dn, endereco, mother, faccao, ficha, spot "
                "FROM suspect p JOIN imagem u ON p.cpf = u.img_cpf "
                "WHERE p.id = ?", (id,)
            ).fetchone()
        )
        """return redirect(url_for("banco.index"))"""

    return render_template("banco/details.html", susp=susp)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""

    if request.method == "POST":
        """file = request.files['image']
        img = file.read()"""
        """"""
        
        name_full = request.form["name_full"]
        cpf = request.form["cpf"]
        file = request.files['image']        
        filename = file.filename
        ##Correto
        path = "C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/"
        
        ##Correto
        if not os.path.exists(path + name_full  + str(cpf)):
            os.mkdir("C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/" + str(name_full)  + str(cpf))
            
        path = "C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/" + name_full  + str(cpf)
        file.save(os.path.join(os.getcwd(), "C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/"+ name_full  + str(cpf)+'/', filename))
        
        path_right =  name_full  + str(cpf) + '/' + filename

        
        rg = request.form["rg"]
        nickname = request.form["nickname"]
        mother = request.form["mother"]
        error = None

        if not name_full:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # inserir os dados do suspeito na tabela "suspect"
            db.execute(
                "INSERT INTO suspect (name_full, cpf, rg, nickname, mother) VALUES ( ?, ?, ?, ?, ?)",
                (name_full, cpf, rg, nickname, mother),
            )
            db.execute(
                "INSERT INTO imagem (path_img, img_cpf) VALUES ( ?, ?)",
                (path_right, cpf),
            )
            db.commit()

            return redirect(url_for("banco.index"))

    return render_template("banco/create.html")


@bp.route("/update", methods=["GET", "POST"])
@bp.route("/<int:id>")
@ login_required
def update(id):
    """Update a post if the current user is the author."""
    susp_up = (
        get_db()
        .execute(
                "SELECT p.id, path_img, name_full, nickname,cpf, rg, dn, endereco, mother, faccao, ficha, spot "
                "FROM suspect p JOIN imagem u ON p.cpf = u.img_cpf "
                "WHERE p.id = ?", (id,)
            ).fetchone()
        )

    if request.method == "POST":

        name_full = request.form["name_full"]
        cpf = request.form["cpf"]
        file = request.files['image']        
        filename = file.filename
        ##Correto
        path = "C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/"
        
        ##Correto
        if not os.path.exists(path + name_full  + str(cpf)):
            os.mkdir("C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/" + str(name_full)  + str(cpf))
            
        path = "C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/" + name_full  + str(cpf)
        file.save(os.path.join(os.getcwd(), "C:/Users/neand/PastaProjectVScode/flask/flaskr/static/images/"+ name_full  + str(cpf)+'/', filename))
        
        path_right =  name_full  + str(cpf) + '/' + filename      
        rg = request.form["rg"]
        nickname = request.form["nickname"]
        mother = request.form["mother"]
        faccao = request.form["faccao"]
        ficha = request.form["ficha"]
        spot = request.form["spot"]
        error = None

        if not name_full:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE suspect SET  name_full = ?  nickname = ?  cpf = ?  rg = ?  mother = ? faccao = ? ficha = ? spot = ? WHERE id = ?", (
                    name_full, nickname, cpf, rg, mother, faccao, ficha, spot,  id))
            db.commit()
            """return redirect(url_for("banco.index"))"""

    return render_template("banco/update.html", susp_up=susp_up)


@ bp.route("/<int:id>/delete", methods=("POST",))
@ login_required
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_suspect(id)
    db = get_db()
    db.execute("DELETE FROM suspect WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("banco.index"))
