class PowerMeterE4418B(): 
    def __init__(self, resource): 
        self.inst = resource
    def identify(self): 
        return self.inst.query("*IDN?")
    def setFrequency(self, hz): 
        self.inst.write(f"SENS:FREQ {hz:.6E}")

    def zeroAndCalibrate(self):
        
        self.inst.write("CALibration[1|2][:ALL]?")
        #self.inst.write("CAL:AUTO ONCE")


    def setUnits(self, units): 
        if units not in ("DBM", "W"): 
            raise ValueError(f"Units must be DBM or W")
        self.inst.write(f"UNIT:POW {units}")

    def measureAvgPower(self): 
        return float(self.inst.query("READ?"))

    def checkErrors(self): 
        errors = []
        while True:
            response = self.inst.query("SYST:ERR?")
            if response.startswith("+0,"):
                return errors 
            errors.append(response)




