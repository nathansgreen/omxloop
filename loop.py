#!/usr/bin/env python2.7

import os
import time
import subprocess as local

omxplayer = 'omxplayer'
stretch = '-r'  # `-r` empty string to disable
hdmi_audio = '-o'  # `-o` empty string to disable


def is_running(omx):
    out = local.call('ps ax |grep -v grep |grep "%s" >/dev/null' % omx,
                     shell=True)
    return out != 0  # len(out) > 0


def omx_cmd():
    out = local.check_output('which %s' % omxplayer, shell=True)
    return out


def list_media_files(media_dir):
    for root, dirs, files in os.walk(media_dir):
        files[:] = [f for f in files if not f[0] == '.']  # not hidden
        dirs[:] = [d for d in dirs if d == root]
    return files;


def get_last_file():
    config = ''
    try:
        with open ('.omxloop', 'r') as file:
            config = file.read().replace('\n', '')
    except (IOError):
        pass
    return config if len(config) > 0 else None


def write_last_file(media_dir, file_name):
    try:
        with open ('.omxloop', 'w') as file:
            file.write(file_name)
    except (IOError):
        pass


def loop(video_dir, restart):
    while is_running(omx_cmd()):
        time.sleep(1)
    files = list_media_files(video_dir)
    for file in files:
        if restart and not file == restart:
            continue
        restart = None
        write_last_file(video_dir, file)
        local.call('clear', shell=True)
        out = local.call('%s %s %s "%s" >/dev/null' % (omxplayer, stretch, hdmi_audio, file),
                         shell=True)
    write_last_file(video_dir, '')
    if restart:
        loop(video_dir, None)

if __name__ == '__main__':
    while True:
        loop('./', get_last_file())
