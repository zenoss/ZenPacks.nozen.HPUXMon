from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
import re

MULTIPLIER = {
    'kB' : 1024,
    'MB' : 1024 * 1024,
    'M' : 1024 * 1024,
    'Megabytes' : 1024 * 1024,
    'GB' : 1024 * 1024 * 1024,
    'G' : 1024 * 1024 * 1024,
    'Gigabytes' : 1024 * 1024 * 1024,
    'b' : 1
}

def parse_mem(command):
    memory = command.split('=')[1].strip()
    return memory

def parse_swap(command):
    swap = command.strip()
    return swap

class HPUXMemory(CommandPlugin):
    """
    find the memory
    """
    maptype = "FileSystemMap"
    command = "/usr/contrib/bin/machinfo | grep 'Memory' && /usr/sbin/swapinfo -tam | grep dev"
    compname = 'hw'
    relname = "filesystems"
    modname = "Products.ZenModel.Filesystem"


    def process(self, device, results, log):
        log.info('Collecting memory for device %s' % device.id)
        maps = []

	command_output = results.strip().split('\n')

        # Process Memory line

	memory1= parse_mem(command_output[0])

	memory = re.sub(r"\s\(\d+\.\d*\s\bGB\b\)","", memory1)

 	swap1 = command_output[1].strip()
        swap = swap1.split()[1] + " MB"
        mem_value, unit= memory.split()
        mem_size = int(mem_value) * MULTIPLIER.get(unit, 1)
	swap_value, unit= swap.split()
	swap_size = int(swap_value) * MULTIPLIER.get(unit, 1)

        maps.append(ObjectMap({"totalMemory": mem_size}, compname="hw"))
	maps.append(ObjectMap({"totalSwap": swap_size}, compname="os"))
        log.debug(maps)
        return maps

