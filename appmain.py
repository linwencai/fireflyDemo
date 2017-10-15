#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""

import os
if os.name!='nt' and os.name!='posix':
    from twisted.internet import epollreactor
    epollreactor.install()

import json,sys
from firefly.server.server import FFServer

# 支持websocket
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol, ServerFactory
from firefly.netconnect.protoc import DefferedErrorHandle
import hashlib, struct, base64
from datetime import datetime
from json import loads

class Broadcaster(Protocol):
    def __init__(self, sockets):
        self.sockets = sockets

    def connectionMade(self):
        if not self.sockets.has_key(self):
            self.sockets[self] = {}
        print datetime.now(), "connect:", self.transport.sessionno, "count:", len(self.sockets)
        # self.transport.loseConnection()

    def dataReceived(self, msg):
        if msg.lower().find('upgrade: websocket') != -1:
            self.hand_shake(msg)
        else:
            raw_str = self.parse_recv_data(msg)
            # from json import dumps
            # from time import time
            # try:
            #     data = {"time": time(), "data": str(raw_str)}
            #     data = dumps(data)
            # except BaseException as err:
            #     print "Err:", err, "Raw_str:", raw_str
            #     data = "Error code:%s" % repr(raw_str)
            # self.send_data(data)
            if not raw_str:
                return

            key, dataStr = raw_str.split(" ", 1)
            deferred = GlobalObject().remote['gate'].callRemote("forwarding", int(key), self.transport.sessionno, dataStr)

            if deferred:
                deferred.addCallback(self.send_data)
                deferred.addErrback(DefferedErrorHandle)

            # self.send_data(str(message))
            # return message

    def connectionLost(self, reason):
        if self.sockets.has_key(self):
            del self.sockets[self]
        print datetime.now(), "lost:", self.transport.sessionno
        return

    def closeConnection(self):
        if self.sockets.has_key(self):
            del self.sockets[self]
        print datetime.now(), "close:", self.transport.sessionno
        return

    def generate_token(self, key1, key2, key3):
        num1 = int("".join([digit for digit in list(key1) if digit.isdigit()]))
        spaces1 = len([char for char in list(key1) if char == " "])
        num2 = int("".join([digit for digit in list(key2) if digit.isdigit()]))
        spaces2 = len([char for char in list(key2) if char == " "])

        combined = struct.pack(">II", num1/spaces1, num2/spaces2) + key3
        return hashlib.md5(combined).digest()

    def generate_token_2(self, key):
        key = key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ser_key = hashlib.sha1(key).digest()

        return base64.b64encode(ser_key)

    def send_data(self, raw_str):
        if self.sockets[self]['new_version']:
            back_str = []
            back_str.append('\x81')
            data_length = len(raw_str)

            if data_length <= 125:
                back_str.append(chr(data_length))
            else:
                back_str.append(chr(126))
                back_str.append(chr(data_length >> 8))
                back_str.append(chr(data_length & 0xFF))

            back_str = "".join(back_str) + raw_str

            self.transport.write(back_str)
        else:
            back_str = '\x00%s\xFF' % (raw_str)
            self.transport.write(back_str)

    def parse_recv_data(self, msg):
        raw_str = ''

        if self.sockets[self]['new_version']:
            code_length = ord(msg[1]) & 127

            if code_length == 126:
                masks = msg[4:8]
                data = msg[8:]
            elif code_length == 127:
                masks = msg[10:14]
                data = msg[14:]
            else:
                masks = msg[2:6]
                data = msg[6:]

            i = 0
            for d in data:
                raw_str += chr(ord(d) ^ ord(masks[i%4]))
                i += 1
        else:
            raw_str = msg.split("\xFF")[0][1:]

        return raw_str

    def hand_shake(self, msg):
        headers = {}
        header, data = msg.split('\r\n\r\n', 1)
        for line in header.split('\r\n')[1:]:
            key, value = line.split(": ", 1)
            headers[key] = value

        headers["Location"] = "ws://%s/" % headers["Host"]

        if headers.has_key('Sec-WebSocket-Key1'):
            key1 = headers["Sec-WebSocket-Key1"]
            key2 = headers["Sec-WebSocket-Key2"]
            key3 = data[:8]

            token = self.generate_token(key1, key2, key3)

            handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Origin: %s\r\n\
Sec-WebSocket-Location: %s\r\n\r\n\
' %(headers['Origin'], headers['Location'])

            self.transport.write(handshake + token)

            self.sockets[self]['new_version'] = False
        else:
            key = headers['Sec-WebSocket-Key']
            token = self.generate_token_2(key)

            handshake = '\
HTTP/1.1 101 Switching Protocols\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n\
' % (token)
            self.transport.write(handshake)

            self.sockets[self]['new_version'] = True

