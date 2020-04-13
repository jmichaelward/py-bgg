#!/usr/bin/env python3
import requests
import xmltodict


class BggApi:
    bgg_base_url = 'https://boardgamegeek.com/xmlapi2/'

    def get_json(self, url):
        """
        Get a JSON response from the BoardGameGeek api.

        :param url:
        :return:
        """
        response = requests.request('GET', self.bgg_base_url + url)
        return response, xmltodict.parse(response.content)


def get_bgg_json(url):
    """
    Get a JSON response from the BoardGameGeek api.

    :param url:
    :return:
    """
    response = requests.request('GET', url)
    return response, xmltodict.parse(response.content)
