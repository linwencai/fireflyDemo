# fireflyDemo

[![Build Status](https://img.shields.io/travis/rust-lang/rust/master.svg)]()
[![Python](https://img.shields.io/badge/Python-2.7-blue.svg)](https://www.python.org/)
[![Firefly](https://img.shields.io/badge/Firefy-1.3-yellowgreen.svg)](https://github.com/9miao/Firefly)

fireflyDemo是一个简单的游戏服务端Demo，基于[Firefly](https://github.com/9miao/Firefly) 框架，多进程单线程异步回调  

--------

## 环境
* Python2.7
* MySQL5.6+
* memcached


## 依赖
* affinity==0.1.0
* DBUtils==1.2
* firefly==1.3.3.dev0
* MySQL-python==1.2.5
* python-memcached==1.58
* six==1.11.0
* Twisted==14.0.0
* zope.interface==4.4.3


## 安装
* 安装Python、MySQL、memcached
* 执行tool目录下的install脚本，安装依赖、导入sql  

  ``` 
  # windows
  >>> install.bat

  # linux
  >>> sh install.sh
  ```

  
## 快速开始
1. 编辑config.json，配置端口、数据库
2. 运行服务端
  ```
  >>> python startmaster.py
  ```
3. 运行客户端模拟器
  ```
  >>> python tool/clienttest.py
  ```


 :relaxed: