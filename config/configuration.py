import json
import os
from util.util import rootPath

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = curPath[:curPath.rfind("Toolbox") + len("Toolbox")]  # Toolbox，也就是项目的根路径

config = dict()

def getConfig():
    global config
    with open(os.path.join(rootPath,r'config/configuration.json'), 'r', encoding='utf-8') as f:
        content = f.read()
        config = json.loads(content)

getConfig()
menus = config.get("menus",[])