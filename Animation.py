from sys import path_importer_cache
from time import thread_time_ns
from tkinter.constants import CURRENT, Y
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
import pyperclip
import pydirectinput as pydi
import time
import json
import sys
import os
import argparse
from easing_functions import *

def getForegroundWindowTitle() -> Optional[str]:            #Get current active Window
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    if buf.value == "MagicaVoxel | Ephtracy":              #If current active Window Magicavoxel then
        return False                                        #Continue script (not very performant)
    else:
        return True
                                                             

def exitprog():
    input("Press Enter to continue...")
    sys.exit()

def writeToMvOld():                                                            
    print("Please open MagicaVoxel and make sure its in the foreground.")
    pause(True)                                            #Wait until window in Active to start script we dont want the script spamming your discord for 
    keyframenum = 0
  
    print("Going")
    runningFrame = 0

    while keyframenum+1 < len(data['keyframe']):
        currentkeyframe = data['keyframe'][keyframenum]
        nextkeyframe = data['keyframe'][keyframenum + 1]
        keyframenum += 1

        print("Setting")
        try:
            frames =          float(currentkeyframe['Frames'])                     
            secondPerRender = float(currentkeyframe['SecondsPerRender'])
            c_dircetion =       currentkeyframe['Direction']
            c_pitch  =          float(currentkeyframe['Pitch'])
            c_yaw    =          float(currentkeyframe['Yaw'])
            c_zoom   =          float(currentkeyframe['Zoom'])
            c_roll   =          float(currentkeyframe['Roll'])
            c_x      =          float(currentkeyframe['X'])
            c_y      =          float(currentkeyframe['Y'])
            c_z      =          float(currentkeyframe['Z'])
            c_fov    =          float(currentkeyframe['Fov'])
            c_focus  =          float(currentkeyframe['Focus'])

            n_pitch  =          float(nextkeyframe['Pitch'])
            n_yaw    =          float(nextkeyframe['Yaw'])
            n_zoom   =          float(nextkeyframe['Zoom'])
            n_roll   =          float(nextkeyframe['Roll'])
            n_x      =          float(nextkeyframe['X'])
            n_y      =          float(nextkeyframe['Y'])
            n_z      =          float(nextkeyframe['Z'])
            n_fov    =          float(nextkeyframe['Fov'])
            n_focus  =          float(nextkeyframe['Focus'])


        except ValueError:
            print("Error in config. Did you accidentally input a letter instead of a number?")
            exitprog()

        try: m_zoom = float((c_zoom-n_zoom)/(0-frames))
        except ZeroDivisionError: m_zoom = 0  

        try: m_roll = float((c_roll-n_roll)/(0-frames))
        except ZeroDivisionError: m_roll = 0

        try: m_x = float((c_x-n_x)/(0-frames))
        except ZeroDivisionError: m_x = 0

        try: m_y = float((c_y-n_y)/(0-frames))
        except ZeroDivisionError: m_y = 0   

        try: m_z = float((c_z-n_z)/(0-frames))
        except ZeroDivisionError: m_z = 0   
                                 
        try: m_pitch = float((c_pitch-n_pitch)/(0-frames))
        except ZeroDivisionError: m_pitch = 0

        try: m_fov = float((c_fov-n_fov)/(0-frames))
        except ZeroDivisionError: m_fov = 0

        try: m_focus = float((c_focus-n_focus)/(0-frames))
        except ZeroDivisionError: m_focus = 0

        try:    
            if c_yaw < n_yaw and c_dircetion == "right":    
                m_yaw = float(((n_yaw-360)-c_yaw)/frames) #not normal right -90 -> 90 
            elif c_yaw > n_yaw and c_dircetion == "right":    
                m_yaw = float((n_yaw-c_yaw)/frames) #normal right 0 -> -90    
            elif c_yaw < n_yaw and c_dircetion == "left":    
                m_yaw = float((n_yaw-c_yaw)/frames) #normal left -90 -> 90 
            elif c_yaw > n_yaw and c_dircetion == "left":    
                m_yaw = float(((n_yaw+360)-c_yaw)/frames) #not normal left 90 -> -90    
            else:
               m_yaw = 0
        except ZeroDivisionError:
            m_yaw = 0

        t_frames = int(frames)              #Determin how often script is going to run
        for x in range(t_frames):
            c_pitch = c_pitch + m_pitch
            c_yaw = c_yaw + m_yaw
            c_zoom = c_zoom + m_zoom
            c_roll = c_roll + m_roll
            c_x = c_x + m_x
            c_y = c_y + m_y
            c_z = c_z + m_z
            c_fov = c_fov + m_fov
            c_focus = c_focus + m_focus

            commandProgOff = "set pt_auto 0"
            commandProgOn = "set pt_auto 1"
            commandFrame = "set a_time " + str(runningFrame)
            command = "cam rx "+str(c_pitch)+" | cam ry "+str(c_yaw)+" | cam zoom "+str(c_zoom) +" | cam rz "+str(c_roll) +" | set pt_fov  "+str(c_fov) 
            command2 = "cam x "+str(c_x)+ " | cam y "+str(c_y)+ " | cam z "+str(c_z) + " | set pt_focus  "+str(c_focus)

            print("Currently on Frame "+str(x+1)+"/"+str(int(frames)))  #Progress
            print(command)
            print()
            print(command2)
            print()

            pause(False)                                   
            pydi.press('f1')
            
            pyperclip.copy(commandProgOff)                     
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(command)                     
            pause(False)

            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(command2)
            pause(False)

            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(commandFrame)                     
            pause(False)
                                    
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(commandProgOn)                     
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pydi.press('f1')
            time.sleep(secondPerRender)                 #Wait image to render

            runningFrame += 1

            if bool(data['saveRenders']):
                pause(False)              
                pydi.press("6")
                typeKeyFrameNumber(runningFrame)
                time.sleep(0.4)
                pydi.press('enter')
                time.sleep(2.0)


