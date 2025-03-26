from flask import Flask
from flask import render_template
from flask import request
import sqlite3
import socket
import select
import queue 
from celery import Celery
    
app = Flask(__name__)

# def make_celery(app):
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery

# app = Flask(__name__)
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(app)
# socket_queue = queue.Queue()

# @celery.task()
# def listen_to_udp():
#     s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s1.bind(('0.0.0.0', 1337))
#     s2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
#     s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s2.bind(('0.0.0.0', 1337))
#     while True:
#         r, w, x = select.select([s1, s2], [], [])
#         for i in r:
#             socket_queue.put((i, i.recvfrom(131072)))


@app.route("/")
# def test_home():
#     listen_to_udp()
#     print(socket_queue.get())
def home():
    return render_template("home.html")

@app.route("/enternew")
def enternew():
    return render_template("record.html")

@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            id = request.form['id']
            coach_number = request.form['coach_number']
            watering_stations = request.form['watering_stations']
            contact_person = request.form['contact_person']
            mobile_number = request.form['mobile_number']
            water_level = request.form['water_level']

            with sqlite3.connect('database1.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO records (id, coach_number, watering_stations, contact_person, mobile_number, water_level) VALUES (?,?,?,?,?,?)", (id, coach_number, watering_stations, contact_person, mobile_number, water_level))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

@app.route('/list')
def list():
    con = sqlite3.connect("database1.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM records")

    rows = cur.fetchall()
    con.close()
    return render_template("list.html", rows=rows)

@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database1.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM records WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            return render_template("edit.html", rows=rows)

@app.route("/editrec", methods=['POST','GET'])
def editrec():
    if request.method == 'POST':
        try:
            rowid = request.form['rowid']
            id = request.form['id']
            coach_number = request.form['coach_number']
            watering_stations = request.form['watering_stations']
            contact_person = request.form['contact_person']
            mobile_number = request.form['mobile_number']
            water_level = request.form['water_level']

            with sqlite3.connect('database1.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE records SET id=?, coach_number=?, watering_stations=?, contact_person=?, mobile_number=?, water_level=? WHERE rowid=?", (id, coach_number, watering_stations, contact_person, mobile_number, water_level, rowid))

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with sqlite3.connect('database1.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM records WHERE rowid=?", (rowid,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port =5000)
