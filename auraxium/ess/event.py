from datetime import datetime
from typing import Dict


class Event():
    def __init__(self, payload: Dict[str, str]) -> None:
        try:
            timestamp = int(payload['timestamp'])
        except TypeError:
            raise ValueError(f'invalid timestamp: {payload["timestamp"]}')
        self.timestamp = datetime.utcfromtimestamp(timestamp)
        self.payload = {}
        # Convert datatypes
        for key, value in payload.items():
            if key == 'timestamp':
                self.payload[key] = datetime.utcfromtimestamp(int(value))
            try:
                self.payload[key] = int(value)
            except ValueError:
                try:
                    self.payload[key] = float(value)
                except ValueError:
                    self.payload[key] = value
