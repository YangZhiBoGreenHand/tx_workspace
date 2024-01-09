
from app.base import app
# 注册试图
from app.blueprints import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
