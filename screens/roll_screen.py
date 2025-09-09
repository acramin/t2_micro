# screens/roll_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Rotate
from components.buttons import PrimaryButton
from utils.calculations import calculate_modifier, calculate_proficiency_bonus
import random
import os
import math

class DiceAnimation(Widget):
    """Widget for displaying dice rolling animation with placeholder graphics"""
    dice_type = NumericProperty(20)
    current_value = NumericProperty(1)
    rotation = NumericProperty(0)
    scale = NumericProperty(1)
    
    def __init__(self, dice_type, **kwargs):
        super().__init__(**kwargs)
        self.dice_type = dice_type
        self.current_value = 1
        self.animation_event = None
        self.rolling = False
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(current_value=self.update_graphics)
        self.bind(rotation=self.update_graphics)
        self.bind(scale=self.update_graphics)
        
    def update_graphics(self, *args):
        """Update the dice graphics"""
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            
            # Center the dice
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2 + 40 
            
            # Apply rotation
            Rotate(angle=self.rotation, origin=(center_x, center_y))
            
            # Scale - made smaller (was 0.8)
            size = min(self.width, self.height) * self.scale * 0.6
            
            # Draw dice based on type
            if self.dice_type == 4:
                self.draw_d4(center_x, center_y, size)
            elif self.dice_type == 6:
                self.draw_d6(center_x, center_y, size)
            elif self.dice_type == 8:
                self.draw_d8(center_x, center_y, size)
            elif self.dice_type == 10:
                self.draw_d10(center_x, center_y, size)
            elif self.dice_type == 12:
                self.draw_d12(center_x, center_y, size)
            elif self.dice_type == 20:
                self.draw_d20(center_x, center_y, size)
            elif self.dice_type == 100:
                self.draw_d100(center_x, center_y, size)
            else:
                self.draw_generic_dice(center_x, center_y, size)
                
            PopMatrix()
    
    def draw_d6(self, x, y, size):
        """Draw a d6 (cube)"""
        Color(0.8, 0.8, 0.8, 1)  # Light gray
        half_size = size / 2
        # Simple square representation
        from kivy.graphics import Rectangle
        Rectangle(pos=(x - half_size, y - half_size), size=(size, size))
        
        # Draw the number
        Color(0, 0, 0, 1)  # Black text
        self.draw_number(x, y, self.current_value)
    
    def draw_d20(self, x, y, size):
        """Draw a d20 (icosahedron)"""
        Color(0.2, 0.6, 0.9, 1)  # Blue
        # Draw as circle for simplicity
        Ellipse(pos=(x - size/2, y - size/2), size=(size, size))
        
        # Draw the number
        Color(1, 1, 1, 1)  # White text
        self.draw_number(x, y, self.current_value)
    
    def draw_d4(self, x, y, size):
        """Draw a d4 (tetrahedron)"""
        Color(0.9, 0.2, 0.2, 1)  # Red
        # Draw as triangle
        from kivy.graphics import Triangle
        half_size = size / 2
        Triangle(points=[x, y + half_size, x - half_size, y - half_size, x + half_size, y - half_size])
        
        Color(1, 1, 1, 1)
        self.draw_number(x, y, self.current_value)
    
    def draw_d8(self, x, y, size):
        """Draw a d8 (octahedron)"""
        Color(0.2, 0.9, 0.2, 1)  # Green
        # Draw as diamond
        from kivy.graphics import Quad
        half_size = size / 2
        Quad(points=[x, y + half_size, x - half_size, y, x, y - half_size, x + half_size, y])
        
        Color(0, 0, 0, 1)
        self.draw_number(x, y, self.current_value)
    
    def draw_d10(self, x, y, size):
        """Draw a d10"""
        Color(0.9, 0.6, 0.2, 1)  # Orange
        # Draw as pentagon-like shape
        Ellipse(pos=(x - size/2, y - size/2), size=(size, size))
        
        Color(0, 0, 0, 1)
        self.draw_number(x, y, self.current_value)
    
    def draw_d12(self, x, y, size):
        """Draw a d12 (dodecahedron)"""
        Color(0.6, 0.2, 0.9, 1)  # Purple
        # Draw as circle with more complex pattern
        Ellipse(pos=(x - size/2, y - size/2), size=(size, size))
        
        Color(1, 1, 1, 1)
        self.draw_number(x, y, self.current_value)
    
    def draw_d100(self, x, y, size):
        """Draw a d100 (percentile)"""
        Color(0.9, 0.9, 0.2, 1)  # Yellow
        # Draw as two d10s side by side
        quarter_size = size / 4
        Ellipse(pos=(x - size/2, y - quarter_size), size=(size/2, size/2))
        Ellipse(pos=(x, y - quarter_size), size=(size/2, size/2))
        
        Color(0, 0, 0, 1)
        self.draw_number(x, y, self.current_value)
    
    def draw_generic_dice(self, x, y, size):
        """Draw a generic dice"""
        Color(0.7, 0.7, 0.7, 1)  # Gray
        Ellipse(pos=(x - size/2, y - size/2), size=(size, size))
        
        Color(0, 0, 0, 1)
        self.draw_number(x, y, self.current_value)
    
    def draw_number(self, x, y, number):
        """Draw the number on the dice (placeholder - in real app would use Label)"""
        # This is a simplified number display
        # In a real implementation, you'd overlay a Label widget
        pass
        
    def start_roll(self, duration=2.0):
        """Start the dice rolling animation"""
        self.rolling = True
        self.current_value = 1
        
        # Schedule value changes to simulate rolling
        self.animation_event = Clock.schedule_interval(self.update_value, 0.1)
        
        # Schedule the end of animation
        Clock.schedule_once(lambda dt: self.stop_roll(), duration)
        
        # Add visual animation (rotation and scaling)
        rotation_anim = Animation(rotation=720, duration=duration)  # Two full rotations
        rotation_anim.start(self)
        
        scale_anim = (Animation(scale=1.3, duration=duration/3) + 
                      Animation(scale=0.8, duration=duration/3) + 
                      Animation(scale=1.0, duration=duration/3))
        scale_anim.start(self)
    
    def update_value(self, dt):
        """Update the displayed value during rolling"""
        if self.rolling:
            self.current_value = random.randint(1, self.dice_type)
            
    def stop_roll(self):
        """Stop the rolling animation and get final result"""
        if self.animation_event:
            self.animation_event.cancel()
            self.animation_event = None
        
        self.rolling = False
        # Final roll
        final_result = random.randint(1, self.dice_type)
        self.current_value = final_result
        
        # Stop rotation smoothly
        stop_anim = Animation(rotation=0, duration=0.3)
        stop_anim.start(self)
        
        return final_result

