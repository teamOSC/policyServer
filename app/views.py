from flask import Flask,render_template, flash, redirect, \
    make_response,request, url_for , session, g, jsonify

import json
from tweets import fetchTweet
from app import app

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


@app.route('/admin')
def admin():
    userTweets = fetchTweet('sauravtom')
    print type(userTweets), userTweets
    return render_template('admin.html', tweet=userTweets)


@app.route('/admin/warnLocal')
def localWarn():
    pass
