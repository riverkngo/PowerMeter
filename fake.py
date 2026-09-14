class FakeE4418B:
    KNOWN_WRITES = {
        "CAL:ZERO:AUTO ONCE",
        "CAL:AUTO ONCE",
        "UNIT:POW DBM",
        "UNIT:POW W",
    }

    def __init__(self):
        self.units = "DBM"
        self.frequency_hz = 50e6
        self.error_queue = []
        self.commands_sent = []

    def write(self, command):
        self.commands_sent.append(command)

        if command.startswith("SENS:FREQ "):
            self.frequency_hz = float(command.split()[1])
            return

        if command not in self.KNOWN_WRITES:
            self.error_queue.append("Undefined")
            return

        if command == "UNIT:POW DBM":
            self.units = "DBM"
        elif command == "UNIT:POW W":
            self.units = "W"

    def query(self, command):
        self.commands_sent.append(command)

        if command == "*IDN?":
            return "Agilent Technologies,E4418B,GB12345678\n"

        if command in ("READ?", "FETC?"):
            if self.units == "DBM":
                return "-1.234500E+01\n"
            return "5.888000E-05\n"

        if command == "SYST:ERR?":
            if self.error_queue:
                return self.error_queue.pop(0) + "\n"
            return '+0,"No error"\n'

        self.error_queue.append("Undefined header")
        return ""