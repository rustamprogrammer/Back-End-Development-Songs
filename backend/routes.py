from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

# client = MongoClient(
#     f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@localhost")
mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"


# Never log database credentials.

try:
    client = MongoClient(url)
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

db = client.songs
db.songs.create_index('id', unique=True)
for song in songs_list:
    db.songs.update_one({'id': song['id']}, {'$setOnInsert': song}, upsert=True)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################

@app.route('/health')
def health():
    client.admin.command('ping')
    return jsonify(status='OK'), 200

@app.route('/count')
def count():
    return jsonify(length=db.songs.count_documents({})), 200

@app.route('/song', methods=['GET'])
def get_songs():
    return jsonify(list(db.songs.find({}, {'_id': 0}))), 200

@app.route('/song/<int:id>', methods=['GET'])
def get_song(id):
    song = db.songs.find_one({'id': id}, {'_id': 0})
    return (jsonify(song), 200) if song else (jsonify(message='Song not found'), 404)

@app.route('/song', methods=['POST'])
def create_song():
    song = request.get_json(silent=True)
    if not isinstance(song, dict) or not isinstance(song.get('id'), int):
        return jsonify(message='A JSON object with an integer id is required'), 400
    if db.songs.find_one({'id': song['id']}):
        return jsonify(Message=f"song with id {song['id']} already present"), 302
    song.pop('_id', None)
    db.songs.insert_one(dict(song))
    return jsonify(song), 201

@app.route('/song/<int:id>', methods=['PUT'])
def update_song(id):
    song = request.get_json(silent=True)
    if not isinstance(song, dict):
        return jsonify(message='A JSON object is required'), 400
    song.pop('_id', None)
    song['id'] = id
    result = db.songs.replace_one({'id': id}, song)
    return (jsonify(song), 200) if result.matched_count else (jsonify(message='Song not found'), 404)

@app.route('/song/<int:id>', methods=['DELETE'])
def delete_song(id):
    result = db.songs.delete_one({'id': id})
    return ('', 204) if result.deleted_count else (jsonify(message='Song not found'), 404)
