import os
import shutil
import json
import discord
from discord.ext import commands
import urbandictionary as ud

TOKEN = os.environ['token']
Client = discord.Client()
client = commands.Bot(command_prefix = '.')

client.remove_command('help')

# -- EVENTS --

@client.event
async def on_ready ():
  await client.change_presence(game=discord.Game(name=".help | nightscape.london"))
  print("Bot's been booted up. Awaiting user interaction")

@client.event
async def on_member_join (member):
  path = 'Users/' + member.name + '#' + member.discriminator
  userFolder = open(path, 'w+')
  userFolder.close()

  userFile(path, member)

@client.event
async def on_member_leave (member):
  path = 'Users/' + member.name + '#' + member.discriminator

  userDataDelete(path, member)

# -- COMMANDS --
@client.command(pass_context = True)
async def help (ctx):
  sender = ctx.message.author
  channel = ctx.message.channel

  embed = discord.Embed(
    colour = discord.Colour.purple()
  )

  if 'Staff' in [y.name.lower() for y in sender.roles]:
    embed.set_author(name = 'Help')
    embed.add_field(name = '.help', value = 'Shows the commands', inline = False)
    embed.add_field(name = '.role [Role]', value = 'Adds a role to you. Check #info for role information', inline = False)
    embed.add_field(name = '.thanks [User]', value = 'Thanks the given user', inline = False)
    embed.add_field(name = '.urban [Search]', value = 'Searches Urban Dictionary for the search item', inline = False)
    embed.add_field(name = '.google [Search]', value = 'Searches Google for the search item', inline = False)

    await client.send_message(channel, embed=embed)
  else:
    embed.set_author(name = 'Help')
    embed.add_field(name = '.help', value = 'Shows the commands', inline = False)
    embed.add_field(name = '.role [Role]', value = 'Adds a role to you. Check #info for role information', inline = False)
    embed.add_field(name = '.thanks [User]', value = 'Thanks the given user', inline = False)
    embed.add_field(name = '.urban [Search]', value = 'Searches Urban Dictionary for the search item', inline = False)
    embed.add_field(name = '.google [Search]', value = 'Searches Google for the search item', inline = False)

    await client.send_message(channel, embed=embed)

@client.command(pass_context = True)
async def role (ctx, role = ""):
  sender = ctx.message.author
  channel = ctx.message.channel
  server = ctx.message.server

  role = role.lower()

  explorer = discord.utils.get(server.roles, name="Explorer")
  rooftopper = discord.utils.get(server.roles, name="Rooftopper")
  photographer = discord.utils.get(server.roles, name="Photographer")

  if role == "":
    await client.send_message(channel, 'Please specify which role you want! (.roles)')
  elif role == "explorer":
    await client.add_roles(sender, explorer)
    await client.send_message(channel, "Cool! You're an explorer!")
  elif role == "rooftopper":
    await client.add_roles(sender, rooftopper)
    await client.send_message(channel, "Cool! You're a rooftopper!")
  elif role == "photographer":
    await client.add_roles(sender, photographer)
    await client.send_message(channel, "Cool! You're a photographer!")

@client.command(pass_context = True)
async def roles (ctx):
  sender = ctx.message.author
  channel = ctx.message.channel

  await client.send_message(channel, 'You can join these: Explorer, Rooftopper & Photographer')

@client.command(pass_context = True)
async def thanks (ctx, user : discord.Member = ""):
  sender = ctx.message.author
  channel = ctx.message.channel

  embed_success = discord.Embed(
    colour = discord.Colour.green()
  )

  embed_error = discord.Embed(
    colour = discord.Colour.red()
  )

  if user == "":
    embed_error.set_author(name = 'Error')
    embed_error.add_field(name = 'Specify', value = 'Please specify a user you want to thank!', inline = False)

    await client.send_message(channel, embed=embed_error)
  else:
    try:
      path = 'Users/' + user.name + '#' + user.discriminator + '/User File.json'
      userFile = open(path, 'r')
      data = json.load(userFile)
      userFile.close()

      tmp = data["thanks"]
      thanksCount = int(data["thanks"]) + 1
      data["thanks"] = thanksCount

      userFile = open(path, 'w+')
      userFile.write(json.dumps(data))
      userFile.close()

      embed_success.set_author(name = 'Success')
      embed_success.add_field(name = 'Thanked', value = 'You just thanked' + user.mention, inline = False)

      await client.send_message(channel, embed=embed_success)
    except:
      embed_error.set_author(name = 'Error')
      embed_error.add_field(name = 'Something went wrong..', value = 'Are you sure the user exists?', inline = False)

      await client.send_message(channel, embed=embed_error)

@client.command(pass_context = True)
async def urban (ctx, search = ""):
  sender = ctx.message.author
  channel = ctx.message.channel
  
  embed_success = discord.Embed(
    colour = discord.Colour.green()
  )

  embed_error = discord.Embed(
    colour = discord.Colour.red()
  )
  
  if search == "":
    embed_error.set_author(name = 'Error')
    embed_error.add_field(name = 'Specify', value = 'Please specify what you wanna search for!', inline = False)
    
    await client.send_message(channel, embed=embed_error)
  else:
    try:
      definitions = ud.define(search)
      
      definition = definitions[0]
      
      embed_success.set_author(name = 'We found a result')
      embed_success.add_field(name = 'Searched word:', value = definition.word, inline = False)
      embed_success.add_field(name = 'Definition:', value = definition.definition, inline = False)
      embed_success.add_field(name = 'Usage Example:', value = definition.example, inline = False)
      embed_success.add_field(name = 'Rating:', value = '👍{}   👎{}'.format(definition.upvotes, definition.downvotes), inline = False)

      await client.send_message(channel, embed=embed_success)
    except:
      embed_error.set_author(name = 'Error')
      embed_error.add_field(name = 'Something went wrong..', value = 'Please make sure you did everything correct!', inline = False)
      
      await client.send_message(channel, embed=embed_error)
      
# -- DEV COMMANDS (REMOVE WHEN RELEASE) --

@client.command(pass_context = True)
async def cuf (ctx, user : discord.Member = ""):
  sender = ctx.message.author
  channel = ctx.message.channel

  if user == "":
    await client.send_message(channel, 'Please specify a user you want to create the file for!')
  else:
    try:
      path = 'Users/' + user.name + '#' + user.discriminator
      os.makedirs(path)

      userFile(path, user)
    except:
      print('Didnt go as planned :/')

# -- OTHER --

def userFile (path, user : discord.Member):
  path = path + '/User File.json'

  os.makedirs(os.path.dirname(path), exist_ok=True)

  userFile = open(path, 'w')
  userFile.write("{\n")
  userFile.write('  "username": "' + user.name + '",\n')
  userFile.write('  "tag": "#' + user.discriminator + '",\n')
  userFile.write('  "thanks": "' + '0' + '"\n')
  userFile.write("}\n")
  userFile.close()

def userDataDelete (path, user : discord.Member):
  shutil.rmtree(path)

if __name__ == '__main__':
  client.run(TOKEN)
