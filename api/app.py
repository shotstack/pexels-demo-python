from flask      import Flask, request, current_app, jsonify
from .utilities import submit, status
app = Flask(
    __name__,
    static_url_path= '', 
    static_folder  = '../web'
)

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/demo/shotstack', methods = ['POST'])
def post_render():
    data  = request.json
    try:
        reply = submit(data)

        return jsonify({
            "status":   "success",
            "message":  "OK",
            "data":     {
                "id":       reply.id,
                "message":  reply.message
            }
        })
    except Exception as e:
        return jsonify({
            "status":   "fail",
            "message":  "Bad Request",
            "data":     e
        })

@app.route('/demo/shotstack/<renderId>')
def render(renderId):
    try:
        reply = status(renderId)

        return jsonify({
            "status":   "success",
            "message":  "OK",
            "data":     {
                "status":   reply.status,
                "url":      reply.url
            }
        })
    except Exception as e:
        return jsonify({
            "status":   "fail",
            "message":  "Bad Request",
            "data":     e
        })