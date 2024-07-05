import logging
import math
import os
import time


class BasicData:
    def __init__(self, hr_data_path: str, gps_data_path: str) -> None:
        self.hr_data_path = hr_data_path
        self.gps_data_path = gps_data_path
        self.current_speed = None
        self.last_valid_speed = None  # Add this attribute
        self.current_heart_rate = None
        self.previous_gps = None
        self.current_gps = None
        self.distance = 0.0

        with open(self.gps_data_path, 'a') as f:
            f.truncate(0)
        with open(self.hr_data_path, 'a') as f:
            f.truncate(0)

    def read_current_hr(self) -> None:
        if not os.path.exists(self.hr_data_path):
            self.current_heart_rate = None
            return

        with open(self.hr_data_path, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            try:
                hr = int(f.readline().decode().rstrip())
                self.current_heart_rate = str(hr)
            except ValueError:
                self.current_heart_rate = None

    def read_current_gps(self) -> None:
        if not os.path.exists(self.gps_data_path):
            self.current_speed = None
            return

        with open(self.gps_data_path, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            try:
                self.previous_gps = self.current_gps
                gps = f.readline().decode().rstrip().split(';')
                self.current_gps = (
                    float(gps[1]), float(gps[0]), float(gps[2]), float(gps[3])
                )
            except IndexError:
                self.previous_gps = None
                self.current_gps = None

    def calculate_speed(self) -> None:
        if not self.previous_gps or not self.current_gps:
            self.current_speed = None
            return

        if time.time() - self.current_gps[3] > 1.5:
            self.current_speed = None
            return

        R = 6373.0
        lat1 = math.radians(self.previous_gps[0])
        lat2 = math.radians(self.current_gps[0])
        lon1 = math.radians(self.previous_gps[1])
        lon2 = math.radians(self.current_gps[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (
            math.sin(dlat / 2)**2 +
            math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        self.distance = 1000 * R * c
        t = self.current_gps[3] - self.previous_gps[3]
        if t:
            self.current_speed = 3.6 * self.distance / t
            self.last_valid_speed = self.current_speed  # Update last valid speed
        logging.debug(f"Distance: {self.distance}, Time: {t}, Speed: {self.current_speed}")
