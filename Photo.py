from Media import Media

from PIL import Image, UnidentifiedImageError
import os
# from pillow_heif import register_heif_opener
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

from datetime import datetime
from util import *


class Photo(Media):
    def __init__(self, file_abs_path):
        Media.__init__(self, file_abs_path)

        self.CREATION_TAG = [306]

        self.set_creation_time()

    @staticmethod
    def get_geotagging(exif):
        exif = exif.get_ifd(34853)

        geo_tagging_info = {}
        if not exif:
            return ""
        else:
            gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                        'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                        'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                        'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude',
                        'GPSDestLongitudeRef',
                        'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef',
                        'GPSDestDistance',
                        'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']

            for k, v in exif.items():
                try:
                    geo_tagging_info[gps_keys[k]] = str(v)
                except IndexError:
                    pass
            return geo_tagging_info

    def set_creation_time(self) -> bool:
        try:
            im = Image.open(self.file_abs_path)
        except UnidentifiedImageError:
            return False
        exif = im.getexif()

        for tag in self.CREATION_TAG:
            if tag in exif:
                creation_time = exif.get(tag)

                try:
                    self.creation_datetime = datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
                    self.valid_creation_datetime = True
                except:
                    pass

        if not self.valid_creation_datetime:
            msg_debug(DEBUG_LEVEL.debug_verbose, "Doesn't have valid time tag for this photo " + self.file_abs_path)
            stat = os.stat(self.file_abs_path)
            self.creation_datetime = datetime.fromtimestamp(stat.st_mtime)

        return True