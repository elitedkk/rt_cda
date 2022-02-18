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
from pickle import NONE

class ActuatorData(BaseIotData):
	"""
	Actuator Data class that is used to interact with the actuator.
	
	"""

	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = None
	
	def getCommand(self) -> int:
		return self.command
	
	def getStateData(self) -> str:
		return self.stateData
	
	def getValue(self) -> float:
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		"""
		Sets the command to the actuator.
		
		@param command Updates or sets the command to the actuator.
		"""
		self.command = command
		self.updateTimeStamp()
	
	def setAsResponse(self):
		pass
		
	def setStateData(self, stateData: str):
		"""
		Sets the state of the actuator.
		
		@param stateData Updates or sets the state data of the actuator.
		"""
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()
	
	def setValue(self, val: float):
		"""
		Set the value of the actuator.
		
		@param val Set the value of the actuator.
		"""
		self.value = val
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
		Update the data of the actuator.
		
		@param data The ActuatorData type that is updated to the actuator.
		"""
		if data and isinstance(data, ActuatorData):
			self.command = data.getCommand()
			self.stateData = data.getStateData()
			self.value = data.getValue()
		