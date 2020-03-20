from flask import Flask, request, Response, json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
redirect_uri=os.getenv("REDIRECT_URI")

app=Flask(__name__)

@app.route("/",methods=['GET'])
def stitchig():
    code=request.args.get('code')[:-2]
    r=requests.post(url='https://api.instagram.com/oauth/access_token', data={
            'client_id':client_id,
            'client_secret':client_secret,
            'grant_type':'authorization_code',
            'redirect_uri':'https://dhruvs009.github.io/me/',
            'code':code
        })
    response=r.json()
    access_token=response['access_token']
    user_id=response['user_id']
    r=requests.get(url='https://graph.instagram.com/'+str(user_id)+'/media?fields=id&access_token='+str(access_token))
    response=r.json()
    data=response['data']


if __name__=="__main__":
    app.run(debug=True)