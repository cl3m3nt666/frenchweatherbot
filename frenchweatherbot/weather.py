#!/usr/bin/python
# -*- coding: utf-8 -*-
#----------------------------------------------------
# Create by cl3m3nt
# weather.py
#----------------------------------------------------
""" get wunderground.com """

import os.path
import urllib2
import json
import sys

#Emojis
CRYINGFACE = u'\U0001F622'
ROUND_PUSHPIN = u'\U0001F4CD'
WIND = u'\U0001F32C'
DROPLET = u'\U0001F4A7'
CLOUD = u'\U00002601'
SUN = u'\U00002600'

#For switch
class switch( object ):
    value = None
    def __new__( class_, value ):
        class_.value = value
        return True

def case( *args ):
    return any( ( arg == switch.value for arg in args ) )

def getJson(city):
    try:
        # Je récupère les informations fournies par wunderground grâce à leur api, au format json
        page_json = urllib2.urlopen('http://api.wunderground.com/api/0def10027afaebb7/forecast/conditions/lang:FR/q/France/'+city+'.json')
        # Je lis la page
        json_string = page_json.read()
        # Je mets cette page dans un parseur
        parsed_json = json.loads(json_string)
        # Et je peux fermer ma page meteo, je n'en ai plus besoin
        page_json.close()

        if parsed_json['current_observation']:
            return parsed_json
        else:
            return 'Les informations météo ne sont pas accessibles sur le site wunderground.com'


    except:
        return 'Les informations météo ne sont pas accessibles sur le site wunderground.com'

def currentWeather(parsed_json):
    if parsed_json != 'Les informations météo ne sont pas accessibles sur le site wunderground.com':
        city = parsed_json['current_observation']['display_location']['city'] # la ville
        last_observation = parsed_json['current_observation']['observation_time'] # l'heure dernière observation
        current_temp = parsed_json['current_observation']['temp_c'] # la température en °C
        current_weather = parsed_json['current_observation']['weather'] # le temps actuel
        humidity = parsed_json['current_observation']['relative_humidity'] # le taux d'humidité en %
        wind_kph = parsed_json['current_observation']['wind_kph'] # la vitesse du vent
        wind_dir = parsed_json['current_observation']['wind_dir'] # l'orientation du vent
        pressure_mb = parsed_json['current_observation']['pressure_mb'] # la pression atmosphérique
        pressure_trend = parsed_json['current_observation']['pressure_trend'] # l'evolution pression atmosphérique
        feelslike_c = parsed_json['current_observation']['feelslike_c'] # la température ressentie
        visibility = parsed_json['current_observation']['visibility_km'] # la visibilité en km
        UV = parsed_json['current_observation']['UV'] # l'indice UV

        #concat string
        result =  ROUND_PUSHPIN +" Meteo pour " + city + "\n\n"
        result +=  "Temperature actuelle " + str(current_temp) + " degre\n"
        if current_weather == "Nuageux":
            result +=  "Actuellement, " + CLOUD + " " +  current_weather + "\n"
        else:
            result +=  "Actuellement, " + current_weather + "\n"
        result +=  "Temperature ressentie " + feelslike_c + " degre\n"
        result +=  WIND + " Vitesse du vent " + str(wind_kph) + "km/h\n"
        result +=   DROPLET + " Taux d'humidite ressentie " + humidity + "\n"
        return result
    else:
        return parsed_json

def forecast(parsed_json):
    if parsed_json != 'Les informations météo ne sont pas accessibles sur le site wunderground.com':
        forecast = parsed_json['forecast']['simpleforecast']['forecastday']
        result = ""
        mois_letter = ""
        for i in forecast:
            jour           = i['date']['day']        # jour
            mois           = i['date']['month']      # mois
            annee          = i['date']['year']       # année
            jour_sem       = i['date']['weekday']    # jour de la semaine
            period         = i['period']             # période
            tempmax        = i['high']['celsius']    # température maximale
            tempmin        = i['low']['celsius']     # température minimale
            condition      = i['conditions']         # conditions
            icon           = i['icon']               # icone en lien avec condition
            skyicon        = i['skyicon']            # le couverture nuagueuse
            pop            = i['pop']                # probabilité de précipitation
            hauteur_precip = i['qpf_allday']['mm']   # hauteur de précipitation pour la journée
            hauteur_neige  = i['snow_allday']['cm']  # hauteur de neige pour la journée
            vent           = i['avewind']['kph']     # vitesse moyenne du vent
            vent_dir       = i['avewind']['dir']     # direction du vent
            tx_humidite    = i['avehumidity']        # taux d'humidité

            #Translate
            while switch(mois):
                if case ( 1):
                    mois_letter = "Janvier"
                    break
                if case ( 2):
                    mois_letter = "Fevrier"
                    break
                if case ( 3):
                    mois_letter = "Mars"
                    break
                if case ( 4):
                    mois_letter = "Avril"
                    break
                if case ( 5):
                    mois_letter = "Mai"
                    break
                if case ( 6):
                    mois_letter = "Juin"
                    break
                if case ( 7):
                    mois_letter = "Juillet"
                    break
                if case ( 8):
                    mois_letter = "Aout"
                    break
                if case ( 9):
                    mois_letter = "Septembre"
                    break
                if case ( 10):
                    mois_letter = "Octobre"
                    break
                if case ( 11):
                    mois_letter = "Novembre"
                    break
                if case ( 12):
                    mois_letter = "Decembre"
                    break


            #concat string
            result += jour_sem.encode('utf8')+ " " + str(jour) + " " + mois_letter + " " +  str(annee) + "\n"
            result += condition.encode('utf8') + "\n"
            result += "Temperature maximale : " + str(tempmax) + " °C\n"
            result += "Temperature minimale : " + str(tempmin) + " °C\n"
            result += "Probabilite de précipitation " + str(pop) + "%\n"
            result +="Taux d'humidité  "  + str(tx_humidite) + "%\n"
            result +="Vitesse moy du vent "  + str(vent) + " km/h\n\n"

        return result
    else:
        return parsed_json
def getLatLon(parsed_json):
    latlon = []
    if parsed_json != 'Les informations meteo ne sont pas accessibles sur le site wunderground.com':
        latlon.append(parsed_json['current_observation']['display_location']['latitude'])
        latlon.append(parsed_json['current_observation']['display_location']['longitude'])
        return latlon
    else:
        return latlon
