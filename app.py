# ライブラリのインポート
import os
from google.cloud import texttospeech
import streamlit as st

# 環境設定
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'
os.environ['GRPC_PYTHON_BUILD_SYSTEM_OPENSSL'] = '1'
os.environ['GRPC_PYTHON_BUILD_SYSTEM_ZLIB'] = '1'

def synthesize_speech(text, lang='日本語', gender='男性'):
    """テキストから音声を生成する

    Args:
        text (str): テキスト
        lang (str, optional): 音声の言語. Defaults to '日本語'.
        gender (str, optional): 話者の性別. Defaults to '男性'.

    Returns:
        dict: 生成された音声データ
    """
    # 設定
    gender_type = {
        '男性': {
            '英語':'en-US-News-M',
            '日本語':'ja-JP-Standard-C', 
            'ssml_gender':texttospeech.SsmlVoiceGender.MALE
        },
        '女性': {
            '英語':'en-US-News-L',
            '日本語':'ja-JP-Standard-B', 
            'ssml_gender':texttospeech.SsmlVoiceGender.FEMALE
        }
    }
    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }

    # 認証
    client = texttospeech.TextToSpeechClient()

    # 音声合成のための設定
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang],name=gender_type[gender][lang], ssml_gender=gender_type[gender]['ssml_gender']
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response

st.title('音声出力アプリ')

# データの準備
st.markdown('### データ準備')
input_option = st.selectbox(
    '入力データの選択',
    ('直接入力', 'テキストファイル')
)
input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力してください。', 'Cloud Speech-to-Text用のサンプル文になります。')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください。', ['txt'])    
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

# 入力データの表示
if input_data is not None:
    st.write('入力データ')
    st.write(input_data)

    # パラメータ設定
    st.markdown('### パラメータ設定')
    st.subheader('言語と話者の性別選択')
    lang = st.selectbox(
        '言語を選択してください',
        ('日本語', '英語')
    )
    gender = st.selectbox(
        '話者の性別を選択してください',
        ('男性', '女性')
    )

    # 音声合成
    st.markdown('### 音声合成')
    st.write('こちらの文章で音声ファイルの生成を行いますか？')
    try:
        if st.button('開始'):
            comment = st.empty()
            comment.write('音声出力を開始します')
            response = synthesize_speech(input_data, lang=lang, gender=gender)
            st.audio(response.audio_content)
            comment.write('完了しました')
    except:
        st.error(
            "不具合が発生しています！リロードし直してみてください。"
        )