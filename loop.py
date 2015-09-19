#!/usr/bin/env python2.7

import os
import time
import subprocess as local

video_dir = './'  # location of video files
omxplayer = 'omxplayer'  # command name
stretch = '-r'  # `-r` empty string to disable
hdmi_audio = '-o hdmi'  # `-o hdmi` empty string to disable


def is_running(omx):
    out = local.call('ps ax |grep -v grep |grep "%s" >/dev/null' % omx,
                     shell=True)
    return out != 0  # len(out) > 0


def omx_cmd():
    out = local.check_output('which %s' % omxplayer, shell=True)
    return out


def config_file_path():
    return os.path.expanduser('~/.omxloop')


def list_media_files(media_dir):
    for root, dirs, files in os.walk(media_dir):
        files[:] = [f for f in files if not f[0] == '.']  # not hidden
        dirs[:] = [d for d in dirs if d == root]
    return files;


def get_last_file():
    config = ''
    try:
        with open (config_file_path(), 'r') as file:
            config = file.read().replace('\n', '')
    except (IOError):
        pass
    return config if len(config) > 0 else None


def write_last_file(media_dir, file_name):
    try:
        with open (config_file_path(), 'w') as file:
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
        cmd = '%s %s %s "%s"' % (omxplayer, stretch, hdmi_audio, file)
        # play video and wait for it to finish
        out = local.call(cmd, shell=False, stdout=None, stderr=None)
    write_last_file(video_dir, '')  # clear restart file
    if restart:
        loop(video_dir, None)


if __name__ == '__main__':
    while True:
        loop(video_dir, get_last_file())
