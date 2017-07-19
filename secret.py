import configparser

CONFIG_FILE = 'movesapi.ini'
SECTION = 'MOVESAPI'

ini = configparser.ConfigParser()
ini.read(CONFIG_FILE)

ClientID = ini.get(SECTION, 'ClientID')
Clientsecret = ini.get(SECTION, 'Clientsecret')
AuthorizationCode = ini.get(SECTION, 'AuthorizationCode')

def writeAuthCode(AuthCode):
    ini.set(SECTION, 'AuthorizationCode', AuthCode)
    with open(CONFIG_FILE, "w", encoding='utf8') as f:
        ini.write(f)

def writeAccessToken(AccessToken):
    ini.set(SECTION, 'AccessToken', AccessToken)
    with open(CONFIG_FILE, "w", encoding='utf8') as f:
        ini.write(f)

def writeRefreshToken(RefreshToken):
    ini.set(SECTION, 'RefreshToken', RefreshToken)
    with open(CONFIG_FILE, "w", encoding='utf8') as f:
        ini.write(f)


def readAuthCode():
    return ini.get(SECTION, 'AuthorizationCode')

def readAccessToken():
    return ini.get(SECTION, 'AccessToken')

def readRefreshToken():
    return ini.get(SECTION, 'RefreshToken')



if __name__ == '__main__':
    print('Client ID = ', ClientID, ', Client secret = ', Clientsecret, ', Authorization Code = ', AuthorizationCode)

