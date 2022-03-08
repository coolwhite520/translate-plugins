from flask import Flask,request,jsonify
import json
import subprocess
import os
from pdf2docx import Converter



app = Flask(__name__)

def p2dx(src_file):
    des_file = os.path.splitext(src_file)[0] + ".docx"
    cv = Converter(src_file)
    cv.convert(des_file)
    cv.close()

@app.route('/convert_file', methods=['POST'])
def convert_file():
    ret = {}
    if request.method == 'POST':
        try:
            a = request.get_data()
            data = json.loads(a)
            convert_type = data['convert_type']
            src_file = data['src_file']
            if convert_type == 'p2dx':
                p2dx(src_file)
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
