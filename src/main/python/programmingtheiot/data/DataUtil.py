#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import json
import logging

from decimal import Decimal
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from pickle import NONE

class DataUtil():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, encodeToUtf8 = False):
		pass
	
	def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False):
		"""
		Converts Actuator Data to Json
		@param data: Actuator Data that is to be converted
		@param useDecForFloat:Flag to notify if a decimal value can be used for floating values
		"""
		if not data:
			logging.debug("Invalid Data type")
			return None
		jsonData = json.dumps(data, indent = 4, cls = JsonDataEncoder)
		return jsonData
	
	def sensorDataToJson(self, data: SensorData = None, useDecForFloat: bool = False):
		"""
		Converts Sensor Data to Json
		@param data: Sensor Data that is to be converted
		@param useDecForFloat:Flag to notify if a decimal value can be used for floating values
		"""
		if not data:
			logging.debug("Invalid Data type")
			return None
		jsonData = json.dumps(data, indent = 4, cls = JsonDataEncoder)
		return jsonData
		
	def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False):
		"""
		Converts System Performance Data to Json
		@param data: SystemPerformanceData that is to be converted
		@param useDecForFloat:Flag to notify if a decimal value can be used for floating values
		"""
		if not data:
			logging.debug("Invalid Data type")
			return None
		jsonData = json.dumps(data, indent = 4, cls = JsonDataEncoder)
		return jsonData
	
	def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts Json to Actuator Data
		@param jsonData: Json value that is to be converted
		@param useDecForFloat:Flag to notify if a decimal value can be used for floating values
		"""
		if not jsonData:
			logging.warning("Invalid type of jsonData")
			return None
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		jsonStruct = json.loads(jsonData)
		ad = ActuatorData()
		varStruct = vars(ad)
		for key in jsonStruct :
			if key in varStruct:
				setattr(ad, key, jsonStruct[key])
		return ad
		
	
	def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts Json to Sensor Data
		@param jsonData: Json value that is to be converted
		@param useDecForFloat:Flag to notify if a decimal value can be used for floating values
		"""
		if not jsonData:
			logging.warning("Invalid type of jsonData")
			return None
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		jsonStruct = json.loads(jsonData)
		sd = SensorData()
		varStruct = vars(sd)
		for key in jsonStruct :
			if key in varStruct:
				setattr(sd, key, jsonStruct[key])
		return sd
	
	def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts Json to System Performance Data
		@param jsonData: Json value that is to be converted
		@param useDecForFloat:Flag to notify if a decimal value can be used for floating values
		"""
		if not jsonData:
			logging.warning("Invalid type of jsonData")
			return None
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		jsonStruct = json.loads(jsonData)
		spd = SystemPerformanceData()
		varStruct = vars(spd)
		for key in jsonStruct :
			if key in varStruct:
				setattr(spd, key, jsonStruct[key])
		return spd
	
class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		return o.__dict__
	