# Phishing Sender

## 介绍

Phishing sender是一款针对钓鱼邮件应急演练所编写的小脚本，实际上是封装了swaks，让人们做演练的时候更加方便快捷。



## 特性

1. 花里胡哨版swaks
2. 多线程发件



## 参数

``` bash
 -h, --help            查看命令帮助
  --fromMail FROMMAIL, -f FROMMAIL
                        指定发件人
  --toMail TOMAIL, -to TOMAIL
                        指定收件人或收件人文件夹（格式：每行一个邮箱地址）
  --eml EML, -e EML     指定邮件正文文件（eml文件）
  --mode {lan,wan,proxy}, -m {lan,wan,proxy}
                        设置发送模式，取值范围{lan,wan,proxy}，分别代表{局域网, 互联网, 代理}
  --username USERNAME, -u USERNAME
                        指定发件服务器的smtp用户（使用代理模式时需要设置）
  --password PASSWORD, -p PASSWORD
                        指定发件服务器的smtp密码（使用代理模式时需要设置）
  --server SERVER, -s SERVER
                        指定发件服务器地址（使用代理模式时需要设置）
  --thread THREAD, -t THREAD
                        指定线程数（默认5个线程）

```



## 使用

**局域网发件模式**

在客户现场接入局域网，且网络可达smtp服务器。

```
python3 sender.py -f hr@test.com -to to@test.com -e test.eml -m lan -s smtp.test.com
```

**互联网发件模式**

在互联网上发送邮件，如客户有邮件网关等设备需要加白名单，不然会被拦截。

```
python3 sender.py -f hr@test.com -to to@test.com -e test.eml -m wan
```

**代理转发模式**

在互联网上发送邮件，可绕过部分邮件网关设备，不需要加白名单。缺点：速度较慢

```
python3 sender.py -f hr@test.com -to to@test.com -e test.eml -m proxy -u smtpuser -p smtppass -s smtpServer
```



## 免责声明

本工具仅限于在合法授权的情况下用于企业安全建设，在使用本工具过程中，您应确保自己所有行为符合当地的法律法规，并且已经取得了足够的授权。 如您在使用本工具的过程中存在任何非法行为，您需自行承担所有后果，本工具所有作者和所有贡献者不承担任何法律及连带责任。 除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要安装并使用本工具。 您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。