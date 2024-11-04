from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def echo_message():
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            return jsonify({key: value})
    else:
        data = request.data.decode("utf-8")
        return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)