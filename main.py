import discord, re, retrieve, json
from discord.ext import tasks

client = discord.Client()
data = {}
data['960978831638949948'] = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    # @tasks.loop(minutes= 2)
    # async def noti_check():
    #     for channels in data:
    #         for courses in data[channels]:
    #             arr = courses.split(' ')
    #             if retrieve.validSection(arr[0], arr[1]) == [True, "has open seats"]:
    #                 channel = client.get_channel(int(channels))
    #                 for users in data[channels][courses]:
    #                     await channel.send(users + " Open seat/s in " + courses)
    #                 data[channels][courses].clear()
    # noti_check.start()

    @tasks.loop(minutes = 2)
    async def noti_check():
        if retrieve.validSection("CMSC420", "0101") == [True, "has open seats"]:
            channel = client.get_channel(960978831638949948)
            await channel.send("<@120992169539534848> Open seat/s in " + "CMSC420 0101")
        if retrieve.validSection("CMSC420", "0201") == [True, "has open seats"]:
            channel = client.get_channel(960978831638949948)
            await channel.send("<@120992169539534848> Open seat/s in " + "CMSC420 0201")
        if retrieve.validSection("CMSC420", "0301") == [True, "has open seats"]:
            channel = client.get_channel(960978831638949948)
            await channel.send("<@120992169539534848> Open seat/s in " + "CMSC420 0301")
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
    channel_id = str(channel.id)
    course_re = (re.search(r'^!course ([\w]+[\d]+)$', msg))
    notify_re = (re.search(r'^!notify ([\w\d]+) ([\w\d]+)$', msg))
    if course_re:
        for sections in retrieve.sections(course_re.group(1).lower()):
            await channel.send(sections)
    elif notify_re:
        output = retrieve.validSection(notify_re.group(1).lower(), notify_re.group(2).lower())
        if output == [True, "no seats"]:
            course_name = notify_re.group(1) + " " + notify_re.group(2)
            mentionID = '<@' + str(message.author.id) + '>'
            if channel_id not in data:
                data[channel_id] = {}
            if course_name not in data[channel_id]:
                data[channel_id][course_name] = []
            if mentionID not in data[channel_id][course_name]:
                data[channel_id][course_name].append(mentionID)
            await channel.send(mentionID + " successful")
        else:
            await channel.send(output[1])
    elif msg == "!notify check":
      out = ""
      if channel_id in data:
        for courses in data[channel_id]:
            for user in data[channel_id][courses]:
                if user[2:20] == str(message.author.id):
                    out += "Notify for " + courses + '\n'
      await channel.send(out) if len(out) > 0 else await channel.send("None")
    elif 'cock' in msg or 'penis' in msg or 'dick' in msg or 'erika' in msg or 'tranny' in msg or 'trans' in msg:
      await channel.send('https://tenor.com/view/toy-dick-boner-sex-toy-dick-penis-toy-gif-20447370')
    elif 'ryan' in msg or 'colossal' in msg or 'fortnite' in msg:
        await channel.send('https://cdn.discordapp.com/attachments/960762579968475146/965823380832018432/video0.mov')
    elif 'best' in msg or 'waifu' in msg or 'manga' in msg or 'episode' in msg or 'season' in msg:
        await channel.send('https://tenor.com/view/makise-kirusu-gif-21154482')
    elif 'science' in msg or 'cool' in msg or 'steins' in msg or 'bitch' in msg or 'anime' in msg:
        await channel.send('https://tenor.com/view/steins-gif-18331409')
      
client.run('OTYzODk0MzI3Njk0NzM3NDY5.YlcujA.38sRAI7qwRaQ7MXY_4BPU7x0xxM')
