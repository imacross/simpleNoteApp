from flask import Flask,request,url_for,redirect,render_template,jsonify
import hashlib
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://simpleNoteSu:123456@postgres:5432/simplenotedb"
secret_key = "endoplazmikretikulum"
#"postgresql://simpleNoteSu:123456@localhost:5432/postgres"
db = SQLAlchemy(app)
class Note(db.Model): #note diye model tanımladım
    __tablename__ = 'simplenotetable' # bunun tablodaki ismi note
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String)
    note = db.Column(db.String)
    isprivate = db.Column(db.Boolean, server_default='f', default=False, nullable=False)
    password = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.datetime.now())
    #initi
    def __init__(self,header, note,password,isprivate):
        self.header = header
        self.note = note
        self.password = password
        self.isprivate = isprivate



@app.route('/', methods = ['POST','GET'] )
def index():
    if request.method == 'POST':
        for req in request.form:
            if req == "isprivate":
                password = request.form['password']
                encoder = hashlib.sha256()
                encoder.update(password.encode("utf-8"))
                encoder.update(secret_key.encode("utf-8"))
                password = encoder.hexdigest()
                data = Note(header=request.form['header'], note=request.form['note'], password=password, isprivate=True)
                break
        else:
            data = Note(header=request.form['header'], note=request.form['note'], password="", isprivate=False)
        db.session.add(data) # ekleme
        db.session.commit() # commit et
        return redirect(url_for('index'))
    else:
        dataQuery = Note.query.all()
        dataQuery.reverse()
        id = 0
        selectData = 0
        return render_template("index.html", dataQuery= dataQuery, id = id, selectData = selectData)
@app.route('/passwordcontrol', methods = ['POST'])
def passwordcontrol():
    s_password = request.form['sPassword']
    sId = request.form['sId']

    select_data = Note.query.filter_by(id=sId).first()

    encoder = hashlib.sha256()
    encoder.update(s_password.encode("utf-8"))
    encoder.update(secret_key.encode("utf-8"))
    s_password = encoder.hexdigest()
    if s_password == select_data.password:
        return jsonify({'header': select_data.header, 'note': select_data.note})
    else:
        return jsonify({'error': "Wrong Password"})

@app.route('/search/<string:id>/')
def searchDetail(id):
    searchText = id.split("-")
    sqlCode = "select header,note,id,date " \
              "from simplenotetable " \
              "where to_tsvector('english', note || ' ' || header) " \
              "@@ to_tsquery('english','"+id+"')"
    sqlResponse =  db.engine.execute(sqlCode)
    result = []
    for res in sqlResponse:
        result.append(res)
    data = [dict(row) for row in result]
    if data == []:
        dataQuery = Note.query.all()
        return render_template('index.html', id=-3, dataQuery=dataQuery, selectData = 0, searchText = id)
    else:
        return render_template('index.html', id=-2, dataQuery=data, selectData = 0, searchText = id)


@app.route('/<string:id>/', methods = ['POST','GET'] )
def detail(id):
    dataQuery = Note.query.all()
    dataQuery.reverse()
    selectData = Note.query.filter_by(id=id).first()

    if selectData == None :
        return render_template('index.html', id=-1 ,dataQuery= dataQuery, selectData = selectData)
    else:
        return render_template('index.html', id=id ,dataQuery= dataQuery, selectData = selectData)

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run()

