# ADB (Android Debug Bridge) Cheatsheet

ADB is the command-line bridge between your dev machine and an Android device/emulator, used for installing apps, debugging, logging, file transfer, and shell access.

## Setup & Connection

```bash
adb devices                     # list connected devices/emulators
adb devices -l                     # with extra details (product, model, transport id)

adb start-server                 # start the adb server
adb kill-server                     # stop it
adb usb                                # switch a device to USB mode

# Wireless debugging (Android 11+, no cable needed after initial pairing)
adb pair 192.168.1.50:41234          # pair using the code shown on-device (Developer Options > Wireless debugging)
adb connect 192.168.1.50:5555           # connect over Wi-Fi
adb disconnect 192.168.1.50:5555

# Wireless debugging (older method, needs an initial USB connection)
adb tcpip 5555                    # switch device to listen over TCP/IP on port 5555
adb connect 192.168.1.50:5555        # then connect over Wi-Fi
adb usb                                 # switch back to USB mode

# Multiple devices — target a specific one with -s
adb devices                     # get the device serial
adb -s emulator-5554 shell           # target a specific device
adb -s <serial> install app.apk

adb -d shell           # target the only connected USB device
adb -e shell               # target the only running emulator
```

## App Installation & Management

```bash
adb install app.apk
adb install -r app.apk                # reinstall, keep data (-r = replace)
adb install -g app.apk                   # grant all runtime permissions automatically
adb install -t app.apk                      # allow test packages
adb install -d app.apk                         # allow version downgrade
adb install --bypass-low-target-sdk-block app.apk

adb install-multiple base.apk split1.apk         # install an app bundle's split APKs

adb uninstall com.example.myapp
adb uninstall -k com.example.myapp          # uninstall but keep data/cache

adb shell pm list packages                 # list all installed packages
adb shell pm list packages -3                 # third-party (user-installed) only
adb shell pm list packages -s                    # system packages only
adb shell pm list packages -f                       # include the APK file path
adb shell pm list packages | grep myapp                # filter by name

adb shell pm path com.example.myapp          # path to the installed APK on-device
adb shell pm clear com.example.myapp             # clear app data/cache (like a factory-reset for that app)
adb shell pm disable com.example.myapp              # disable an app
adb shell pm enable com.example.myapp                  # re-enable
adb shell pm grant com.example.myapp android.permission.CAMERA
adb shell pm revoke com.example.myapp android.permission.CAMERA
adb shell dumpsys package com.example.myapp                # full package info dump
```

## Launching & Controlling Apps

```bash
adb shell am start -n com.example.myapp/.MainActivity      # launch a specific activity
adb shell am start -a android.intent.action.VIEW -d "https://example.com"    # launch via intent (e.g. open a URL)
adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p com.example.myapp    # launch app's default entry point

adb shell am force-stop com.example.myapp        # force-stop an app
adb shell am kill com.example.myapp                  # kill a background process (gentler than force-stop)
adb shell am broadcast -a com.example.MY_ACTION           # send a broadcast intent

adb shell monkey -p com.example.myapp -c android.intent.category.LAUNCHER 1     # launch via monkey tool (random-event stress testing tool)
adb shell monkey -p com.example.myapp -v 500          # send 500 random events (stress test)

adb shell dumpsys activity activities | grep mResumedActivity     # what's currently in the foreground
```

## Logging (Logcat)

```bash
adb logcat                    # stream all logs (very verbose)
adb logcat -c                    # clear the log buffer
adb logcat -d                       # dump current buffer and exit (don't stream)

adb logcat *:E                # only Error level and above, all tags
adb logcat *:W                   # Warning and above
adb logcat MyTag:D *:S               # only "MyTag" at Debug+, silence everything else (:S = silent)

adb logcat --pid=$(adb shell pidof -s com.example.myapp)      # filter to a specific app's process
adb logcat | grep com.example.myapp

adb logcat -v time              # include timestamps
adb logcat -v threadtime           # timestamps + thread/process IDs (most detailed common format)

adb logcat -f /sdcard/log.txt         # write log output to a file on-device
adb logcat > log.txt                     # redirect to a file on your machine

# Log levels: V (Verbose), D (Debug), I (Info), W (Warning), E (Error), F (Fatal), S (Silent)
```

