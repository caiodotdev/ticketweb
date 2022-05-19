#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import logging
import time

from bs4 import BeautifulSoup

from app.models import Ticket, Airline
from engine.core import EngineModel

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

IDA_E_VOLTA = 'roundtrip'
IDA_SOLO = 'oneway'

URL_IDA = 'https://www.decolar.com/shop/flights/results/oneway/{origin}/{destination}/{start_date}'
URL_IDA_VOLTA = 'https://www.decolar.com/shop/flights/results/roundtrip/{origin}/{destination}/{start_date}/{end_date}'


class DecolarModel(EngineModel):
    def __init__(self, origem, destino, start_date, end_date, time_sleep):
        super(DecolarModel, self).__init__()
        self.origem = origem
        self.destino = destino
        self.passageiros = '/2/0/0/'
        self.classe = 'EC'
        self.time_sleep = time_sleep
        self.FILENAME = 'voos.csv'
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.diarias = (self.end_date - self.start_date).days
        self.url = 'https://www.decolar.com/shop/flights/results/oneway/{origin}/{destination}/{start_date}'

    def get_dates(self, start_date, end_date):
        date_list = []
        for n in range(self.diarias):
            date_list.append(start_date + datetime.timedelta(n))
        return date_list

    def get_info(self, args, **kwargs):
        print('Start SEARCH_VOO')
        if 'thread' in kwargs:
            thread = kwargs['thread']
        else:
            thread = None
        date_filter = kwargs['date_filter']
        url = self.url.format(origin=self.origem, destination=self.destino,
                              start_date=date_filter) + self.passageiros
        print('Search in: {}'.format(url))
        self.browser.get(url)
        time.sleep(self.time_sleep)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        voos = soup.findAll("span", {"class": "fare-wrapper -eva-3-p-md"})
        # self.remove_duplicates(date_filter, voos)
        itineraries = soup.findAll('ul', {'class': 'itineraries-group'})
        for voo_index in range(len(voos)):
            durations, final_price, hour_arrive, hour_leave, price_per_adult, stops, taxes, total_price = self.extract_data(
                itineraries, voo_index, voos)
            ticket = self.save_new_ticket(durations, final_price, hour_arrive, hour_leave, price_per_adult, stops,
                                          taxes, total_price, url, voo_index, voos, date_filter, thread=thread)
            self.save_airline(itineraries, ticket, voo_index)
        print('Finish SEARCH_VOO')

    def save_airline(self, itineraries, ticket, voo_index):
        airlines = [
            logo.img for logo in itineraries[voo_index].findAll('airline-logo')]
        for line in airlines:
            air = Airline()
            air.name = line['alt']
            air.logo_url = line['src']
            air.ticket = ticket
            air.save()

    def save_new_ticket(self, durations, final_price, hour_arrive, hour_leave, price_per_adult, stops, taxes,
                        total_price, url, voo_index, voos, date_filter, thread=None):
        ticket = Ticket()
        if thread:
            ticket.thread = thread
        ticket.price_per_adult = price_per_adult
        ticket.total_price_per_adult = total_price
        ticket.taxes = taxes
        ticket.final_total_price = final_price
        ticket.hour_leave = hour_leave
        ticket.hour_arrive = hour_arrive
        ticket.stops = stops
        ticket.durations = durations
        ticket.url = url
        ticket.data_trip = (datetime.datetime.strptime(
            date_filter, '%Y-%m-%d')).date()
        ticket.origin = self.origem
        ticket.destination = self.destino
        ticket.save()
        print('Save ticket {} of {}'.format(
            str(voo_index + 1), str(len(voos))))
        return ticket

    def extract_data(self, itineraries, voo_index, voos):
        price_per_adult = int(
            str(voos[voo_index].findAll('span', {'class': 'price-amount'})[0].text).replace('.', ''))
        total_price = int(
            str(voos[voo_index].findAll('span', {'class': 'price-amount'})[1].text).replace('.', ''))
        taxes = int(str(voos[voo_index].findAll(
            'span', {'class': 'price-amount'})[2].text).replace('.', ''))
        final_price = int(
            str(voos[voo_index].findAll('span', {'class': 'price-amount'})[-1].text).replace('.', ''))
        hour_leave = [hours.text for hours in
                      itineraries[voo_index].findAll('itinerary-element', {'class': 'leave'})]
        hour_arrive = [hours.text for hours in
                       itineraries[voo_index].findAll('itinerary-element', {'class': 'arrive'})]
        stops = [stops.text for stops in itineraries[voo_index].findAll(
            'span', {'class': 'stops-text'})]
        durations = [duration.text for duration in
                     itineraries[voo_index].findAll('span', {'class': 'duration-item-container'})]
        return durations, final_price, hour_arrive, hour_leave, price_per_adult, stops, taxes, total_price

    def remove_duplicates(self, date_filter, voos):
        if len(voos) > 0:
            tickets = Ticket.objects.filter(data_trip=(
                datetime.datetime.strptime(date_filter, '%Y-%m-%d')).date())
            if tickets:
                tickets.delete()

    # def scrapper_info_hotels(self, browser, url_hotel, data_inicio, data_fim, diarias):
    #     print(url_hotel)
    #     browser.get(url_hotel)
    #     time.sleep(8)
    #     html = browser.page_source
    #     soup = BeautifulSoup(html, 'html.parser')
    #     hoteis = soup.find_all("div", {"class": "sr_item"})
    #
    #     for i in range(len(hoteis)):
    #         valor_hotel = int(
    #             str(hoteis[i].find('div', {'class': 'bui-price-display__value'}).text).replace('\n', '').replace(
    #                 'R$\xa0',
    #                 '').replace(
    #                 '.', ''))
    #         nome = str(hoteis[i].find('span', {'class': 'sr-hotel__name'}).text).replace('\n', '').rstrip().lstrip()
    #         avaliacao = str(hoteis[i].find('div', {'class': 'bui-review-score__badge'}).text)
    #         preenche_tabela_hoteis(valor_hotel, nome, avaliacao, data_inicio, data_fim, diarias)

    # def runner():
    #     while True:
    #         for i in range(num_dias):
    #             apartir = date_initial + datetime.timedelta(days=i + 1)
    #             data = str(apartir).split(' ')[0]

