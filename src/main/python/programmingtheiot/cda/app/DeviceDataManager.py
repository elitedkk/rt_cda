#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
from programmingtheiot.cda.connection.CoapServerAdapter import CoapServerAdapter
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from future.backports.xmlrpc.client import boolean

class DeviceDataManager(IDataMessageListener):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self):
		self.configUtil = ConfigUtil()
		logging.info('Initialiazing Device Data Manager')
		self.sysPerfMgr = SystemPerformanceManager()
		self.sysPerfMgr.setDataMessageListener(self)
		
		self.sensorAdapterMgr = SensorAdapterManager()
		self.sensorAdapterMgr.setDataMessageListener(self)
		
		self.actuatorAdapterMgr = ActuatorAdapterManager()
		self.actuatorAdapterMgr.setDataMessageListener(self)
		
		self.handleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
		self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY);
		self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY);
		self.enableMqttClient = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_MQTT_CLIENT_KEY)
				
		self.mqttClient = None
		logging.debug('MQTT enabled = ' + str(self.enableMqttClient))
		if self.enableMqttClient:
			self.mqttClient = MqttClientConnector()
			self.mqttClient.setDataMessageListener(self)
		
		self.enableCoapClient = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_COAP_CLIENT_KEY)
		
		logging.debug('CoAP enabled = ' + str(self.enableCoapClient))
		if self.enableCoapClient :
			self.coapClient = CoapClientConnector(dataMsgListener = self)
		
		
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		
		@param name
		@return ActuatorData
		"""
		pass
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		
		@param name
		@return SensorData
		"""
		pass
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		
		@param name
		@return SystemPerformanceData
		"""
		pass
	
	def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
		"""
		This callback method will be invoked by the connection that's handling
		an incoming ActuatorData command message.
		
		@param data The incoming ActuatorData command message.
		@return boolean
		"""
		if data:
			logging.info("Processing actuator command message.")
			
			# TODO: add further validation before sending the command
			return self.actuatorAdapterMgr.sendActuatorCommand(data)
		else:
			logging.warning("Received invalid ActuatorData command message. Ignoring.")
			return None
	
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		"""
		This callback method will be invoked by the actuator manager that just
		processed an ActuatorData command, which creates a new ActuatorData
		instance and sets it as a response before calling this method.
		
		@param data The incoming ActuatorData response message.
		@return boolean
		"""
		logging.info('Handling the Actuator Command Response')
		#self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, data)		
		#self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, data)		
		
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		This callback method is generic and designed to handle any incoming string-based
		message, which will likely be JSON-formatted and need to be converted to the appropriate
		data type. You may not need to use this callback at all.
		
		@param data The incoming JSON message.
		@return boolean
		"""
		logging.info('Handling the incoming message')
		self._handleIncomingDataAnalysis(msg)
	
	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		This callback method will be invoked by the sensor manager that just processed
		a new sensor reading, which creates a new SensorData instance that will be
		passed to this method.
		
		@param data The incoming SensorData message.
		@return boolean
		"""
		#def handleSensorMessage(self, data: SensorData = None) -> bool:
		if data:
			logging.info("Incoming sensor data received (from sensor manager): " + str(data))
			
			# TODO: Optionally, implement `_handleSensorDataAnalysis()` to handle internal analytics
			#self._handleSensorDataAnalysis(data)
			
			# Convert the `SensorData` instance to JSON
			jsonData = DataUtil().sensorDataToJson(data = data)
			#logging.debug('JSON DATA = ' + str(jsonData))
			# Pass the resource and newly generated JSON data to `_handleUpstreamTransmission()`
			self._handleUpstreamTransmission(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = jsonData)
			
			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			
			return False
		
	
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		"""
		This callback method will be invoked by the system performance manager that just
		processed a new sensor reading, which creates a new SystemPerformanceData instance
		that will be passed to this method.
		
		@param data The incoming SystemPerformanceData message.
		@return boolean
		"""
		if data:
			logging.info("Incoming System Performance data received (from system performance manager): " + str(data))
			
			# TODO: Optionally, implement `_handleSensorDataAnalysis()` to handle internal analytics
			#self._handleSensorDataAnalysis(data)
			
			# Convert the `System Performace` instance to JSON
			jsonData = DataUtil().systemPerformanceDataToJson(data = data)
			
			# Pass the resource and newly generated JSON data to `_handleUpstreamTransmission()`
			
			self._handleUpstreamTransmission(resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, msg = jsonData)
			
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
			
			return False
			
	def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
		pass
			
	def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
		pass
			
	def startManager(self):
		logging.info('Starting the Manager')
		if self.sysPerfMgr:
			self.sysPerfMgr.startManager()
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.startManager()
		if self.mqttClient:
			self.mqttClient.connectClient()
			self.mqttClient.subscribeToTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, callback = None, qos = ConfigConst.DEFAULT_QOS)
		
	def stopManager(self):
		if self.sysPerfMgr:
			self.sysPerfMgr.stopManager()
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.stopManager()
		if self.mqttClient:
			self.mqttClient.unsubscribeFromTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
			self.mqttClient.disconnectClient()
		
	def _handleIncomingDataAnalysis(self, msg: str):
		"""
		Call this from handleIncomeMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
		2) Convert msg: Use DataUtil to convert if appropriate.
		3) Act on msg: Determine what - if any - action is required, and execute.
		"""
		logging.debug('Handling the Incoming data analysis')
		
		
	def _handleSensorDataAnalysis(self, data: SensorData):
		"""
		Call this from handleSensorMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Check config: Is there a rule or flag that requires immediate processing of data?
		2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
		"""
		logging.debug('Handling the Sensor Data Analysis')
		if self.enableHandleTempChangeOnDevice:
			pass
		
	def _handleUpstreamTransmission(self, resource: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
		"""
		#def _handleUpstreamTransmission(self, resource = None, msg: str = None):
		logging.info("Upstream transmission invoked. Checking comm's integration.")
		
		# NOTE: If using MQTT, the following will attempt to publish the message to the broker
		if self.mqttClient:
			if self.mqttClient.publishMessage(resource = resource, msg = msg):
				logging.debug("Published incoming data to resource (MQTT): %s", str(resource))
			else:
				logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resource))
		
		# NOTE: If using CoAP, the following will attempt to PUT the message to the server
		if self.coapClient:
			if self.coapClient.sendPostRequest(resource = resource, payload = msg):
				logging.debug("Posted incoming message data to resource (CoAP): %s", str(resource))
			else:
				logging.warning("Failed to post incoming message data to resource (CoAP): %s", str(resource))
		
	def onActuatorCommandMessage(self, client, userdata, msg):
		logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
		
		if self.dataMsgListener:
			try:
				# assumes all data is encoded using UTF-8 (between GDA and CDA)
				actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))
				
				self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
			except:
				logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")
