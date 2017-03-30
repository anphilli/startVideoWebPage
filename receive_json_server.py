#!/usr/bin/env python

from flask import Flask, jsonify, render_template, Response, request
import json
import pexpect
import os

app = Flask(__name__)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = True


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




@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/videoaction', methods=['POST'])
def receive_video_action():

    print('You are here!!')
    payload = request.form

    action = payload['action']

    if action == 'start-video':
    	if (os.path.isfile('./startvideofile.txt')):
            returnmessage =  {'message' : 'Video Steam Already Started'}
        else:
            # If the startvideo.txt file does not exist, create the file then start the video
    	    print(action)
            #create a text file to show start video script has been run
            with open('startvideofile.txt', "w") as f:
                f.write('True')
                f.close
            #set the flag variable as start video to send to server
            startstop = "startvideo"
            startStopVideo(startstop)
            #if video is already start, delete the stopvideofile.txt, to allow stop command
            os.system('rm stopvideofile.txt')
            returnmessage =  {'message' : 'Started Video Stream'}
                

    elif action == 'stop-video':
        # Check to see if stopvideofile.txt exists, if it does send message saying video already started
        if (os.path.isfile('./stopvideofile.txt')):
            returnmessage =  {'message' : 'Video Stream Already Stopped'}
        else:
            #if video not started, create file, then start video
            with open('stopvideofile.txt', "w") as f:
                f.write('True')
                f.close
            startstop = "stopvideo"
            startStopVideo(startstop)       
    	    returnmessage =  {'message' : 'Stopped Video Stream'}
            os.system('rm startvideofile.txt')
    	

    print (returnmessage)
    resp = json.dumps(returnmessage)
    return Response(resp, status=200, mimetype='application/json')


app.run(host='127.0.0.1', port=8083)