#             for diarias in diarias_range:
#                 ate = str(apartir + datetime.timedelta(days=diarias)).split(' ')[0]
#                 url_voo = 'https://www.decolar.com/shop/flights/results/roundtrip/' + origem + '/' + destino + '/' \
#                           + data + '/' + ate + passageiros
#                 scrapper_info_voos(browser, url_voo, data, ate, diarias, origem)
#                 # url_voo = 'https://www.decolar.com/shop/flights/results/roundtrip/' + origem_2 + '/' + destino + '/' \
#                 #           + data + '/' + ate + passageiros
#                 # scrapper_info_voos(browser, url_voo, data, ate, diarias, origem_2)
#                 # checkin = apartir
#                 # checkout = apartir + datetime.timedelta(days=diarias)
#                 # url_hoteis = 'https://www.booking.com/searchresults.pt-br.html?aid=304142&ac_position=0&checkin_month=' + str(
#                 #     checkin.month) + '&checkin_monthday=' + str(checkin.day) + '&checkin_year=' + str(
#                 #     checkin.year) + '&checkout_month=' + str(checkout.month) + '&checkout_monthday=' + str(
#                 #     checkout.day) + '&checkout_year=' + str(
#                 #     checkout.year) + '&class_interval=1&dest_id=-671824&dest_type=city&from_sf=1&group_adults=2&group_children=0&iata=SAO&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=71b27dc149ed0024&ss=S%C3%A3o%20Paulo%2C%20Estado%20de%20S%C3%A3o%20Paulo%2C%20Brasil&ss_raw=sao%20paulo&ssb=empty&top_ufis=1&nflt=mealplan%3D1%3Bprice%3DBRL-min-250-1%3B&mealplan=1&rsf=&order=popularity&offset='
#                 # scrapper_info_hotels(browser, url_hoteis, data, ate, diarias)
#             browser.close()
#             browser.quit()
#
#         # if check_status_tabela(tabela_voos):
#         # reset_status_tabela(tabela_voos)
#         # reset_status_tabela(tabela_hoteis)
#         new_tabela_voos = sorted(tabela_voos, key=itemgetter(*['valor_voo', 'diarias']))
#         df = pd.DataFrame(new_tabela_voos)
#         df.to_csv(FILENAME, index=False)
#         sys.exit(0)
#         # if len(new_tabela_voos) >20:
#         #     new_tabela_voos = new_tabela_voos[:20]
#         # mensagem_completa = ''
#         # for i in range(len(new_tabela_voos)):
#         #     mensagem = '' + str(i + 1) + 'º Voo: \nPreço: ' + str(new_tabela_voos[i]['valor_voo']) + '\nData Ida: ' + \
#         #                new_tabela_voos[i]['data_inicio'] + '\nData Volta: ' + new_tabela_voos[i]['data_fim'] + \
#         #                '\nDuração Voo: ' + new_tabela_voos[i]['duracao'] + \
#         #                '\nDiarias: ' + str(new_tabela_voos[i]['diarias']) + '\nSaindo de: ' + new_tabela_voos[i]['origem'] + '\n \n'
#         #     mensagem_completa += mensagem
#
#         # for i in range(len(tabela_hoteis)):
#         #     mensagem = '' + str(i + 1) + 'º Hotel: \nPreço: ' + str(tabela_hoteis[i]['valor_hotel']) + '\nCheckin: ' + \
#         #                tabela_hoteis[i]['data_inicio'] + '\nCheckout: ' + tabela_hoteis[i]['data_fim'] + \
#         #                '\nAvaliacao: ' + tabela_hoteis[i]['avaliacao'] + \
#         #                '\nDiarias: ' + str(tabela_hoteis[i]['diarias']) + '\nHotel: ' + tabela_hoteis[i]['nome_hotel'] \
#         #                + '\n \n'
#         #     mensagem_completa += mensagem
#         # send_announcments(bot_message=mensagem_completa)
#         print('vou dormir...')
#         time.sleep(600)

#
# Thread(target=runner).start()