class RollScreen(Screen):
    """Screen for displaying dice rolls and results"""
    
    roll_type = StringProperty("")  # "attack", "saving_throw", "ability_check", "basic", "damage"
    dice_type = NumericProperty(20)
    result = NumericProperty(0)
    modifier = NumericProperty(0)
    total = NumericProperty(0)
    roll_description = StringProperty("")
    critical_hit = BooleanProperty(False)
    critical_fail = BooleanProperty(False)
    show_attack_result = BooleanProperty(False)
    attack_success = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.dice_animation = None
        self.roll_callback = None
        self.weapon_data = None  # Store weapon data for damage rolls
        
    def on_enter(self):
        """Called when the screen is displayed"""
        # Get reference to the app instance
        if not self.app:
            from kivy.app import App
            self.app = App.get_running_app()
        
        # Reset UI state completely
        self.show_attack_result = False
        self.attack_success = False
        self.result = 0
        self.total = 0
        
        # Clear result label immediately
        if self.ids.get('result_label'):
            self.ids.result_label.text = "Preparing roll..."
        
        # Clear any existing content only once at start
        self.clear_all_containers()
        
        # Cancel any existing update events
        if hasattr(self, 'update_event'):
            self.update_event.cancel()
        
        # Start the roll animation with a small delay to ensure layout is ready
        Clock.schedule_once(lambda dt: self.start_roll(), 0.2)
    
    def clear_all_containers(self):
        """Clear all dynamic containers once"""
        if self.ids.get('animation_container'):
            self.ids.animation_container.clear_widgets()
        if self.ids.get('followup_container'):
            self.ids.followup_container.clear_widgets()
        if self.ids.get('attack_result_container'):
            self.ids.attack_result_container.clear_widgets()

    def setup_roll(self, roll_type, dice_type=20, modifier=0, description="", callback=None, weapon_data=None):
        """Set up the roll parameters"""
        self.roll_type = roll_type
        self.dice_type = dice_type
        self.modifier = modifier
        self.roll_description = description
        self.roll_callback = callback
        self.weapon_data = weapon_data
        self.critical_hit = False
        self.critical_fail = False
        self.show_attack_result = False
        self.attack_success = False
        
    def start_roll(self):
        """Start the dice roll animation"""
        if self.ids.get('animation_container') and self.roll_type != "damage":
            # Only clear if there's existing content
            container = self.ids.animation_container
            if container.children:
                container.clear_widgets()
            
            # Update result label to show rolling state
            if self.ids.get('result_label'):
                self.ids.result_label.text = "Rolling..."
            
            # Create the dice animation with bigger size for the larger container
            self.dice_animation = DiceAnimation(
                dice_type=self.dice_type,
                size_hint=(None, None),
                size=(180, 180)  # Increased from (140, 140) to (180, 180)
            )
            
            # Calculate center position before adding to container
            def setup_animation(*args):
                if container.size[0] > 0 and container.size[1] > 0:
                    # Position dice in center of container
                    self.dice_animation.center_x = container.center_x
                    self.dice_animation.center_y = container.center_y
                    
                    # Add the dice to container
                    container.add_widget(self.dice_animation)
                    
                    # Create text label positioned below dice (bigger)
                    self.current_value_label = Label(
                        text=str(self.dice_animation.current_value),
                        font_size=32,  # Increased from 24 to 32
                        bold=True,
                        color=(1, 1, 0.8, 1),  # Light yellow
                        size_hint=(None, None),
                        size=(100, 40),  # Increased from (80, 30) to (100, 40)
                        center_x=container.center_x,
                        y=self.dice_animation.y - 40  # Increased offset from -60 to -80
                    )
                    container.add_widget(self.current_value_label)
                    
                    # Start the animation
                    self.dice_animation.start_roll(duration=2.0)
                    
                    # Schedule periodic updates of the text
                    self.update_event = Clock.schedule_interval(self.update_dice_text, 0.15)
                    
                    # Schedule the result display
                    Clock.schedule_once(lambda dt: self.show_result(), 2.3)
            
            # Wait for layout to be complete, then setup animation
            Clock.schedule_once(setup_animation, 0.1)
        else:
            # For damage rolls, show result immediately
            if self.ids.get('result_label'):
                self.ids.result_label.text = "Calculating damage..."
            Clock.schedule_once(lambda dt: self.show_result(), 0.1)
    
    def update_dice_text(self, dt):
        """Update the dice value text during animation"""
        if hasattr(self, 'current_value_label') and self.dice_animation:
            self.current_value_label.text = str(self.dice_animation.current_value)
            if self.dice_animation.rolling:
                self.current_value_label.color = (1, 1, 0, 1)  # Yellow while rolling
                # Keep result label showing "Rolling..." during animation
                if self.ids.get('result_label'):
                    self.ids.result_label.text = "Rolling..."
            else:
                self.current_value_label.color = (1, 1, 1, 1)  # White when stopped
                if hasattr(self, 'update_event'):
                    self.update_event.cancel()
    
    def show_result(self):
        """Display the roll result"""
        if self.dice_animation and self.roll_type != "damage":
            # Get the final result from animation
            roll_result = self.dice_animation.current_value
        else:
            # For damage rolls, calculate directly
            roll_result = random.randint(1, self.dice_type)
        
        self.result = roll_result
        self.total = roll_result + self.modifier
        
        # Check for critical hits/fails
        if self.dice_type == 20 and self.roll_type in ["attack", "saving_throw", "ability_check"]:
            self.critical_hit = (roll_result == 20)
            self.critical_fail = (roll_result == 1)
        
        # Update the result label
        self.update_result_display()
        
        # Handle follow-up actions based on roll type
        if self.roll_type == "attack":
            self.handle_attack_result()
        elif self.roll_type == "damage":
            self.handle_damage_result()
    
    def update_result_display(self):
        """Update the result display with formatting"""
        if self.ids.get('result_label'):
            if self.roll_type == "damage":
                result_text = f"Damage: {self.total}"
                if self.critical_hit:
                    result_text += " (Critical Damage!)"
            else:
                if self.modifier != 0:
                    modifier_text = f" + {self.modifier}" if self.modifier > 0 else f" - {abs(self.modifier)}"
                    result_text = f"{self.result}{modifier_text} = {self.total}"
                else:
                    result_text = f"Result: {self.result}"
                
                if self.critical_hit:
                    result_text += " (CRITICAL HIT!)"
                elif self.critical_fail:
                    result_text += " (CRITICAL FAIL!)"
            
            self.ids.result_label.text = result_text
    
    def handle_attack_result(self):
        """Handle the result of an attack roll - let user decide hit/miss"""
        # Show the result and let the user decide if it hit or missed
        self.show_attack_result = True
        
        # Add simple message prompting user to decide
        # if self.ids.get('attack_result_container'):
        #     container = self.ids.attack_result_container
        #     if not container.children:  # Only add if empty
                
        #         # Prompt user to decide hit or miss
        #         prompt_label = Label(
        #             text="Did the attack hit or miss?",
        #             color=(0.925, 0.941, 0.945, 1),  # Light color
        #             font_size=18,
        #             bold=True,
        #             halign="center",
        #             valign="middle"
        #         )
        #         container.add_widget(prompt_label)
    
    def confirm_hit(self):
        """User confirms the attack hit - proceed to damage roll"""
        if self.weapon_data:
            self.roll_damage(None)
        else:
            # Fallback if no weapon data
            self.back_to_main()
    
    def confirm_miss(self):
        """User confirms the attack missed - return to main"""
        self.back_to_main()
    
    def handle_damage_result(self):
        """Handle the result of a damage roll"""
        # Show damage-specific buttons - only if container is empty
        if self.ids.get('followup_container'):
            container = self.ids.followup_container
            if not container.children:  # Only add if empty
                
                button_layout = BoxLayout(spacing=20, size_hint_y=None, height=60)
                
                # Roll damage again
                reroll_btn = PrimaryButton(
                    text="Roll Again",
                    size_hint_x=0.5
                )
                reroll_btn.bind(on_press=lambda x: self.roll_damage(None))
                button_layout.add_widget(reroll_btn)
                
                # Back to main
                main_btn = PrimaryButton(
                    text="Back to Main",
                    size_hint_x=0.5
                )
                main_btn.bind(on_press=lambda x: self.back_to_main())
                button_layout.add_widget(main_btn)
                
                container.add_widget(button_layout)
    
    def roll_damage(self, instance):
        """Roll damage for an attack"""
        if not self.weapon_data:
            # Default damage if no weapon data
            damage_dice = "1d8"
            damage_bonus = 0
            damage_type = "slashing"
        else:
            damage_dice = self.weapon_data.get('damage_dice', '1d8')
            damage_bonus = self.weapon_data.get('damage_bonus', 0)
            damage_type = self.weapon_data.get('damage_type', 'slashing')
        
        # Parse damage dice (e.g., "2d6")
        if 'd' in damage_dice:
            parts = damage_dice.split('d')
            count = int(parts[0]) if parts[0] else 1
            sides = int(parts[1])
            
            # Double dice on critical hit
            if self.critical_hit:
                count *= 2
                description = f"Critical Damage: {count}d{sides}"
            else:
                description = f"Damage: {damage_dice}"
            
            if damage_bonus != 0:
                description += f" + {damage_bonus}"
            description += f" ({damage_type})"
            
            # Calculate total damage
            dice_damage = sum(random.randint(1, sides) for _ in range(count))
            total_damage = dice_damage + damage_bonus
            
            # Set up damage roll display
            self.setup_roll(
                roll_type="damage",
                dice_type=sides,
                modifier=damage_bonus,
                description=description,
                weapon_data=self.weapon_data
            )
            
            # Set the result directly (showing individual dice + bonus)
            self.result = dice_damage
            self.total = total_damage
            self.show_result()
    
    def new_roll(self):
        """Start a new roll of the same type"""
        # Cancel any existing update events
        if hasattr(self, 'update_event'):
            self.update_event.cancel()
        
        # Reset critical states
        self.critical_hit = False
        self.critical_fail = False
        self.show_attack_result = False
        self.attack_success = False
        self.result = 0
        self.total = 0
        
        # Clear result label immediately
        if self.ids.get('result_label'):
            self.ids.result_label.text = "Preparing roll..."
        
        # Clear containers only once
        self.clear_all_containers()
        
        # Restart the roll with a small delay
        Clock.schedule_once(lambda dt: self.start_roll(), 0.2)
    
    def back_to_main(self):
        """Return to the main screen"""
        self.app.screen_manager.current = 'main'

