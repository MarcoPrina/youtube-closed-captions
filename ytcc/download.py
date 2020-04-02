# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import glob, os

import youtube_dl
from pycaption import WebVTTReader
from os import remove
import re
from urllib.parse import urlencode

from ytcc import credential
from ytcc.storage import Storage
from ytcc.fake_logger import FakeLogger


class Download():
    base_url = 'http://www.youtube.com/watch'

    def __init__(self, opts: dict = {}, playlist: bool = False) -> None:
        self.opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'outtmpl': 'subtitle_%(id)s',
            'logger': FakeLogger(),
            'username': credential.username,
            'password': credential.password,
            'cookiefile': "cookies.txt"
        }
        self.opts.update(opts)
        self.playlist = playlist
        if playlist:
            self.base_url = 'http://www.youtube.com/playlist'


    def update_opts(self, opts: dict) -> None:
        self.opts.update(opts)

    def get_captions(self, video_id: str, language: str = 'it') -> dict:
        result = self.get_result(video_id, language)

        if result != 0:
            raise Exception(
                'Unable to download and extract captions: {0}'.format(result))



        output = {}

        for file_path in glob.glob("*.vtt"):
            storage = Storage(file_path)
            id = storage.get_video_id()
            with open(file_path) as f:
                output[id] = (self.get_captions_from_output(f.read()))
            storage.remove_file()
        return output

    def get_result(self, video_id: str, language: str = 'it') -> int:
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
        if self.playlist:
            parameter = "list"
        else:
            parameter = 'v'
        return '{0}?{1}'.format(self.base_url, urlencode({parameter : video_id}))

    def get_captions_from_output(self, output: str) -> str:

        temp_final = output.replace('\n', "\r\n").replace('"', "'")

        final = self.remove_duplicate_lines(temp_final)

        return final

    def remove_duplicate_lines(self, temp_final: str) -> str:
        final = ''
        for line in temp_final.split("\r\n"):
            if line.__contains__('<c>'):
                final += line.replace('<c>', '').replace('</c>', '') + "\r\n"

        return final


class DownloadException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
