import base64
import hmac
import time

import json
import redis
import requests

key_sign = "Today I want to eat noodle."


def generate_sha1(content):
    digest_maker = hmac.new(key_sign.encode('utf-8'), b'', digestmod='sha1')
    digest_maker.update(content.encode('utf-8'))
    digest = digest_maker.digest()
    return base64.b64encode(digest).decode('utf-8')


def call_http(src_lang, des_lang, content):
    url = 'http://{0}:{1}/translate'.format("trans_core", 5000)
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


class TranslateAPI(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='trans_redis', port=6379, db=0, decode_responses=True, charset='UTF-8',
                                   encoding='UTF-8')

    def translate(self, src_lang, des_lang, content):
        format_str = "src_lang={0}&des_lang={1}&content={2}".format(src_lang, des_lang, content)
        sha1_str = generate_sha1(format_str)
        trans_content = self.r.get(sha1_str)
        if trans_content is None:
            trans_content = call_http(src_lang, des_lang, content)
            self.r.set(sha1_str, trans_content)
        return trans_content

    def close(self):
        self.r.close()


