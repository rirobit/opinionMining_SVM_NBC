from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
#from flask_mysqldb import MySQL,MySQLdb
import pandas
import bcrypt
import json
import trainingset
import trainingsetwoig
import klasifikasi
import klasakurasi
from datetime import date, timedelta
import time
from random import seed, randrange
#from passlib.hash import sha256_crypt

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="4KulupaSand!",
  database="sentista")

pd = pandas
curl = mydb.cursor()
dataset = pd.read_csv('file:///home/riro/Desktop/sistemopini/venv/data_training.csv')
training = trainingset.Trainingset(dataset)
datauji = ''

@app.route('/')
def home():
    page = 'home.html'
    if session.get('logged_in'):
        if session['tipe'] == 'admin':
            page = 'home.html'
        else:
            page = 'mahasiswa/home.html'
    else:
        page = 'login.html'          
    return render_template(page)

@app.route('/login',methods=["GET","POST"])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            iduser = request.form['iduser']
            password_login = request.form['password']
            curl.execute("SELECT * FROM user WHERE user_id=%s",(iduser,))
            user = curl.fetchone()
            if user:
                password = user[3]
                if password_login == password:
                    session['name'] = user[1]
                    session['logged_in'] = True
                    session['tipe'] = user[2]
                    if session['tipe'] == 'admin':
                        return render_template("home.html")
                    else:
                        return render_template("mahasiswa/home.html")
                else:
                    return "ID dan password tidak sesuai"
                curl.close()
            else:
                return "Error user not found"
        else:
            return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("login.html")

@app.route('/akurasi')
def akurasi():
    return render_template('akurasi.html')

@app.route('/sentimen')
def sentimen():
    return render_template('sentimen.html')

@app.route('/opinibaru', methods=["GET"])
def opinibaru():
    if request.method == "GET":
        req = request.url
        pd = pandas
        query = "SELECT * FROM opini WHERE opini_label=''"
        datauji = pd.read_sql_query(query, mydb)
        if req == 'http://127.0.0.1:5000/opinibaru?cek=':
            p = len(datauji)
            return render_template("home.html",n=p)
        else:
            label = training.get_label()
            prob = training.get_prob()
            klas = klasifikasi.Klasifikasi(query, mydb)
            klas.classifikasi(label, prob)
            hasil = klas.getdataset()
            index = len(hasil)
            positif = 0
            negatif = 0
            for i in range(0, index):
                if hasil['opini_label'][i] == 'p':
                    positif += 1
                else:
                    negatif += 1
            listsentimen = [positif, negatif, index]
            return render_template("home.html",a=listsentimen)
    #return render_template('sentimen.html')

@app.route('/simpan',methods=["POST"])
def simpan():
    opini = request.form['textopini']
    tanggal = date.today()
    tanggal = tanggal.strftime("%Y-%m-%d")
    tanggalsimpan = str(tanggal)[0:7]
    curl.execute("INSERT INTO opini (opini_tanggal, opini_dokumen) VALUES (%s, %s)",(tanggalsimpan, opini))
    mydb.commit()
    return redirect(url_for('home'))

@app.route('/data',methods=["POST"])
def data():
    awal = request.form['awal']
    y = int(awal[:4])
    m = int(awal[5:7])
    d = int(awal[-2:])
    depan = date(y, m, d)
    akhir = request.form['akhir']
    y = int(akhir[:4])
    m = int(akhir[5:7])
    d = int(akhir[-2:])
    belakang = date(y, m, d)
    delta = timedelta(days=28)
    awal = depan.strftime("%d/%m/%Y")
    akhir = belakang.strftime("%d/%m/%Y")
    #text = 'Tidak ditemukan opini pada rentang waktu' + str(awal) + ' hingga ' + str(akhir)
    p = 0
    n = 0
    bulan = ""
    while depan <= belakang:
        if str(depan)[0:7] != bulan:
            bulan = str(depan)[0:7]
            curl.execute("SELECT opini_label FROM opini WHERE opini_tanggal = %s",(bulan,))
            label = curl.fetchall()
            if label:
                p = p + label.count(('p',))
                n = n + label.count(('n',))
        else:
            bulan = str(depan)[0:7]       
        depan += delta

    datasentimen = [p, n, p + n, awal, akhir]
    return render_template('sentimen.html', d =datasentimen)


@app.route('/hitungakurasi',methods=["POST"])
def hitungakurasi():
    recordakurasi = []
    ig = float(request.form['standarig'])
    datauji = pd.read_csv('file:///home/riro/Desktop/sistemopini/venv/data_training.csv')
    traininguji = trainingsetwoig.Trainingset(dataset, ig)
    prob1 = traininguji.get_prob().copy()
    label = traininguji.get_label()
    traininguji = trainingsetwoig.Trainingset(dataset, 0)
    prob2 = traininguji.get_prob().copy()
    d = [500, 1000, 2450, 3729, 4500]
    datatest = []
    randrange(1000)
    seed(randrange(1000))
    randrange(1000)
    panjang = len(datauji)
    for x in d:
        opinitest = {'opini_dokumen': [],'opini_label': []}
        z = []
        for y in range(x):
            index = randrange(panjang)
            opinitest['opini_dokumen'].append(datauji['opini_dokumen'][index])
            opinitest['opini_label'].append(datauji['opini_label'][index])
        opinitest = pd.DataFrame(opinitest)   
        datatest.append(opinitest)
    
    for x in datatest:
        lisakurasi =[]
        labelbenar = x['opini_label']
        p = 0
        n = 0
        
        for y in labelbenar:
            if y == 'p':
                p += 1
            elif y == 'n':
                n += 1
        pbenar = p
        nbenar = n
        semua = p + n

        klas = klasakurasi.Klasifikasi(x)
        awal = time.time()
        klas.classifikasi(label, prob1)
        hasil = klas.getdataset()
        labelhasil = hasil['opini_label']

        p = 0
        n = 0
        for y in labelhasil:
            if y == 'p':
                p += 1
            elif y == 'n':
                n += 1  
        
        semua = p + n
        eror = abs(p - pbenar) + abs(n - nbenar)
        akurasi = (semua - eror) * 100 / semua
        akhir = time.time()
        durasi = akhir - awal 
        lisakurasi.append(akurasi)
        lisakurasi.append(durasi)



        awal = time.time()
        klas.classifikasi(label, prob2)
        hasil = klas.getdataset()
        labelhasil = hasil['opini_label']
        p = 0
        n = 0
        for y in labelhasil:
            if y == 'p':
                p += 1
            elif y == 'n':
                n += 1  
        semua = p + n
        eror = abs(p - pbenar) + abs(n - nbenar)
        akurasi = (semua - eror) * 100 / semua 
        akhir = time.time()
        durasi = akhir - awal
        lisakurasi.append(akurasi)
        lisakurasi.append(durasi)     
        recordakurasi.append(lisakurasi)
    recordakurasi.append(len(prob1))
    recordakurasi.append(len(prob2))
    recordakurasi.append(ig)
    recordakurasi.append(d)
    return render_template("akurasi.html", h = recordakurasi)


@app.route('/hapus')
def hapus():
    if request.method == "GET":
        curl.execute("UPDATE opini SET opini_label = ''")
        mydb.commit()
    return render_template("home.html")


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)