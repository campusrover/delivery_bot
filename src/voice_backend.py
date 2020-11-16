from flask import Flask, request, jsonify, Response
import rospy
from std_msgs.msg import String

app = Flask(__name__)


@app.route('/')
def backend_entrance():
    return Response(status=200)

@app.route('/deliver', methods=['GET', 'POST'])
def deliver():
    print(request.data)
    return "received"

if __name__ == '__main__':
    app.run()