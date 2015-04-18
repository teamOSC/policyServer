from flask import Flask,render_template, flash, redirect, \
    make_response,request, url_for , session, g, jsonify
import json
from tweets import fetchTweet
from app import app


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