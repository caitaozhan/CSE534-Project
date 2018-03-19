CSE 534 Project

# Install Shadowsocks
### server-side:
wget --no-check-certificate -O shadowsocks-all.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh

chmod +x shadowsocks-all.sh

./shadowsocks-all.sh 2>&1 | tee shadowsocks-all.log

### client-side:
pip install shadowsocks

# Run Shadowsocks

### server-side
ssserver -c /etc/shadowsocks-python/config.json

OR

sudo /etc/init.d/shadowsocks-python start

### client-side
sslocal -s 45.32.154.172 -p 14392 -k 1234567890 -m rc4-md5

You need to input the correct parameters:

1. -s: server ip
2. -p: server port for shadowsocks process
3. -k: password
4. -m: encryt method


# Resources:

[Simple proxy using python](http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/)

[Shadowsocks：一个混淆工具](https://lixingcong.github.io/2015/08/31/shadowsocks_is_not_a_vpn/)

[Socks5 Protocal](https://www.ietf.org/rfc/rfc1928.txt)
[翻译](http://blog.csdn.net/whatday/article/details/39668233)

[SOCKS5协议的原理和应用](http://www.cppblog.com/noflybird/archive/2009/12/26/104149.html)

[SOCKS 5协议简析](https://geesun.github.io/posts/2015/09/socks5_protocol.html)

[一些实现思路](https://blog.codingnow.com/2011/05/xtunnel.html)

[你也能写个 Shadowsocks](https://segmentfault.com/a/1190000011862912)

[通过WireShark抓包学习SOCKS5协议](https://www.skyreal.me/tong-guo-wireshark-zhua-bao-xue-xi-socks5-xie-yi/)


# 大致构想

### Client:

1.Client和本地应用socks5握手。

Lightsocks是把握手信息也转发给代理服务器，服务器和本地应用握手，但shadowsocks是Client和本地应用握手，我觉得这样更省时间，而且感觉握手header长度信息太明显了。

2.Client转发
在Stream阶段，Client接受本地应用传来的socks5协议包裹好的包，然后加密转发到服务器。同时，收取代理服务器的数据，解密并转发给本地应用。

Lightsocks采用很简单的对称加密法，找一个1-256（一个字节的大小）的permutation，然后i变成其permutation中的第i位，只要知道permutation，就能解密，如果不知道，只能暴力枚举去解，我们可以采取这个简单的，不过加密模块可以独立出来，先不管这个。


### Server

1. Socks5协议unpack 和 pack
2. 监听端收到数据解密，unpack后获得真正信息，转发到目的地，同时读取返回的数据，pack，然后加密转发会客户端。

还没研究server端，大概的想法如下：
客户端和server端的socket连接要开着，对应的server段和目的端的连接要开着，等目的端没信息了再把两个连接断掉。


## Shadowsocks关键函数
```python
# tcprelay.py
def _on_local_read(self):
    ...
    try:
        data = self._local_sock.recv(BUF_SIZE) # 尝试读取本地应用传来的数据
    ...
    if not data:
        self.destroy() # 没有data就把连接关闭了
    ...
    if self._stage == STAGE_STREAM:
        self._handle_stage_stream(data)
    elif is_local and self._stage == STAGE_INIT:  
        self._handle_stage_init(data) # _handle_stage_init 只用在了这里，所以握手是Client和本地应用完成的。 
    ...
    elif (is_local and self._stage == STAGE_ADDR): # 还没看懂STAGE_ADDR是干嘛，看起来似乎是和UDP有关
    ...
```