def typeKeyFrameNumber(keyFrameNumber):
    if(keyFrameNumber) < 10:
        pydi.press(str(keyFrameNumber))
    else:
        tens = (keyFrameNumber % 100)
        units = (keyFrameNumber % 10)
        pydi.press(str(int(tens/10)))
        pydi.press(str(units))

def pause(firsttime):
    if firsttime:
        while getForegroundWindowTitle():
            time.sleep(3)    
        pass
    else:   
        if getForegroundWindowTitle():
            print("Progress paused...")
            while getForegroundWindowTitle():
                time.sleep(5)                                   
            print("WARNING: You exited magicavoxel while the render was in progress.")
            print("To avoid problems make sure the console is not selected and if it has any contenct delete it as this might lead to some issues.")
            input("Press enter to confirm")
            print("Select magicavoxel")

            while getForegroundWindowTitle():
                time.sleep(5)              

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Turn on verbose mode", action="store_true")
    parser.add_argument("-c", "--camera", help="Specify camera json path. Defaults to ./camera.json", default="camera.json")
    parser.add_argument("-d", "--dryRun", help="Dry run turned on will not attempt to save files", action="store_true")
    parser.add_argument("-s", "--secondsPerFrame", help="Specify how long to a render per frame in seconds, Defaults to 1 second", type=int, default=1)
    global args
    args = parser.parse_args()

    if args.verbose:
        print(args)

    try:
        with open(args.camera) as json_file:             
            global data
            data = json.load(json_file)

        if args.verbose:
            print(f"{args.camera}:")
            print(json.dumps(data, indent=4, sort_keys=True))

        json_file.close()                                 
    except:                                                
        print(f"ERROR: unable to open {args.camera}")
        exitprog()

    cameraKeyFrameData = generateCameraData(data)
    writeToMV(cameraKeyFrameData)

