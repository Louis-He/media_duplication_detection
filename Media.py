import os
from datetime import datetime
import time
from util import *

class Media:
    def __init__(self, _file_abs_path):
        self.file_abs_path = _file_abs_path
        self.file_name = os.path.basename(_file_abs_path)
        _, _file_extension = os.path.splitext(_file_abs_path)
        self.file_extension = _file_extension.lower()

        self.file_size = None
        self.valid_creation_datetime = False
        self.creation_datetime = None

        self.set_file_size()

    @staticmethod
    def is_Duplicate(media_a, media_b) -> bool:

        return True

    def set_creation_time(self) -> None:
        raise NotImplementedError

    def override_creation_time(self) -> None:
        if self.creation_datetime is not None and self.valid_creation_datetime:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            timestamp = time.mktime(self.creation_datetime.timetuple())
            try:
                os.utime(self.file_abs_path, (ts, timestamp))
            except:
                msg_debug(DEBUG_LEVEL.warning, "Creation time override failed: " + self.file_abs_path)
        else:
            msg_debug(DEBUG_LEVEL.info, "Override failed. Creation time cannot get from the photo: " + self.file_abs_path)

    def set_file_size(self) -> None:
        file_stats = os.stat(self.file_abs_path)
        self.file_size = file_stats.st_size

    def get_hashable_str(self) -> str:
        return str(self.file_size) + str(self.creation_datetime)
