# screens/main_screen.py
from typing import Optional

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock

from utils.motion_sensor import MotionSensorWatcher

class MainScreen(Screen):
    """Main screen with dice rolling interface"""
    
    # Properties
    current_character = StringProperty("None")
    motion_status = StringProperty("")
    motion_button_text = StringProperty("Motion Sensor Roll (d20)")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.motion_watcher: Optional[MotionSensorWatcher] = None
        self._motion_button_default = "Motion Sensor Roll (d20)"
        
    def on_enter(self):
        """Called when the screen is displayed"""
        # Get reference to the app instance
        if not self.app:
            from kivy.app import App
            self.app = App.get_running_app()
            
        # Update current character display
        if self.app.current_profile:
            self.current_character = self.app.current_profile.get('name', 'Unknown')
        else:
            self.current_character = "None"
        if not self.motion_status:
            self.motion_status = "Press to arm the motion sensor"
    
    def initiate_attack_roll(self):
        """Initiate an attack roll"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_weapon_dialog()

    def initiate_saving_throw(self):
        """Initiate a saving throw"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_ability_dialog("saving_throw")

    def initiate_ability_check(self):
        """Initiate an ability check"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_ability_dialog("ability_check")

    def show_custom_dice_dialog(self):
        """Show custom dice dialog"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_custom_dice_dialog()

    def roll_dice(self, sides):
        """Roll a specific die"""
        print(f"Rolling d{sides}")
        if self.app and self.app.roll_manager:
            self.app.roll_manager.roll_dice(sides)

    # ------------------------------------------------------------------
    # Motion sensor integration
    # ------------------------------------------------------------------
    def start_motion_roll(self):
        """Toggle motion sensor monitoring and roll a d20 when triggered."""
        if self.motion_watcher is None:
            self.motion_watcher = MotionSensorWatcher()

        if not self.motion_watcher.available:
            self.motion_status = "Motion sensor unavailable on this device"
            self.motion_button_text = self._motion_button_default
            return

        if self.motion_watcher.is_running:
            self.motion_watcher.stop()
            self.motion_status = "Motion sensor cancelled"
            self.motion_button_text = self._motion_button_default
            return

        def handle_detected():
            Clock.schedule_once(lambda dt: self._handle_motion_detected(), 0)

        def handle_status(message: str) -> None:
            Clock.schedule_once(lambda dt: self._update_motion_status(message), 0)

        def handle_error(exc: Exception) -> None:
            Clock.schedule_once(lambda dt: self._handle_motion_error(exc), 0)

        try:
            started = self.motion_watcher.start_monitoring(
                on_detected=handle_detected,
                on_status=handle_status,
                on_error=handle_error,
            )
        except RuntimeError as exc:
            self.motion_status = f"Motion sensor unavailable: {exc}"
            self.motion_button_text = self._motion_button_default
            return

        if started:
            self.motion_button_text = "Cancel Motion Wait"
            self.motion_status = "Waiting for motion... (press again to cancel)"

    def _update_motion_status(self, message: str) -> None:
        self.motion_status = message

    def _handle_motion_detected(self) -> None:
        self.motion_status = "Motion detected! Rolling d20..."
        self.motion_button_text = self._motion_button_default
        # Ensure watcher is stopped before rolling to allow re-arming later
        if self.motion_watcher and self.motion_watcher.is_running:
            self.motion_watcher.stop()
        self.roll_dice(20)
        Clock.schedule_once(
            lambda dt: self._update_motion_status("Motion roll complete"),
            1.0,
        )

    def _handle_motion_error(self, exc: Exception) -> None:
        self.motion_button_text = self._motion_button_default
        if self.motion_watcher and self.motion_watcher.is_running:
            self.motion_watcher.stop()
        self.motion_status = f"Sensor error: {exc}"

    def on_leave(self, *args):  # noqa: D401 - inherited hook
        """Reset motion sensor watcher when leaving the screen."""
        if self.motion_watcher and self.motion_watcher.is_running:
            self.motion_watcher.stop()
        self.motion_button_text = self._motion_button_default
        return super().on_leave(*args)