def generateCameraData(data):
    # go through json data
    # loop through keyframes
    # get all camera settings
    # interpolate all camera values for frames size

    cameraKeyFrameData = []

    # prob should make these a map function
    for i in range(len(data['keyframes'])):
        currentFrameData = []
        currentFrameData = [{} for i in range(data['keyframes'][i]['frames'])] 
        for currentFrame in range(data['keyframes'][i]['frames']):
            if 'x' in data['keyframes'][i]['camera']:
                x = data['keyframes'][i]['camera']['x']
                if 'end' in x: 
                    if not 'interpolation' in x:
                        x['interpolation'] = 'linear'

                    currentFrameData[currentFrame]['x'] = interpolate(x['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, x['start'], x['end'], data['keyframes'][i]['frames'])
                elif not 'end' in x:
                    currentFrameData[currentFrame]['x'] =  x['start']

            if 'y' in data['keyframes'][i]['camera']:
                y = data['keyframes'][i]['camera']['y']
                if 'end' in y:
                    if not 'interpolation' in y:
                        y['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['y'] = interpolate(y['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, y['start'], y['end'], data['keyframes'][i]['frames'])
                elif not 'end' in y:
                    currentFrameData[currentFrame]['y'] =  y['start']

            if 'z' in data['keyframes'][i]['camera']:
                z = data['keyframes'][i]['camera']['z']
                if 'end' in z:
                    if not 'interpolation' in y:
                        z['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['z'] = interpolate(z['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, z['start'], z['end'], data['keyframes'][i]['frames'])
                elif not 'end' in z:
                    currentFrameData[currentFrame]['z'] =  z['start']

            if 'pitch' in data['keyframes'][i]['camera']:
                pitch = data['keyframes'][i]['camera']['pitch']
                if 'end' in pitch:
                    if not 'interpolation' in pitch:
                        pitch['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['pitch'] = interpolate(pitch['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, pitch['start'], pitch['end'], data['keyframes'][i]['frames'])
                elif not 'end' in pitch:
                    currentFrameData[currentFrame]['pitch'] =  pitch['start']       

            if 'yaw' in data['keyframes'][i]['camera']:
                yaw = data['keyframes'][i]['camera']['yaw']
                if 'end' in yaw:
                    if not 'interpolation' in yaw:
                        yaw['interpolation'] = 'linear'
                    # special case in yaw to set direction
                    # TODO: need to mod so it can rotate mulitple times
                    if yaw['start'] <= yaw['end'] and yaw['direction'] == 'counterclockwise':
                        currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, yaw['start'], yaw['end'], data['keyframes'][i]['frames'])
                    elif yaw['start'] > yaw['end'] and yaw['direction'] == 'counterclockwise':
                        currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, yaw['start'], yaw['end'] + 360, data['keyframes'][i]['frames'])
                    elif yaw['start'] <= yaw['end'] and yaw['direction'] == 'clockwise':
                        currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, yaw['start'] + 360, yaw['end'], data['keyframes'][i]['frames'])
                    elif yaw['start'] > yaw['end'] and yaw['direction'] == 'clockwise':
                        currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, yaw['start'], yaw['end'], data['keyframes'][i]['frames'])
                elif not 'end' in z:
                    currentFrameData[currentFrame]['yaw'] =  yaw['start']

            if 'roll' in data['keyframes'][i]['camera']:
                roll = data['keyframes'][i]['camera']['roll']
                if 'end' in roll:
                    if not 'interpolation' in roll:
                        roll['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['roll'] = interpolate(roll['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, roll['start'], roll['end'], data['keyframes'][i]['frames'])
                elif not 'end' in roll:
                    currentFrameData[currentFrame]['roll'] =  roll['start']       

            if 'zoom' in data['keyframes'][i]['camera']:
                zoom = data['keyframes'][i]['camera']['zoom']
                if 'end' in zoom:
                    if not 'interpolation' in zoom:
                        zoom['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['zoom'] = interpolate(zoom['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, zoom['start'], zoom['end'], data['keyframes'][i]['frames'])
                elif not 'end' in zoom:
                    currentFrameData[currentFrame]['zoom'] =  zoom['start']
                    
            if 'fov' in data['keyframes'][i]['camera']:
                fov = data['keyframes'][i]['camera']['fov']
                if 'end' in fov:
                    if not 'interpolation' in fov:
                        fov['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['fov'] = interpolate(fov['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, fov['start'], fov['end'], data['keyframes'][i]['frames'])
                elif not 'end' in fov:
                    currentFrameData[currentFrame]['fov'] =  fov['start']

            if 'focus' in data['keyframes'][i]['camera']:
                focus = data['keyframes'][i]['camera']['focus']
                if 'end' in focus:
                    if not 'interpolation' in focus:
                        focus['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['focus'] = interpolate(focus['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, focus['start'], focus['end'], data['keyframes'][i]['frames'])
                elif not 'end' in focus:
                    currentFrameData[currentFrame]['focus'] =  focus['start']


        cameraKeyFrameData.append(currentFrameData)

    return cameraKeyFrameData

def interpolate(type, percent, elapsed, start, end, total):
    match type:
        case 'linear':
            return linear(percent, elapsed, start, end, total)
        case 'easeIn':
            return easeIn(percent, elapsed, start, end, total)
        case 'easeOut':
            return easeOut(percent, elapsed, start, end, total)
        case 'easeInOut':
            return easeInOut(percent, elapsed, start, end, total)
        case _:
            return linear(percent, elapsed, start, end, total)

