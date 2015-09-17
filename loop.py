#!/usr/bin/env python2.7

import os
import time
import subprocess as local

omxplayer = 'omxplayer'


def is_running(omx):
    out = local.call('ps ax |grep -v grep |grep "%s" >/dev/null' % omx, shell=True)
    return out != 0  # len(out) > 0


def omx_cmd():
    out = local.check_output('which %s' % omxplayer, shell=True)
    return out


def list_media_files(media_dir):
    for root, dirs, files in os.walk(media_dir):
        files = [f for f in files if not f[0] == '.']  # not hidden
        dirs[:] = [d for d in dirs if d == root]
    return files;


def loop(video_dir):
    while is_running(omx_cmd()):
        time.sleep(1)
    local.call('clear', shell=True)
    files = list_media_files(video_dir)
    for file in files:
        out = local.call('%s %s >/dev/null' % (omxplayer, file), shell=True)

if __name__ == '__main__':
    while True:
        loop('./')
