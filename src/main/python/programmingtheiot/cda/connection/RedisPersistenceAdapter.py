import redis
import logging
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.DataUtil import DataUtil
from _cffi_backend import string

class RedisPersistenceAdapter():
    """
    Shell representation of class for student implementation.
    
    """
    
    redisclient=''

    def __init__(self, clientID: str = None):
        """
        Default constructor. This will set remote broker information and client connection
        information based on the default configuration file contents.
        
        @param clientID Defaults to None. Can be set by caller. If this is used, it's
        critically important that a unique, non-conflicting name be used so to avoid
        causing the MQTT broker to disconnect any client using the same name. With
        auto-reconnect enabled, this can cause a race condition where each client with
        the same clientID continuously attempts to re-connect, causing the broker to
        disconnect the previous instance.
        """
        try:
            self.config = ConfigUtil()
            self.dataMsgListener = None
            
            self.host = \
                self.config.getProperty( \
                    ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
            self.port = \
            self.config.getProperty( \
                ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_RTSP_STREAM_PORT)
            self.redisclient = redis.Redis(host=self.host,port=self.port,password=None)
        except:
            logging.error("Error in init redis")
    
    def connectClient(self):
        try:
            if not self.redisclient:
                logging.info("Attempting to connect to redis")
                self.redisclient = redis.Redis(host=self.host,port=self.port,password=None)
            else:
                logging.warning("Already connected to redis")
            return True
        except:
            logging.error("Error connecting redis client")
            return False
        
    def storeData(self, resource: ResourceNameEnum, data: str):
        try:
            logging.info("Attempting to store into redis for %s", str(resource))
            self.redisclient.set(str(resource),str(data))
        except:
            logging.error("Error putting into redis")
        
'''logging.info("hello")  '''      
'''rpa=RedisPersistenceAdapter()'''
'''logging.info("world")'''
'''rpa.storeData("abc", "data")'''