def linear(percent, elapsed, start, end, total):
    # percent 0 - 1.0
    # elapsed time running
    # start at 0%
    # end at 100%
    # total length
    return start+(end-start)*percent

def easeIn(percent, elapsed, start, end, total):
    ease = QuadEaseIn(start, end, total)
    return ease(elapsed)


def easeOut(percent, elapsed, start, end, total):
    ease = QuadEaseOut(start, end, total)
    return ease(elapsed)

def easeInOut(percent, elapsed, start, end, total):
    ease = QuadEaseInOut(start, end, total)
    return ease(elapsed)



def cameraCommandBuilder(cameraCommand, cameraType):
    cameraCommandArray = []
    cameraCommandString = ' | '
    # need better naming type
    if cameraType=='rotationsFovZoom':
        if 'pitch' in cameraCommand:
            cameraCommandArray.append("cam rx " + str(cameraCommand['pitch']))
        if 'yaw' in cameraCommand:
            cameraCommandArray.append("cam ry " + str(cameraCommand['yaw']))
        if 'roll' in cameraCommand:
            cameraCommandArray.append("cam rz " + str(cameraCommand['roll']))
        if 'zoom' in cameraCommand:
            cameraCommandArray.append("cam zoom " + str(cameraCommand['zoom']))
        if 'fov' in cameraCommand:
            cameraCommandArray.append("set pt_fov " + str(cameraCommand['fov']))
    elif cameraType=='xyz':
        if 'x' in cameraCommand:
            cameraCommandArray.append("cam x " + str(cameraCommand['x']))
        if 'y' in cameraCommand:
            cameraCommandArray.append("cam y " + str(cameraCommand['y']))
        if 'z' in cameraCommand:
            cameraCommandArray.append("cam z " + str(cameraCommand['z']))
    elif cameraType=='focus':
        if 'focus' in cameraCommand:
            cameraCommandArray.append("set pt_focus " + str(cameraCommand['focus']))

    cameraCommandString = cameraCommandString.join(cameraCommandArray)
    return cameraCommandString



def writeToMV(cameraKeyFrameData):
    print("Please open MagicaVoxel and make sure it's in the foreground.")
    pause(True) # await till active window is MagicaVoxel


    keyframenum = 0
    runningFrame = 0

    # cameraKeyFrameData contains all the info for the scene
    # camereaScene is each set of keyframes in cameraKeyFrameData
    # cameraShot is each set of frame of a camereaScene
    for cameraIndex, cameraScene in enumerate(cameraKeyFrameData):
        print(f"Camera Scene Number: {cameraIndex}")
        for index, cameraShot in enumerate(cameraScene):
            print(f"Rendering Frame Number: {index}/{len(cameraScene)-1}")

            commandPauseRender = "set pt_auto 0"
            commandResumeRender = "set pt_auto 1"
            commandRotations = cameraCommandBuilder(cameraShot, 'rotationsFovZoom')
            commandXYZ = cameraCommandBuilder(cameraShot, 'xyz')
            commandFocus = cameraCommandBuilder(cameraShot, 'focus')
            commandAnimationFrame = "set a_time " + str(runningFrame)

            if args.verbose:
                print(commandRotations)
                print(commandXYZ)
                print(commandFocus)
                print()

            pause(False)                                   
            pydi.press('f1')

            pyperclip.copy(commandPauseRender)                     
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(commandRotations)                     
            pause(False)
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')


            pyperclip.copy(commandXYZ)                     
            pause(False)
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(commandFocus)                     
            pause(False)
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(commandAnimationFrame)                     
            pause(False)
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pyperclip.copy(commandResumeRender)                     
            pydi.keyDown("ctrl")
            pydi.press("v")
            pydi.keyUp("ctrl")
            pydi.press('enter')

            pydi.press('f1')
            time.sleep(args.secondsPerFrame)   

            if not args.dryRun:
                pause(False)              
                pydi.press("6")
                typeKeyFrameNumber(runningFrame)
                time.sleep(0.4)
                pydi.press('enter')
                time.sleep(2.0)

            runningFrame += 1


try:
    main()
except KeyboardInterrupt:
    print('Interrupted')
    sys.exit(0)