## File Transfer

```bash
adb push local_file.txt /sdcard/           # copy from computer to device
adb push local_dir/ /sdcard/remote_dir/       # copy a whole directory

adb pull /sdcard/file.txt ./                 # copy from device to computer
adb pull /sdcard/DCIM/ ./photos/                # copy a whole directory

adb shell ls /sdcard/
adb shell ls -la /data/local/tmp/

adb shell mkdir /sdcard/mydir
adb shell rm /sdcard/file.txt
adb shell rm -r /sdcard/mydir

# Pull an installed app's APK off the device
adb shell pm path com.example.myapp
adb pull /data/app/~~xxxx/com.example.myapp-xxxx/base.apk ./myapp.apk
```

## Shell Access

```bash
adb shell                    # interactive shell on the device
adb shell <command>              # run a single command and return

adb shell pwd
adb shell whoami
adb shell id
adb shell getprop                     # list all system properties
adb shell getprop ro.build.version.release      # Android version
adb shell getprop ro.product.model                 # device model
adb shell setprop debug.myprop value                  # set a property (some require root)

adb shell su               # switch to root (requires a rooted device/emulator)
adb root                       # restart adbd with root permissions (on rootable builds, e.g. emulators)
adb unroot                        # go back to unprivileged adbd

adb shell input tap 500 1000           # simulate a tap at (x, y)
adb shell input swipe 100 500 100 100     # simulate a swipe
adb shell input text "hello"                 # type text
adb shell input keyevent 4                      # simulate a key press (4 = BACK)
adb shell input keyevent KEYCODE_HOME              # can use symbolic names too
adb shell input keyevent KEYCODE_ENTER

# Common keyevent codes: 3=HOME, 4=BACK, 26=POWER, 82=MENU, 24/25=VOLUME_UP/DOWN
```

## Device Info & Diagnostics

```bash
adb shell dumpsys battery              # battery stats
adb shell dumpsys battery set level 50    # simulate battery level (testing)
adb shell dumpsys battery reset               # reset to real values

adb shell dumpsys meminfo com.example.myapp     # memory usage for an app
adb shell dumpsys cpuinfo                          # CPU usage snapshot
adb shell top                                          # live process monitor (like Linux top)
adb shell ps                                              # list running processes
adb shell ps -A | grep myapp

adb shell dumpsys connectivity           # network connectivity state
adb shell dumpsys wifi                      # wifi state
adb shell settings get global wifi_on          # check a specific setting
adb shell settings put global wifi_on 0           # turn wifi off programmatically
adb shell svc wifi enable                            # alternate way to control wifi
adb shell svc wifi disable
adb shell svc data enable                               # mobile data on/off
adb shell svc data disable

adb shell wm size                # screen resolution
adb shell wm density                # screen density (dpi)
adb shell wm size 1080x1920           # override resolution (testing)
adb shell wm density 420                 # override density
adb shell wm size reset                     # reset overrides

adb bugreport                # generate a full bug report bundle (very detailed system dump)
adb shell dumpsys > full_dump.txt      # full system service dump
```

## Screenshots & Screen Recording

```bash
adb shell screencap /sdcard/screenshot.png
adb pull /sdcard/screenshot.png ./

adb exec-out screencap -p > screenshot.png     # capture directly to your machine, no intermediate file

adb shell screenrecord /sdcard/demo.mp4              # record until Ctrl+C or 3-min limit
adb shell screenrecord --time-limit 30 /sdcard/demo.mp4    # limit to 30 seconds
adb shell screenrecord --bit-rate 4000000 /sdcard/demo.mp4    # custom bitrate
adb pull /sdcard/demo.mp4 ./
```

