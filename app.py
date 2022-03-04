from flask import Flask,request,jsonify
from converters.converter import Converters
import json

app = Flask(__name__)


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




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, threaded=True)
