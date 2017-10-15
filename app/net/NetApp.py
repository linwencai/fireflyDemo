#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
from twisted.python import log
from twisted.internet import defer


# class NetCommandService(CommandService):
#     def callTargetSingle(self,targetKey,*args,**kw):
#         """call Target by Single
#         @param conn: client connection
#         @param targetKey: target ID
#         @param data: client data
#         """
#         self._lock.acquire()
#         try:
#             target = self.getTarget(0)
#             if not target:
#                 log.err('the command '+str(targetKey)+' not Found on service')
#                 return None
#             # if targetKey not in self.unDisplay:
#             #     log.msg("call method %s on service[single]"%target.__name__)
#             defer_data = target(targetKey,*args,**kw)
#             if not defer_data:
#                 return None
#             if isinstance(defer_data,defer.Deferred):
#                 return defer_data
#             d = defer.Deferred()
#             d.callback(defer_data)
#         finally:
#             self._lock.release()
#         return d
#
# netservice = NetCommandService("loginService")
#
# def netserviceHandle(target):
#     netservice.mapTarget(target)
#
# GlobalObject().netfactory.addServiceChannel(netservice)


from firefly.server.globalobject import netserviceHandle

def callTarget(self, targetKey, *args, **kw):
    target = self.getTarget(0)
    return target(targetKey, *args, **kw)
CommandService.callTarget = callTarget

@netserviceHandle
def Forwarding_0(key, _conn, data):
    '''转发服务器.用来接收客户端的消息转发给其他服务
    '''
    log.msg("Recv Key:%s dynamicId:%s data:%s" % (key, _conn.transport.sessionno, data))
    message = GlobalObject().remote['gate'].callRemote("forwarding", key, _conn.transport.sessionno, data)
    return message

