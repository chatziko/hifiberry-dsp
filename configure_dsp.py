#!/usr/bin/env python
# encoding: utf-8
'''
configure_dsp -- shortdesc

configure_dsp is a description

It defines classes_and_methods

@author:     user_name
            
@copyright:  2013 organization_name. All rights reserved.
            
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import argparse
import filtering.dspxml
from hardware import sigmaimporter, adau1701


__all__ = []
__version__ = 0.1
__date__ = '2013-11-11'
__updated__ = '2013-11-11'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''
    
    program_version = "v0.1"
    program_build_date = "%s" % __updated__
 
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2013 Daniel Matuschek (Crazy Audio)\
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"
 

    parser = argparse.ArgumentParser(version=program_version_string, epilog=program_longdesc, description=program_license)
    parser.add_argument('xmlfile',help='the name of a filter configuration file')
    parser.add_argument('--response',action='store_true',help='display the frequency response')
    parser.add_argument('--writedsp',action='store_true',help='write the config to the DSP')
        
    args = parser.parse_args()
    print "Processing "+args.xmlfile

    (network, hardware) = filtering.dspxml.configuration_from_xml_file(args.xmlfile)
    
    if args.response:
        network.print_response()
        
    if args.writedsp:
        filename=hardware.get_programfile()
        data=sigmaimporter.read_txbuffer(filename)
        hardware.read_param_h()
        adau1701.dsp_write_blocks(data, verbose=True)
        corereg=data[len(data)-1]
        print corereg
        # Calculate parameter value
        parameters=hardware.network_to_sigmadsp_config(network)
        # write calculated parameters
        # TODO: mute
        pa=[]
        # convert string to addresses and sort them
        for paramaddrstr in parameters:
            pa.append(int(paramaddrstr))
            
        for paramaddr in sorted(pa):
            adau1701.write_param(paramaddr,parameters[str(paramaddr)])
        # TODO: unmute

if __name__ == "__main__":
    sys.exit(main(sys.argv))