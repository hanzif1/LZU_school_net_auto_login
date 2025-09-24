###功能介绍
说明：由于本人使用平板电脑远程主机，但主机会抽风掉线，故写出这个脚本。

本脚本是LZU自动连接校园网的脚本，支持开机自动连接和不知道什么原因突然被断掉连接的情况，脚本直接连接elearning账号（无流量上限限制），可以设置检测时间，默认为5分钟，可在代码的最后一行进行更改，单位为秒。

建议把.bat文件放到开机启动项里，操作方法如下：

1.按住win+R打开运行，输入shell:startup回车

2.将压缩包里的bat文件复制到打开的文件夹里

###使用说明：
1.注意更改bat文件中的命令，需要正确填写自己的conda路径和py文件存放的位置

2.注意更改auto_login.py文件中的账号密码，需要正确填写自己的账号密码

3.更改chromedriver的路径为自己的,chromedriver文件夹放到chrome安装目录下，如"C:\Program Files\Google\Chrome\Application\chromedriver-win64"

如果提示Chrome内核识别失败，需要检查自己的Chrome版本并去[Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/#stable) 找到属于自己的版本后用wget下载解压。
