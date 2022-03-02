from flask import Flask,request,jsonify
from parsers.simple_factory import SimpleFactory
from converters.converter import Converters
import json

app = Flask(__name__)


# @app.route('/')
# def test():
#     parser = SimpleFactory.product_parser(99, "test_files/aa.eml", "test_files/aa2.eml", "English", "Chinese")
# #     parser = SimpleFactory.product_parser(99, "test_files/attachment.eml", "test_files/attachment2.eml", "Chinese", "English")
#     parser.parse()
#     return 'hello'

@app.route('/convert_file', methods=['POST'])
def convert_file():
    ret = {}
    if request.method == 'POST':
        try:
            a = request.get_data()
            data = json.loads(a)
            convert_type = data['convert_type']
            src_file = data['src_file']
            c = Converters(convert_type, src_file)
            c.convert()
            ret["code"] = 200
            ret["msg"] = "success"
            return jsonify(ret)
        except Exception as e:
            ret["code"] = -1002
            ret['msg'] = e
            return jsonify(ret)
    else:
        ret["code"] = -1003
        return jsonify(ret)


@app.route('/trans_file', methods=['POST'])
def trans_file():
    ret = {}
    if request.method == 'POST':
        try:
            a = request.get_data()
            print(a)
            data = json.loads(a)
            row_id = data['row_id']
            src_lang = data['src_lang']
            des_lang = data['des_lang']
            src_file = data['src_file']
            des_file = data['des_file']
            parser = SimpleFactory.product_parser(row_id, src_file, des_file, src_lang, des_lang)
            parser.parse()
            ret["code"] = 200
            ret["msg"] = "success"
            return jsonify(ret)
        except Exception as e:
            ret['msg'] = e
            ret["code"] = -1002
            return jsonify(ret)
    else:
        ret["code"] = -1003
        return jsonify(ret)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, threaded=True)
