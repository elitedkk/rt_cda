#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

from threading import Thread
from time import sleep

import traceback

from threading import Thread

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.handlers.GetTelemetryResourceHandler import GetTelemetryResourceHandler
from programmingtheiot.cda.connection.handlers.UpdateActuatorResourceHandler import UpdateActuatorResourceHandler
from programmingtheiot.cda.connection.handlers.GetSystemPerformanceResourceHandler import GetSystemPerformanceResourceHandler

class CoapServerAdapter():
	"""
	Definition for a CoAP communications server, with embedded test functions.
	
	"""
	
	def __init__(self, dataMsgListener = None):
		self.config = ConfigUtil()
		self.dataMsgListener = dataMsgListener
		self.enableConfirmedMsgs = False
		
		self.host = self.config.getProperty(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		self.port = self.config.getInteger(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_COAP_PORT)
		
		self.coapServer     = None
		self.coapServerTask = None
		
		# NOTE: the self.rootResource = None only used for aiocoap
		#self.rootResource   = None
		
		# NOTE: the self.listenTimeout = 30 only used for CoAPthon3
		self.listenTimeout = 30
		
		logging.info("CoAP server configured for host and port: coap://%s:%s", self.host, str(self.port))
		
	def addResource(self, resourcePath: ResourceNameEnum = None, endName: str = None, resource = None):
		pass
				
	def startServer(self):
		if self.coapServer:
			logging.info("Starting CoAP server...")
			
			if self.coapServerTask and self.coapServerTask.isAlive():
				self.stopServer()
				self.coapServerTask= None
				
			self.coapServerTask = Thread(target = self._runServer)
			self.coapServerTask.setDaemon(True)
			self.coapServerTask.start()
			
			logging.info("\n\n***** CoAP server started. *****\n\n")
		else:
			logging.warn("CoAP server not yet initialized (shouldn't happen).")
	
	def stopServer(self):
		if self.coapServer:
			logging.info("Stopping CoAP server...")
			
			self.coapServer.close()
			self.coapServerTask.join(5)
		else:
			logging.warn("CoAP server not yet initialized (shouldn't happen).")
	
	def _runServer(self):
		try:
			self.coapServer.listen(self.listenTimeout)
		except Exception as e:
			traceback.print_exception(type(e), e, e.__traceback__)
			logging.warn("Failed to run server.")
	
	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		pass
	
	def _initServer(self):
		pass
