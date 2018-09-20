#!/usr/bin/env Python
# coding=utf-8

class AdminLanguageMapping:

    def __init__(self):
        self.current = "chinese"

    def get_admin_mapping_table(self):
        admin_mapping = {
            "/admin/member": "成员管理",
        }


