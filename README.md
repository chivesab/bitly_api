This application implements a clone of Bitly REST API using Python Flask framework, which includs these APIs

1. Shorten a link : 

2. Create a Bitlink

3. Update a Bitlink

4. Retrieve a Bitlink

5. Get Clicks for a Bitlink



## 1. Shorten a link API
#### Request:
    curl -H 'Content-Type: application/json' -X POST -d '{"long_url": "https://www.google.com"}' http://127.0.0.1:5000/shorten

#### Response
    {
      "deeplinks": [
        {
          "app_uri_path": "", 
          "install_type": ""
        }
      ], 
      "long_url": "https://www.google.com", 
      "shortened_url": "bit.ly/Sn0lDCxc02Hs", 
      "tags": [], 
      "title": ""
    }


## 2. Create a Bitlink
#### Request
    curl -H 'Content-Type:application/json' -X POST -d'{"long_url":"https://www.google.com","domain":"bit2.ly","title":"Bitl
    y API Documentation","tags":["bitly","api"],"deeplinks":[{"app_uri_path":"/store?id=123456","install_type":"promote_install"}]}' http://127.0.0.1:5000/bitlinks
#### Response

    {
      "deeplinks": [
        {
          "app_uri_path": "", 
          "install_type": ""
        }
      ], 
      "long_url": "https://www.google.com", 
      "shortened_url": "bit.ly/Sn0lDCxc02Hs", 
      "tags": [], 
      "title": ""
    }


## 3. Update a Bitlink
#### Request
    curl -H 'Content-Type: application/json' -X PATCH -d '{"link":"https://www.google.com","id":"bit.ly/documentation","long_url":"https://www.google.com","title":"BITLY","archived":false,"created_at":"","created_by":"YucheLin","tags":["bitly","api"],"deeplinks":[{"app_uri_path":"https://test","install_url":"ABDDDD","os":"Yosemite"}]}' http://127.0.0.1:5000/bitlinks/bit.ly/Sn0lDCxc02Hs


#### Response
    {
      "archived": false, 
      "client_id": "", 
      "created_at": "", 
      "created_by": "", 
      "custom_bitlinks": [
        ""
      ], 
      "deeplinks": [
        {
          "app_uri_path": "", 
          "bitlink": "", 
          "install_type": "", 
          "os": ""
        }
      ], 
      "id": "", 
      "link": "", 
      "long_url": "https://www.google.com", 
      "shortened_url": "bit.ly/Sn0lDCxc02Hs", 
      "tags": [
        ""
      ], 
      "title": ""
    }

## 4. Retrieve a Bitlink
#### Request
    curl -X GET http://127.0.0.1:5000/bitlinks/bit.ly/Sn0lDCxc02Hs

#### Response

    {
      "archived": "", 
      "click": 1, 
      "client_id": "", 
      "created_at": "Mon, 11 Oct 2021 02:03:08 GMT", 
      "created_by": "", 
      "deeplinks": [
        {
          "app_uri_path": "", 
          "install_type": "", 
          "install_url": "", 
          "os": ""
        }
      ], 
      "id": "", 
      "link": "", 
      "long_url": "https://www.google.com", 
      "shortened_url": "bit.ly/Sn0lDCxc02Hs", 
      "title": ""
    }


## 5. Get Clicks for a Bitlink
#### Request
    curl -X GET http://127.0.0.1:5000/bitlinks/bit.ly/Sn0lDCxc02Hs/clicks\?unit\=month\&units\=5\&unit_reference\=2006-01-02T15%3A04%3A05-0700
#### Response

    {
      "link_clicks": [
        {
          "clicks": 1, 
          "date": "Mon, 11 Oct 2021 02:05:03 GMT"
        }
      ], 
      "unit": "month", 
      "unit_reference": "2006-01-02T15:04:05-0700", 
      "units": "5"
    }