class BroadcastFactory(ServerFactory):
    def __init__(self):
        self.sockets = {}

    def buildProtocol(self, addr):
        return Broadcaster(self.sockets)


from firefly.netconnect.protoc import LiberateFactory
from twisted.web import vhost
from firefly.web.delayrequest import DelaySite
from firefly.distributed.root import PBRoot,BilateralFactory
from firefly.distributed.node import RemoteObject
from firefly.dbentrust.dbpool import dbpool
from firefly.dbentrust.memclient import mclient
from firefly.server.logobj import loogoo
from firefly.server.globalobject import GlobalObject
from twisted.python import log
#from twisted.internet import reactor
from firefly.utils import services
import os,sys,affinity


def config(self, config, servername=None, dbconfig=None,
            memconfig=None, masterconf=None):
    '''配置服务器
    '''
    GlobalObject().json_config = config
    webSocketPost = config.get("webSocketPort")  # webSocket端口
    netport = config.get('netport')#客户端连接
    webport = config.get('webport')#http连接
    rootport = config.get('rootport')#root节点配置
    self.remoteportlist = config.get('remoteport',[])#remote节点配置列表
    if not servername:
        servername = config.get('name')#服务器名称
    logpath = config.get('log')#日志
    hasdb = config.get('db')#数据库连接
    hasmem = config.get('mem')#memcached连接
    app = config.get('app')#入口模块名称
    cpuid = config.get('cpu')#绑定cpu
    mreload = config.get('reload')#重新加载模块名称
    self.servername = servername
    if masterconf:
        masterport = masterconf.get('rootport')
        masterhost = masterconf.get('roothost')
        self.master_remote = RemoteObject(servername)
        addr = ('localhost',masterport) if not masterhost else (masterhost,masterport)
        self.master_remote.connect(addr)
        GlobalObject().masterremote = self.master_remote

    if netport:
        self.netfactory = LiberateFactory()
        netservice = services.CommandService("netservice")
        self.netfactory.addServiceChannel(netservice)
        reactor.listenTCP(netport,self.netfactory)
        reactor.listenTCP(netport,self.netfactory,interface='::')  # ipv6

    if webport:
        self.webroot = vhost.NameVirtualHost()
        GlobalObject().webroot = self.webroot
        reactor.listenTCP(webport, DelaySite(self.webroot))
        reactor.listenTCP(webport, DelaySite(self.webroot),interface='::')  # ipv6

    if rootport:
        self.root = PBRoot()
        rootservice = services.Service("rootservice")
        self.root.addServiceChannel(rootservice)
        reactor.listenTCP(rootport, BilateralFactory(self.root))

    if webSocketPost:
        reactor.listenTCP(webSocketPost, BroadcastFactory())
        reactor.listenTCP(webSocketPost, BroadcastFactory(),interface='::')  # ipv6

    for cnf in self.remoteportlist:
        rname = cnf.get('rootname')
        self.remote[rname] = RemoteObject(self.servername)

    if hasdb and dbconfig:
        log.msg(str(dbconfig))
        dbpool.initPool(**dbconfig)

    if hasmem and memconfig:
        urls = memconfig.get('urls')
        hostname = str(memconfig.get('hostname'))
        mclient.connect(urls, hostname)

    if logpath:
        log.addObserver(loogoo(logpath))#日志处理
    log.startLogging(sys.stdout)

    if cpuid:
        affinity.set_process_affinity_mask(os.getpid(), cpuid)
    GlobalObject().config(netfactory = self.netfactory, root=self.root,
                remote = self.remote)
    if app:
        __import__(app)
    if mreload:
        _path_list = mreload.split(".")
        GlobalObject().reloadmodule = __import__(mreload,fromlist=_path_list[:1])
    GlobalObject().remote_connect = self.remote_connect
    import firefly.server.admin
FFServer.config = config


if __name__=="__main__":
    args = sys.argv
    servername = None
    config = None
    if len(args)>2:
        servername = args[1]
        config = json.load(open(args[2],'r'))
    else:
        raise ValueError
    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers',{})
    masterconf = config.get('master',{})
    serconfig = sersconf.get(servername)
    ser = FFServer()
    ser.config(serconfig, servername=servername, dbconfig=dbconf, memconfig=memconf, masterconf=masterconf)
    ser.start()
    
    
