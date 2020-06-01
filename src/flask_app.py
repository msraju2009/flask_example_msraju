from flask import Flask, jsonify, request
from multiprocessing import Value
import subprocess, sys, os

counter = Value('i', 0)
app = Flask(__name__)


@app.route('/counter', methods=["GET", "POST", "DELETE"])
def index():
    if request.method == "GET":
        with counter.get_lock():
            counter.value += 1
            output = counter.value
        return jsonify(count=output)
    elif request.method == "POST":
        with counter.get_lock():
            counter.value += 2
            output = counter.value
        return jsonify(count=output)
    elif request.method == "DELETE":
        with counter.get_lock():
            counter.value -= 1
            output = counter.value
        return jsonify(count=output)


@app.route("/info", methods=["GET"])
def development_info():
    # specify the path where git repository exists
    file_path = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(os.path.join("C","Users","Administrator","Documents","GitHub","RP-demo"))
    os.chdir(file_path)
    development_info = {}
    try:
        development_info["git_hash_code"] = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    except Exception as e:
        print("Exception occurred while fetching git hash code , below is exception \n {}".format(e))
    try:
        development_info["git_private_branch_name"] = subprocess.check_output(
            ['git', 'symbolic-ref', '--short', 'HEAD']).strip()
    except Exception as e:
        print("Exception occurred while fetching git branch name , below is exception \n {}".format(e))
    try:
        development_info["python_environment_name"] = sys.prefix
    except Exception as e:
        print("Exception occurred while fetching python environment name , below is exception \n {}".format(e))
    try:
        development_info["hostname"] = subprocess.check_output(['hostname']).strip()
    except Exception as e:
        print("Exception occurred while fetching HOSTNAME , below is exception \n {}".format(e))
    return jsonify(development_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
