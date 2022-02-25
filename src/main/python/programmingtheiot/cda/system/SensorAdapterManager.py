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

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from pickle import FALSE, TRUE
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

class SensorAdapterManager():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		self.configUtil = ConfigUtil()
		self.pollRate = self.configUtil.getInteger(section = ConfigConst.CONSTRAINED_DEVICE,key=ConfigConst.POLL_CYCLES_KEY, defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)
		self.useSimulator = self.configUtil.getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SIMULATOR_KEY)
		self.useEmulator = self.configUtil.getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
		self.locationID = self.configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		self.useSenseHat = self.configUtil.getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SENSE_HAT_KEY)
		self.useSenseHatI2CBus = False
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		
		self.resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
		self.isEnvSensingActive = False
		self.dataMsgListener = False
		self._initEnvironmentalSensorTasks()
		'''
		configUtil = ConfigUtil()
		tempFloor = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
		tempCeiling = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
			
		pressureFloor = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		pressureCeiling = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
		
		humidityFloor = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
		humidityCeiling = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)

		#if self.useSimulator:
		self.dataGenerator = SensorDataGenerator()
					
		tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(minValue = tempFloor, maxValue = tempCeiling, useSeconds = False)
		pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(minValue = pressureFloor, maxValue = pressureCeiling, useSeconds=False)
		humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(minValue = humidityFloor, maxValue = humidityCeiling, useSeconds=False)
		
		self.tempAdapter = TemperatureSensorSimTask(dataSet = tempData)
		self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)
		self.humidityAdapter = HumiditySensorSimTask(dataSet = humidityData)
		'''
	def handleTelemetry(self):
		"""
		Gets the values of sensors. Callback function that is connected to data listener function
		"""
		if self.isEnvSensingActive:
			tempData = self.tempAdapter.generateTelemetry()
			pressureData = self.pressureAdapter.generateTelemetry()
			humidityData = self.humidityAdapter.generateTelemetry()
			tempData.setLocationID(self.locationID)
			pressureData.setLocationID(self.locationID)
			humidityData.setLocationID(self.locationID)
			
			logging.debug('Temperature Data: ' + str(tempData))
			logging.debug('Pressure Data: ' + str(pressureData))
			logging.debug('Humidity Data: ' + str(humidityData))
			
			if self.dataMsgListener:
				self.dataMsgListener.handleSensorMessage(data = tempData)
				self.dataMsgListener.handleSensorMessage(data = pressureData)
				self.dataMsgListener.handleSensorMessage(data = humidityData)
		else:
			logging.debug('Sensing not active.')
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
	
	def startManager(self):
		if not self.scheduler.running:
			self.scheduler.start()
			return True
		else:
			return False
		
	def stopManager(self):
		self.scheduler.shutdown()
	
	def _initEnvironmentalSensorTasks(self):
		humidityFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
		humidityCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
		
		pressureFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		pressureCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		
		tempFloor       = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
		tempCeiling     = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		
		if not self.useEmulator:
			self.dataGenerator = SensorDataGenerator()
			
			humidityData = \
				self.dataGenerator.generateDailyEnvironmentHumidityDataSet( \
					minValue = humidityFloor, maxValue = humidityCeiling, useSeconds = False)
			pressureData = \
				self.dataGenerator.generateDailyEnvironmentPressureDataSet( \
					minValue = pressureFloor, maxValue = pressureCeiling, useSeconds = False)
			tempData     = \
				self.dataGenerator.generateDailyIndoorTemperatureDataSet( \
					minValue = tempFloor, maxValue = tempCeiling, useSeconds = False)
			
			self.humidityAdapter = HumiditySensorSimTask(dataSet = humidityData)
			self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)
			self.tempAdapter     = TemperatureSensorSimTask(dataSet = tempData)
	
		else:
			heModule = import_module('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', 'HumiditySensorEmulatorTask')
			heClazz = getattr(heModule, 'HumiditySensorEmulatorTask')
			self.humidityAdapter = heClazz()
			
			peModule = import_module('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', 'PressureSensorEmulatorTask')
			peClazz = getattr(peModule, 'PressureSensorEmulatorTask')
			self.pressureAdapter = peClazz()
			
			teModule = import_module('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', 'TemperatureSensorEmulatorTask')
			teClazz = getattr(teModule, 'TemperatureSensorEmulatorTask')
			self.tempAdapter = teClazz()
