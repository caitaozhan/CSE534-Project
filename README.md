CSE 534 Project

# Install Shadowsocks
### server-side:
wget --no-check-certificate -O shadowsocks-all.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh

chmod +x shadowsocks-all.sh

./shadowsocks-all.sh 2>&1 | tee shadowsocks-all.log

### client-side:
sudo pip install shadowsocks

# Run Shadowsocks

### server-side
1. ssserver -c /etc/shadowsocks-python/config.json
2. sudo /etc/init.d/shadowsocks-python start

### client-side
sslocal -s 45.32.154.172 -p 14392 -k 1234567890 -m rc4-md5

You need to input the correct parameters:

-s: server ip

-p: server port for shadowsocks process

-k: password

-m: encryt method

