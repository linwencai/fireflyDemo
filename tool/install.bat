pip install affinity==0.1.0
pip install six==1.11.0
pip install zope.interface==4.4.3
pip install Twisted==14.0.0
pip install python-memcached
easy_install MySQL-python
pip install DBUtils
pip install firefly
@rem easy_install https://ncu.dl.sourceforge.net/project/pywin32/pywin32/Build%20220/pywin32-220.win32-py2.7.exe
pip install pypiwin32
@echo import sql?
@pause
mysql -uroot -p < mysql.sql
@echo success!