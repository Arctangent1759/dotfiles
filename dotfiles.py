from json import loads
from os import path
import os
import shutil

class Symlink:
    def __init__(self,dotfile_dir, conf_dir, a):
        self.to_loc = a[0]
        self.from_loc = path.join(dotfile_dir, conf_dir, a[1])

class AppConfig:
    def __init__(self, dotfile_dir, conf_dir, a):
        self.conf_dir = conf_dir
        self.symlinks = []
        for symlink in a['symlinks']:
            self.symlinks.append(Symlink(dotfile_dir, conf_dir, symlink))

class DotfileConfig:
    def __init__(self,s):
        conf_json = loads(s)
        self.dotfile_dir = conf_json['dotfile_dir']
        self.conf = []
        for conf_dir in conf_json['conf']:
            self.conf.append(AppConfig(self.dotfile_dir, conf_dir, conf_json['conf'][conf_dir]))

class Dotfiles:
    def __init__(self):
        self.conf = DotfileConfig(open("./manifest.json").read())
    def install(self):
        if path.exists(path.expanduser(self.conf.dotfile_dir)):
            return False
        for conf in self.conf.conf:
            for symlink in conf.symlinks:
                os.symlink(
                    path.expanduser(symlink.from_loc),
                    path.expanduser(symlink.to_loc))
        shutil.copytree("dotfiles", path.expanduser(self.conf.dotfile_dir))
        return True
