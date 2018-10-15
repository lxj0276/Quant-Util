# -*- coding: utf-8 -*-
import os
from .env import MEM_CACHE_SIZE, CACHE_PATH
from .utils import hash_args, pickle_load, pickle_dump
from collections import OrderedDict


class MemCache(OrderedDict):
    """Memory Cache."""

    def __init__(self, *args, **kwargs):
        self.size_limit = kwargs.pop("size_limit", None)
        super(MemCache, self).__init__(*args, **kwargs)
        self._check_size_limit()

    def __setitem__(self, key, value):
        super(MemCache, self).__setitem__(key, value)
        self._check_size_limit()

    def __getitem__(self, key):
        value = super(MemCache, self).__getitem__(key)
        super(MemCache, self).__delitem__(key)
        super(MemCache, self).__setitem__(key, value)
        return value

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)

mem_cache = MemCache(size_limit=MEM_CACHE_SIZE)
