import datetime
import requests
import json
import subprocess

if __name__ == '__api_docomo__':
    pass

TMP_PATH            = "C:/"
APIKEY              = "xxxx"
API_URL_TALK        = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY={}".format(APIKEY)
API_URL_TEXT_SPEECH = "https://api.apigw.smt.docomo.ne.jp/aiTalk/v1/textToSpeech?APIKEY={}".format(APIKEY)

def reqTalkApi(talk_text, context, mode):

    payload = {
        "nickname": "光",
        "nickname_y": "ヒカリ",
        "sex": "女",
        "bloodtype": "B",
        "birthdateY": "1997",
        "birthdateM": "5",
        "birthdateD": "30",
        "age": "16",
        "constellations": "双子座",
        "place": "東京",
    }
    payload["utt"]     = talk_text
    payload["context"] = context
    payload["mode"]    = mode
    req = requests.post(API_URL_TALK, data=json.dumps(payload))
    return req.json()

def reqTextSpeechApi(speech_text):
    prm = {
        'speaker' : 'nozomi',
        'pitch' : '1',
        'range' : '1',
        'rate' : '1',
        'volume' : '1.5'
    }

    # SSML生成
    # ===========================================
    xml = u'<?xml version="1.0" encoding="utf-8" ?>'
    voice = '<voice name="' + prm["speaker"] + '">'
    prosody = '<prosody rate="'+ prm['rate'] +'" pitch="'+ prm['pitch'] +'" range="'+ prm['range'] +'">'
    xml += '<speak version="1.1">'+ voice + prosody + speech_text + '</prosody></voice></speak>'

    # utf-8にエンコード
    xml = xml.encode("UTF-8")

    # headers
    headers = {
        'Content-Type': 'application/ssml+xml',
        'Accept' : 'audio/L16',
        'Content-Length' : str(len(xml))
    }

    # Docomo APIアクセス
    # ===========================================
    response = requests.post(
        API_URL_TEXT_SPEECH,
        data=xml,
        headers=headers
    )

    if response.status_code != 200 :
        print("Error API : " + response.status_code)
        exit()

    else :
        #現在日時を取得
        now = datetime.datetime.now()
        tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')

        #保存するファイル名
        rawFile = tstr + ".raw"
        wavFile = tstr + ".wav"

        #バイナリデータを保存
        fp = open(TMP_PATH + rawFile, 'wb')
        fp.write(response.content)
        fp.close()

        # バイナリデータ → wav に変換
        # ===========================================

        # macのsoxを使って raw→wavに変換
        cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 " + TMP_PATH + rawFile + " "+ TMP_PATH + wavFile
        # コマンドの実行
        subprocess.Popen(cmd, shell=True)
        return TMP_PATH + wavFile
