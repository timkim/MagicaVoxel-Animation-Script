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
                                                             

MV_TITLE = "MagicaVoxel | Ephtracy"

def foregroundTitle() -> str:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    return buf.value

def waitForTitle(predicate, timeout):
    end = time.time() + timeout
    while time.time() < end:
        title = foregroundTitle()
        if predicate(title):
            return title
        time.sleep(0.1)
    return None

def pasteLine(text):
    """Paste one line into the (already focused) console and run it."""
    pyperclip.copy(text)
    pydi.keyDown("ctrl"); pydi.press("v"); pydi.keyUp("ctrl")
    time.sleep(0.1)
    pydi.press('enter')

def saveSnapshot(name):
    """Snapshot via the console (`snap scene`, the command the 6 hotkey runs) while the console is still open,
    wait for the save dialog, paste the whole file name, confirm, and wait for the dialog to close.
    Pressing 6 relied on the console having been toggled shut with F1; one lost F1 made every later 6 land in
    the console ("66666"). Closing the save dialog always leaves the console closed, ready for the next frame."""
    pasteLine("snap scene")
    dialog = waitForTitle(lambda t: t != MV_TITLE and t != "", args.dialogTimeout)
    if dialog is None:
        print(f"WARNING: save dialog did not open for frame {name}; skipping this snapshot")
        return False
    time.sleep(0.3)
    pyperclip.copy(name)
    pydi.keyDown("ctrl"); pydi.press("a"); pydi.keyUp("ctrl")      # replace the default snap name
    pydi.keyDown("ctrl"); pydi.press("v"); pydi.keyUp("ctrl")
    time.sleep(0.2)
    pydi.press('enter')
    # Wait for the dialog to close. If Windows asks to confirm an overwrite (re-render), answer Yes.
    for _ in range(3):
        back = waitForTitle(lambda t: t == MV_TITLE, args.dialogTimeout)
        if back is not None:
            time.sleep(args.afterSaveSeconds)   # let MagicaVoxel finish writing/refocusing before the next F1
            return True
        print(f"Frame {name}: '{foregroundTitle()}' is still open (overwrite prompt?) - answering Yes")
        pydi.keyDown("alt"); pydi.press("y"); pydi.keyUp("alt")
    print(f"WARNING: could not confirm the save for frame {name}")
    return False

def exitprog():
    input("Press Enter to continue...")
    sys.exit()

def typeKeyFrameNumber(keyFrameNumber):
    if(keyFrameNumber) < 10:
        pydi.press(str(keyFrameNumber))
    elif(keyFrameNumber) > 99:
        hundreds = (keyFrameNumber % 1000)
        tens = (keyFrameNumber % 100)
        units = (keyFrameNumber % 10)
        pydi.press(str(int(hundreds/100)))
        pydi.press(str(int(tens/10)))
        pydi.press(str(units))
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
    parser.add_argument("-t", "--cameraText", help="Display camera commands and don't save any renders", action="store_true")
    parser.add_argument("--padding", help="Digits in saved frame names, e.g. 4 -> 0016. Defaults to 4", type=int, default=4)
    parser.add_argument("--dialogTimeout", help="Seconds to wait for MagicaVoxel's save dialog to open or close. Defaults to 20", type=float, default=20.0)
    parser.add_argument("--afterSaveSeconds", help="Seconds to wait after the save dialog closes before the next frame. Defaults to 2", type=float, default=2.0)
    parser.add_argument("--startFrame", help="Skip frames before this overall frame number (to resume an interrupted render). Defaults to 0", type=int, default=0)
    parser.add_argument("--settleSeconds", help="Seconds to wait after sending a frame's commands before the render timer starts (raise for heavy animated scenes). Defaults to 2", type=float, default=2.0)
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
                    if not 'interpolation' in z:
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

                    currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, yaw['start'], yaw['end'], data['keyframes'][i]['frames'])
                    #if yaw['direction'] == 'clockwise':
                        #currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, normalise(yaw['start']), normalise(yaw['end']), data['keyframes'][i]['frames'])
                    #elif yaw['direction'] == 'counterclockwise':
                        #currentFrameData[currentFrame]['yaw'] = interpolate(yaw['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, normalise(yaw['start']), normaliseNeg(yaw['end']), data['keyframes'][i]['frames'])

                elif not 'end' in yaw:
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

            if 'aperture' in data['keyframes'][i]['camera']:
                aperture = data['keyframes'][i]['camera']['aperture']
                if 'end' in aperture:
                    if not 'interpolation' in aperture:
                        aperture['interpolation'] = 'linear'
                    currentFrameData[currentFrame]['aperture'] = interpolate(aperture['interpolation'], currentFrame/data['keyframes'][i]['frames'], currentFrame, aperture['start'], aperture['end'], data['keyframes'][i]['frames'])
                elif not 'end' in aperture:
                    currentFrameData[currentFrame]['aperture'] =  aperture['start']

        cameraKeyFrameData.append(currentFrameData)

    return cameraKeyFrameData

