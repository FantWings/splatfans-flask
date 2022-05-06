import requests
import base64
import hashlib
import os
import json
import time
import uuid
import re
from crud.user import Users
from functions.loginrequired import loginRequired
from utils.database import db
from utils.redis import Redis

session = requests.session()

version = "1.7.1"
nsoapp_version = "2.0.0"

# 通用码
auth_code_verifier = base64.urlsafe_b64encode(os.urandom(32))


@loginRequired
def get_login_url(uid):
    '''生成登录链接'''

    link = Redis.read(f'{uid}/connect_link')
    if link:
        return {"data": link, "msg": "重复请求，从缓存中读取"}

    auth_state = base64.urlsafe_b64encode(os.urandom(36))

    auth_cv_hash = hashlib.sha256()
    auth_cv_hash.update(auth_code_verifier.replace(b"=", b""))
    auth_code_challenge = base64.urlsafe_b64encode(auth_cv_hash.digest())

    app_head = {
        'Host': 'accounts.nintendo.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8n',
        'DNT': '1',
        'Accept-Encoding': 'gzip,deflate,br',
    }

    body = {
        'state': auth_state,
        'redirect_uri': 'npf71b963c1b7b6d119://auth',
        'client_id': '71b963c1b7b6d119',
        'scope': 'openid user user.birthday user.mii user.screenName',
        'response_type': 'session_token_code',
        'session_token_code_challenge': auth_code_challenge.replace(b"=", b""),
        'session_token_code_challenge_method': 'S256',
        'theme': 'login_form'
    }

    url = 'https://accounts.nintendo.com/connect/1.0.0/authorize'
    response = session.get(url, headers=app_head, params=body)
    Redis.write(f'{uid}/connect_link', response.history[0].url, 120)
    return {"data": response.history[0].url}


@loginRequired
def get_session_token(uid, account_url):
    '''Helper function for log_in().'''
    session_token_code = re.search('de=(.*)&', account_url).group(1)

    # nsoapp_version = get_nsoapp_version()

    app_head = {
        'User-Agent': 'OnlineLounge/' + nsoapp_version + ' NASDKAPI Android',
        'Accept-Language': 'en-US',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '540',
        'Host': 'accounts.nintendo.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    body = {
        'client_id': '71b963c1b7b6d119',
        'session_token_code': session_token_code,
        'session_token_code_verifier': auth_code_verifier.replace(b"=", b"")
    }

    url = 'https://accounts.nintendo.com/connect/1.0.0/api/session_token'
    r = session.post(url, headers=app_head, data=body)
    QUERY_RESULT = Users.query.get(uid)
    try:
        QUERY_RESULT.session_token = json.loads(r.text)["session_token"]
    except Exception:
        {"status": 1, "msg": r.text}

    db.session.add(QUERY_RESULT)
    db.session.commit()

    return {"status": 0}


