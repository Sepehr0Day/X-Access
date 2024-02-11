# XAccess

XAccess is a Python package designed to facilitate remote server management and interaction. It consists of a client-side module for executing commands and managing files on a remote server and a server-side module for handling these commands and providing server information.

## Installation

You can install the client-side module via pip:

```
pip install XAccess
```

For the server-side module, you can clone the repository from GitHub:

```
git clone https://github.com/Sepehr0Day/XAccess.git
```

## Usage

### Server-side Usage

The server module runs on the server side to handle incoming requests and execute commands. Here's how you can set it up:

```bash
git clone https://github.com/Sepehr0Day/XAccess.git
cd XAccess
python3 install.py
screen python3 API.py | If run this command, after close window remote server process not kill
```

### Client-side Usage

The client module allows you to interact with remote servers. Here's how you can use it:

```python
from XAccess.Server import Server
from XAccess.Actions import Actions

# Initialize server object with IP, port, and authorization code
actions = Actions(server=Server(
    "X Session Name",
    ip="",
    port="",
    authorization="",
))

# Get server information
server_info = actions.server.get_info_server()
print(server_info)

```

## Next Update
- Add Panel Interface On Web
- Add Support For Windows Server (Just Web Panel)
  
## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Sepehr0Day/XAccess/blob/main/LICENSE) file for details.

<a href="https://pypi.org/project/DbUnify/"><img src="https://img.shields.io/badge/XAccess-1.0-blue"></a> 

## Developer
- **Telegram**: [t.me/Sepehr0Day](https://t.me/Sepehr0Day)

---

Feel free to contribute to the project or report any issues on the GitHub repository!