def normalise(val):
    return 

def normaliseNeg(val):
    return (val % -360 + -360) % -360

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
        case 'circularOut':
            return circularOut(percent, elapsed, start, end, total)
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

def circularOut(percent, elapsed, start, end, total):
    ease = CircularEaseOut(start, end, total)
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
    elif cameraType=='aperture':
        if 'aperture' in cameraCommand:
            cameraCommandArray.append("set pt_dof " + str(cameraCommand['aperture']))

    cameraCommandString = cameraCommandString.join(cameraCommandArray)
    return cameraCommandString



def writeToMV(cameraKeyFrameData):
    print("Please open MagicaVoxel and make sure it's in the foreground, in Render mode, with the console NOT active.")
    pause(True) # await till active window is MagicaVoxel


    keyframenum = 0
    runningFrame = 0
    animationFrame = 0
    totalFrames = sum(len(scene) for scene in cameraKeyFrameData)
    print(f"{totalFrames} frames in {len(cameraKeyFrameData)} camera segment(s)")
    if args.startFrame:
        print(f"Resuming from frame {args.startFrame}")

    # cameraKeyFrameData contains all the info for the scene
    # camereaScene is each set of keyframes in cameraKeyFrameData
    # cameraShot is each set of frame of a camereaScene
    for cameraIndex, cameraScene in enumerate(cameraKeyFrameData):
        if args.verbose:
            print(f"Camera Scene Number: {cameraIndex}")
        for index, cameraShot in enumerate(cameraScene):
            if runningFrame < args.startFrame:          # resuming: skip frames already rendered
                animationFrame += 1
                runningFrame += 1
                continue
            print(f"Rendering frame {runningFrame}/{totalFrames-1} (segment {cameraIndex}, shot {index+1}/{len(cameraScene)}) -> {runningFrame:0{args.padding}d}.png")

            commandPauseRender = "set pt_auto 0"
            commandResumeRender = "set pt_auto 1"
            commandRotations = cameraCommandBuilder(cameraShot, 'rotationsFovZoom')
            commandXYZ = cameraCommandBuilder(cameraShot, 'xyz')
            commandFocus = cameraCommandBuilder(cameraShot, 'focus')
            commandAperture = cameraCommandBuilder(cameraShot, 'aperture')

            commandAnimationFrame = "set a_time " + str(int((animationFrame)))

            if args.verbose:
                print(commandRotations)
                print(commandXYZ)
                print(commandFocus)
                print(commandAperture)
                print()

            pause(False)

            if not args.cameraText:
                # The console is closed here: either the run just started, or MagicaVoxel's save dialog just
                # closed (which always leaves the console closed). F1 is a toggle, so we only ever press it from
                # this known state; everything else for the frame goes through the open console.
                pydi.press('f1')
                time.sleep(0.3)

                # Send the whole frame as ONE chained console line. Separate pastes sent while MagicaVoxel was
                # busy after `set a_time` got dropped, which left progressive rendering paused.
                parts = [commandPauseRender, commandRotations, commandXYZ, commandFocus, commandAperture,
                         commandAnimationFrame, commandResumeRender]
                frameCommand = ' | '.join(p for p in parts if p)
                if args.verbose:
                    print(frameCommand)
                pasteLine(frameCommand)                 # console stays open after Enter
                time.sleep(args.settleSeconds)          # let heavy scenes finish posing before the render timer starts
                time.sleep(args.secondsPerFrame)

                if not args.dryRun:
                    pause(False)
                    saveSnapshot(f"{runningFrame:0{args.padding}d}")   # closes the console via the save dialog
                else:
                    pydi.press('f1')                    # dry run: close the console again ourselves
                    time.sleep(0.3)

            animationFrame += 1
            runningFrame += 1


try:
    main()
except KeyboardInterrupt:
    print('Interrupted')
    sys.exit(0)


