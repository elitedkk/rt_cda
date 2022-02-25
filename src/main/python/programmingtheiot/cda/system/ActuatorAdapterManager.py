#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from pickle import NONE
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	#dataMsgListener, 
	def __init__(self, IDataMessageListener = None):
		"""
		Constructor for Adapter Manager
		"""
		#self.dataMsgListener = dataMsgListener
		self.configUtil = ConfigUtil()
		self.useSimulator= self.configUtil.getBoolean(section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_SIMULATOR_KEY)
		self.useEmulator= self.configUtil.getBoolean(section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_EMULATOR_KEY)
		self.locationID = self.configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		if self.useEmulator:
			logging.debug('Emulators will be used')
		else:
			logging.debug('Simulators will be used')
			
		# create the humidifier actuator
		self.humidifierActuator = None
		# create the HVAC actuator
		self.hvacActuator = None
		self.ledDisplayActuator = None
		self.resource = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
		self.isEnvActuationActive = False
		#self.dataMsgListener = False
		self._initEnvironmentalActuationTasks()
		
		
		
		
		#self.isEnvActuationActive = False
		#self.initEnvironmentalActuationTasks()
		

	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		"""
		Update the actuator with the data that is passed.
		
		@param data The data which is to be updated.
		@result Return True if the actuator was updated
		"""
		if data and not data.isResponseFlagEnabled():
			if data.getLocationID() == self.locationID:
				logging.info('Acuator command called at '+ str(data.getLocationID()))
				aType = data.getTypeID()
				responseData = None
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE:
					responseData = self.hvacActuator.updateActuator(data)
				else:
					logging.warning('No valid actuator for the command ', data.getTypeID())
				return responseData
			else:
				logging.warning('Problem with the location, check ' + data.getLocationID() + ' and ' + self.locationID)
		else:
			logging.warning('Empty message for the request')
		return None
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		"""
		Initialization of class.
		
		@param listener Sets the listener to this class so that this class is able to listen to the events.
		"""
		if listener is not None:
			self.dataMsgListener = listener
	def _initEnvironmentalActuationTasks(self):
		if not self.useEmulator:
			# load the environmental tasks for simulated actuation
			self.humidifierActuator = HumidifierActuatorSimTask()
			
			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()
		else:
			hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidiferEmulatorTask')
			hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
			self.humidifierActuator = hueClazz()
			
			# create the HVAC actuator emulator
			hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
			hveClazz = getattr(hveModule, 'HvacEmulatorTask')
			self.hvacActuator = hveClazz()
			
			# create the LED display actuator emulator
			leDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
			leClazz = getattr(leDisplayModule, 'LedDisplayEmulatorTask')
			self.ledDisplayActuator = leClazz()
