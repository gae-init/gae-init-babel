# -*- coding: utf-8 -*-

import hashlib


class BaseX(object):
  @classmethod
  def retrieve_one_by(cls, name, value):
    cls_db_list = cls.query(getattr(cls, name) == value).fetch(1)
    if cls_db_list:
      return cls_db_list[0]
    return None


class ConfigX(object):
  @classmethod
  def get_master_db(cls):
    return cls.get_or_insert('master')


class UserX(object):
  @property
  def avatar_url(self):
    # r=g means suitable for display on all websites with any audience type
    return '//gravatar.com/avatar/%s?d=identicon&r=g' % (
        hashlib.md5((self.email or self.name).encode('utf-8')).hexdigest().lower()
      )
