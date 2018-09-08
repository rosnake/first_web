#!/usr/bin/env Python
# coding=utf-8

# Session类型：cache/redis/memcached


class SessionConfig:
    SESSION_TYPE = "cache"
    # Session超时时间（秒）
    SESSION_EXPIRES = 60 * 20
