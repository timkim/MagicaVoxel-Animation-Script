# MagicaVoxel Animation Script

Animate MagicaVoxel's camera for dynamic renders and animations.

The script drives MagicaVoxel through its console. For each frame it sends the camera position, rotation, zoom, field of view and depth of field, advances the scene's animation by one frame, waits for the progressive renderer, and saves a snapshot. Camera moves are described as keyframe segments in a JSON file and interpolated with linear or eased curves.

> **Windows only.** The script sends keystrokes to the MagicaVoxel window (`pydirectinput`) and uses the clipboard to paste commands into the console.

## Requirements

- Windows
- [MagicaVoxel](https://ephtracy.github.io/) (originally built for 0.99.6.4)
- [Python](https://www.python.org/) 3.10 or newer

## Installation

```powershell
git clone https://github.com/timkim/MagicaVoxel-Animation-Script.git
cd MagicaVoxel-Animation-Script
pip install -r requirements.txt
```

## Usage

1. Open your scene in MagicaVoxel and switch to **Render** mode. Make sure the console is **closed**.
2. Run the script with a camera file:

   ```powershell
   python .\Animation.py -c .\camera.json -s 15
   ```

3. Click the MagicaVoxel window. The script waits until MagicaVoxel is in the foreground, then starts rendering.

Each frame is saved through MagicaVoxel's snapshot dialog as a zero-padded file name (`0000.png`, `0001.png`, ...).

Don't use the computer while a render is running. If you switch away from MagicaVoxel, the script pauses and waits until you bring it back. Press `Ctrl+C` in the terminal to stop.

### Options

| Option | Default | Description |
| --- | --- | --- |
| `-c`, `--camera` | `camera.json` | Path to the camera JSON file. |
| `-s`, `--secondsPerFrame` | `1` | Seconds to let each frame render before saving. |
| `--settleSeconds` | `2` | Extra wait after sending a frame's commands, before the render timer starts. Increase it for heavy animated scenes. |
| `--startFrame` | `0` | Skip frames before this number. Use it to resume an interrupted render. |
| `--padding` | `4` | Digits in saved file names (4 gives `0016.png`). |
| `--dialogTimeout` | `20` | Seconds to wait for the save dialog to open or close. |
| `--afterSaveSeconds` | `2` | Seconds to wait after the save dialog closes before the next frame. |
| `-d`, `--dryRun` | off | Move the camera through every frame without saving snapshots. |
| `-t`, `--cameraText` | off | Don't send anything to MagicaVoxel. Only print progress (add `-v` to print the commands too). |
| `-v`, `--verbose` | off | Print the parsed arguments, the camera file and the generated console commands. |

To resume a render that stopped after frame 41:

```powershell
python .\Animation.py -c .\metro_fall.json -s 15 --startFrame 42
```

## Camera file format

A camera file is a list of keyframe segments that play one after another. Each segment has a frame count and a set of camera properties.

```json
{
    "keyframes": [
        {
            "frames": 40,
            "camera": {
                "x":     { "start": -8 },
                "y":     { "start": -8 },
                "z":     { "start": 30 },
                "zoom":  { "start": 260, "end": 340, "interpolation": "easeInOut" },
                "pitch": { "start": -18, "end": -22, "interpolation": "easeInOut" },
                "yaw":   { "start": 35,  "end": 50 },
                "roll":  { "start": 0 }
            }
        },
        {
            "frames": 60,
            "camera": {
                "zoom":  { "start": 340, "end": 1200, "interpolation": "easeInOut" },
                "pitch": { "start": -22, "end": -30, "interpolation": "easeInOut" },
                "yaw":   { "start": 50,  "end": 90 }
            }
        }
    ]
}
```

Each property takes:

- `start` (required): the value at the first frame of the segment.
- `end` (optional): the value to move toward. Without it, the property stays at `start` for the whole segment.
- `interpolation` (optional): `linear` (default), `easeIn`, `easeOut`, `easeInOut` (quadratic curves) or `circularOut` (starts fast, slows sharply into `end`). Unknown values fall back to `linear`.

The last frame of a segment stops one step short of `end`. To get a seamless move, start the next segment at the previous segment's `end` value.

Properties you leave out of a segment are not sent, so the camera keeps its current value.

### Camera properties

| Property | MagicaVoxel command | Description |
| --- | --- | --- |
| `x`, `y`, `z` | `cam x`, `cam y`, `cam z` | Camera target position. |
| `pitch` | `cam rx` | Rotation around the X axis. |
| `yaw` | `cam ry` | Rotation around the Y axis. |
| `roll` | `cam rz` | Rotation around the Z axis. |
| `zoom` | `cam zoom` | Distance from the target. |
| `fov` | `set pt_fov` | Field of view. |
| `focus` | `set pt_focus` | Depth-of-field focus distance. |
| `aperture` | `set pt_dof` | Depth-of-field aperture. |

### Scene animation

Every rendered frame also runs `set a_time <n>`, where `n` is the overall frame number. Animated models in the scene advance one animation frame per rendered frame, in sync with the camera.

## Example camera files

The repository includes `camera.json` and the `metro_fall*.json` paths as starting points.

## Credits

Based on the original MagicaVoxel Animation Script by DimasVoxel ([executable](https://dimasvoxel.gumroad.com/l/KrSWL), [video walkthrough](https://youtu.be/9lkYa2ao8XM)). The video covers the original version, which used a different camera file format.
