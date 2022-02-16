import hmac
import base64
import requests, json
import time
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

key_sign = "Today I want to eat noodle."
ProxyUrl = '192.168.3.32'
Port = 5000


def generate_sha1(content):
    digest_maker = hmac.new(key_sign.encode('utf-8'), b'', digestmod='sha1')
    digest_maker.update(content.encode('utf-8'))
    digest = digest_maker.digest()
    return base64.b64encode(digest).decode('utf-8')


def call_http(src_lang, des_lang, content):
    url = 'http://{0}:{1}/translate'.format(ProxyUrl, Port)
    now = time.time()  # 返回float数据
    now = int(now)
    format_str = "src_lang={0}&des_lang={1}&content={2}&timestamp={3}".format(src_lang, des_lang, content, now)
    sha1_str = generate_sha1(format_str)
    data_json = json.dumps({'src_lang': src_lang,
                            'des_lang': des_lang,
                            'content': content,
                            'timestamp': now,
                            'sign': sha1_str})
    resp = requests.post(url, data_json)
    data = json.loads(resp.text)
    if data['code'] == 200:
        return data['data']
    return ''


class API(object):

    @staticmethod
    def translate(src_lang, des_lang, content):
        format_str = "src_lang={0}&des_lang={1}&content={2}".format(src_lang, des_lang, content)
        sha1_str = generate_sha1(format_str)
        trans_content = r.get(sha1_str)
        if trans_content is None:
            trans_content = call_http(src_lang, des_lang, content)
            r.set(sha1_str, trans_content)
        return trans_content
