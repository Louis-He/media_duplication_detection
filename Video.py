from Media import Media
import ffmpeg

from datetime import datetime
import time
from util import *


class Video(Media):
    def __init__(self, file_abs_path):
        Media.__init__(self, file_abs_path)

        self.set_creation_time()

    def set_creation_time(self) -> None:
        vid = ffmpeg.probe(self.file_abs_path)
        if "format" in vid:
            video_format = vid["format"]
            if "tags" in video_format:
                video_tags = video_format["tags"]
                if "creation_time" in video_tags:
                    creation_time = video_tags["creation_time"]
                    self.creation_datetime = datetime.strptime(creation_time[:creation_time.find('.')],
                                                               "%Y-%m-%dT%H:%M:%S")
                    self.valid_creation_datetime = True
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError