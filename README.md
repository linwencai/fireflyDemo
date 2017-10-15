# fireflyDemo

[![Build Status](https://img.shields.io/travis/rust-lang/rust/master.svg)]()
[![Python](https://img.shields.io/badge/Python-2.7-blue.svg)](https://www.python.org/)
[![Firefly](https://img.shields.io/badge/Firefy-1.3-yellowgreen.svg)](https://github.com/9miao/Firefly)

fireflyDemo��һ���򵥵���Ϸ�����Demo������[Firefly](https://github.com/9miao/Firefly) ��ܣ�����̵��߳��첽�ص�  

--------

## ����
* Python2.7
* MySQL5.6+
* memcached


## ����
* affinity==0.1.0
* DBUtils==1.2
* firefly==1.3.3.dev0
* MySQL-python==1.2.5
* python-memcached==1.58
* six==1.11.0
* Twisted==14.0.0
* zope.interface==4.4.3


## ��װ
* ��װPython��MySQL��memcached
* ִ��toolĿ¼�µ�install�ű�����װ����������sql  

  ``` 
  # windows
  >>> install.bat

  # linux
  >>> sh install.sh
  ```

  
## ���ٿ�ʼ
1. �༭config.json�����ö˿ڡ����ݿ�
2. ���з����
  ```
  >>> python startmaster.py
  ```
3. ���пͻ���ģ����
  ```
  >>> python tool/clienttest.py
  ```


 :relaxed: