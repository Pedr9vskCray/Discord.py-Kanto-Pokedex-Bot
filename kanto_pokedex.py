import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import json
import random

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"}

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())

# working fine


@bot.event
async def on_ready():
    print("Estou Pronto!")
    print(f"Estou conectado como: {bot.user}")

# commands


@bot.command(name='dex')
async def kanto_dex(ctx, dexargument):

    with open('pokedex.json') as f:
        kanto_dex = json.load(f)

    for item in range(len(kanto_dex)):
        if kanto_dex[item]['name'] == dexargument.capitalize():
            pokemon_index = item

    try:
        print(kanto_dex[pokemon_index]['name'])
    except NameError:
        failed = 'This pokémon name may be incorrect. Make sure you typed it correctly.'
        await ctx.send(failed)

    # nintendo official pokedex scraping

    url = f'https://www.pokemon.com/br/pokedex/{dexargument.capitalize()}'
    response = requests.get(url, headers=headers)
    site = BeautifulSoup(response.content, 'html.parser')

    image = site.find('img', attrs={'alt': f'{dexargument.capitalize()}'})
    description = site.find("p", attrs={"class": "version-x active"}).text
    title = f'{kanto_dex[pokemon_index]["name"]} - N° {kanto_dex[pokemon_index]["id"]}'

    # webscraping sprite images

    sprite_url = 'https://www.pokemondb.net/sprites/'
    sprite_response = requests.get(sprite_url, headers=headers)
    sprite_site = BeautifulSoup(sprite_response.content, 'html.parser')

    sprite_src = sprite_site.find(
        'img', attrs={'alt': f'{kanto_dex[pokemon_index]["name"]}'})

    # random pokeball setup

    ball_list = ['poke', 'great', 'ultra', 'master', 'beast', 'cherish', 'dive', 'dream', 'dusk', 'fast', 'friend', 'heal', 'heavy', 'level',
                 'love', 'lure', 'luxury', 'moon', 'nest', 'net', 'park', 'premier', 'quick', 'repeat', 'safari', 'sport', 'strange', 'timer']

    random_ball = random.randint(0, len(ball_list))

    # embed

    embed = discord.Embed(
        title=title,
        description=description,
        colour=6564916
    )

    embed.set_author(
        name='Pokémon', icon_url=f'https://www.serebii.net/itemdex/sprites/{ball_list[random_ball]}ball.png')

    embed.set_thumbnail(url=sprite_src['src'])

    embed.set_image(url=image['src'])

    try:
        embed.set_footer(
            text=f'{kanto_dex[pokemon_index]["type"][0].capitalize()}, {kanto_dex[pokemon_index]["type"][1].capitalize()} type pokémon.')
    except IndexError:
        embed.set_footer(
            text=f'{kanto_dex[pokemon_index]["type"][0].capitalize()} type pokémon.')

    embed.add_field(name='HP', value=kanto_dex[pokemon_index]['stats']['hp'])
    embed.add_field(
        name='Attack', value=kanto_dex[pokemon_index]['stats']['attack'])
    embed.add_field(
        name='Defense', value=kanto_dex[pokemon_index]['stats']['defense'])
    embed.add_field(
        name='SP-ATK', value=kanto_dex[pokemon_index]['stats']['sp-atk'])
    embed.add_field(
        name='SP-DEF', value=kanto_dex[pokemon_index]['stats']['sp-def'])
    embed.add_field(
        name='Speed', value=kanto_dex[pokemon_index]['stats']['speed'])

    await ctx.send(embed=embed)


# bot.run

bot.run('discord.py token')