## Emulator Control

```bash
emulator -list-avds                # list available virtual devices
emulator -avd Pixel_7_API_34            # launch a specific AVD
emulator -avd Pixel_7_API_34 -no-snapshot-load     # cold boot, skip snapshot

adb emu geo fix -122.084 37.4219         # set mock GPS location (lng, lat) on the emulator
adb emu kill                                # kill the running emulator

adb -e shell            # target the emulator specifically when multiple devices are connected
```

## Backup & Restore

```bash
adb backup -apk -all -f backup.ab           # full device backup (deprecated on modern Android, limited use)
adb restore backup.ab

# Modern approach — app-specific data extraction
adb shell bmgr backupnow com.example.myapp        # trigger Backup Manager backup for one app (needs backup agent configured)
```

## Package/Build Debugging (relevant to Android dev workflows)

```bash
adb shell dumpsys package com.example.myapp | grep versionName     # installed version
adb shell dumpsys package com.example.myapp | grep versionCode

adb shell content query --uri content://com.example.myapp.provider/table    # query a ContentProvider directly

adb logcat -b crash              # dedicated crash log buffer
adb logcat -b all                   # all log buffers (main, system, crash, radio, events)

adb shell am start -W -n com.example.myapp/.MainActivity    # launch + report cold-start timing (great for perf checks)
```

## Port Forwarding & Reverse Tunneling

```bash
adb forward tcp:8080 tcp:8080         # host port -> device port (access a device-side server from your machine)
adb forward --list
adb forward --remove tcp:8080
adb forward --remove-all

adb reverse tcp:3000 tcp:3000            # device port -> host port (device connects to something running on your machine,
                                              # e.g. a local dev API server — very common for React Native / mobile dev)
adb reverse --list
adb reverse --remove tcp:3000
adb reverse --remove-all
```

## Common Development Workflow Snippets

```bash
# Full reinstall-and-launch cycle during active development
adb install -r app-debug.apk && adb shell am start -n com.example.myapp/.MainActivity

# Clear app data and relaunch fresh (useful for testing first-run/onboarding flows)
adb shell pm clear com.example.myapp && adb shell am start -n com.example.myapp/.MainActivity

# Watch logs for just your app while reproducing a bug
adb logcat -c && adb logcat --pid=$(adb shell pidof -s com.example.myapp)

# Check if a specific permission was granted
adb shell dumpsys package com.example.myapp | grep -A1 "requested permissions"

# Grab a fresh screenshot straight into your project's screenshots folder
adb exec-out screencap -p > ./screenshots/latest.png

# Simulate low battery / airplane mode for testing
adb shell dumpsys battery set level 15
adb shell settings put global airplane_mode_on 1
adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
```

## Common Gotchas

- `adb devices` showing "unauthorized" means the device hasn't accepted the RSA debugging key prompt yet — check the device screen and tap "Allow."
- `adb install -r` preserves app data; a plain reinstall without `-r` after uninstalling wipes it — decide deliberately based on whether you're testing fresh-install behavior.
- Multiple connected devices/emulators require `-s <serial>` (or `-d`/`-e` shortcuts) on every command, or ADB will error out asking you to specify one.
- `adb logcat` without filters is extremely noisy — always filter by tag, level, or PID for anything beyond a first look.
- Wireless debugging pairing codes and connection are two separate steps on Android 11+ (`adb pair` then `adb connect`) — don't confuse them with the older `adb tcpip` method, which requires an initial USB connection.
- `adb root` only works on debuggable builds (emulators, userdebug/eng builds) — it will fail silently or with a permission error on a standard retail device.
- File paths on Android are case-sensitive and `/sdcard/` is typically a symlink to the actual external storage path — behavior can vary slightly by Android version/OEM.
