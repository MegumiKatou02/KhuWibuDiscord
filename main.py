import asyncio
from datetime import datetime, timedelta
import random
import discord
from discord.ext import commands
from tabulate import tabulate
from discord.ui import Select, View

import chatting
import config
import game
import help_list

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True

clients = commands.Bot(command_prefix='>>', intents=intents)

@clients.event
async def on_ready():
    print("ready !!!")
    print("----------")
    game = discord.Game("Khu Wibu")
    await clients.change_presence(activity=game)

    await clients.tree.sync() 

    print("----------")

#goodbye
@clients.command()
async def goodbye(interaction: discord.Interaction):
    await interaction.response.send_message("Cook gium cai <(\")")

#member join
@clients.event
async def member_join(member):
    channel = clients.get_channel(1210656611270533222)
    if channel:
        print("nice.")
        await channel.send(f"Welcome, {member.name}!")
    else:
        print("Channel not found or invalid channel ID.")

#say
@clients.tree.command(description="Nói thông qua bot")
async def say(interaction: discord.Interaction, *, message: str):
    await interaction.response.send_message("Đang xử lý...", ephemeral=True)
    await interaction.channel.purge(limit=1, check=lambda msg: msg.author == interaction.user)
    await interaction.channel.send(message)

#roll
@clients.tree.command(name = 'roll', description="Random số")
async def roll_command(interaction: discord.Interaction, min_value: int = 0, max_value: int = 1000):
    await game.roll(interaction, min_value, max_value)

#check prefix
@clients.event
async def on_message(message):
    await chatting.on_message(message, clients) 

#server
@clients.tree.command(description = "Hiển thị thông tin máy chủ") #
async def server(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(title=f"Thông tin về server {guild.name}", color=discord.Color.blue())

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    else:
        embed.add_field(name="Icon Server", value='Không có icon', inline=False)
    embed.add_field(name="Tên Server", value=guild.name, inline=False)
    embed.add_field(name="ID Server", value=guild.id, inline=False)
    embed.add_field(name="Ngày tạo", value=guild.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=False)
    embed.add_field(name="Số Thành Viên", value=guild.member_count, inline=False)
    embed.add_field(name="Số Kênh", value=len(guild.channels), inline=False)

    owner = guild.owner
    embed.add_field(name="Server Owner", value=owner.mention, inline=False)

    await interaction.response.send_message(embed=embed)

#help
@clients.tree.command(description="Help / Show commands")
async def help(interaction: discord.Interaction):
    await help_list.send_help_message(interaction)

#avatar
@clients.tree.command(description="Hiển thị avatar của một thành viên")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if not member:
        member = interaction.user  
    
    avatar_url = member.display_avatar.url 

    embed = discord.Embed(
        title=f"Avatar của {member.display_name}",
        description="",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)

    await interaction.response.send_message(embed=embed)

#avt
@clients.tree.command(description="Hiển thị avatar của một thành viên")
async def avt(interaction: discord.Interaction, member: discord.Member = None):
    if not member:
        member = interaction.user  
    
    avatar_url = member.display_avatar.url 

    embed = discord.Embed(
        title=f"Avatar của {member.display_name}",
        description="",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)

    await interaction.response.send_message(embed=embed)

#run
@clients.command()
async def run(ctx):
    await ctx.send("Khu Wibu bot discord is running")

#choose
@clients.tree.command(name="choose", description = "Random 1 trong nhiều lựa chọn")
async def choose(interaction: discord.Interaction, choice1: str, choice2: str, choice3: str = None, 
                 choice4: str = None, choice5: str = None, choice6: str = None, choice7: str = None,
                 choice8: str = None, choice9: str = None, choice10: str = None):
    choice_list = [choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9, choice10]
    
    choice_list = [choice.strip() for choice in choice_list if choice]
    
    if not choice_list:
        await interaction.response.send_message("Please provide some options to choose from!", ephemeral=True)
        return
    
    chosen_option = random.choice(choice_list)
    
    await interaction.response.send_message(f"I choose: {chosen_option}")

#find member
@clients.tree.command(name= "find_member", description="Tạo ra chủ đề và tìm người chiến thắng")
async def find_member(interaction: discord.Interaction, topic: str,
                      member1: discord.Member,
                      member2: discord.Member = None, 
                      member3: discord.Member = None,
                      member4: discord.Member = None,
                      member5: discord.Member = None,
                      member6: discord.Member = None,
                      member7: discord.Member = None,
                      member8: discord.Member = None,
                      member9: discord.Member = None,
                      member10: discord.Member = None):
    members = [member for member in [member1, member2, member3, member4, member5,
                                     member6, member7, member8, member9, member10] if member]

    if not members:
        await interaction.response.send_message("Please provide some options to choose from!", ephemeral=True)
        return
    
    chosen_member = random.choice(members)

    await interaction.response.send_message(f'**{topic}**: {chosen_member.mention}')

#reminder
@clients.tree.command(description="Đặt nhắc nhở")
async def reminder(interaction: discord.Interaction, time: str, *, message: str):
    try:
        reminder_time = datetime.strptime(time, "%H:%M")
        
        now = datetime.now()
        wait_time = (reminder_time - now).total_seconds()

        if wait_time < 0:
            reminder_time += timedelta(days=1)
            wait_time = (reminder_time - now).total_seconds()

        await interaction.response.send_message(f"Nhắc nhở của bạn đã được đặt vào lúc {reminder_time.strftime('%H:%M')}! Tôi sẽ nhắc bạn: **{message}**", ephemeral=True)

        await asyncio.sleep(wait_time)

        await interaction.user.send(f"**Nhắc nhở bạn đã đặt**: {message}")
    
    except ValueError:
        await interaction.response.send_message("Vui lòng nhập thời gian đúng định dạng HH:MM (vd: 02:24)", ephemeral=True)

clients.run(config.TOKEN)