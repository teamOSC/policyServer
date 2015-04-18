from flask import Flask,render_template, flash, redirect, \
    make_response,request, url_for , session, g, jsonify

from tweets import fetchTweet
from app import app
from dbHelper import DB
import json,urllib2,xml,datetime,hashlib,time,requests,base64
from base64 import b64encode
from credentials import client_id,client_secret


def upload_imgur(img_file=''):
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
        return response.json()['data']['link']
    else:
        return ""


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')

    print request.form
    print request.files
    title = request.form['title']
    user_location = request.form['user_location']
    user_email = request.form['user_email']
    user_name = request.form['user_name']
    user_phone = request.form['user_phone']

    try:
        img_url = request.form['image_url']
    except:
        item_image = request.files['item_image']
        img_url = upload_imgur(item_image)

    D = DB()
    date_ = datetime.datetime.now().strftime("%d/%m/%Y,%H:%M")
    item_id = D.add_item(title, img_url,user_location,user_email,user_name)
    resp = jsonify(data={"Success"})
    resp.status_code = 200
    return resp


@app.route('/api/bar', methods=['GET', 'POST'])
def main():
    try:
        barcode = request.args.post('barcode')
    except:
        barcode = request.args.get('barcode')
    return json.dumps(str(barcode))


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
    userTweets = fetchTweet('sauravtom')
    print type(userTweets), userTweets
    return render_template('admin.html', tweet=userTweets)


@app.route('/admin/warnLocal')
def localWarn():
    pass
