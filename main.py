from config import TOKEN
import discord
from discord import Message, Option, Member
from discord.commands.context import ApplicationContext as AC
import datetime
import math
import asyncio

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_message(m: Message):
    if m.author.bot:
        return
    if m.content == 'привет':
        await m.channel.send(f'{m.author.mention} привет, тьфу ')
    elif m.content == 'приветик':
        await m.author.send(f'{m.author.name}, привет ;)')
    elif m.content == 'как дела?':
        await m.author.send(f'{m.author.name}, всё хорошо, а у тебя?:>')
    elif m.content == 'да':
        await m.channel.send(f'{m.author.mention} согласен!!! ')
    elif m.content == 'нет':
        await m.reply('фу, кринж')
    if "зебра" in m.content:
        await m.delete(delay=2)
        await m.channel.send("Полосатые — только коты!")
    else:
        await m.reply('я получил сообщение;>')


@bot.slash_command(description='Текущее время в Амстердаме')
async def time_amst(ctx: AC):
    amst = datetime.timezone(datetime.timedelta(hours=2))
    data = datetime.datetime.now(amst).strftime('%H:%M:%S')
    await ctx.respond(f'В Амстердаме сейчас {data}')


@bot.slash_command(description='Текущее время в Баку')
async def time_baku(ctx: AC):
    baku = datetime.timezone(datetime.timedelta(hours=4))
    data2 = datetime.datetime.now(baku).strftime('%H:%M:%S')
    await ctx.respond(f'В Баку сейчас {data2}')


@bot.slash_command(description='Математические примеры')
async def example(ctx: AC, first: Option(int), second: Option(int), third: Option(int)):
    result = first * second / math.sqrt(third)
    await ctx.respond(round(result, 3))


@bot.message_command(name='Повысить репутацию')
async def plus_rep(ctx: AC, m: Message):
    await ctx.respond(f'+ Rep, {m.author.mention}')


@bot.user_command(name="Дата регистрации")
async def account_creation_date(ctx, member: Member):
    await ctx.respond(f"{member.name} создал аккаунт {member.created_at}")


@bot.slash_command(description='Таймер')
async def timer(ctx: AC, second: Option(float)):
    await ctx.respond(f'{ctx.author.mention} твой таймер на {second} сек запущен')
    await asyncio.sleep(second)
    await ctx.channel.send(f'{ctx.author.mention} твоё время закончилось')


@bot.event
async def on_member_join(memb: discord.Member):
    channels = memb.guild.channels
    for ch in channels:
        if ch.name == "основной":
            await ch.send(f'Привет ,@{memb.name}')


@bot.event
async def on_member_remove(memb: discord.Member):
    channels = memb.guild.channels
    for ch in channels:
        if ch.name == "основной":
            await ch.send(f"{memb.name.title()} вышел с сервера...")


@bot.event
async def on_member_update(old: discord.Member, gold: discord.Member):
    channel = None
    channels = gold.guild.channels
    for ch in channels:
        if ch.name == "основной":
            channel = ch
    if old.nick != gold.nick:
        await channel.send(f"{old.name if not old.nick else old.nick} теперь "
                           f"{'без ника' if not gold.nick else gold.nick}")
    if old.roles != gold.roles:
        await channel.send(f"У {old.name} изменилась роль!")


@bot.event
async def on_user_update(old: discord.User, gold: discord.User):
    channel = None
    members = bot.get_all_members()
    for mem in members:
        if mem.name == gold.name:
            channels = mem.guild.channels
    for ch in channels:
        if ch.name == "основной":
            channel = ch
    if old.avatar != gold.avatar:
        await channel.send(f"У {gold.name} новая ава!")
        await channel.send(gold.avatar.url)
        await channel.send("👍👍👍")


@bot.slash_command(description="Удаление")
async def clear(ctx: AC, num: discord.Option(int) = 3):
    await ctx.respond('АААААА УДАЛЯЮ!!!')
    await ctx.channel.purge(limit=num)


bot.run(TOKEN)
