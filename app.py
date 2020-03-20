from flask import Flask, request, Response, json, send_file
import requests
import os
from dotenv import load_dotenv
import urllib.request
from PIL import Image, ImageChops
import math
import random
from io import BytesIO

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
redirect_uri=os.getenv("REDIRECT_URI")

app=Flask(__name__)

sizeOfImage=60

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im

def processImg(image, imgArray):
    size=sizeOfImage, sizeOfImage
    image=trim(image)
    im_resized=image.resize(size, Image.BICUBIC)
    imgArray.append(im_resized)

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
        if response['media_type']=="IMAGE":
            image=Image.open(urllib.request.urlopen(response['media_url']))
            processImg(image,imgArray)
        elif response['media_type']=="CAROUSEL_ALBUM":
            for child in response['children']['data']:
                rtemp=requests.get(url='https://graph.instagram.com/'+str(child['id'])+'?fields=media_url,media_type,children&access_token='+str(access_token))
                responsetemp=rtemp.json()
                image=Image.open(urllib.request.urlopen(responsetemp['media_url']))
                processImg(image,imgArray)
    n=math.ceil(math.sqrt(len(imgArray)))
    result=Image.new('RGB',(sizeOfImage*n,sizeOfImage*n))#,(255,255,255))
    pos=[]
    for i in range(n):
        temp=[]
        for j in range(n):
            temp.append((i,j))
        pos.append(temp)
    while(len(imgArray)!=0):
        a=random.randint(0,len(pos)-1)
        b=random.randint(0,len(pos[a])-1)
        c=random.randint(0,len(imgArray)-1)
        imgToPaste=imgArray[c]
        xpos,ypos=pos[a][b]
        pos[a].pop(b)
        if(len(pos[a])==0):
            pos.pop(a)
        imgArray.pop(c)
        result.paste(im=imgToPaste,box=(xpos*sizeOfImage,ypos*sizeOfImage))
    toReturn=BytesIO()
    result.save(toReturn, 'JPEG', quality=70)
    toReturn.seek(0)
    return send_file(toReturn, mimetype='image/jpeg')

if __name__=="__main__":
    app.run(debug=True)