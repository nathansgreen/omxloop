#!/usr/bin/env python2.7

import argparse
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
    return out == 0  # len(out) > 0


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


def omx_cmd():
    """return the full path to the omxplayer command"""
    out = local.check_output('which %s' % omxplayer, shell=True)
    return out.strip() if not is_number(out) else omxplayer


def config_file_path():
    """Full path to config file"""
    return os.path.expanduser('~/.omxloop')


def list_media_files(media_dir):
    """Given a 'media_dir', list immediate children"""
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


def clear_restart(video_dir):
    """Clear restart position from settings file"""
    write_last_file(video_dir, '')


def loop(video_dir, restart):
    while is_running(omx_cmd()):
        time.sleep(1)
    files = list_media_files(video_dir)
    for file in files:
        if restart and not file == restart:
            continue
        restart = None
        write_last_file(video_dir, file)
        cmd = 'clear; %s %s %s "%s/%s"' % (omx_cmd(), stretch, hdmi_audio, video_dir, file)
        # play video and wait for it to finish
        out = local.call(cmd, shell=True, stdout=None, stderr=None)
        if out != 0:
            raise Exception(cmd)  # try to explain what went wrong
    clear_restart(video_dir)
    if restart:
        loop(video_dir, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play a list of videos repeatedly.')
    parser.add_argument('--reset', action='store_true', help='reset configuration')
    args = parser.parse_args()
    if args.reset:
        clear_restart(video_dir)

    while True:
        video_dir = os.path.abspath(video_dir)
        loop(video_dir, get_last_file())
