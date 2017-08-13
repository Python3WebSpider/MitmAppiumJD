import json
import pymongo
from urllib.parse import unquote
import re

client = pymongo.MongoClient('localhost')
db = client['jd']
comments_collection = db['comments']
products_collection = db['products']

def response(flow):
    global comments_collection, products_collection
    url = 'api.m.jd.com/client.action'
    if url in flow.request.url:
        pattern = re.compile('sku\".*?\"(\d+)\"')
        body = unquote(flow.request.text)
        id = re.search(pattern, body).group(1) if re.search(pattern, body) else None
        text = flow.response.text
        data = json.loads(text)
        comments = data.get('commentInfoList') or []
        for comment in comments:
            if comment.get('commentInfo') and comment.get('commentInfo').get('commentData'):
                info = comment.get('commentInfo')
                text = info.get('commentData')
                date = info.get('commentDate')
                nickname = info.get('userNickName')
                pictures = info.get('pictureInfoList')
                print(text, date)
                comments_collection.insert({
                    'id': id,
                    'text': text,
                    'date': date,
                    'nickname': nickname,
                    'pictures': pictures
                })
    url = 'cdnware.m.jd.com'
    if url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        if data.get('wareInfo') and data.get('wareInfo').get('basicInfo'):
            info = data.get('wareInfo').get('basicInfo')
            id = info.get('wareId')
            name = info.get('name')
            images = info.get('wareImage')
            print(id, name, images)
            products_collection.insert({
                'id': id,
                'name': name,
                'images': images
            })