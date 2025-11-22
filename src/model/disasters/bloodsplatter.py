from model.disasters.disaster import Disaster
from parameters import ViewParameters
class BloodSplatter(Disaster):

    @classmethod
    def getMaxDamage(cls):
        return 30

    @classmethod
    def getDuration(cls):
        return 10

    @classmethod
    def getMaxTemperatureDifference(cls):
        return 60

    @classmethod
    def getTexturePath(cls):
        return ViewParameters.BLOOD_SPLATTER

    def __init__(self, strength: float):
        super().__init__(strength)