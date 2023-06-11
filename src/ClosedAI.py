import discord
import json

from discord.ext import commands
from discord import app_commands

from src.Utils.ScrapAI.text import generate_response, transcript, generate_response_thread
from src.Utils.ScrapAI.image import generate_image

class ClosedAI(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @app_commands.command(name="askgpt4", description="Ask GPT4 for a response")
    async def askgpt4(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        gpt4_response = await generate_response(prompt)
        await interaction.followup.send(gpt4_response[0])

        for k in range(1, len(gpt4_response)):
            interaction.channel.send(gpt4_response[k])

    @app_commands.command(name="yt-summary", description="Provides a short description of a youtube video")
    async def _summarize(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer()

        try:
            tr = await transcript(link)
            await interaction.followup.send(tr[0])

            for k in range(1, len(tr)):
                interaction.channel.send(tr[k])

        except :
            await interaction.followup.send(
                content='Please only provide youtube url, if the link you send is a yoube url feel free to report the issue',
                ephemeral=True)

    @app_commands.command(name="imagine", description="Générer une image")
    @app_commands.choices(style=[
        app_commands.Choice(name='Imagine V3', value='IMAGINE_V3'),
        app_commands.Choice(name='Imagine V4 Beta', value='IMAGINE_V4_Beta'),
        app_commands.Choice(name='Imagine V4 creative', value='V4_CREATIVE'),
        app_commands.Choice(name='Anime', value='ANIME_V2'),
        app_commands.Choice(name='Realistic', value='REALISTIC'),
        app_commands.Choice(name='Disney', value='DISNEY'),
        app_commands.Choice(name='Studio Ghibli', value='STUDIO_GHIBLI'),
        app_commands.Choice(name='Graffiti', value='GRAFFITI'),
        app_commands.Choice(name='Medieval', value='MEDIEVAL'),
        app_commands.Choice(name='Fantasy', value='FANTASY'),
        app_commands.Choice(name='Neon', value='NEON'),
        app_commands.Choice(name='Cyberpunk', value='CYBERPUNK'),
        app_commands.Choice(name='Landscape', value='LANDSCAPE'),
        app_commands.Choice(name='Japanese Art', value='JAPANESE_ART'),
        app_commands.Choice(name='Steampunk', value='STEAMPUNK'),
        app_commands.Choice(name='Sketch', value='SKETCH'),
        app_commands.Choice(name='Comic Book', value='COMIC_BOOK'),
        app_commands.Choice(name='Cosmic', value='COMIC_V2'),
        app_commands.Choice(name='Logo', value='LOGO'),
        app_commands.Choice(name='Pixel art', value='PIXEL_ART'),
        app_commands.Choice(name='Interior', value='INTERIOR'),
        app_commands.Choice(name='Mystical', value='MYSTICAL'),
        app_commands.Choice(name='Super realism', value='SURREALISM'),
        app_commands.Choice(name='Minecraft', value='MINECRAFT'),
        app_commands.Choice(name='Dystopian', value='DYSTOPIAN')
    ])
    @app_commands.choices(ratio=[
        app_commands.Choice(name='Square (1:1)', value='RATIO_1X1'),
        app_commands.Choice(name='Vertical (9:16)', value='RATIO_9X16'),
        app_commands.Choice(name='Horizontal (16:9)', value='RATIO_16X9'),
        app_commands.Choice(name='Standard (4:3)', value='RATIO_4X3'),
        app_commands.Choice(name='Classic (3:2)', value='RATIO_3X2')
    ])
    @app_commands.choices(upscale=[
        app_commands.Choice(name='Yea sure', value='True'),
        app_commands.Choice(name='No thanks', value='False')
    ])
    async def imagine(self, interaction: discord.Interaction, prompt: str, style: app_commands.Choice[str], ratio: app_commands.Choice[str],
                    negative: str = None, upscale: app_commands.Choice[str] = None):

        if upscale is not None and upscale.value == 'True':
            upscale_status = True
        else:
            upscale_status = False

        await interaction.response.defer()

        prompt_to_detect = prompt

        if negative is not None:
            prompt_to_detect = f"{prompt} Negtive Prompt : {negative}"

        imagefileobj = await generate_image(prompt, style.value, ratio.value, negative, upscale_status)

        file = discord.File(imagefileobj, filename=f"image.png")
        embed = discord.Embed(color=0x141414)
        embed.set_author(name="Generated Image")
        embed.add_field(name="Prompt", value=f"{prompt}", inline=False)
        embed.add_field(name="Style", value=f"{style.name}", inline=True)
        embed.add_field(name="Ratio", value=f"{ratio.name}", inline=True)
        embed.set_image(url="attachment://image.png")

        if upscale_status:
            embed.set_footer(
                text="⚠️ Upscaling is only noticeable when you open the image in a browser because Discord reduces image quality.")
        else:
            embed.set_footer(text="To create more images use /imagine")

        if negative is not None:
            embed.add_field(name="Negative", value=f"{negative}", inline=False)

        await interaction.followup.send(content=f"Generated image for{interaction.user.mention}", file=file, embed=embed)


    @app_commands.command(name="create_thread",description="Creates a new chat with memory")
    @app_commands.choices(mode=[
        app_commands.Choice(name="Sortie de Prison de l'avatar fictif", value='JAILBREAK'),
        app_commands.Choice(name="Assistant dev",value='DEV')
    ])

    async def create_thread(self, interaction: discord.Interaction, title: str, mode: str):
        await interaction.response.defer()

        if isinstance(interaction.channel,discord.Thread):
            await interaction.followup.send('this command does not work in a thread', ephemeral=True)
            return

        with open('src/Utils/ScrapAI/preprompts.json', "r") as f:
            data = json.load(f)
        thread = await interaction.channel.create_thread(name=title.replace(" ", "_"), invitable=True)
        await thread.send(data[mode]+str(interaction.user.mention))
        await interaction.followup.send('Thread created',ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.Thread) and message.author.id != self.client.user.id :
            async with message.channel.typing():
                history = [msg.content async for msg in message.channel.history(limit=200)]
                response = await generate_response_thread(history)
                await message.channel.send(response[0])

                for k in range(1, len(response)):
                    message.channel.send(response[k])

        else:
            await self.client.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(ClosedAI(bot))