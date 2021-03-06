import os, logging, asyncio
from telethon.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**๐'๐ฆ ๐sแดษดแดสแด แดแดษดแดษชแดษด สแดแด**, ๐ข ๐๐๐ง ๐๐๐ง๐ญ๐ข๐จ๐ง ๐๐ฅ๐ฅ ๐๐๐ฆ๐๐๐ซ๐ฌ ๐๐ง ๐๐ซ๐จ๐ฎ๐ฉ ๐๐ซ ๐๐ก๐๐ง๐ง๐๐ฅ ๐ป\n๐๐ฅ๐ข๐๐ค **/help** ๐๐จ๐ซ ๐๐จ๐ซ๐ ๐๐ง๐๐จ๐ซ๐ฆ๐๐ญ๐ข๐จ๐ง__\n\n ๐๐จ๐ฅ๐ฅ๐จ๐ฐ [sแดษดแดสแดsส](https://t.me/santhu_music_bot) แดษด แดแดสแดษขสแดแด",
    link_preview=False, 
    buttons=(  
      [
                [
                    InlineKeyboardButton(
                        "๐แดสสแด ษดษช แดแดแด แดสแดsแดแดแดษดแดษช๐", url="https://t.me/Santhugroupmentionbot?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                        "โน๏ธแดแดกษดแดส๐", url="https://t.me/santhu_music_bot"
                    ),
                    InlineKeyboardButton(
                        "๐ษขสแดแดแด๐", url="https://t.me/santhuvc"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "๐ษดแดแดแดกแดสแด๐", url="https://t.me/santhubotupadates"
                    )]
            ]
       ),
    )
    
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of ๐sแดษดแดสแดsส แดแดษดแดษชแดษด สแดแด**\n\nCommand: @all\n__You can use this command with text what you want to mention others.__\nExample: `@all Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nFollow [sแดษดแดสแดsส](https://youtube.com/channel/UC7QMr8IDR65vciXrwx4XLiQ) สแดแดแดแดสแด "
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('๐แดแดกษดแดส๐ป', 'https://t.me/santhu_music_bot'),
        Button.url('๐ษดแดแดแดกแดสแด๐', 'https://t.me/santhuvc')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^@all ?(.*)"))
async def all(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command Can Be Use In Groups And Channels @santhuvc !__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only Admins Can Mention All\n\nFor More Go On @santhuvc !__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I Can't Mention Members For Older Messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply To a Message Or Give Me Some Text To Mention Others\n\nMade bY  [sแดษดแดสแดsส](https://youtube.com/channel/UC7QMr8IDR65vciXrwx4XLiQ) !__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}\n\nMade bY  [sแดษดแดสแดsส](https://youtube.com/channel/UC7QMr8IDR65vciXrwx4XLiQ)"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There Is No Proccess On Going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__แดแดษดแดษชแดษด แดแดษดแดแดสโ แดสแดsแด สแด ษดษชสสแด ๐.__')

print(">> ๐sแดษดแดสแด แดแดษดแดษชแดษด สแดแด<<")
client.run_until_disconnected()
