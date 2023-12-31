from discord.ui.item import Item
import requests
from dotenv import load_dotenv
from os import getenv
from discord import Option, utils, ApplicationContext, ButtonStyle, AutocompleteContext
from discord.ext import commands
from discord.ui import View, button
from utils.embeds import SuccessEmbed, ErrorEmbed, UnsureEmbed

load_dotenv()

class Languages:
    def __init__(self, response) -> None:
        self.languages = response
        self.language_names = [lang["name"] for lang in self.languages]

    def get_version_and_id_by_name(self, language_name):
        for lang in self.languages:
            if lang["name"] == language_name:
                return lang["versions"], lang["id"]
        return [], None
    
    def get_name_by_language_id(self, language_id):
        for lang in self.languages:
            if lang["id"].lower() == language_id.lower():
                return lang["name"]

    def language_autocomplete(self, ctx: ApplicationContext):
        language_choice = ctx.options["language"]
        return [lang for lang in self.language_names if language_choice.lower() in lang.lower()]
    
    def version_autocomplete(self, ctx: ApplicationContext):
        language_choice = ctx.options["language"]
        versions, language_id = self.get_version_and_id_by_name(language_choice)
        if versions:
            versions.reverse()
            return ["latest", *versions]
        else: 
            return []
    

class CompilerResponse:
    def __init__(self, response) -> None:
        self.cpu_time = response["cpuTime"]
        self.memory = response["memory"]
        self.output = response["output"]
        self.language_id = response["language"]["id"]
        self.language_version = response["language"]["version"]
        self.language_version_name = response["language"]["version_name"]
    
    def convert_output(self):
        return f"```\n{self.output}\n```"

    def get_language_name(self):
        return languages.get_name_by_language_id(self.language_id)
    
    def create_embed(self):
        embed = SuccessEmbed(title="Compiler Results")
        embed.add_field(name="CPU Time", value=self.cpu_time, inline=False)
        embed.add_field(name="Memory Usage", value=self.memory, inline=False)
        embed.add_field(name="Result", value=self.convert_output(), inline=False)
        embed.set_footer(text=f"{self.get_language_name()}, {self.language_version_name}")
        return embed

class CompilerApi:
    def __init__(self) -> None:
        self.host = "online-code-compiler.p.rapidapi.com"
        self.base_url = f"https://{self.host}/v1/"
        self.languages_url = f"{self.base_url}languages/"
        self.headers = {
            "X-RapidAPI-Key": getenv("RAPID_API_KEY"),
            "X-RapidAPI-Host": self.host,
            "content-type": "application/json"
        }
    
    def get_languages(self):
        return Languages(requests.get(self.languages_url, headers=self.headers).json())

    def create_compiler(self, language_id, language_version="latest", input=None):
        def compiler(raw_code) -> CompilerResponse:
            return CompilerResponse(response=requests.post(self.base_url, headers=self.headers, json={
                "language": language_id,
                "version": language_version,
                "input": input,
                "code": raw_code
            }).json())
        return compiler
    
class RecompileButton(View):

    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, ctx, user_message, compiler, message_id_to_delete=None):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.ctx: ApplicationContext = ctx
        self.user_message = user_message
        self.compiler = compiler
        self.message_id_to_delete=None

    @button(label="recompile", style=ButtonStyle.primary)
    async def recompile(self, button, interaction):
        if interaction.user.id != self.user_message.author.id:
            return
        message = await self.ctx.fetch_message(self.user_message.id)
        raw_code = parse_code_block(message.content)
        response = self.compiler(raw_code)
        embed = response.create_embed()
        bot_message = await interaction.response.send_message(embed=embed)
        bot_message.edit(view=RecompileButton(ctx=self.ctx, user_message=self.user_message, compiler=self.compiler, message_id_to_delete=bot_message.id))

    @button(label="delete", style=ButtonStyle.danger)
    async def delete(self, button, interaction):
        try:
            message = await self.ctx.fetch_message(self.message_id_to_delete)
            await message.delete()
        except Exception as e:
            print(e)

compiler_api = CompilerApi()
languages = compiler_api.get_languages()

def parse_code_block(content):
    return "\n".join(content.split("\n")[1:][:-1])

@commands.slash_command()
async def compile(ctx: ApplicationContext, language: Option(str, autocomplete=utils.basic_autocomplete(languages.language_autocomplete)), version: Option(str, autocomplete=utils.basic_autocomplete(languages.version_autocomplete)), input: str = None):
    versions, language_id = languages.get_version_and_id_by_name(language)

    if not language_id:
        await ctx.respond(embed=ErrorEmbed(description=f"Invalid language name: '{language}'\n\nPlease use autocomplete options."))
        return
    elif version not in versions and version != "latest":
        await ctx.respond(embed=ErrorEmbed(description=f"Invalid language version: '{version}.\n\nPlease use autocomplete options.'"))
        return
    else:
        await ctx.defer()
        help_message = UnsureEmbed(description="Please send your code block. Please use code block command for more information. Must use new lines after the start of your code block, and before the end.")
        help_message.add_field(name="Example:", value="\\```\ncode here\n```")
        message = await ctx.send(embed=help_message)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        
        user_code_message = await ctx.bot.wait_for("message", check=check, timeout=180)

        raw_code = parse_code_block(user_code_message.content)

        await message.delete()

        compiler = compiler_api.create_compiler(language_id, version, input)
        
        response = compiler(raw_code)
        embed = response.create_embed()
        bot_message = await ctx.respond(embed=embed)

        await bot_message.edit(embed=embed, view=RecompileButton(ctx=ctx, user_message=user_code_message, compiler=compiler, message_id_to_delete=bot_message.interaction.id))
