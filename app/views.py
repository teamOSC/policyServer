from flask import Flask,render_template, flash, redirect, \
    make_response,request, url_for , session, g, jsonify

from app import app

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return flask.render_template('upload.html')

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

    


