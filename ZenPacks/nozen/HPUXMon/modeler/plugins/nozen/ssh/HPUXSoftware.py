import re
from datetime import date, datetime, time

from Products.ZenUtils.Utils import prepId
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

#YYYYMMDDHHMM.SS

def parse_date(odt):
    #"Parse the date and convert to YYYY/MM/DD HH:MM:SS"
    dt = datetime.strptime(odt, "%Y%m%d%H%M.%S")
    moddate = dt.strftime("%Y/%m/%d %H:%M:%S")

    return moddate

class HPUXSoftware(CommandPlugin):
    """
    swlist -l product -a title -a revision -a install_date -a vendor_tag
    """

    command = "/usr/sbin/swlist -v -l product -a vendor_tag -a title -a revision -a install_date | awk '/^bundle/ || /^product/ {interesting=1 ; title="'""'"};/^vendor_tag/ {vendor_tag=$2};/^revision/ {revision=$2};/^install_date/ {install_date=$2};/^title/ {sub(/^title */,"'""'"); title=$0};{if(title != "'""'" && interesting == 1) {printf("'"%s..%s %s..%s\\n"'",vendor_tag,title,revision,install_date);interesting=0}}'"
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"

#PHCO_31684            Japanese PM-USYNC manpages 1.0            200502101146.50 HP

    def process(self, device, results, log):
        log.info('Collecting Software Installed for device %s' % device.id)
        rm = self.relMap()
	package1 = results.strip()
	package2 = package1.replace('+','plus ')
	package3 = package2.replace('/',' ')
	package4 = package3.replace('"','')
	package5 = package4.replace('=',' ')
	package6 = package5.replace(';', ' ')
	package7 = package6.replace('&', 'and')
	package8 = package7.replace(':', '')
	package9 = package8.replace('[', '')
	package10 = package9.replace(']', '')
	package11 = package10.replace("'", '')
	package = package11.replace("_", ' ')
	
	for line in package.split('\n'):
	    om = self.objectMap()
	    splitter = line.split('..')
    	    e_manu = splitter[0]
	    if e_manu == '':
	       manufacturer = "unknown"
	    else:
	       manufacturer = splitter[0]
	    e_id = splitter[1]
	    if e_id == '':
	       om.id = "unknown"
	    else:
	       om.id = splitter[1]
	    e_date = splitter[2]
	    if e_date == '':
	       om.setInstallDate = parse_date('200001011200.00')
	    else:
	       om.setInstallDate = parse_date(e_date)
	    om.setProductKey = MultiArgs(om.id, manufacturer)
            if om.id:
               rm.append(om)

	log.debug(rm)
        return rm



