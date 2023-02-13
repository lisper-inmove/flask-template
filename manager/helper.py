# -*- coding: utf-8 -*-

from manager.base_manager import ignore_none_argument


class ManagerHelper:

    @staticmethod
    @ignore_none_argument
    def update_city(obj, city):
        obj.city = city

    @staticmethod
    @ignore_none_argument
    def update_prov(obj, prov):
        obj.prov = prov

    @staticmethod
    @ignore_none_argument
    def update_region(obj, region):
        obj.region = region

    @staticmethod
    @ignore_none_argument
    def update_address(obj, address):
        obj.address = address

    @staticmethod
    @ignore_none_argument
    def update_lnt(obj, lnt):
        obj.lnt = float(lnt)

    @staticmethod
    @ignore_none_argument
    def update_lat(obj, lat):
        obj.lat = float(lat)
