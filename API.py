from flask import Flask, request, jsonify, send_file, url_for
from colorama import Fore
from Account.Authorization import *
from Server.get_info_server import *
from Server.GETuser import *
from Actions.vaild import *
from Actions.search import *
import psutil, platform, time, os, subprocess, json

Authorization = "credentials/Authorization.json"
app = Flask(__name__)
DEFAULT_UPLOAD_PATH = "uploads/"
PORT = ""
app.config['UPLOAD_FOLDER'] = DEFAULT_UPLOAD_PATH

if os.path.isfile(Authorization):
    with open(Authorization, "r") as Auth:
        file_content = Auth.read()
        if file_content.strip() == "":
            Key = KeyAuthorization()
            AuthorizationCode = SaveAuthorization(Key)
            print(f"{Fore.YELLOW}[+] {Fore.GREEN}Your Authorization Key Is : {Fore.BLUE}{AuthorizationCode}{Fore.RESET}")
        else:
            try:
                data = json.loads(file_content)
                AuthValue = data.get("Authorization", "")
                if not AuthValue:
                    Key = KeyAuthorization()
                    AuthorizationCode = SaveAuthorization(Key)
                    print(f"{Fore.YELLOW}[+] {Fore.GREEN}Your Authorization Key Is : {Fore.BLUE}{AuthorizationCode}{Fore.RESET}")
                else:
                    AuthorizationCode = AuthValue
                    print(f"{Fore.YELLOW}[+] {Fore.GREEN}Your Authorization Key Is : {Fore.BLUE}{AuthValue}{Fore.RESET}")
            except json.JSONDecodeError as e:
                print(f"{Fore.RED}[!] {Fore.RED}Error decoding JSON: {e}{Fore.RESET}")
    try:
        with open("SettingRunner/port.json", "r") as port:
            _port = port.read()
            if not _port.strip():
                raise ValueError("PORT is empty in port.json file")
            data = json.loads(_port)
            PORT = data.get("PORT", "")
            if not PORT:
                raise ValueError("PORT is empty in port.json file")
            print(f"{Fore.YELLOW}[+] {Fore.GREEN}Port is set to : {Fore.BLUE}{PORT}{Fore.RESET}")
    except FileNotFoundError:
        print(f"{Fore.RED}[!] {Fore.RED}The file 'port.json' does not exist.{Fore.RESET}")
    except (json.JSONDecodeError, ValueError) as e:
        PORT = input(f"{Fore.YELLOW}Enter port you want to run the API on: {Fore.GREEN}")
        print(f"{Fore.RESET}")       
        with open("SettingRunner/port.json", "w") as _w_port:
            json.dump({"PORT": PORT}, _w_port)
else:
    print(f"{Fore.YELLOW}[!] {Fore.RED}The file {Authorization} does not exist.{Fore.RESET}")

@app.route('/Account/Authorization', methods=['POST'])
def check_authorization():
    try:
        received_code = request.json.get('auth')

        if received_code == AuthorizationCode:
            return jsonify({'status': 'success', 'message': 'Authorization successful'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/SERVER', methods=['POST'])
def SERVER():
        return jsonify({'status': 'success', 'message': 'successful'}), 200

@app.route('/SERVER/get_info_server', methods=['POST'])
def get_info_server():
    received_code = request.json.get('auth')
    if received_code != AuthorizationCode:
        return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401

    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_logical_count = psutil.cpu_count(logical=True)
    ram_info = psutil.virtual_memory()
    disk_partitions = psutil.disk_partitions()
    disk_usage = [psutil.disk_usage(partition.mountpoint) for partition in disk_partitions]
    power_time = psutil.boot_time()
    uptime = round(time.time() - power_time)
    os_name = platform.system()
    os_version = platform.version()
    try:
        import GPUtil
        gpu_info = GPUtil.getGPUs()[0]
        gpu_name = gpu_info.name
        gpu_memory_total = gpu_info.memoryTotal
        gpu_memory_used = gpu_info.memoryUsed
    except ImportError:
        gpu_name = "N/A"
        gpu_memory_total = 0
        gpu_memory_used = 0

    return jsonify({
        'cpu_info': {
            'percent': int(cpu_percent),
            'count_physical': cpu_count,
            'count_logical': cpu_logical_count
        },
        'ram_info': {
            'percent': int(ram_info.percent),
            'total': format_size(ram_info.total),
            'used': format_size(ram_info.used)
        },
        'disk_info': [
            {
                'mountpoint': partition.mountpoint,
                'total': format_size(usage.total),
                'used': format_size(usage.used)
            } for partition, usage in zip(disk_partitions, disk_usage)
        ],
        'power_time': power_time,
        'uptime': uptime,
        'os_info': {
            'name': os_name,
            'version': os_version
        },
        'gpu_info': {
            'name': gpu_name,
            'memory_total': format_size(gpu_memory_total),
            'memory_used': format_size(gpu_memory_used)
        }
    }), 200

@app.route('/SERVER/get_username', methods=['POST'])
def get_username():
    received_code = request.json.get('auth')
    if received_code != AuthorizationCode:
        return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401

    user = GETuser()
    return jsonify({'username': user['username']})

@app.route('/Actions/command', methods=['POST'])
def command():
    received_code = request.json.get('auth')
    command = request.json.get('command')
    
    if received_code != AuthorizationCode:
        return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({'output': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.output, 'error': str(e)})

@app.route('/Actions/file_upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']

        upload_address = request.form.get('address')
        received_code = request.form.get('auth')

        if valid(upload_address):
            upload_path = f"uploads/{upload_address}/"
        else:
            upload_path = DEFAULT_UPLOAD_PATH

        if received_code != AuthorizationCode:
            return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401

        path_exists = os.path.exists(upload_path)
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, file.filename))

        response_message = {
            "status": "success",
            "message": "File uploaded successfully",
            "path": upload_path,
            "path_exists": path_exists,
        }

        return jsonify(response_message)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/Actions/file_search', methods=['POST'])
def search():

    received_code = request.json.get('auth')
    file_name = request.json.get('file_name')    
    if received_code != AuthorizationCode:
        return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401

    file_name = request.json['file_name']
    result = search_file(file_name)

    return jsonify(result)

@app.route('/Actions/file_download', methods=['POST'])
def download_file():
    received_code = request.json.get('auth')
    file_name = request.json.get('file_name')    
    
    if received_code != AuthorizationCode:
        return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401
    
    if os.path.isfile(file_name):
        download_url = url_for('download_file_endpoint', file_name=file_name, _external=True)
        return jsonify({'url': download_url+f'?auth={AuthorizationCode}'})
    else:
        return jsonify({'error': f'File not found: {file_name}'}), 404

@app.route('/Actions/download/<file_name>', methods=['GET'])
def download_file_endpoint(file_name):
    received_code = request.args.get('auth')  
    print("file_name : " + file_name)
    if received_code != AuthorizationCode:
        return jsonify({'status': 'error', 'message': 'Invalid authorization code'}), 401

    if os.path.isfile(file_name):
        return send_file(file_name, as_attachment=True)
    else:
        return jsonify({'error': f'File not found: {file_name}'}), 404

if __name__ == '__main__':
    app.run(port=PORT)
