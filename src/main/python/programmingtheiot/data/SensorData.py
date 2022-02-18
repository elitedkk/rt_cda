#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
	"""
	Sensor class used to interact with the Sensors.
	
	"""
	def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(SensorData, self).__init__(name = name, typeID = typeID, d = d)
		self.value=ConfigConst.DEFAULT_VAL
	
	def getSensorType(self) -> int:
		"""
		Returns the sensor type to the caller.
		
		@return int
		"""
		return self.sensorType
	
	def getValue(self) -> float:
		"""
		Returns the value to the caller.
		
		@return float
		"""
		return self.value
	
	def setValue(self, newVal: float):
		"""
		Sets the value of the sensor.
		
		@param newVal Updates or sets the value of the sensor.
		"""
		self.value = newVal
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
		Update the value of the sensor if data is an object of SensorData.
		
		@param data Updates the value of the sensor.
		"""
		if data and isinstance(data, SensorData):
			self.value = data.getValue()
			
	