class RollManager:
    """Manager class for handling different types of rolls"""
    
    def __init__(self, app):
        self.app = app
        self.current_weapon_index = 0
        self.current_ability = "STR"

    def show_ability_dialog(self, roll_type):
        """Show ability selection dialog"""
        from components.dialogs import ComprehensiveAbilityDialog
        
        def on_dialog_dismiss(instance):
            if instance.selected_option:
                self.current_ability = instance.selected_option
                if roll_type == "saving_throw":
                    self.roll_saving_throw(instance.selected_option)
                elif roll_type == "ability_check":
                    self.roll_ability_check(instance.selected_option)
        
        dialog = ComprehensiveAbilityDialog(profile_data=self.app.current_profile)
        dialog.bind(on_dismiss=on_dialog_dismiss)
        dialog.open()

    def show_weapon_dialog(self):
        """Show weapon selection dialog"""
        print("\n" + "="*40)
        print("⚔️  WEAPON SELECTION DEBUG")
        print("="*40)

        if not self.app.current_profile:
            print("❌ ERROR: No current profile found!")
            return None

        profile = self.app.current_profile
        print(f"📋 Profile: {profile.get('name', 'Unknown')}")

        weapons = self.app.current_profile.get('weapons', [])
        print(f"🔍 Found {len(weapons)} weapons in profile:")

        for i, weapon in enumerate(weapons):
            print(f"   {i}: {weapon.get('name', 'Unnamed')} (Ability: {weapon.get('ability', 'STR')}, Proficient: {weapon.get('proficient', False)})")

        if not weapons:
            print("❌ ERROR: No weapons found in profile!")
            print("💡 Please create weapons in the profile editor first")
            return None

        print("✅ Opening weapon selection dialog...")
        print("="*40 + "\n")

        from components.dialogs import WeaponDialog

        def on_dialog_dismiss(instance):
            if instance.selected_option is not None:
                weapon_index = weapons.index(next(w for w in weapons if w.get('name') == instance.selected_option))
                print(f"🎯 Selected weapon index: {weapon_index}")
                self.roll_attack(weapon_index)

        dialog = WeaponDialog(weapons)
        dialog.bind(on_dismiss=on_dialog_dismiss)
        dialog.open()
    
    def show_custom_dice_dialog(self):
        """Show custom dice selection dialog"""
        from components.dialogs import DiceDialog
        
        def on_dialog_dismiss(instance):
            if instance.selected_option:
                if instance.selected_option == "Custom":
                    self.show_custom_dice_input()
                else:
                    # Parse dice notation (e.g., "2d6")
                    if 'd' in instance.selected_option:
                        parts = instance.selected_option.split('d')
                        count = int(parts[0]) if parts[0] else 1
                        sides = int(parts[1])
                        self.roll_custom_dice(count, sides)
        
        dialog = DiceDialog()
        dialog.bind(on_dismiss=on_dialog_dismiss)
        dialog.open()

    def show_custom_dice_input(self):
        """Show custom dice input dialog"""
        # This would be implemented with a more complex dialog
        # For now, just roll 1d20 as a placeholder
        self.roll_custom_dice(1, 20)

    def roll_custom_dice(self, count, sides):
        """Roll custom dice"""
        # For multiple dice, we'll need to modify the roll screen to handle this
        # For now, just roll one die of the specified type
        roll_screen = self.app.screen_manager.get_screen('roll')
        roll_screen.setup_roll(
            roll_type="custom",
            dice_type=sides,
            modifier=0,
            description=f"{count}d{sides} Roll"
        )
        
        self.app.screen_manager.current = 'roll'

    def roll_attack(self, weapon_index=0):
        """Roll an attack with the selected weapon"""
        print("\n" + "="*50)
        print("🎲 WEAPON ATTACK CALCULATION DEBUG")
        print("="*50)

        if not self.app.current_profile:
            print("❌ ERROR: No current profile found!")
            return None

        profile = self.app.current_profile
        print(f"📋 Profile Name: {profile.get('name', 'Unknown')}")
        print(f"📊 Profile Level: {profile.get('level', 1)}")

        # Print all ability scores
        abilities = profile.get('abilities', {})
        print("🏋️  Ability Scores:")
        for ability, score in abilities.items():
            modifier = (score - 10) // 2
            print(f"   {ability}: {score} (modifier: {modifier:+d})")

        weapons = profile.get('weapons', [])
        print(f"⚔️  Weapons in Profile: {len(weapons)}")

        for i, weapon in enumerate(weapons):
            print(f"   Weapon {i}: {weapon}")

        # Only create sample weapons if this is a fresh profile with no weapons ever created
        if not weapons:
            print("⚠️  No weapons found, creating default weapons")
            weapons = [
                {
                    'name': 'Longsword',
                    'ability': 'STR',
                    'proficient': True,
                    'damage_dice': '1d8',
                    'damage_bonus': calculate_modifier(profile['abilities'].get('STR', 10)),
                    'damage_type': 'slashing'
                },
                {
                    'name': 'Dagger',
                    'ability': 'DEX',
                    'proficient': True,
                    'damage_dice': '1d4',
                    'damage_bonus': calculate_modifier(profile['abilities'].get('DEX', 10)),
                    'damage_type': 'piercing'
                }
            ]
            # Update profile with default weapons
            profile['weapons'] = weapons

        if weapon_index >= len(weapons):
            print(f"❌ ERROR: Weapon index {weapon_index} out of range (max: {len(weapons)-1})")
            weapon_index = 0

        weapon = weapons[weapon_index]
        print(f"\n🎯 Selected Weapon Details:")
        print(f"   Name: {weapon.get('name', 'Unknown')}")
        print(f"   Ability: {weapon.get('ability', 'STR')}")
        print(f"   Proficient: {weapon.get('proficient', False)}")
        print(f"   Damage Dice: {weapon.get('damage_dice', 'd6')}")
        print(f"   Damage Bonus: {weapon.get('damage_bonus', 0)}")

        ability = weapon.get('ability', 'STR')
        proficient = weapon.get('proficient', False)

        # Calculate modifiers
        ability_score = profile['abilities'].get(ability, 10)
        ability_mod = calculate_modifier(ability_score)
        prof_bonus = calculate_proficiency_bonus(profile['level']) if proficient else 0
        modifier = ability_mod + prof_bonus

        print(f"\n🧮 Modifier Calculation:")
        print(f"   Ability Score ({ability}): {ability_score}")
        print(f"   Ability Modifier: {ability_mod}")
        print(f"   Proficiency Bonus: {prof_bonus} ({'proficient' if proficient else 'not proficient'})")
        print(f"   Total Modifier: {modifier}")
        print("="*50 + "\n")

        # Set up the roll screen
        roll_screen = self.app.screen_manager.get_screen('roll')
        roll_screen.setup_roll(
            roll_type="attack",
            dice_type=20,
            modifier=modifier,
            description=f"Attack with {weapon.get('name', 'Weapon')}",
            weapon_data=weapon
        )

        self.app.screen_manager.current = 'roll'
        return modifier
    
    def roll_saving_throw(self, ability):
        """Roll a saving throw for the specified ability"""
        if not self.app.current_profile:
            return None
        
        profile = self.app.current_profile
        proficient = ability in profile.get('saving_throw_proficiencies', [])
        
        # Calculate modifiers
        ability_mod = calculate_modifier(profile['abilities'].get(ability, 10))
        prof_bonus = calculate_proficiency_bonus(profile['level']) if proficient else 0
        modifier = ability_mod + prof_bonus
        
        # Set up the roll screen
        roll_screen = self.app.screen_manager.get_screen('roll')
        roll_screen.setup_roll(
            roll_type="saving_throw",
            dice_type=20,
            modifier=modifier,
            description=f"{ability} Saving Throw"
        )
        
        self.app.screen_manager.current = 'roll'
        return modifier
    
    def roll_ability_check(self, ability_or_skill):
        """Roll an ability check for the specified ability or skill"""
        if not self.app.current_profile:
            return None
        
        profile = self.app.current_profile
        
        print("\n" + "="*50)
        print("🎯 ABILITY/SKILL CHECK DEBUG")
        print("="*50)
        print(f"📋 Profile: {profile.get('name', 'Unknown')}")
        print(f"🎲 Rolling: {ability_or_skill}")
        
        # Define skill-to-ability mapping
        skill_abilities = {
            "Acrobatics": "DEX",
            "Animal Handling": "WIS",
            "Arcana": "INT",
            "Athletics": "STR",
            "Deception": "CHA",
            "History": "INT",
            "Insight": "WIS",
            "Intimidation": "CHA",
            "Investigation": "INT",
            "Medicine": "WIS",
            "Nature": "INT",
            "Perception": "WIS",
            "Performance": "CHA",
            "Persuasion": "CHA",
            "Religion": "INT",
            "Sleight of Hand": "DEX",
            "Stealth": "DEX",
            "Survival": "WIS"
        }
        
        # Check if it's a skill or basic ability
        if ability_or_skill in skill_abilities:
            # It's a skill
            ability = skill_abilities[ability_or_skill]
            skill_proficiencies = profile.get('skill_proficiencies', [])
            print(f"🔍 Skill Proficiencies in Profile: {skill_proficiencies}")
            is_proficient = ability_or_skill in skill_proficiencies
            print(f"✅ Is proficient in {ability_or_skill}? {is_proficient}")
            
            # Calculate modifiers
            ability_score = profile['abilities'].get(ability, 10)
            ability_mod = calculate_modifier(ability_score)
            prof_bonus = calculate_proficiency_bonus(profile['level']) if is_proficient else 0
            modifier = ability_mod + prof_bonus
            
            print(f"🧮 Modifier Calculation for {ability_or_skill}:")
            print(f"   Base Ability ({ability}): {ability_score} (modifier: {ability_mod:+d})")
            print(f"   Proficiency Bonus: {prof_bonus} (Level {profile['level']})")
            print(f"   Total Modifier: {modifier:+d}")
            
            description = f"{ability_or_skill} ({ability}) Check"
            if is_proficient:
                description += " (Proficient)"
        else:
            # It's a basic ability check
            ability_mod = calculate_modifier(profile['abilities'].get(ability_or_skill, 10))
            modifier = ability_mod
            print(f"🧮 Basic Ability Check: {ability_or_skill} modifier = {modifier:+d}")
            description = f"{ability_or_skill} Check"
        
        print("="*50 + "\n")
        
        # Set up the roll screen
        roll_screen = self.app.screen_manager.get_screen('roll')
        roll_screen.setup_roll(
            roll_type="ability_check",
            dice_type=20,
            modifier=modifier,
            description=description
        )
        
        self.app.screen_manager.current = 'roll'
        return modifier
    
    def roll_dice(self, dice_type):
        """Roll a basic die with no modifiers"""
        # Set up the roll screen
        roll_screen = self.app.screen_manager.get_screen('roll')
        roll_screen.setup_roll(
            roll_type="basic",
            dice_type=dice_type,
            modifier=0,
            description=f"d{dice_type} Roll"
        )
        
        self.app.screen_manager.current = 'roll'
        return 0