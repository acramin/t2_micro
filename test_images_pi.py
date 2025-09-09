#!/usr/bin/env python3
"""
Test script to diagnose image loading issues on Raspberry Pi
Run this on the Pi to check if images load properly
"""

import os
import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock

class ImageTestApp(App):
    def build(self):
        # Print system info
        print(f"🖥️ Platform: {platform.platform()}")
        print(f"🏗️ Architecture: {platform.architecture()}")
        print(f"💻 Machine: {platform.machine()}")
        print(f"🏠 Node: {platform.node()}")
        
        # Check if we're on Pi
        is_pi = 'arm' in platform.machine().lower() or 'raspberry' in platform.node().lower()
        print(f"🥧 Raspberry Pi detected: {is_pi}")
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Add title
        title = Label(text='Dice Image Loading Test', font_size='24sp', size_hint_y=0.2)
        layout.add_widget(title)
        
        # Test loading each dice image
        dice_types = [4, 6, 8, 10, 12, 20, 100]
        
        for dice_type in dice_types:
            image_path = f"assets/images/d{dice_type}.png"
            abs_path = os.path.abspath(image_path)
            
            print(f"\n🎲 Testing d{dice_type}:")
            print(f"   Path: {image_path}")
            print(f"   Absolute: {abs_path}")
            print(f"   Exists: {os.path.exists(abs_path)}")
            
            if os.path.exists(abs_path):
                # Create image widget
                img = Image(
                    source=abs_path,
                    allow_stretch=True,
                    keep_ratio=True,
                    size_hint=(None, None),
                    size=(80, 80)
                )
                
                # Schedule texture check
                Clock.schedule_once(lambda dt, d=dice_type, i=img: self.check_texture(d, i), 0.5)
                
                # Add to layout
                row = BoxLayout(orientation='horizontal', size_hint_y=0.1)
                label = Label(text=f"D{dice_type}:", size_hint_x=0.3)
                row.add_widget(label)
                row.add_widget(img)
                layout.add_widget(row)
            else:
                print(f"   ❌ File not found!")
        
        return layout
    
    def check_texture(self, dice_type, image_widget):
        """Check if image texture loaded properly"""
        if image_widget.texture:
            print(f"✅ D{dice_type} texture loaded: {image_widget.texture.width}x{image_widget.texture.height}")
        else:
            print(f"❌ D{dice_type} texture failed to load")
            
    def on_start(self):
        # Print Kivy image providers
        try:
            from kivy.core.image import Image as CoreImage
            print(f"\n📷 Available image providers: {CoreImage.providers}")
        except Exception as e:
            print(f"❌ Error getting image providers: {e}")

if __name__ == '__main__':
    ImageTestApp().run()
