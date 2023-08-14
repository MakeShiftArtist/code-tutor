import requests
from dotenv import load_dotenv
from os import getenv
from discord import Embed, Option, utils, Color, ApplicationContext
from discord.ext import commands

load_dotenv()

def get_langs():
    url = "https://online-code-compiler.p.rapidapi.com/v1/languages/"
    headers = {
        "X-RapidAPI-Key": getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "online-code-compiler.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def compile_code(language, version, code, input):
    url = "https://online-code-compiler.p.rapidapi.com/v1/"
    payload = {
        "language": language,
        "version": version,
        "code": code,
        "input": input
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "online-code-compiler.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

langs = get_langs()

async def autocomplete_version(ctx):
    lang_name = ctx.options["language"]
    for lang in langs:
        if lang["name"] == lang_name:
            return ["latest", *lang["versions"]]
        
def get_lang_info(language):
    for lang in langs:
        if lang["name"] == language:
            return lang["id"], lang["versions"]
        
async def autocomplete_language(ctx):
    language = ctx.options["language"]
    choices = [lang["name"] for lang in langs if language.lower() in lang["name"].lower()][:25]
    return choices

@commands.slash_command()
async def compile(ctx: ApplicationContext, language: Option(str, autocomplete=utils.basic_autocomplete(autocomplete_language)), version: Option(str, autocomplete=utils.basic_autocomplete(autocomplete_version)), input: str = None):
    lang_id, lang_versions = get_lang_info(language)
    
    if not lang_id:
        await ctx.respond(embed=Embed(
            description=f"Invalid language name: '{language}'\n\nPlease use autocomplete options.",
            color=Color.red()
        ))
        return
    elif version not in lang_versions and version != "latest":
        await ctx.respond(embed=Embed(
            description=f"Invalid language version: '{version}.\n\nPlease use autocomplete options.'",
            color=Color.red()
        ))
        return
    else:
        await ctx.defer()
        message = await ctx.send(embed=Embed(
            description="Please send your code block. Please use code block command for more information. Do ***not*** add a language in the code block format. Expires in 3 minutes.",
            color=Color.green()
        ))

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        
        code_block = await ctx.bot.wait_for("message", check=check, timeout=180)
        print(code_block)
        await ctx.send(f"Hello {code_block.author}, \n{code_block.content}")
        
        #print(code_block.content[3:][:-3])
    