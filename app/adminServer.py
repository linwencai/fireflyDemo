#coding:utf8
"""
Created on 2014-09-11
@author: Linwencai
"""

from twisted.web import resource
from twisted.python import log
from firefly.server.globalobject import GlobalObject, webserviceHandle
import json


@webserviceHandle("admin")
class admin(resource.Resource):
    def render(self, request):
        return """
            <form name="input" action="/GetUserInfo" method="get">
            uuid:
            <input type="text" name="uuid" />
            <input type="submit" value="Submit"/>
            </form>
            <form name="input" action="/GiveItem" method="get">
            uuid:
            <input type="text" name="uuid" />
            itemId:
            <input type="text" name="itemId" value="" />
            count:
            <input type="text" name="count" value="" />
            <input type="submit" value="Submit"/>
            </form>
            """

@webserviceHandle("test")
class gateToGame(resource.Resource):
    def render(self, request):
        message = GlobalObject().remote['gate'].callRemote("forwarding", 1, 1, "")
        return message
