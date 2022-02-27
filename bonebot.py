
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import json
import requests
import os
TOKEN = os.environ.get('TOKEN')

updater = Updater(TOKEN, use_context=True)

bone_types_raw = []
bone_types_raw.extend(["Shoulder Joint (2)"]*2)
bone_types_raw.extend(["Humerus (2)"]*2)
bone_types_raw.extend(["Vertebrae (6)"]*6)
bone_types_raw.extend(["Sternum (1)"]*1)
bone_types_raw.extend(["Rib 3 - Right (1)"]*1)
bone_types_raw.extend(["Rib 3 - Left (1)"]*1)
bone_types_raw.extend(["Rib 2 - Right (1)"]*1)
bone_types_raw.extend(["Rib 2 - Left (1)"]*1)
bone_types_raw.extend(["Rib 1 - Right (1)"]*1)
bone_types_raw.extend(["Rib 1 - Left (1)"]*1)
bone_types_raw.extend(["Clavicle - Right (1)"]*1)
bone_types_raw.extend(["Clavicle - Left (1)"]*1)
bone_types_raw.extend(["Nasal Bone (1)"]*1)
bone_types_raw.extend(["Maxilla Bone - Left (1)"]*1)
bone_types_raw.extend(["Maxilla Bone - Right (1)"]*1)
bone_types_raw.extend(["Mandible (1)"]*1)
bone_types_raw.extend(["Lower Teeth (1)"]*1)
bone_types_raw.extend(["Upper Teeth (1)"]*1)
bone_types_raw.extend(["Zygomatic Bone - Right (1)"]*1)
bone_types_raw.extend(["Zygomatic Bone - Left (1)"]*1)
bone_types_raw.extend(["Temporal Bone (1)"]*1)
bone_types_raw.extend(["Sphenoid Bone (2)"]*2)
bone_types_raw.extend(["Frontal Bone (1)"]*1)
bone_types_raw.extend(["Parietal Bone (1)"]*1)



def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi! My name is Bertrand Bones. I can show you what bones you need to get a custom! NYEEEEH")

def bones(update: Update, context: CallbackContext):
    bones_needed = bone_types_raw.copy()
    walletstrip = update.message.text
    wallet = walletstrip.replace("/bones ", "")
    reqstr = "https://proton.api.atomicassets.io/atomicassets/v1/assets?collection_name=221321151252&owner="+wallet+"&page=1&limit=100&order=desc&sort=asset_id"
    r = requests.get(reqstr)
    bonecontent = json.loads(r.content.decode())
    refined = bonecontent["data"]
    for i in refined:
        removable = i["name"]
        if removable in bones_needed:
            bones_needed.remove(removable)
    
    formattedmessage = "Here is an overview of the bones you still need: "
    for item in set(bones_needed):
        formattedmessage += "\n"
        formattedmessage += item.split(" (")[0]
        formattedmessage += ": " + str(bones_needed.count(item))
    
    update.message.reply_text(formattedmessage)

def holding(update: Update, context: CallbackContext):
    bones_held = []
    walletstrip = update.message.text
    wallet = walletstrip.replace("/holding ", "")
    reqstr = "https://proton.api.atomicassets.io/atomicassets/v1/assets?collection_name=221321151252&owner="+wallet+"&page=1&limit=100&order=desc&sort=asset_id"
    r = requests.get(reqstr)
    bonecontent = json.loads(r.content.decode())
    refined = bonecontent["data"]
    for i in refined:
        bone = i["name"]
        bones_held.append(bone)

    
    formattedmessage = "These are the bones you own: "
    for item in set(bones_held):
        formattedmessage += "\n"
        formattedmessage += item.split(" (")[0]
        formattedmessage += ": " + str(bones_held.count(item))
    
    update.message.reply_text(formattedmessage)

def help(update: Update, context: CallbackContext):
    update.message.reply_text("Find out how many bones you need like so: /bones [wallet] \n\nYou can also check the bones you own by using: /holding [wallet]")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('bones', bones))
updater.dispatcher.add_handler(CommandHandler('holding', holding))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
  
updater.start_polling()
