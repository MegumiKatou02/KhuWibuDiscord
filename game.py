import random
import discord

async def roll(interaction: discord.Interaction, min_value: int = 0, max_value: int = 1000):
    if min_value > max_value:
        await interaction.response.send_message('Nhập sai thứ tự', ephemeral = True)
        return
    
    if max_value > 100000:
        await interaction.response.send_message('Yêu cầu nhập số nhỏ hơn 100000', ephemeral = True)
        return

    result = random.randint(min_value, max_value)
    await interaction.response.send_message(f'Kết quả: {result}')