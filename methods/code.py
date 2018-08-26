#!/usr/bin/env Python
# coding=utf-8


class VerifyCode:
    verify_code = ""

    @staticmethod
    def get_verify_code():
        return VerifyCode.verify_code


    @staticmethod
    def set_verify_code(verify_code):
        VerifyCode.verify_code = verify_code
