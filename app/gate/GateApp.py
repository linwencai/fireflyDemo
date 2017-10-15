#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from json import dumps
from twisted.python import log
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
from twisted.internet import defer


class LocalService(CommandService):
    def callTargetSingle(self, targetKey, *args, **kw):
        """call Target by Single
        @param conn: client connection
        @param targetKey: target ID
        @param data: client data
        """

        self._lock.acquire()
        try:
            target = self.getTarget(targetKey)
            if not target:
                log.err('the command ' + str(targetKey) + ' not Found on service')
                return None
            # if targetKey not in self.unDisplay:
            #     log.msg("call method %s on service[single]" % target.__name__)
            defer_data = target(targetKey, *args, **kw)
            if not defer_data:
                return None
            if isinstance(defer_data, defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d
localservice = LocalService('localservice')


def localserviceHandle(target):
    """服务处理
    @param target: func Object
    """
    localservice.mapTarget(target)


def SendMessage(state, message, topicID=0, dynamicIdList=None):
    """ 返回消息
    :param state: 返回的状态
    :param message: 返回的消息
    :param topicID: 协议号
    :param dynamicIdList: 推送的客户端Id列表
    :return:
    """
    jsonData = dumps({'State': state, 'Data': message}, separators=(',', ':'))
    if dynamicIdList:
        GlobalObject().root.callChild("net", "pushObject", topicID, jsonData, dynamicIdList)
    return jsonData
