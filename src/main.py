from Utils.api_docomo import reqTalkApi, reqTextSpeechApi
from Utils.audio import playWav
import time

if __name__ == '__main__':
    pass

input_word   = ''
context      = ''
mode         = 'dialog'
sleep_second = 0.5

while 1:
    # 入力値の取得
    input_word = input()

    # TalkAPIを呼び出し結果を取得
    res_talk   = reqTalkApi(input_word, context, mode)
    context    = res_talk['context']
    mode       = res_talk['mode']

    # 返信をテキスト出力
    print(res_talk["utt"])

    # 合成音声APIを呼び出し音声ファイルを作成
    talk_sound = reqTextSpeechApi(res_talk["utt"])

    # 音声ファイルを再生
    time.sleep(sleep_second)    # ファイル書き込みラグのため一時待機
    playWav(talk_sound)

    if input_word == 'またね':
        print('トークを終了します。ありがとうございました。')
        exit
