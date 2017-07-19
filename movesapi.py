from bottle import route, run, template, get, post, request
import secret #IDやトークンを管理
import requests
import json

def createURL(API):
'''
APIを呼びだすURLはここでまとめて管理
引数
    API : APIエントリポイントを示す文字列
返り値
    url : APIを呼び出すURL
'''
    if API=='OATH':
        url = 'https://api.moves-app.com/oauth/v1/authorize?response_type=code&client_id=' + secret.ClientID + '&scope=location activity'
    if API=='ACCESS':
        url = 'https://api.moves-app.com/oauth/v1/access_token'
    if API=='PROFILE':
        url = 'https://api.moves-app.com/api/1.1/user/profile?access_token=' + secret.readAccessToken()
    return url

@route('/getAuthorizationCode')
def getAuthorizationCode():
'''
認証キーを取得する
'''
    return template('getAuth', url=createURL('OATH'))

@get('/AuthorizationCode')
def AuthorizationCode():
'''
認証キーを発行したMOVESサーバーがこのURLを呼び出す
呼び出されたURLの中のcodeが認証キー
読み取った認証キーはsecret.py経由でINIファイルに保存する
'''
    my_dict = request.query.decode()
    myAuthCode = my_dict['code']
    secret.writeAuthCode(myAuthCode)
    return template('Authorization Code={{code}}', code = myAuthCode)

@route('/getAccessToken')
def getAccessToken():
'''
アクセストークンを取得する
POSTリクエストを送り，レスポンス(JSON)に含まれる
アクセストークンとリフレッシュトークンをsecret.py経由で
INIファイルに保存する
'''
    pars = {'grant_type':'authorization_code', 'code':secret.readAuthCode(), 'client_id':secret.ClientID,
            'client_secret':secret.Clientsecret, 'redirect_uri':'http://localhost:8080/AccessToken'}

    response = requests.post(createURL('ACCESS'), pars).json()

    secret.writeAccessToken(response["access_token"])
    secret.writeRefreshToken(response["refresh_token"])

    #return json.dumps(response)\
    return response


@route('/refreshToken')
def refreshToken():
'''
リフレッシュトークンを送り，新しいアクセストークンを取得する
アクセストークンとリフレッシュトークンをsecret.py経由で
INIファイルに保存する
'''
    pars = {'grant_type':'refresh_token', 'refresh_token':secret.readRefreshToken(), 'client_id':secret.ClientID,
            'client_secret':secret.Clientsecret}

    response = requests.post(createURL('ACCESS'), pars).json()

    secret.writeAccessToken(response["access_token"])
    secret.writeRefreshToken(response["refresh_token"])

    return json.dumps(response)

@route('/getProfile')
def getProfile():
'''
アクセストークンを使ってユーザープロファイルを取得する
取得したプロファイルはテンプレートを使ってHTMLで表示する
'''
    response = requests.get(createURL('PROFILE')).json()

    return template('userprofile',
                    userId = response["userId"],
                    firstDate = response["profile"]["firstDate"],
                    TZ = response["profile"]["currentTimeZone"]["id"] + "(GMT{:+.0f})".format(response["profile"]["currentTimeZone"]["offset"]/3600),
                    language = response["profile"]["localization"]["language"],
                    platform = response["profile"]["platform"],
    )




if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)




