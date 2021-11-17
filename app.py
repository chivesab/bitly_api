from base64 import b64encode
from hashlib import blake2b
import random
import re
import collections
from datetime import datetime


from flask import Flask, abort, jsonify, redirect, request

app = Flask(__name__)

def url_valid(url):
    return re.match(regex, url) is not None


def shorten(url):
    url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    while url_hash in shortened:
        url += str(random.randint(0, 9))
        url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    b64 = b64encode(url_hash.digest(), altchars=b'-_')
    return b64.decode('utf-8')


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/shorten', methods=['POST'])
def shorten_url():
    if not request.json:
        return bad_request('Long url must be provided in json format.')
    
    if 'long_url' not in request.json:
        return bad_request('Long url parameter not found.')
    
    long_url = request.json['long_url']
    try:
        domain = request.json['domain']
        title = request.json['title']
        tags = request.json['tags']
        app_uri_path = request_json["app_uri_path"]
        install_type = request.json['install_type']
    except:
        domain = "bit.ly"
        title = ""
        tags = []
        app_uri_path = ""
        install_type = ""
    # For redirection purposes, we want to append http at some point.
    if long_url[:4] != 'http':
        long_url = 'http://' + long_url

    if not url_valid(long_url):
        return bad_request('Provided url is not valid.')

    shortened_url = domain + '/' + shorten(long_url)
    shortened[shortened_url] = long_url
    longurls[long_url] = shortened_url

    return jsonify({"long_url":long_url,"title":title,"tags":tags,"deeplinks":[{"app_uri_path":app_uri_path, "install_type":install_type}],'shortened_url' : shortened_url}), 201


@app.route('/shorten_url', methods=['GET'])
def shorten_url_get():
    return bad_request('Must use POST.')


@app.route('/bitlinks/<domain>/<alias>', methods=['GET'])
def retrieve_shorten_url(domain, alias):
    alias = domain + '/' + alias
    if alias not in shortened:
        return bad_request('Unknown alias.')
    click_dict[alias] = click_dict.get(alias, 0) + 1
    url = shortened[alias]
    count = click_dict[alias]
    now = datetime.now()
    #return jsonify({'shortened_url' : alias, "long_url":url,"click":count, "created_at":now}), 200
    return jsonify({"link":"", "id":"", "title":"","archived":"","created_at":now,"created_by":"","client_id":"","shortened_url":alias,
                    "long_url":url, "deeplinks":[{"app_uri_path":"","install_url":"","os":"","install_type":""}], "click":count}), 201
    # return redirect(url, code=302)

@app.route('/bitlinks/<domain>/<alias>', methods=['PATCH'])
def update_link(domain, alias):
    alias = domain + '/' + alias
    if alias not in shortened:
        return bad_request('Unknown alias.')
    long_url = shortened[alias]
    created_at = datetime.now()
    try:
        link = request.json['link']
        id = request.json['id']
        title = request.json['title']
        archived = request.json['archived']
        created_at = request.json['created_at']
        created_by = request.json['created_by']
        client_id = request.json["client_id"]
        custom_bitlinks = request.json["custom_bitlinks"]
        domain = request.json['domain']
        tags = request.json['tags']
        app_uri_path = request_json["deeplinks"][0]["app_uri_path"]
        install_type = request.json["deeplinks"][0]['install_type']
        bitlink = request.json["deeplinks"][0]["bitlink"]
        os = request.json["deeplinks"][0]["os"]
    except:
        link = ""
        id = ""
        title = ""
        archived = False
        created_at = ""
        created_by = ""
        client_id = ""
        custom_bitlinks = [""]
        domain = "bit.ly"
        tags = [""]
        app_uri_path = ""
        install_type = ""
        bitlink = ""
        os = ""
    return jsonify({"link":link, "id":id, "long_url":long_url,"title":title,"tags":tags,"custom_bitlinks":custom_bitlinks, "client_id":client_id,"created_at":created_at, "created_by":created_by,"archived":archived,
                    "deeplinks":[{"app_uri_path":app_uri_path, "install_type":install_type, "bitlink":bitlink, "os":os}],'shortened_url' : alias}), 201
 

@app.route('/bitlinks', methods=['POST'])
def create_short_link():
    if not request.json:
        return bad_request('Long url must be provided in json format.')
    
    long_url = request.json["long_url"]
    if "long_url" not in request.json:
        return bad_request('Long url parameter not found.')
    try:
        domain = request.json["domain"]
        title = request.json["title"]
        tags = request.json["tags"]
        app_uri_path = request_json["deeplinks"][0]["app_uri_path"]
        install_type = request.json["deeplinks"][0]["install_type"]
    except:
        domain = "bit.ly"
        title = ""
        tags = []
        app_uri_path = ""
        install_type = ""
    # For redirection purposes, we want to append http at some point.
    if long_url[:4] != 'http':
        long_url = 'http://' + long_url

    if not url_valid(long_url):
        return bad_request("Provided url is not valid.")

    shortened_url = domain + '/' + shorten(long_url)
    shortened[shortened_url] = long_url
    longurls[long_url] = shortened_url
    return jsonify({"long_url":long_url,"title":title,"tags":tags,"deeplinks":[{"app_uri_path":app_uri_path, "install_type":install_type}],"shortened_url" : shortened_url}), 201

@app.route('/bitlinks/<domain>/<alias>/clicks', methods=['GET'])
def get_click(domain, alias):
    alias = domain + '/' + alias
    print("shortened = ", shortened)
    if alias not in shortened:
        return bad_request('Unknown alias.')
    count = click_dict[alias]
    units = request.args.get("units")
    unit = request.args.get("unit")
    unit_reference = request.args.get("unit_reference")
    return jsonify({"link_clicks":[{"clicks":count, "date":datetime.now()}],"units":units,"unit":unit,"unit_reference":unit_reference}), 200

    
    




# Slightly modified to not use ftp.
regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
DIGEST_SIZE = 9 
click_dict = collections.defaultdict(int)
shortened = {}
longurls = {}

if __name__ == '__main__':
    app.run(debug=True)