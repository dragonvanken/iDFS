import socket

def getEthIp():
    """返回本机局域网IP地址(str)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.0.1", 80))
    return s.getsockname()[0]

def getOpenPort():
    """选取一个空闲的端口并返回端口号(int)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return int(port)