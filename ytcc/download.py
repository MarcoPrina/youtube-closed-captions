# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import youtube_dl
from pycaption import WebVTTReader
from os import remove
import re
from urllib.parse import urlencode
from ytcc.storage import Storage
from ytcc.fake_logger import FakeLogger


class Download():
    base_url = 'http://www.youtube.com/watch'

    def __init__(self, opts: dict = {}) -> None:
        self.opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'outtmpl': 'subtitle_%(id)s',
            'logger': FakeLogger()
        }
        self.opts.update(opts)

    def update_opts(self, opts: dict) -> None:
        self.opts.update(opts)

    def get_captions(self, video_id: str, language: str = 'en') -> str:
        result = self.get_result(video_id, language)

        if result != 0:
            raise Exception(
                'Unable to download and extract captions: {0}'.format(result))

        storage = Storage(video_id, language)
        file_path = storage.get_file_path()
        with open(file_path) as f:
            output = self.get_captions_from_output(f.read(), language)
        storage.remove_file()
        return output

    def get_result(self, video_id: str, language: str = 'en') -> int:
        opts = self.opts
        if language:
            opts['subtitleslangs'] = [*opts.get('subtitleslangs', []), language]

        with youtube_dl.YoutubeDL(opts) as ydl:
            try:
                return ydl.download([self.get_url_from_video_id(video_id)])
            except youtube_dl.utils.DownloadError as err:
                raise DownloadException(
                    "Unable to download captions: {0}".format(str(err)))
            except youtube_dl.utils.ExtractorError as err:
                raise DownloadException(
                    "Unable to extract captions: {0}".format(str(err)))
            except Exception as err:
                raise DownloadException(
                    "Unknown exception downloading and extracting captions: {0}".format(
                        str(err)))

    def get_url_from_video_id(self, video_id: str) -> str:
        return '{0}?{1}'.format(self.base_url, urlencode({'v': video_id}))

    def get_captions_from_output(self, output: str, language: str = 'en') -> str:
        reader = WebVTTReader()

        temp_final = ''
        for caption in reader.read(output, language).get_captions(language):
            stripped = str(caption).replace(r'\n', "\r\n").replace(r'"', "'")
            temp_final += stripped

        final = self.remove_duplicate_lines(temp_final)

        return final

    def remove_duplicate_lines(self, temp_final: str) -> str:
        final = ''
        previous = ["", ""]
        for line in temp_final.split("\r\n"):
            part = line.split("''")

            if previous[0] == part[0] and len(part) == 2:
                start = previous[1].split(" --> ")[0]
                end = part[1].split(" --> ")[1]
                part[1] = start + " --> " + end
                previous = part

            if previous[0] != part[0]:
                final += "\r\n" + "''".join(previous)
                previous = part

        final += "\r\n" + "''".join(previous)
        return final


class DownloadException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
