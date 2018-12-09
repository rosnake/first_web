#!/usr/bin/env Python
# coding=utf-8

from ui_handlers.generator import NavigationModule
from ui_handlers.generator import AdminSidebarModule
from ui_handlers.generator import HeaderModule
from ui_handlers.generator import SubtitleModule

# UI模板入口
ui = [
    {"Navigation": NavigationModule, },
    {"AdminSidebar": AdminSidebarModule, },
    {"Header": HeaderModule, },
    {"Subtitle": SubtitleModule, }
    ]
