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
