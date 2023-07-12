import discord
import dotenv
import os

import emoji

bot = discord.Bot()

dotenv.load_dotenv()
token = os.getenv('POLL_BOT_TOKEN')

embed_color = 0xefb034


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(description='Create simple poll')
async def simple_poll(ctx, question, choice_a=None, choice_b=None, choice_c=None, choice_d=None, choice_e=None,
                      choice_f=None, choice_g=None, choice_h=None, choice_i=None, choice_j=None, choice_k=None,
                      choice_l=None, choice_m=None, choice_n=None, choice_o=None, choice_p=None, choice_q=None,
                      choice_r=None, choice_s=None, choice_t=None):
    choices = [choice_a, choice_b, choice_c, choice_d, choice_e, choice_f, choice_g, choice_h, choice_i, choice_j,
               choice_k, choice_l, choice_m, choice_n, choice_o, choice_p, choice_q, choice_r, choice_s, choice_t]
    choices = [i for i in choices if i]
    choices_emojis = []
    # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    #            'u', 'v', 'w', 'x', 'y', 'z']
    regional_indicators = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴',
                           '🇵', '🇶', '🇷', '🇸', '🇹']
    # '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']

    desc_str = ''
    text = '📊** ' + question + '**'
    if choices:
        for i in range(0, len(choices)):
            e_dict = emoji.emoji_list(choices[i])
            # print(e_dict)
            e = ''
            try:
                e = e_dict[0]['emoji']
            except IndexError:
                pass
            if e:
                choices_emojis.append(e[0])
                desc_str_i = choices[i]
                if desc_str_i[0] == e[0]:
                    desc_str = desc_str + e[0] + 'ᅠ' + desc_str_i[1:] + '\n'
                else:
                    desc_str = desc_str + e[0] + 'ᅠ' + desc_str_i + '\n'
            else:
                # print(i)
                choices_emojis.append(regional_indicators[i])
                desc_str = desc_str + regional_indicators[i] + 'ᅠ' + choices[i] + '\n'
        embed = discord.Embed(description=desc_str, color=embed_color)
        interaction = await ctx.respond(text, embed=embed)
        for e0 in choices_emojis:
            msg = await interaction.original_response()
            # print(emoji)
            await msg.add_reaction(e0)
    else:
        interaction = await ctx.respond(text)
        msg = await interaction.original_response()
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


@bot.message_command(name='Close poll')
async def poll_results(ctx: discord.ApplicationContext, message: discord.Message):
    if message.author.id != bot.user.id:
        await ctx.respond("Oops.. It seems it's not my message :(", ephemeral=True)
        return
    if message.embeds[0].footer:
        await ctx.respond("This poll is already closed", ephemeral=True)
        return
    all_reactions = message.reactions
    reactions = []
    for reaction in all_reactions:
        async for i in reaction.users():
            if i.id == bot.user.id:
                reactions.append(reaction)
                continue
    print(reactions)
    reactions.sort(key=lambda x: x.count, reverse=True)
    print(reactions)

    def squares(n):
        return ''.join([':blue_square:' for _ in range(n)])

    info = {}
    text = message.embeds[0].description
    for line in text.splitlines(False):
        ind = line.find('ᅠ')
        key = line[:ind]
        value = line[ind + 1:]
        print(f'[{key}], [{value}]')
        info[key] = value
    max_reactions = reactions[0].count - 1
    texts = []
    for i in reactions:
        if max_reactions != 0:
            num = round((i.count - 1) * 20 / max_reactions)
        else:
            num = 0
        e = str(i.emoji)
        print(num, e)
        choice = info[e]
        text = squares(num) + '\n' + e + 'ᅠ' + choice + 'ᅠ' + str(i.count - 1)
        texts.append(text)
    desc = '\n\n'.join(texts)
    embed = discord.Embed(title="Results:", description=desc, color=embed_color)
    embed.set_footer(text='Poll closed')
    await message.edit(embed=embed)
    await ctx.respond("Done results", ephemeral=True)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    channel = bot.get_channel(payload.channel_id)
    pre_message = channel.get_partial_message(payload.message_id)
    message = await pre_message.fetch()
    if message.author.id != bot.user.id:
        return
    if message.embeds[0].footer:
        member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        await message.remove_reaction(payload.emoji, member)

bot.run(token)
