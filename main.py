import discord
from discord.ext import commands
from asyncio import TimeoutError
from random import choice

client = commands.Bot(command_prefix='f!', case_insensitive=True)


@client.event
async def on_ready():
    print(f'Entrei como {client.user}.')


@client.command()
async def play(ctx):
    game = True
    alreadySelectedWords = []
    formForca = ['```X===:===\nX   :\nX\nX\nX\nX\nX\n===========```',
                 '```X===:===\nX   :\nX   O\nX\nX\nX\nX\n===========```',
                 '```X===:===\nX   :\nX   O\nX  \|\nX\nX\nX\n===========```',
                 '```X===:===\nX   :\nX   O\nX  \|/\nX\nX\nX\n===========```',
                 '```X===:===\nX   :\nX   O\nX  \|/\nX   |\nX\nX\n===========```',
                 '```X===:===\nX   :\nX   O\nX  \|/\nX   |\nX  /\nX\n===========```',
                 '```X===:===\nX   :\nX   O\nX  \|/\nX   |\nX  / \ \nX\n===========```']
    alphabetCharacters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    embed = discord.Embed(
        title='Jogo da Forca',
        description='Você terá 1 minuto entre cada tentativa.',
        colour=1776411
    )
    embed.add_field(name='⠀', value='⠀', inline=False)
    embed.add_field(name='⠀', value='⠀')
    embed.add_field(name='⠀', value='⠀')

    def check_theme(m):
        return m.content.lower() == 'filmes' or m.content.lower() == 'frutas' or\
               m.content.lower() == 'animais' or m.content.lower() == 'profissões' and \
               m.author == ctx.author and m.channel == ctx.channel

    def check_attempt(m):
        return m.channel == ctx.channel and len(m.content) == 1 and\
               m.content.lower() in alphabetCharacters

    def check_game(m):
        return m.content.lower() == 's' or m.content.lower() == 'n' and\
               m.author == ctx.author and m.channel == ctx.channel

    while game:
        wrongs = 0
        attempts = True

        x = await ctx.send(f'**Filmes / Frutas / Animais / Profissões**\nescolha um dos temas acima.')

        try:
            themeChoice = await client.wait_for('message', timeout=60.0, check=check_theme)
            await themeChoice.delete()
            await x.delete()
        except TimeoutError:
            await ctx.send('Tempo esgotado.')
            game = False
        else:
            if themeChoice.content.lower() == 'filmes':
                words = ['os vingadores', 'coringa', 'avatar', 'slender man', 'bacurau', 'malévola', 'parasita',
                         'a casa monstro', 'homem de ferro', 'star wars']
            elif themeChoice.content.lower() == 'frutas':
                words = ['banana', 'pera', 'melância', 'maracujá', 'laraja', 'maça', 'abacaxi']
            elif themeChoice.content.lower() == 'animais':
                words = ['cachorro', 'gato', 'elefante', 'galhinha', 'tucano', 'vaca', 'ovelha', 'hipopótamo',
                         'cavalo', 'rato', 'urubu', 'porco', 'girafa']
            elif themeChoice.content.lower() == 'Profissões':
                words = ['medico', 'professor', 'dentista', 'taxista', 'goleiro', 'advogado', 'costureira',
                         'garçom', 'músico']

            try:
                for w in alreadySelectedWords:
                    words.remove(w)
                selectedWord = choice(words)
                alreadySelectedWords += selectedWord
            except IndexError:
                await ctx.send('Ocorreu um erro. Por favor, escolha outro tema.')
                game = False
            else:
                typedLetters = []
                hits = ['-']

                selectedWord = selectedWord.split()
                selectedWord = '-'.join(selectedWord)

                embed.set_field_at(0, name=f'Tema: **{themeChoice.content}**', value=f'⠀', inline=False)
                msg = await ctx.send(embed=embed)
                while attempts:
                    answer = ''
                    for l in str(selectedWord):
                        if l in hits:
                            answer += l
                        else:
                            answer += ' _ '

                    embed.set_field_at(1, name='Forca', value=f'{formForca[wrongs]}', inline=True)
                    embed.set_field_at(2, name='Palavra',
                                       value=f'``` \n\n\n\n\n\n{answer.lstrip().rstrip().upper()}\n ```', inline=True)
                    embed.set_footer(text=' - '.join(typedLetters))
                    await msg.edit(embed=embed)

                    if answer == selectedWord:
                        embed.set_field_at(0, name=f'Tema: **{themeChoice.content}**', value=f'**Você venceu!!! \o/**', inline=False)
                        await msg.edit(embed=embed)
                        attempts = False
                    elif wrongs >= 6:
                        embed.set_field_at(0, name=f'Tema: **{themeChoice.content}**', value=f'**Você foi enforcado(a)! D:**', inline=False)
                        await msg.edit(embed=embed)
                        attempts = False
                    else:
                        try:
                            attempt = await client.wait_for('message', timeout=60.0, check=check_attempt)
                            await attempt.delete()
                        except TimeoutError:
                            await ctx.send('Tempo esgotado.')
                            attempts = False
                            game = False
                        else:
                            if attempt.content.lower() in typedLetters:
                                embed.set_field_at(0, name=f'Tema: **{themeChoice.content}**', value=f'Você já tentou essa letra.', inline=False)
                                await msg.edit(embed=embed)
                            else:
                                typedLetters += attempt.content.lower()

                                if attempt.content.lower() in selectedWord:
                                    hits += attempt.content.lower()
                                    embed.set_field_at(0, name=f'Tema: **{themeChoice.content}**', value=f'Você acertou! :D', inline=False)
                                else:
                                    wrongs += 1
                                    embed.set_field_at(0, name=f'Tema: **{themeChoice.content}**', value=f'Você errou! :(', inline=False)

                                await msg.edit(embed=embed)

                x = await ctx.send('Você deseja jogar novamente? [s / n]')
                try:
                    msg = await client.wait_for('message', timeout=60.0, check=check_game)
                    await x.delete()
                    await msg.delete()
                except TimeoutError:
                    await ctx.send('Tempo esgotado.')
                    game = False
                else:
                    if msg.content.lower() == 'n':
                        game = False


client.run('ODgwMDg2NTA2MTM4NjQwNDE0.YSZKbg.B1oHm2aPRo2vxHQIbFgh07GCd3M')
