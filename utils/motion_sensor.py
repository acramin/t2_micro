"""Utilities for monitoring a PIR motion sensor on the Raspberry Pi."""

from __future__ import annotations

import threading
import time
from typing import Callable, Optional

try:  # pragma: no cover - GPIO is only available on the Pi
    import RPi.GPIO as GPIO  # type: ignore
except (ImportError, RuntimeError):
    GPIO = None  # type: ignore

StatusCallback = Optional[Callable[[str], None]]
ErrorCallback = Optional[Callable[[Exception], None]]
DetectedCallback = Optional[Callable[[], None]]


class MotionSensorWatcher:
    """Background helper that waits for motion and triggers a callback."""

    def __init__(
        self,
        pin: int = 17,
    settle_time: float = 20.0,
        poll_interval: float = 0.1,
    ) -> None:
        self.pin = pin
        self.settle_time = settle_time
        self.poll_interval = poll_interval

        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

        self._on_detected: DetectedCallback = None
        self._on_status: StatusCallback = None
        self._on_error: ErrorCallback = None

        self._is_running = False

    @property
    def available(self) -> bool:
        """Return True when RPi.GPIO is available on the device."""
        return GPIO is not None

    @property
    def is_running(self) -> bool:
        """Indicate whether the watcher is currently monitoring the sensor."""
        return self._is_running

    def start_monitoring(
        self,
        *,
        on_detected: DetectedCallback,
        on_status: StatusCallback = None,
        on_error: ErrorCallback = None,
    ) -> bool:
        """Start watching the PIR sensor in a background thread."""
        if not self.available:
            raise RuntimeError("RPi.GPIO is not available on this system")

        if self._thread and self._thread.is_alive():
            return False  # Already running

        self._stop_event.clear()
        self._on_detected = on_detected
        self._on_status = on_status
        self._on_error = on_error

        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        self._is_running = True
        return True

    def stop(self) -> None:
        """Stop monitoring and clean up GPIO resources."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._cleanup_gpio()
        self._is_running = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _monitor_loop(self) -> None:
        try:
            if self._on_status:
                self._on_status("Stabilizing sensor...")

            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)

            if self.settle_time > 0:
                time.sleep(self.settle_time)

            if self._on_status:
                self._on_status("Ready - waiting for motion")

            while not self._stop_event.is_set():
                if GPIO.input(self.pin):
                    if self._on_status:
                        self._on_status("Motion detected!")
                    if self._on_detected:
                        self._on_detected()
                    break
                time.sleep(self.poll_interval)
        except Exception as exc:  # pragma: no cover - hardware specific
            if self._on_error:
                self._on_error(exc)
        finally:
            self._cleanup_gpio()
            self._is_running = False

    def _cleanup_gpio(self) -> None:
        if GPIO is None:
            return
        try:
            GPIO.cleanup(self.pin)
        except RuntimeError:
            # GPIO.cleanup can raise if GPIO wasn't set up; swallow gently
            pass
