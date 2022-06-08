import discord, re, retrieve
from discord.ext import tasks

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    @tasks.loop(minutes = 2)
    async def noti_check():
        if retrieve.validSection("CMSC420", "0101") == [True, "has open seats"]:
            channel = client.get_channel(960978831638949948)
            await channel.send("<@120992169539534848> Open seat/s in " + "CMSC420 0101")
        if retrieve.validSection("CMSC420", "0201") == [True, "has open seats"]:
            channel = client.get_channel(960978831638949948)
            await channel.send("<@120992169539534848> Open seat/s in " + "CMSC420 0201")
        if retrieve.validSection("CMSC420", "0401") == [True, "has open seats"]:
            channel = client.get_channel(960978831638949948)
            await channel.send("<@120992169539534848> Open seat/s in " + "CMSC420 0401")
    noti_check.start()
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    channel = message.channel
    course_re = (re.search(r'^!course ([\w]+[\d]+\w?)$', msg))
    if course_re:
        for sections in retrieve.sections(course_re.group(1).lower()):
            await channel.send(sections)


client.run(DISCORD_KEY)
