from flask import Flask,request
from models.simple_factory import SimpleFactory
from api.api import API
app = Flask(__name__)


@app.route('/trans_file')
def trans_file():
    if request.method == 'POST':
        try:
            a = request.get_data()
            data = json.loads(a)
            src_lang = data['src_lang']
            des_lang = data['des_lang']
            src_file = data['src_file']
            des_file = data['des_file']
            parser = SimpleFactory.product_parser(src_file, des_file, src_lang, des_lang)
            parser.parse()
            ret = {}
            ret["code"] = 200
            ret["msg"] = "success"
            return jsonify(ret)
        except:
            ret = {}
            ret["code"] = -1002
            return jsonify(ret)
    else:
        ret = {}
        ret["code"] = -1003
        return jsonify(ret)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, threaded=True)