@loginRequired
def get_cookie(uid, userLang='en_US'):
    '''Returns a new cookie provided the session_token.'''

    QUERY_RESULT = Users.query.get(uid)
    session_token = QUERY_RESULT.session_token

    timestamp = int(time.time())
    guid = str(uuid.uuid4())

    app_head = {
        'Host': 'accounts.nintendo.com',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Language': userLang,
        'Content-Length': '439',
        'Accept': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'OnlineLounge/' + nsoapp_version + ' NASDKAPI Android'
    }

    body = {
        'client_id': '71b963c1b7b6d119',  # Splatoon 2 service
        'session_token': session_token,
        'grant_type':
        'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token'
    }

    url = "https://accounts.nintendo.com/connect/1.0.0/api/token"

    r = requests.post(url, headers=app_head, json=body)
    id_response = json.loads(r.text)

    # get user info
    try:
        app_head = {
            'User-Agent':
            'OnlineLounge/' + nsoapp_version + ' NASDKAPI Android',
            'Accept-Language': userLang,
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(id_response["access_token"]),
            'Host': 'api.accounts.nintendo.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
    except Exception:
        return {
            "status":
            1,
            "msg":
            f"Error from Nintendo (in api/token step):\
                {json.dumps(id_response, indent=2)}"
        }
    url = "https://api.accounts.nintendo.com/2.0.0/users/me"

    r = requests.get(url, headers=app_head)
    user_info = json.loads(r.text)

    nickname = user_info["nickname"]

    # get access token
    app_head = {
        'Host': 'api-lp1.znc.srv.nintendo.net',
        'Accept-Language': userLang,
        'User-Agent':
        'com.nintendo.znca/' + nsoapp_version + ' (Android/7.1.2)',
        'Accept': 'application/json',
        'X-ProductVersion': nsoapp_version,
        'Content-Type': 'application/json; charset=utf-8',
        'Connection': 'Keep-Alive',
        'Authorization': 'Bearer',
        # 'Content-Length':   '1036',
        'X-Platform': 'Android',
        'Accept-Encoding': 'gzip'
    }

    body = {}
    try:
        idToken = id_response["access_token"]

        flapg_nso = call_flapg_api(idToken, guid, timestamp, "nso")

        parameter = {
            'f': flapg_nso["f"],
            'naIdToken': flapg_nso["p1"],
            'timestamp': flapg_nso["p2"],
            'requestId': flapg_nso["p3"],
            'naCountry': user_info["country"],
            'naBirthday': user_info["birthday"],
            'language': user_info["language"]
        }
    except Exception as e:
        print(e)
        return {
            "status": 1,
            "msg": "Error(s) from Nintendo",
            "data": [id_response, user_info]
        }
    body["parameter"] = parameter

    url = "https://api-lp1.znc.srv.nintendo.net/v1/Account/Login"

    r = requests.post(url, headers=app_head, json=body)
    splatoon_token = json.loads(r.text)

    try:
        idToken = splatoon_token["result"]["webApiServerCredential"][
            "accessToken"]
        flapg_app = call_flapg_api(idToken, guid, timestamp, "app")
    except Exception:
        print("Error from Nintendo (in Account/Login step):")
        print(json.dumps(splatoon_token, indent=2))
        return {
            "status": 1,
            "msg": "Error from Nintendo (in Account/Login step)",
            "data": splatoon_token
        }

    # get splatoon access token
    try:
        app_head = {
            'Host':
            'api-lp1.znc.srv.nintendo.net',
            'User-Agent':
            'com.nintendo.znca/' + nsoapp_version + ' (Android/7.1.2)',
            'Accept':
            'application/json',
            'X-ProductVersion':
            nsoapp_version,
            'Content-Type':
            'application/json; charset=utf-8',
            'Connection':
            'Keep-Alive',
            'Authorization':
            'Bearer {}'.format(splatoon_token["result"]
                               ["webApiServerCredential"]["accessToken"]),
            'Content-Length':
            '37',
            'X-Platform':
            'Android',
            'Accept-Encoding':
            'gzip'
        }
    except Exception:
        print("Error from Nintendo (in Account/Login step):")
        print(json.dumps(splatoon_token, indent=2))
        return {
            "status":
            1,
            "msg":
            f"Error from Nintendo (in Account/Login step):\
                {json.dumps(splatoon_token, indent=2)}"
        }

    body = {}
    parameter = {
        'id': 5741031244955648,
        'f': flapg_app["f"],
        'registrationToken': flapg_app["p1"],
        'timestamp': flapg_app["p2"],
        'requestId': flapg_app["p3"]
    }
    body["parameter"] = parameter

    url = "https://api-lp1.znc.srv.nintendo.net/v2/Game/GetWebServiceToken"

    r = requests.post(url, headers=app_head, json=body)
    splatoon_access_token = json.loads(r.text)

    # get cookie
    try:
        app_head = {
            'Host': 'app.splatoon2.nintendo.net',
            'X-IsAppAnalyticsOptedIn': 'false',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate',
            'X-GameWebToken': splatoon_access_token["result"]["accessToken"],
            'Accept-Language': userLang,
            'X-IsAnalyticsOptedIn': 'false',
            'Connection': 'keep-alive',
            'DNT': '0',
            'User-Agent':
            'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
            'X-Requested-With': 'com.nintendo.znca'
        }
    except Exception:
        print("Error from Nintendo (in Game/GetWebServiceToken step):")
        print(json.dumps(splatoon_access_token, indent=2))
        return {
            "status":
            1,
            "msg":
            f"Error from Nintendo (in Game/GetWebServiceToken step):\
                {json.dumps(splatoon_access_token, indent=2)}"
        }

    url = f"https://app.splatoon2.nintendo.net/?lang={userLang}"
    r = requests.get(url, headers=app_head)

    QUERY_RESULT.nickname = nickname
    QUERY_RESULT.cookie = r.cookies["iksm_session"]

    db.session.add(QUERY_RESULT)
    db.session.commit()

    return {"status": 0}


def get_hash_from_s2s_api(id_token, timestamp):
    '''
    Passes an id_token and timestamp to the s2s API and
    fetches the resultant hash from the response.
    '''

    # proceed normally
    try:
        api_app_head = {'User-Agent': f"splatnet2statink/{version}"}
        api_body = {'naIdToken': id_token, 'timestamp': timestamp}
        api_response = requests.post("https://elifessler.com/s2s/api/gen2",
                                     headers=api_app_head,
                                     data=api_body)
        return json.loads(api_response.text)["hash"]
    except Exception:
        print("Error from the splatnet2statink API:\n{}".format(
            json.dumps(json.loads(api_response.text), indent=2)))


def call_flapg_api(id_token, guid, timestamp, type):
    '''
    Passes in headers to the flapg API (Android emulator)
    and fetches the response.
    '''

    try:
        api_app_head = {
            'x-token': id_token,
            'x-time': str(timestamp),
            'x-guid': guid,
            'x-hash': get_hash_from_s2s_api(id_token, timestamp),
            'x-ver': '3',
            'x-iid': type
        }
        api_response = requests.get("https://flapg.com/ika2/api/login?public",
                                    headers=api_app_head)
        f = json.loads(api_response.text)["result"]
        return f
    except Exception:
        try:  # if api_response never gets set
            if api_response.text:
                print(u"Error from the flapg API:\n{}".format(
                    json.dumps(json.loads(api_response.text),
                               indent=2,
                               ensure_ascii=False)))
            elif api_response.status_code == requests.codes.not_found:
                print("Error from the flapg API: Error 404\
                         (offline or incorrect headers).")
            else:
                print("Error from the flapg API: Error {}.".format(
                    api_response.status_code))
        except Exception:
            pass


@loginRequired
def unlink_account(uid):
    """取消链接账户"""
    QUERY_RESULT = Users.query.get(uid)
    QUERY_RESULT.cookie = None
    QUERY_RESULT.sessoin_token = None
    db.session.add(QUERY_RESULT)
    db.session.commit()

    return {}
