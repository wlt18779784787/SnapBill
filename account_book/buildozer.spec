[app]

title = \u667a\u80fd\u8bb0\u8d26\u672c
package.name = account_book
package.domain = org.snapbill

source.dir = .
source.include_exts = py,kv,db,png,jpg,jpeg,gif,webp,ttf,ttc,otf
source.include_patterns = assets/fonts/*
source.exclude_dirs = .git,.idea,.omc,__pycache__,tests,dist

version = 1.0.0
requirements = python3,kivy,pillow,requests

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 21
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
