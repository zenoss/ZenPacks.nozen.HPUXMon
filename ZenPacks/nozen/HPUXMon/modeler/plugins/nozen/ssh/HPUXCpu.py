import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

CPUMULTIPLIER = {
    'MHz' : 1,
    'GHz' : 1000
}

L2MULTIPLIER = {
    'kB' : 1,
    'M' : 1024,
    'MB' : 1024,
    'Megabytes' : 1024,
}

class HPUXCpu(CommandPlugin):
    """
    find the cpu information
    """
    maptype = "CPUMap"
    command = '/usr/contrib/bin/machinfo | head -n 24'
    compname = 'hw'
    relname = "cpus"
    modname = "Products.ZenModel.CPU"

    def process(self, device, results, log):

        """parse command output from this device"""
        log.info('processing processor resources %s' % device.id)
        rm = self.relMap()
	
	command_replace0 = results.replace('=', ':')

	command_replace1 = command_replace0.replace('CPU info:\n',"")
	command_replace2 = command_replace1.replace('Cache info:\n',"")
	command_replace3 = command_replace2.replace(' CPUID registers\n',"")
	command_replace4 = command_replace3.replace('Bus features\n',"")
	command_replace5 = command_replace4.replace('Intel(R)','Intel')
	command_replace = command_replace5.replace('size : ',"")

	command_output = command_replace

	command_output1 = re.sub(r"\s\bBus\sLock\sSignal\smasked\b\s+","", command_output)

	command_output2 = re.sub(r"\w,\s\bassociativity\b\s:\s\d+","", command_output1)
	
	command_output2 = command_output2.strip()

        command_output = command_output2.split('\n')
		
	#log.info( command_output2 )
	#log.info ( command_output )
        om = self.objectMap()
        number = 0
        for line in command_output:
            if line: #check for blnk lines
                key, value = line.split(':')
                key = key.strip()
   
                if key == 'processor model':
		    newstring = value.replace('1',"")
                    om.description = newstring.strip()
                    manufacturer = om.description.split()[0]
                    om.setProductKey = MultiArgs(om.description,manufacturer)

                if key == 'Clock speed':
                    speed, unit = value.strip().split()
                    om.clockspeed = float(speed) * CPUMULTIPLIER.get(unit, 1)
           
                if key == 'Bus Speed':
                    speed, unit = value.strip().split()
                    om.extspeed = float(speed) * CPUMULTIPLIER.get(unit, 1)
   
                if key == 'Number of CPUs':
                    number = int(value.strip())

                if key == 'L3 Unified':
                    cache, unit = value.strip().split()
                    om.cacheSizeL2 = int(cache) * L2MULTIPLIER.get(unit, 1)
		     
        #insert an objectMap for each CPU
        for n in range(number):
            om.id = str(n)
            om.socket = str(n)
            rm.append(om)    
        log.debug(rm)
        return rm



