from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

def parse_serial(command):
    serial = command.split('=')[1].strip()
    return serial

def parse_hwmodel(command):
    hwmodel = command.split('=')[1].strip()
    return hwmodel

def parse_osversion(command):
    osversion = command.split('=')[1].strip()
    return osversion

class device(CommandPlugin):
    maptype = "DeviceMap"
    compname = ""
    command = "/usr/bin/uname -a && /usr/contrib/bin/machinfo | grep 'machine serial number' && /usr/contrib/bin/machinfo | grep 'model string' && /usr/contrib/bin/machinfo | grep 'release' | head -n 1"

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing info for device %s" % device.id)
	
        om = self.objectMap()

	precommand = results.replace('"',"").strip()

        command_output = precommand.split('\n')
        om.snmpDescr = command_output[0].strip()
        om.uname = om.snmpDescr.split()[0]
        om.snmpSysName = om.snmpDescr.split()[1]
	om.setHWSerialNumber = parse_serial(command_output[1])
        hwmodel = parse_hwmodel(command_output[2])
        om.setHWProductKey = MultiArgs(hwmodel, "HP")
        osversion = parse_osversion(command_output[3])
        om.setOSProductKey = MultiArgs(osversion,"HP")

        log.debug(om)
        return om
