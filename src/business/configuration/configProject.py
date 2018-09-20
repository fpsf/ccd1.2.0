from PyQt5 import QtCore

from src.business.configuration.constants import project as p
from src.ui.commons.verification import cb


class ConfigProject:
    def __init__(self):
        self._settings = QtCore.QSettings(p.CONFIG_FILE, QtCore.QSettings.IniFormat)

    def get_value(self, menu, value):
        return self._settings.value(menu + '/' + value)

    def set_site_settings(self, name, site_id, imager_id):
        self._settings.beginGroup(p.SITE_TITLE)
        self._settings.setValue(p.NAME, name)
        self._settings.setValue(p.SITE_ID, site_id)
        self._settings.setValue(p.IMAGER_ID, imager_id)
        self._settings.endGroup()

    def set_geographic_settings(self, lat, long, elev, press, temp):
        self._settings.beginGroup(p.GEOGRAPHIC_TITLE)
        self._settings.setValue(p.LATITUDE, lat)
        self._settings.setValue(p.LONGITUDE, long)
        self._settings.setValue(p.ELEVATION, elev)
        self._settings.setValue(p.PRESSURE, press)
        self._settings.setValue(p.TEMPERATURE, temp)
        self._settings.endGroup()

    def set_moonsun_settings(self, solarelev, ignoreLunar, lunarph, lunarpos):
        self._settings.beginGroup(p.SUN_MOON_TITLE)
        self._settings.setValue(p.MAX_SOLAR_ELEVATION, solarelev)
        self._settings.setValue(p.IGNORE_LUNAR_POSITION, ignoreLunar)
        self._settings.setValue(p.MAX_LUNAR_PHASE, lunarph)
        self._settings.setValue(p.MAX_LUNAR_ELEVATION, lunarpos)
        self._settings.endGroup()

    def save_settings(self):
        self._settings.sync()

    def get_site_settings(self):
        return self.get_value(p.SITE_TITLE, p.NAME), \
               self.get_value(p.SITE_TITLE, p.SITE_ID), \
               self.get_value(p.SITE_TITLE, p.IMAGER_ID)

    def get_geographic_settings(self):
        m = p.GEOGRAPHIC_TITLE
        return self.get_value(m, p.LATITUDE), \
               self.get_value(m, p.LONGITUDE), \
               self.get_value(m, p.ELEVATION), \
               self.get_value(m, p.PRESSURE), \
               self.get_value(m, p.TEMPERATURE)

# cb(self.get_value(m, p.IGNORE_LUNAR_POSITION))
# self._settings.value(p.IGNORE_LUNAR_POSITION, type=bool)
    def get_moonsun_settings(self):
        m = p.SUN_MOON_TITLE
        return self.get_value(m, p.MAX_SOLAR_ELEVATION), \
               cb(self.get_value(m, p.IGNORE_LUNAR_POSITION)), \
               self.get_value(m, p.MAX_LUNAR_PHASE), \
               self.get_value(m, p.MAX_LUNAR_ELEVATION)