from flask import Flask, request, Response, json
import requests
import os
from dotenv import load_dotenv
import urllib.request
from PIL import Image
import math
import random

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
redirect_uri=os.getenv("REDIRECT_URI")

app=Flask(__name__)

@app.route("/",methods=['GET'])
def stitchig():
    code=request.args.get('code')
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
    imgArray=[]
    width=0
    height=0
    for row in data:
        r=requests.get(url='https://graph.instagram.com/'+str(row['id'])+'?fields=media_url,media_type,children&access_token='+str(access_token))
        response=r.json()
        print(response)
        if response['media_type']=="IMAGE":
            image=Image.open(urllib.request.urlopen(response['media_url']))
            size=150, 150
            im_resized=image.resize(size, Image.ANTIALIAS)
            imgArray.append(im_resized)
        elif response['media_type']=="CAROUSEL_ALBUM":
            for child in response['children']['data']:
                rtemp=requests.get(url='https://graph.instagram.com/'+str(child['id'])+'?fields=media_url,media_type,children&access_token='+str(access_token))
                responsetemp=rtemp.json()
                image=Image.open(urllib.request.urlopen(responsetemp['media_url']))
                size=150, 150
                im_resized=image.resize(size, Image.ANTIALIAS)
                imgArray.append(im_resized)
    n=math.ceil(math.sqrt(len(imgArray)))
    result=Image.new('RGB',(150*n,150*n),(255,255,255))
    x=[0]*n
    y=[0]*n
    for i in range(n):
        x[i]=i
        y[i]=i
    while(len(imgArray)!=0):
        a=random.randint(0,len(x)-1)
        b=random.randint(0,len(y)-1)
        c=random.randint(0,len(imgArray)-1)
        imgToPaste=imgArray[c]
        xpos=x[a]
        ypos=y[b]
        x.pop(a)
        y.pop(b)
        imgArray.pop(c)
        result.paste(im=imgToPaste,box=(xpos*150,ypos*150))
    result.save("result.jpeg","JPEG")
    return ''

if __name__=="__main__":
    app.run(debug=True)