import os
from os.path import isdir, join
from collections import deque

from PIL import Image
from pillow_heif import register_heif_opener

from Video import Video
from Photo import Photo

from util import *


class PhotoFolder:
    def __init__(self, path):
        self.ACCEPTABLE_PHOTO_TYPE = [
            '.jpg',
            '.jpeg',
            '.png',
            '.heic'
        ]

        self.ACCEPTABLE_RAW_TYPE = [
            '.cr2',
            '.dng',
        ]

        self.ACCEPTABLE_VIDEO_TYPE = [
            '.mov',
            '.mp4',
        ]

        self.ACCEPTABLE_EDIT_TYPE = [
            '.aae'
        ]

        self.imageMap = None  # from file_abs_path -> Media Obj
        self.topPath = path

        register_heif_opener()

    # def is_acceptable_file_type(self, file_abs_path: str) -> bool:
    #     """
    #     Return if the file is an acceptable type or not
    #     :param file_abs_path: the absolute path to the file
    #     :return:
    #     """
    #     filename = os.path.basename(file_abs_path)
    #
    #     # We only process files that are not hidden file
    #     if len(filename) > 0 and filename[0] == ".":
    #         return False
    #
    #     _, file_extension = os.path.splitext(file_abs_path)
    #
    #     if self.is_photo_file_type(file_abs_path):
    #         return True
    #     elif self.is_video_file_type(file_abs_path):
    #         return True
    #     elif file_extension.lower() in self.ACCEPTABLE_EDIT_TYPE:
    #         return True
    #     else:
    #         if file_extension.lower() not in self.unrecognizedType:
    #             self.unrecognizedType.append(file_extension.lower())
    #         self.unrecognizedFile.append(file_abs_path)
    #         return False

    def is_hidden_file(self, file_abs_path: str) -> bool:
        filename = os.path.basename(file_abs_path)
        if len(filename) > 0 and filename[0] == ".":
            return True
        return False

    def is_photo_file_type(self, file_abs_path: str) -> bool:
        _, file_extension = os.path.splitext(file_abs_path)
        if file_extension.lower() in self.ACCEPTABLE_PHOTO_TYPE:
            return True
        return False

    def is_video_file_type(self, file_abs_path: str) -> bool:
        _, file_extension = os.path.splitext(file_abs_path)
        if file_extension.lower() in self.ACCEPTABLE_VIDEO_TYPE:
            return True
        return False

    #
    # def get_media_creation_time(self, file_abs_path: str):
    #     if self.is_photo_file_type(file_abs_path):
    #
    #     elif self.is_video_file_type(file_abs_path):

    def set_path(self, path: str) -> None:
        self.topPath = path

    def construct_image_map(self) -> None:
        self.imageMap = {}
        count = 0

        file_queue = deque()
        file_queue.append(self.topPath)
        while file_queue:
            explore_path = file_queue.pop()
            if os.path.isdir(explore_path):
                for subFile in os.listdir(explore_path):
                    file_queue.append(os.path.join(explore_path, subFile))
            elif os.path.isfile(explore_path):
                if self.is_hidden_file(explore_path):
                    continue

                if self.is_photo_file_type(explore_path):
                    media_instance = Photo(explore_path)
                elif self.is_video_file_type(explore_path):
                    media_instance = Video(explore_path)
                else:
                    continue

                count += 1
                msg_debug(DEBUG_LEVEL.debug_super_verbose, "processing: ", count, "of", len(file_queue),
                          "file path", explore_path)

                media_key = media_instance.file_abs_path

                self.imageMap[media_key] = media_instance
            else:
                continue

        msg_debug(DEBUG_LEVEL.debug, "imagemap size", len(self.imageMap))

        if count == 0:
            msg_debug(DEBUG_LEVEL.warning, "Folder contain no media file")
            self.imageMap = None

    def detect_duplicate_photo(self):
        if self.imageMap is None:
            msg_debug(DEBUG_LEVEL.warning, "Need to construct image map first")
            return

        duplicate_map = {}
        duplicate = 0
        count = 0

        map_size = len(self.imageMap)
        for file_abs_path, mediaObj in self.imageMap.items():
            msg_debug(DEBUG_LEVEL.debug_super_verbose, "checking: ", count, "of", map_size,
                      "file path", file_abs_path)

            media_key = mediaObj.get_hashable_str()

            if media_key in duplicate_map:
                msg_debug(DEBUG_LEVEL.info, "Duplicate", file_abs_path, duplicate_map[media_key].file_abs_path)

                duplicate += 1
            else:
                duplicate_map[media_key] = mediaObj

            # im = Image.open(explore_path)
            # exif = im.getexif()
            #
            # # creation_time = exif.get(36867)
            #
            # print(exif)
            #
            # file_name = os.path.basename(explore_path)
            # if file_name in imageMap:
            #     print("Duplicate", explore_path, imageMap[file_name])
            #     duplicate+=1
            # else:
            #     imageMap[file_name] = explore_path

        msg_debug(DEBUG_LEVEL.debug, "Duplication count", duplicate)

    def override_file_time(self):
        if self.imageMap is None:
            msg_debug(DEBUG_LEVEL.warning, "Need to construct image map first")
            return

        map_size = len(self.imageMap)
        count = 1
        for file_abs_path, mediaObj in self.imageMap.items():
            msg_debug(DEBUG_LEVEL.debug_super_verbose, "Overriding: ", count, "of", map_size,
                      "file path", file_abs_path)

            mediaObj.override_creation_time()
            count += 1
