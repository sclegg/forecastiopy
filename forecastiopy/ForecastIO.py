# -*- coding: utf-8 -*-
"""
This module recieves the api key and the configurations to build the request
url.
It then gets the weather data based on those configurations.
The resulting object is used by the other classes to get the information.
"""

import sys
import json
import requests


class ForecastIO(object):
    """
    This class recieves the api key and the configurations to build the request
    url.
    It then gets the weather data based on those configurations.
    The resulting object is used by the other classes to get the information.
    """

    forecast_io_url = 'https://api.forecast.io/forecast/'

    forecast_io_api_key = None
    units_url = None
    time_url = None
    exclude_url = None
    lang_url = None
    extend = None
    cache_control = None
    expires = None
    x_forecast_api_calls = None
    x_responde_time = None
    raw_response = None

    UNITS_US = 'us'
    UNITS_SI = 'si'
    UNITS_CA = 'ca'
    UNITS_UK = 'uk'
    UNITS_AUTO = 'auto'
    LANG_BOSNIAN = 'bs'
    LANG_GERMAN = 'de'
    LANG_ENGLISH = 'en'
    LANG_SPANISH = 'es'
    LANG_FRENCH = 'fr'
    LANG_ITALIAN = 'it'
    LANG_DUTCH = 'nl'
    LANG_POLISH = 'pl'
    LANG_PORTUGUESE = 'pt'
    LANG_TETUM = 'tet'
    LANG_PIG_LATIN = 'x-pig-latin'
    LANG_RUSSIAN = 'ru'

    def __init__(self, api_key, extend=False, units_url=UNITS_AUTO, \
    lang_url=LANG_ENGLISH, latitude=None, longitude=None):
        """
        A valid api key must be provided in the object instantiation.
        Other options are available.
        Units, language, extended reply can be set.
        It is useful to provide coordinates (latitude and longitude) to get a
        reply.
        """

        if api_key.__len__() == 32:
            self.forecast_io_api_key = api_key
            self.extend = extend
            self.units_url = units_url
            self.lang_url = lang_url
            self.latitude = latitude
            self.longitude = longitude
            if latitude is not None and longitude is not None:
                self.get_forecast(latitude, longitude)
        else:
            print 'The API Key doesn\'t seam to be valid.'

    def get_forecast(self, latitude, longitude):
        """
        Gets the weather data and stores it in the respective dictionaries if
        available.
        This function should be used to fetch weather information.
        """
        reply = self.http_get(self.url_builder(latitude, longitude))
        self.forecast = json.loads(reply)
        if 'currently' in self.forecast:
            self.currently = self.forecast['currently']
        if 'minutely' in self.forecast:
            self.minutely = self.forecast['minutely']
        if 'hourly' in self.forecast:
            self.hourly = self.forecast['hourly']
        if 'daily' in self.forecast:
            self.daily = self.forecast['daily']
        if 'flags' in self.forecast:
            self.flags = self.forecast['flags']
        if 'alerts' in self.forecast:
            self.alerts = self.forecast['alerts']

    def url_builder(self, latitude, longitude):
        """
        This function is used to build the correct url to make the requestto the
        forecast.io api.
        Recieves the latitude and the longitude.
        Return a string with the url.
        """
        try:
            float(latitude)
            float(longitude)
        except ValueError:
            raise ValueError('Latitude and Longitude must be a (float) number')
        url = self.forecast_io_url + self.forecast_io_api_key + '/'
        url += str(latitude).strip() + ',' + str(longitude).strip()
        if self.time_url and not self.time_url.isspace():
            url += ',' + self.time_url.strip()
        url += '?units=' + self.units_url.strip()
        url += '&lang=' + self.lang_url.strip()
        if self.exclude_url and not self.exclude_url.isspace():
            url += '&exclude=' + self.exclude_url.strip()
        if self.extend is True:
            url += 'extend=hourly'
        return url

    def http_get(self, request_url):
        """
        This function recieves the request url and it is used internaly to get
        the information via http.
        Returns the response content.
        Raises Timeout, TooManyRedirects, RequestException.
        Raises KeyError if headers are not present.
        Raises HTTPError if responde code is not 200.
        """
        try:
            headers = {'Accept-Encoding': 'gzip, deflate'}
            response = requests.get(request_url, headers=headers)
        except requests.exceptions.Timeout:
            print 'Error: Timeout'
        except requests.exceptions.TooManyRedirects:
            print 'Error: TooManyRedirects'
        except requests.exceptions.RequestException as ex:
            print ex
            sys.exit(1)

        try:
            self.cache_control = response.headers['Cache-Control']
            self.expires = response.headers['Expires']
            self.x_forecast_api_calls = response.headers['X-Forecast-API-Calls']
            self.x_responde_time = response.headers['X-Response-Time']
        except KeyError as kerr:
            print 'Warning: Could not get headers. %s' % kerr

        if response.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response')

        self.raw_response = response.content
        return response.content

    def has_currently(self):
        """
        Return True if currently information is available. False otherwise.
        """
        return 'currently' in self.forecast

    def get_currently(self):
        """
        Returns currently information or None if it is not available.
        """
        if self.has_currently() == True:
            return self.currently
        else:
            return None

    def has_daily(self):
        """
        Return True if daily information is available. False otherwise.
        """
        return 'daily' in self.forecast

    def get_daily(self):
        """
        Returns daily information or None if it is not available.
        """
        if self.has_daily() == True:
            return self.daily
        else:
            return None

    def has_hourly(self):
        """
        Return True if hourly information is available. False otherwise.
        """
        return 'hourly' in self.forecast

    def get_hourly(self):
        """
        Returns hourly information or None if it is not available.
        """
        if self.has_hourly() == True:
            return self.hourly
        else:
            return None

    def has_minutely(self):
        """
        Return True if minutly information is available. False otherwise.
        """
        return 'minutely' in self.forecast

    def get_minutely(self):
        """
        Returns minutely information or None if it is not available.
        """
        if self.has_minutely() == True:
            return self.minutely
        else:
            return None

    def has_flags(self):
        """
        Return True if flags information is available. False otherwise.
        """
        return 'flags' in self.forecast

    def get_flags(self):
        """
        Returns flags information or None if it is not available.
        """
        if self.has_flags() == True:
            return self.flags
        else:
            return None

    def has_alerts(self):
        """
        Return True if alerts information is available. False otherwise.
        """
        return 'alerts' in self.forecast

    def get_alerts(self):
        """
        Returns alerts information or None if it is not available.
        """
        if self.has_alerts() == True:
            return self.alerts
        else:
            return None
