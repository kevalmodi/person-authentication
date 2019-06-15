# -*- coding: utf-8 -*-
import pymysql
from datetime import date, datetime
from flask import Flask, request,jsonify
from flask import render_template

import camera

UPLOAD_FOLDER = 'thumbnail_images'
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'mp4', 'bmp'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET'])
def helmet_detect():
    # upload_to = 'static/videos/'
    output = {}
    email=request.args.get('userName')

    loginId = request.args.get('loginId')

    print("userName=",email)
    print("loginid=",loginId)
    # videoName=request.args.get('videoName')

    # camera.start_app('static/videos/{}'.format(videoName))
    EMOTIONS_LIST = ["Angry", "Disgust",
                     "Fear", "Happy",
                     "Sad", "Surprise",
                     "Neutral"]

    lst=camera.start_app(path=0,email=email)
    for i in range(len(lst)):
        output[EMOTIONS_LIST[i]]=lst[i]
    Angry = str(output['Angry'])
    Disgust = str(output['Disgust'])
    Fear = str(output['Fear'])
    Happy = str(output['Happy'])
    Sad = str(output['Sad'])
    Surprise = str(output['Surprise'])
    Neutral = str(output['Neutral'])


    detectionDate = str(date.today())
    detectionTime = str(datetime.time(datetime.now()))

    print("date=",detectionDate,"detectionTime=",detectionTime)
    print("angryCount=",Angry,"Disgust=",Disgust,"Fear=",Fear,"Happy=",Happy,"Sad=",Sad,"Surprise=",Surprise,"Neutral=",Neutral)

    connection = pymysql.connect(
        host = "localhost",
        user="root",
        password="root",
        db ="misbehavedetection"
    )
    cursor1 = connection.cursor()
    cursor1.execute(
        "INSERT INTO face_detection(Angry,Disgust,Fear,Happy,sad,Surprise,Neutral,detectionDate,detectionTime,detection_loginId) VALUES ('"+Angry+"','"+Disgust+"','"+Fear+"','"+Happy+"','"+Sad+"','"+Surprise+"','"+Neutral+"','"+detectionDate+"','"+detectionTime+"','"+str(loginId)+"')"
    )
    connection.commit()
    cursor1.close()
    connection.close()


    response = jsonify(output)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/getgraph', methods=['GET', 'POST'])
def graph_detect():
    camera.get_graph()


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


app.run(debug=True, port=5011)
