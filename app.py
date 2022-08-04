from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import numpy

conn = sqlite3.connect('sqlite3.db')
c = conn.cursor()

c.execute("SELECT Ambient_Temp, TOTAL_HEAT_REJECTION FROM User WHERE COND_FLUID_OUT==105")

list1 = c.fetchall()
x1 = []
y1 = []

for item in list1:
    x1.append(float(item[0]))
    y1.append(float(item[1]))
c.execute("SELECT Ambient_Temp, TOTAL_HEAT_REJECTION FROM User WHERE COND_FLUID_OUT==117.5")
list2 = c.fetchall()
x2 = []
y2 = []

for item in list2:
    x2.append(float(item[0]))
    y2.append(float(item[1]))
c.execute("SELECT Ambient_Temp, TOTAL_HEAT_REJECTION FROM User WHERE COND_FLUID_OUT==130")
list3 = c.fetchall()
x3 = []
y3 = []

for item in list3:
    x3.append(float(item[0]))
    y3.append(float(item[1]))

c = numpy.poly1d(numpy.polyfit(x1, y1, deg=5))
b = numpy.poly1d(numpy.polyfit(x2, y2, deg=5))
a = numpy.poly1d(numpy.polyfit(x3, y3, deg=5))

c_temp = 105
a_temp = 130
b_temp = 117.5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/", methods=['POST','GET'])
def calculate():
    total_heat_rejection = ''
    if request.method == 'POST' and 'Condfluidout' in request.form and 'Ambienttemp' in request.form:
        Condfluidout = float(request.form.get('Condfluidout'))
        Ambienttemp = float(request.form.get('Ambienttemp'))
        if Condfluidout <= b_temp and Condfluidout >= c_temp:
            diff = (Condfluidout - c_temp) / (b_temp - c_temp)
            total_heat_rejection = c(Ambienttemp) - ((c(Ambienttemp) - b(Ambienttemp)) * (diff))
        elif Condfluidout <= a_temp and Condfluidout >= b_temp:
            diff = (Condfluidout - b_temp) / (a_temp - b_temp)
            total_heat_rejection = b(Ambienttemp) - ((b(Ambienttemp) - a(Ambienttemp)) * (diff))
        else:
            return "Invalid Condenser Fluid Out Temperature"
    return render_template("index.html", total_heat_rejection=total_heat_rejection)

@app.route("/cpaz40", methods=['POST','GET'])
def cpaz40():
    return "gy"

if __name__ == "__main__":
    app.run()

'''
class User(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    REFRIGERANT = db.Column(db.String)
    COND_FLUID = db.Column(db.String)
    HEAT_REJECTION_CIRCUIT = db.Column(db.Float)
    TOTAL_HEAT_REJECTION = db.Column(db.Float)
    COND_FLUID_IN = db.Column(db.Float)
    COND_FLUID_OUT = db.Column(db.Float)
    COND_FLOW = db.Column(db.Float)
    COND_P_PSI = db.Column(db.Float)
    COOLING_CAPACITY_CIRCUIT = db.Column(db.Float)
    TOTAL_COOLING_CAPACITY = db.Column(db.Float)
    Ambient_Temp = db.Column(db.Float)
    LEAVING_TEMP_DB = db.Column(db.Float)
    LEAVING_TEMP_WB = db.Column(db.Float)
    EVAP_AIR_FLOW = db.Column(db.Float)
    TOTAL_AIR_FLOW = db.Column(db.Float)
    Air_Friction = db.Column(db.Float)
    COMPRESSOR_POWER_INPUT = db.Column(db.Float)
    COMPRESSORS_USED = db.Column(db.Float)
    FAN_POWER_INPUT_POWER = db.Column(db.Float)
    FANS_USED = db.Column(db.Float)

    def __repr__(self):
        return f'{self.Ambient_Temp}'
'''

conn.commit()
conn.close()
