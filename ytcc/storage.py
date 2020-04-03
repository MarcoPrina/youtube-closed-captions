# -*- coding: UTF-8 -*-

import os


class Storage():

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_video_id(self) -> str:
        return self.file_path[9:-7]

    def remove_file(self) -> None:
        os.remove(self.file_path)
