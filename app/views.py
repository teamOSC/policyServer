from flask import Flask,render_template, flash, redirect, \
    make_response,request, url_for , session, g, jsonify

from tweets import fetchTweet
from app import app
from dbHelper import DB
import json,urllib2,xml,datetime,hashlib,time,requests,base64
from base64 import b64encode
from credentials import client_id,client_secret
from parse_rest.installation import Push
from parse_rest.connection import register
register('9nhyJ0OEkfqmGygl44OAYfdFdnapE27d9yj9UI5x', 'xsipM4oBX3sRx415UsWPXHCuuTPhetfmmrubRiPx', master_key=None)
import multiprocessing
import os
from matching import imageMatch
from bot import pushTwitter


def upload_imgur(img_file):
    headers = {"Authorization": "Client-ID %s"%client_id}
    api_key = client_secret
    url = "https://api.imgur.com/3/upload.json"

    if not img_file:
        img_data = b64encode(open('1.png', 'rb').read())
    else:
        img_data = b64encode(img_file.read())

    response = requests.post(
        url, 
        headers = headers,
        data = {
            'key': api_key,
            'image': img_data,
            'type': 'base64',
            'name': '1.jpg',
            'title': 'Picture no. 1'
        }
    )
    print response.text
    if response.json()['status'] == 200:
        img_url = response.json()['data']['link']
        return img_url
    else:
        return ""


@app.route('/upload',methods=['GET','POST'])
def upload():
    title = request.form['title']
    user_location = request.form['user_location']
    user_email = request.form['user_email']
    user_name = request.form['user_name']
    user_phone = request.form['user_phone']
    item_image = request.files['item_image']
    item_image.save(os.path.join(app.config['UPLOAD_FOLDER']+"/tmp", item_image.filename))

    img_url = upload_imgur(item_image)
    #img_url=''
    #process = multiprocessing.Process(target=upload_imgur,args=(item_image,img_url))
    confidence = imageMatch(os.path.join(app.config['UPLOAD_FOLDER']+"/tmp", item_image.filename), os.path.join(app.config['UPLOAD_FOLDER'], "puma.png"))

    #pushTwitter(os.path.join(app.config['UPLOAD_FOLDER']+"/tmp", item_image.filename),'hi')

    D = DB()
    D.add_item(title, img_url,user_location,user_email,user_name)
    Push.message(confidence, channels=[""])
    resp = jsonify(data=str(confidence['confidence']))
    resp.status_code = 200
    return resp


@app.route('/api/complaint', methods=['GET', 'POST'])
def manualComplaint():
    try:
        comp = request.form['complaint']
        location = request.form['location']
    except:
        comp = request.args.get('complaint')
        location = request.args.get('location')

    D = DB()
    D.add_complaint(comp, location)

    loc = str(location).split(',')
    lat = loc[0]
    lon = loc[1]

    return jsonify("your complaint has been registered")


@app.route('/api/bar', methods=['GET', 'POST'])
def main():
    try:
        barcode = request.form['barcode']
    except:
        barcode = request.args.get('barcode')

    confidence = 0.5
    D = DB()
    D.add_bar(barcode, confidence)
    conf = {"confidence": str(confidence)}

    return jsonify(data=conf)


@app.route('/api/push',methods=['GET'])
def push():
    msg = request.args.get('msg')
    d ={}
    d['msg'] = msg
    d['type'] = 'push'
    Push.message(json.dumps(d),channels=[""])
    return jsonify(data="success")



@app.route('/feed')
def feed():
    userTweets = fetchTweet('jaaag0')
    arr = []
    for i in userTweets:
        d = {}
        d['title'] = i.text
        try:
            d['picture'] = i.media[0]['media_url']
        except:
            continue
            d['picture'] = ""
        arr.append(d)
    return jsonify(data=arr)


@app.route('/analysis', methods=['GET'])
def analysis():
    state = request.args.get('state')
    dist = request.args.get('dist')

    if state is not None:
        return render_template('analysis.html', state=state, query=1)
    else:
        states = ['Delhi', 'Uttar Pradesh', 'Haryana', 'Maharashtra', 'Andhra Pradesh']
        return render_template('analysis.html', states=states, query=0)


@app.route('/admin')
def admin():
    userTweets = fetchTweet('jaaag0')
    arr = []
    for i in userTweets:
        d = {}
        d['title'] = i.text
        d['id'] = i.id
        try:
            d['picture'] = i.media[0]['media_url']
        except:
            continue
            d['picture'] = ""
        arr.append(d)
    return render_template('admin.html',arr=arr)


@app.route('/mainFeed')
def mainFeed():
    userTweets = fetchTweet('sauravtom')
    arr = []
    for i in userTweets:
        d = {}
        d['title'] = i.text
        try:
            d['picture'] = i.media[0]['media_url']
        except:
            d['picture'] = ""
        arr.append(d)
    return render_template('feed.html', arr=arr)
