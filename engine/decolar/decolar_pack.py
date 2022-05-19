#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import logging
import time

from bs4 import BeautifulSoup

from app.models import Pack
from engine.core import EngineModel

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class DecolarPackModel(EngineModel):
    def __init__(self, start_date, end_date, time_sleep=10, origem='CIT_3399', destino='CIT_982'):
        super(DecolarPackModel, self).__init__()
        self.origem = origem
        self.destino = destino
        self.time_sleep = time_sleep
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.diarias = (self.end_date - self.start_date).days
        self.url = 'https://www.decolar.com/trip/start/FH/{origin}/{destination}/{start_date}/{end_date}/{destination}/{start_date}/{end_date}/2'

    def get_info(self, args, **kwargs):
        print('Start GET_INFO')
        day_range = self.diarias
        if self.diarias > 15:
            day_range = 15
        if self.diarias <= 1:
            day_range = 2
        for i in range(0, day_range):
            for j in range(1, day_range + 1):
                start_date = self.start_date + datetime.timedelta(days=i)
                end_date = start_date + datetime.timedelta(days=j)
                diarias = (end_date - start_date).days
                if diarias > 0:
                    start_date = str(start_date).split(' ')[0]
                    end_date = str(end_date).split(' ')[0]
                    url = self.url.format(origin=self.origem, destination=self.destino,
                                          start_date=start_date,
                                          end_date=end_date)
                    print('Search in: {}'.format(url))
                    self.browser.get(url)
                    time.sleep(self.time_sleep)
                    html = self.browser.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    packs = soup.findAll("div", {"class": "cluster-container"})
                    if packs:
                        for pack_index in range(len(packs)):
                            try:
                                name, address, score, description_hotel, flight_info, price_adult, total_price = self.extract_data(
                                    pack_index, packs)
                                pack = self.save_new_pack(name, address, score, description_hotel, flight_info,
                                                          price_adult,
                                                          total_price, diarias, start_date, end_date)
                                print('Save Pack {} of {}'.format(str(pack_index + 1), str(len(packs))))
                            except (Exception,):
                                print('Nenhum Pack nesta pagina')
                    else:
                        print('Nenhum resultado encontrado')

    def save_new_pack(self, name, address, score, description_hotel, flight_info, price_adult, total_price, diarias,
                      start_date, end_date):
        pack = Pack()
        pack.diarias = diarias
        pack.name_hotel = name
        pack.address = address
        pack.score = score
        pack.flight_info = description_hotel + ' | \n\n ' + flight_info
        pack.price_adult = price_adult
        pack.price_total = total_price
        pack.leave_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        pack.arrive_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        pack.save()
        return pack

    def extract_data(self, pack_index, packs):
        name = packs[pack_index].findAll('span', {'class': 'accommodation-name'})[0].text
        address = packs[pack_index].findAll('aloha-location-name')[0].text
        score = packs[pack_index].findAll('aloha-rating')[0].text
        description_hotel = ";".join([info.text for info in packs[pack_index].findAll('aloha-tooltip')])
        flight_info = packs[pack_index].findAll('div', {'class': 'flight-data-container'})[0].text
        price_adult = str(packs[pack_index].findAll('div', {'class': 'price-info-container'})[0].text).replace('.',
                                                                                                               '').replace(
            'R$', '').replace(',', '.').strip()
        total_price = str(packs[pack_index].findAll('p', {'class': 'tertiary-price'})[0].text).replace('.', '').replace(
            'R$', '').replace(',', '.').replace(' Total 2 pessoas ', '').strip()
        return name, address, score, description_hotel, flight_info, price_adult, total_price
