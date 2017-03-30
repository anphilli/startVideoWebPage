#!/usr/bin/env python

import pexpect
import os



def startStopVideo(startstop):
    ''' Start or stop the video session on remote server
        within APIC EM Demo Environment send flag to determine 
        if starting of stopping video stream                    '''

    host_username = "administrator"
    host_password = "Cisco12345"
    host_ip = "10.55.16.27"
    scriptname = ""


    ''' Run start or stop script '''
    if startstop == 'startvideo':
        scriptname = 'start_remotevideo.py'
    elif startstop == 'stopvideo':
        scriptname = 'stop_video.py'


    #Build ssh command from variables
    ssh_cmd = 'ssh -l {0} {1}'.format(host_username,host_ip)

    print("\nSSH'ing to host {0} to {1} video stream".format(host_ip, startstop))
    try:
        s = pexpect.spawn(ssh_cmd)
        s.expect('.*password: ')
        s.sendline(host_password)
        s.expect('\\$ ')
        s.sendline('cd /home/administrator/Desktop/scripts/')
        s.expect('.*\\$ ')
	print('./{0}'.format(scriptname))
        s.sendline('./{0}'.format(scriptname))
        s.expect('.*\\$')
	s.sendline('exit')
        scriptstate = s.after
        #print(portstate)               
    except pexpect.TIMEOUT as err:
        print("pexpect timed out! See error message below\n")
        print(err)         

        print(scriptstate)

        videostatus = 'script was run on remote host'
        
        return videostatus


if __name__ == "__main__":

	startstop = "stopvideo"
	startStopVideo(startstop)
