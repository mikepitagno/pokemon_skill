#!/usr/bin/env python3

from lxml import html
import requests
import re
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors
import datetime
import socket

app = Flask(__name__)
ask = Ask(app, "/")

poke_dict = {'bulbasaur': '1', 'ivysaur': '2', 'venusaur': '3', 'charmander': '4', 'charmeleon': '5', 'charizard': '6', 'squirtle': '7', 'wartortle': '8', 'blastoise': '9', 'caterpie': '10', 'metapod': '11', 'butterfree': '12', 'weedle': '13', 'kakuna': '14', 'beedrill': '15', 'pidgey': '16', 'pidgeotto': '17', 'pidgeot': '18', 'rattata': '19', 'raticate': '20', 'spearow': '21', 'fearow': '22', 'ekans': '23', 'arbok': '24', 'pikachu': '25', 'raichu': '26', 'sandshrew': '27', 'sandslash': '28', 'nidoran-f': '29', 'nidorina': '30', 'nidoqueen': '31', 'nidoran-m': '32', 'nidorino': '33', 'nidoking': '34', 'clefairy': '35', 'clefable': '36', 'vulpix': '37', 'ninetales': '38', 'jigglypuff': '39', 'wigglytuff': '40', 'zubat': '41', 'golbat': '42', 'oddish': '43', 'gloom': '44', 'vileplume': '45', 'paras': '46', 'parasect': '47', 'venonat': '48', 'venomoth': '49', 'diglett': '50', 'dugtrio': '51', 'meowth': '52', 'persian': '53', 'psyduck': '54', 'golduck': '55', 'mankey': '56', 'primeape': '57', 'growlithe': '58', 'arcanine': '59', 'poliwag': '60', 'poliwhirl': '61', 'poliwrath': '62', 'abra': '63', 'kadabra': '64', 'alakazam': '65', 'machop': '66', 'machoke': '67', 'machamp': '68', 'bellsprout': '69', 'weepinbell': '70', 'victreebel': '71', 'tentacool': '72', 'tentacruel': '73', 'geodude': '74', 'graveler': '75', 'golem': '76', 'ponyta': '77', 'rapidash': '78', 'slowpoke': '79', 'slowbro': '80', 'magnemite': '81', 'magneton': '82', 'farfetchd': '83', 'doduo': '84', 'dodrio': '85', 'seel': '86', 'dewgong': '87', 'grimer': '88', 'muk': '89', 'shellder': '90', 'cloyster': '91', 'gastly': '92', 'haunter': '93', 'gengar': '94', 'onix': '95', 'drowzee': '96', 'hypno': '97', 'krabby': '98', 'kingler': '99', 'voltorb': '100', 'electrode': '101', 'exeggcute': '102', 'exeggutor': '103', 'cubone': '104', 'marowak': '105', 'hitmonlee': '106', 'hitmonchan': '107', 'lickitung': '108', 'koffing': '109', 'weezing': '110', 'rhyhorn': '111', 'rhydon': '112', 'chansey': '113', 'tangela': '114', 'kangaskhan': '115', 'horsea': '116', 'seadra': '117', 'goldeen': '118', 'seaking': '119', 'staryu': '120', 'starmie': '121', 'mr-mime': '122', 'scyther': '123', 'jynx': '124', 'electabuzz': '125', 'magmar': '126', 'pinsir': '127', 'tauros': '128', 'magikarp': '129', 'gyarados': '130', 'lapras': '131', 'ditto': '132', 'eevee': '133', 'vaporeon': '134', 'jolteon': '135', 'flareon': '136', 'porygon': '137', 'omanyte': '138', 'omastar': '139', 'kabuto': '140', 'kabutops': '141', 'aerodactyl': '142', 'snorlax': '143', 'articuno': '144', 'zapdos': '145', 'moltres': '146', 'dratini': '147', 'dragonair': '148', 'dragonite': '149', 'mewtwo': '150', 'mew': '151'}

@app.route('/')
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    thisHost = socket.gethostname()
    templateData = {
        'title' : thisHost,
        'time': timeString
    }
    return render_template('main.html', **templateData)

@ask.launch
def skill_launch():
    welcome_msg = render_template('welcome')
    reprompt_msg = render_template('reprompt')
    return question(welcome_msg) \
        .reprompt(reprompt_msg)

@ask.intent('YesIntent')
def ask_pokemon():
    pokemon_msg = render_template('pokemon')
    reprompt2_msg = render_template('reprompt2')
    return question(pokemon_msg) \
        .reprompt(reprompt2_msg)

@ask.intent('NoIntent')
def goodbye():
    goodbye_msg = render_template('goodbye')
    return statement(goodbye_msg)

@ask.intent('RetryIntent')
def retry(poke_name):
    session.attributes['poke_name'] = poke_name
    reprompt2_msg = render_template('reprompt2')
    retry_msg = render_template('retry', poke_name=poke_name)
    return question(retry_msg) \
        .reprompt(reprompt2_msg)

@ask.intent('AnswerIntent')
def get_desc(poke_name):
    if poke_name not in poke_dict:
        return retry(poke_name)
    else:
        poke_id = poke_dict[poke_name]
        regex = re.compile(r'[\n\r\t]')
        user_agent = {'User-agent': 'Mozilla/5.0'}
        url = 'https://pokemon.gameinfo.io/en/pokemon/' + poke_id + '-' + poke_name
        page = requests.get(url, headers = user_agent)
        tree = html.fromstring(page.content)
        desc_raw = tree.xpath('//p[@class="description"]/text()')
        desc_str = str(desc_raw[0])
        desc_final = regex.sub("", desc_str).replace("PokÃ©mon", "Pokemon")       
        return statement(desc_final)

@ask.intent('AMAZON.StopIntent')
def stop():
    goodbye_msg = render_template('goodbye')
    return statement(goodbye_msg)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    goodbye_msg = render_template('goodbye')
    return statement(goodbye_msg)

if __name__ == '__main__':
    app.run(debug=True)
