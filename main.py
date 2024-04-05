import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import databases
import pytz
from datetime import datetime

databases.creat_database_tables()

TOKEN ='6598066482:AAGWDZFzYKqZw3rOCKieOkoNQ2vBDntNVuU'

uid_for_send_message=0
status="off"
admin=6555370485
chanel_id=-1002138408979
chanel_info_id=-1002027679857
dict_country_mid={"آمریکا":[3,4],"روسیه":[5,6], "چین":[7,8] ,"ژاپن":[9,10] ,"هند":[11,12] ,"فرانسه":[13,14],"کره جنوبی":[15,16],"ایتالیا":[17,18], "پاکستان":[19,20] ,"مصر":[21,22] ,"المان":[23,24] , "کانادا":[25,26] ,"استرالیا":[27,28], "ایران":[29,30] ,"عراق":[31,32] ,"اسرائیل":[33,34] ,"لبنان":[35,36] ,"عربستان":[37,38] ,"ترکیه":[39,40] ,"فلسطین":[41,42] ,"برزیل":[45,46] ,"اسپانیا":[43,44] ,"انگلیس":[47,48] ,"اوکراین":[49,50], "افغانستان":[51,52] ,"قزاقستان":[53,54], "سوریه":[55,56] ,"کره شمالی":[57,58]}#{country_name:[mid]}
userStep={}
list_country=["آمریکا","روسیه", "چین" ,"ژاپن" ,"هند" ,"فرانسه" ,"کره جنوبی","ایتالیا", "پاکستان" ,"مصر" ,"المان" , "کانادا" ,"استرالیا", "ایران" ,"عراق" ,"اسرائیل" ,"لبنان" ,"عربستان" ,"تورکیه" ,"فلسطین" ,"برزیل" ,"اسپانیا" ,"انگلیس" ,"اوکراین", "افغانستان" ,"قزاقستان", "سوریه" ,"کره شمالی"]
list_country_selecting=[]
dict_cid_countryname={}#{cid:cuntry}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0

def is_user_member(user_id, channel_id):
    try:
        chat_member = bot.get_chat_member(channel_id, user_id)
        return chat_member.status == "member" or chat_member.status == "administrator" or chat_member.status == "creator"
    except Exception as e:
        #print(f"Error checking membership: {e}")
        return False

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m)
        cid = m.chat.id
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + "New photo recieved")
        elif m.content_type == 'document':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + 'New Document recieved')

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.callback_query_handler(func=lambda call: call.data.startswith("start"))
def call_callback_data(call):
    global status
    cid = call.message.chat.id
    mid = call.message.message_id
    status="on"
    for i in dict_cid_countryname:
        bot.send_message(i,"بازیکن عزیز بازی شروع شد")
    markup=InlineKeyboardMarkup()
    if status=="off":
        markup.add(InlineKeyboardButton("شروع بازی",callback_data="start"))
    elif status=="on":
        markup.add(InlineKeyboardButton("پایان بازی",callback_data="stop"))
    markup.add(InlineKeyboardButton("مشاهده و تنظیمات بازیکنان",callback_data="show"))
    markup.add(InlineKeyboardButton('آمار تمامی کاربران',callback_data='panel_amar'))
    markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='panel_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='panel_forall'))

    bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    bot.answer_callback_query(call.id,"بازی شروع شد")

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("پایان بازی",callback_data="sstop"),InlineKeyboardButton("لغو",callback_data="back_panel"))
    bot.edit_message_text("آیا از پایان بازی اطمینان دارید؟",cid,mid,reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith("sstop"))
def call_callback_data(call):
    global status
    global list_country_selecting
    global dict_cid_countryname
    cid = call.message.chat.id
    mid = call.message.message_id
    list_country_selecting=[]
    
    status="off"
    for i in dict_cid_countryname:
        bot.send_message(i,"بازیکن عزیز بازی به پایان رسید ")
        bot.send_message(i,"برای شرکت در بازی بعدی /start را بزنید")
    dict_cid_countryname={}
    bot.delete_message(cid,mid)
    markup=InlineKeyboardMarkup()
    if status=="off":
        markup.add(InlineKeyboardButton("شروع بازی",callback_data="start"))
    elif status=="on":
        markup.add(InlineKeyboardButton("پایان بازی",callback_data="stop"))
    markup.add(InlineKeyboardButton("مشاهده و تنظیمات بازیکنان",callback_data="show"))
    markup.add(InlineKeyboardButton('آمار تمامی کاربران',callback_data='panel_amar'))
    markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='panel_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='panel_forall'))
    bot.send_message(cid,"پنل ادمین",reply_markup=markup)
    bot.answer_callback_query(call.id,"بازی به پایان رسید ")

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def def_delete(call):
    global list_country_selecting
    cid = call.message.chat.id
    mid = call.message.message_id
    uid=int(call.data.split("_")[1])
    bot.send_message(chanel_id,f"کشور '{dict_cid_countryname[uid]}' از بازی حذف شد")
    print(list_country_selecting)
    list_country_selecting.remove(dict_cid_countryname[uid])
    print(list_country_selecting)
    dict_cid_countryname.pop(uid)
    bot.delete_message(cid,mid)
    bot.send_message(uid,"شما از بازی حذف شدید")
    bot.answer_callback_query(call.id,"بازیکن حذف شد")

@bot.callback_query_handler(func=lambda call: call.data.startswith("sends"))
def call_callback_panel_sends(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")  
    count=0  
    count_black=0
    if data[1] =="brodcast":
        list_user=databases.use_users()
        for i in list_user:
            try:
                bot.copy_message(i,cid,int(data[-1]))
                count+=1
            except:
                databases.delete_users(i)
                count_black+=1
                # print("eror")
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
        text=f"به {count} نفر ارسال شد"
        if count_black!=0:
            text=f"\n و به {count_black} نفر ارسال نشد احتمالا ربات را بلاک کرده اند و از دیتابیس ما حذف میشوند \n"
        bot.edit_message_text(text,cid,mid,reply_markup=markup)
    if data[1] =="forall":
        list_user=databases.use_users()
        for i in list_user:
            try:
                bot.forward_message(i,cid,int(data[-1]))
                count+=1
            except:
                databases.delete_users(i)
                count_black+=1
                # print("eror")
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
        text=f"به {count} نفر ارسال شد"
        if count_black!=0:
            text=f"\n و به {count_black} نفر ارسال نشد احتمالا ربات را بلاک کرده اند و از دیتابیس ما حذف میشوند \n"
        bot.edit_message_text(text,cid,mid,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("send"))
def def_delete(call):
    global uid_for_send_message
    cid = call.message.chat.id
    mid = call.message.message_id
    uid=int(call.data.split("_")[1])  
    uid_for_send_message=uid
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
    bot.send_message(cid,"لطفا برای ارسال پیام به کاربر پیام خود را ارسال کنید:",reply_markup=markup)
    userStep[cid]=10

@bot.callback_query_handler(func=lambda call: call.data.startswith("select"))
def def_admin_change(call):
    global list_country_selecting
    cid = call.message.chat.id
    mid = call.message.message_id
    uid=int(call.data.split("_")[1])
    country_name_new= call.data.split("_")[2]
    bot.delete_message(cid,mid)
    list_country_selecting.remove(dict_cid_countryname[uid])
    list_country_selecting.append(country_name_new)
    dict_cid_countryname[uid]=country_name_new
    list_mid_info=dict_country_mid[country_name_new]
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")
    markup.add("ارتباط با ادمین👤")
    bot.send_message(uid,"🔴کشور شما توسط ادمین تغییر کرد")
    bot.copy_message(uid,chanel_info_id,60)
    for i in list_mid_info:
        bot.copy_message(uid,chanel_info_id,i)
    bot.send_message(uid,"برای بازی از دکمه های زیر استفاده کنید",reply_markup=markup) 
    bot.send_message(cid,"کشور بازیکن تغییر کرد")   


@bot.callback_query_handler(func=lambda call: call.data.startswith("change"))
def def_admin_change(call):
    global list_country_selecting
    cid = call.message.chat.id
    mid = call.message.message_id
    uid=int(call.data.split("_")[1])  
    markup=InlineKeyboardMarkup()
    list_markup=[]
    for i in list_country:
        
        if i not in list_country_selecting:
            list_markup.append(InlineKeyboardButton(i,callback_data=f"select_{uid}_{i}"))
    markup.add(*list_markup)
    markup.add(InlineKeyboardButton("لغو و بازگشت به پنل",callback_data="back_panel"))
    bot.send_message(cid,"کشور جدید بازیکن را انتخاب کنید",reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("show"))
def def_admin(call):
    global list_country_selecting
    cid = call.message.chat.id
    mid = call.message.message_id
    if len(dict_cid_countryname)==0:
        bot.answer_callback_query(call.id,"فعلا بازیکنی وجود ندارد")
        return
    for i in dict_cid_countryname:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("حذف بازیکن",callback_data=f"delete_{i}"))
        markup.add(InlineKeyboardButton("تغییر کشور بازیکن",callback_data=f"change_{i}"))
        markup.add(InlineKeyboardButton("ارسال پیام به بازیکن",callback_data=f"send_{i}"))
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
        bot.send_message(cid,f"""
آی دی عددی کاربر:{i}
کشور :{dict_cid_countryname[i]}
""",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
def call_callback_panel_amar(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    bot.delete_message(cid,mid)
    userStep[cid]=0
    markup=InlineKeyboardMarkup()
    if status=="off":
        markup.add(InlineKeyboardButton("شروع بازی",callback_data="start"))
    elif status=="on":
        markup.add(InlineKeyboardButton("پایان بازی",callback_data="stop"))
    markup.add(InlineKeyboardButton("مشاهده و تنظیمات بازیکنان",callback_data="show"))
    markup.add(InlineKeyboardButton('آمار تمامی کاربران',callback_data='panel_amar'))
    markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='panel_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='panel_forall'))
    bot.send_message(cid,"""
برای مدیریت بازی از دکمه های زیر استفاده کنید
""",reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("barresi"))
def def_barresi(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    command_start(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("panel"))
def call_callback_panel_amar(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")[-1]
    countOfUsers=len(databases.use_users())
    if countOfUsers>0:
        if data=="amar":
            countOfUsers=len(databases.use_users())
            txt = f'آمار کاربران: {countOfUsers} نفر '
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
            bot.edit_message_text(txt,cid,mid,reply_markup=markup)
        elif data=="brodcast":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
            bot.edit_message_text("برای ارسال همگانی پیام لطفا پیام خود را ارسال کنید و در غیر این صورت برای بازگشت به پنل از دکمه زیر استفاده کنید",cid,mid,reply_markup=markup)
            userStep[cid]=11
        elif data=="forall":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
            bot.edit_message_text("برای فوروارد همگانی پیام لطفا پیام خود را ارسال کنید و در غیر این صورت برای بازگشت به پنل از دکمه زیر استفاده کنید",cid,mid,reply_markup=markup)
            userStep[cid]=12
    else:
        bot.answer_callback_query(call.id,"هنوز کاربری وجود ندارد")

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid != admin:
        databases.insert_users(cid)
    fname=m.chat.first_name
    userStep[cid]=0
    if cid == admin:
        markup=InlineKeyboardMarkup()
        if status=="off":
            markup.add(InlineKeyboardButton("شروع بازی",callback_data="start"))
        elif status=="on":
            markup.add(InlineKeyboardButton("پایان بازی",callback_data="stop"))
        markup.add(InlineKeyboardButton("مشاهده و تنظیمات بازیکنان",callback_data="show"))
        markup.add(InlineKeyboardButton('آمار تمامی کاربران',callback_data='panel_amar'))
        markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='panel_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='panel_forall'))
        bot.send_message(cid,"""
سلام ادمین گرامی 
برای مدیریت بازی از دکمه های زیر استفاده کنید
""",reply_markup=markup)
    else:
        if is_user_member(cid ,chanel_id) :
            if cid not in dict_cid_countryname:
                if status=="off":
                    markup=ReplyKeyboardMarkup()
                    list_markup=[]
                    for i in list_country:
                        if i not in list_country_selecting:
                            list_markup.append(i)
                    markup.add(*list_markup)
                    bot.send_message(cid,"لطفا برای شروع بازی کشور مورد نظر خود را انتخاب کنید",reply_markup=markup)
                else:
                    bot.send_message(cid,"""
شما نمیتوانید عضو  بازی شوید 🚫

بازی درحال برگزاری است☢️

اطلاعات بیشتر⬇️

                                 @game_war_smokey
""")
            else:
                markup=ReplyKeyboardMarkup()
                markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
                markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
                markup.add("خرید یورو🛍️")  
                markup.add("ارتباط با ادمین👤")
                bot.send_message(cid,"شما قبلا کشور خود را انتخاب کرده اید",reply_markup=markup)
        else:
            markup=InlineKeyboardMarkup() 
            markup.add(InlineKeyboardButton("کانال بازی",url="https://t.me/game_war_smokey"))
            markup.add(InlineKeyboardButton("گروه بازی",url="https://t.me/+M1lWxTZxKC05Mzk8"))
            markup.add(InlineKeyboardButton("بررسی",callback_data="barresi")) 
            # markup.add(InlineKeyboardButton("کانال",url="https://t.me/+37s4G1zPx5E1YTlk")) # https://t.me/game_war_smokey
            bot.send_message(cid,f"""
سلام {fname} عزیز
به ربات بازی خوش آمدید 
برای  شروع بازی لطفا در کانال زیر عضو شوید
""",reply_markup=markup)


@bot.message_handler(func=lambda m: m.text=="لغو و بازگشت به منو")
def menu(m):
    cid = m.chat.id
    text=m.text
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    bot.send_message(cid,"برای بازی از دکمه های زیر استفاده کنید",reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="ارتباط با ادمین👤" or m.text=="خرید زیرساخت و تجاری🏗️" or m.text=="خرید نظامی 🪖" or m.text=="بیانیه کشور🗺️" or m.text=="اختراعات و سناریو📝" or m.text=="خرید یورو🛍️"  )
def ability(m):
    cid = m.chat.id
    text=m.text
    if text=="ارتباط با ادمین👤":
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("لغو و بازگشت به منو")
        bot.send_message(cid,"لطفا پیام خود را ارسال کنید:",reply_markup=markup)
        userStep[cid]=6
        return
    elif text=="اختراعات و سناریو📝":
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("لغو و بازگشت به منو")
        bot.send_message(cid,"اختراع یا سناریو مورد نظرتان را وارد کنید",reply_markup=markup)
        userStep[cid]=4
        return
    elif text=="خرید یورو🛍️":
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("لغو و بازگشت به منو")
        bot.send_message(cid,"قیمت هر 3000 میلیون یورو 100 هزار تومان \n برای اطلاعات بیشتر و خرید پیام خود را ارسال کنید (پیام شما برای ادمین ارسال میشود)",reply_markup=markup)
        userStep[cid]=5
        return
    if status=="on":
        tz = pytz.timezone('Asia/Tehran')
        now = datetime.now(tz)
        start_time = now.replace(hour=16, minute=0, second=0, microsecond=0)  # 4 PM
        end_time = now.replace(hour=20, minute=0, second=0, microsecond=0) 
        if text=="خرید زیرساخت و تجاری🏗️":
            if start_time <= now <= end_time:
                markup=ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("لغو و بازگشت به منو")
                bot.send_message(cid,"لطفا نام ، تعداد و قیمت زیر ساختی را که میخواهید خریداری کنید ارسال کنید",reply_markup=markup)
                userStep[cid]=1
            else:
                bot.send_message(cid,"این قابلیت فقط از 4 ظهر تا 9 شب فعال است")
        elif text=="خرید نظامی 🪖":
            if start_time <= now <= end_time:
                markup=ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("لغو و بازگشت به منو")
                bot.send_message(cid,"لطفا نام وسیله نظامی, تعداد و قیمت را ارسال کنید",reply_markup=markup)
                userStep[cid]=2
            else:
                bot.send_message(cid,"این قابلیت فقط از 4 ظهر تا 9 شب فعال است")
        elif text=="بیانیه کشور🗺️":
            if start_time <= now <= end_time:   
                markup=ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("لغو و بازگشت به منو")
                bot.send_message(cid,"هر بیانیه  که میخاهید با کشور های دیگر در میان بگذارید را باید اینجا ارسال کنید",reply_markup=markup)
                userStep[cid]=3
            else:
                bot.send_message(cid,"این قابلیت فقط از 4 ظهر تا 9 شب فعال است")
        # elif text=="اختراعات و سناریو📝":
        #     markup=ReplyKeyboardMarkup(resize_keyboard=True)
        #     markup.add("لغو و بازگشت به منو")
        #     bot.send_message(cid,"لطفا اختراع خود را ارسال کنید",reply_markup=markup)
        #     userStep[cid]=4
        # elif text=="خرید یورو🛍️":
        #     markup=ReplyKeyboardMarkup(resize_keyboard=True)
        #     markup.add("لغو و بازگشت به منو")
        #     bot.send_message(cid,"قیمت هر 3000 میلیون یورو 100 هزار تومان \n برای اطلاعات بیشتر و خرید پیام خود را ارسال کنید (پیام شما برای ادمین ارسال میشود)",reply_markup=markup)
        #     userStep[cid]=5
        # elif text=="ارتباط با ادمین👤":
        #     markup=ReplyKeyboardMarkup(resize_keyboard=True)
        #     markup.add("لغو و بازگشت به منو")
        #     bot.send_message(cid,"لطفا پیام خود را ارسال کنید:",reply_markup=markup)
        #     userStep[cid]=6
    else:
        bot.send_message(cid,"برای استفاده از این قابلیت ها باید صبر کنید که بازی شروع شود در صورت شروع بازی برای شما پیام ارسال میشود")

# @bot.message_handler(content_types=['photo','video',"video_note","audio","voice","document","sticker","location","contact","text"])
# def panel_set_photo(m):
#     global userstep
#     cid = m.chat.id
#     mid = m.message_id
#     if m.chat.type=="private":
#         if get_user_step(m.chat.id)==1:

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def send_music(m):
    cid=m.chat.id
    text=m.text
    print(m)
    bot.send_message(chanel_id,f"""
#{dict_cid_countryname[cid]}
*خرید زیرساخت و تجاری🏗️*
- - - - - - - - - - - - - - - - - -
{text}
""")
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    userStep[cid]=0
    bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==2)
def send_music(m):
    cid=m.chat.id
    text=m.text
    bot.send_message(chanel_id,f"""
#{dict_cid_countryname[cid]}
*خرید نظامی 🪖*
- - - - - - - - - - - - - - - - - -
{text}
""")
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    userStep[cid]=0
    bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)    

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==3)
def send_music(m):
    cid=m.chat.id
    text=m.text
    bot.send_message(chanel_id,f"""
#{dict_cid_countryname[cid]}


{text}
""")
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    userStep[cid]=0
    bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==4)
def send_music(m):
    cid=m.chat.id
    text=m.text
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ارسال پیام به کاربر",callback_data=f"send_{cid}"))
    bot.send_message(admin,f"""
#{dict_cid_countryname[cid]}
آی دی بازیکن:@{m.from_user.username}
نام بازیکن : {m.chat.first_name}
*اختراعات و سناریو📝*
- - - - - - - - - - - - - - - - - -
{text}
""",reply_markup=markup)
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    userStep[cid]=0
    bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==5)
def send_music(m):
    cid=m.chat.id
    text=m.text
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ارسال پیام به کاربر",callback_data=f"send_{cid}"))
    bot.send_message(admin,f"""
#{dict_cid_countryname[cid]}
آی دی بازیکن:@{m.from_user.username}
نام بازیکن : {m.chat.first_name}
*خرید یورو🛍️*
- - - - - - - - - - - - - - - - - -
{text}
""",reply_markup=markup)
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    userStep[cid]=0
    bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==6)
def send_music(m):
    cid=m.chat.id
    text=m.text
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ارسال پیام به کاربر",callback_data=f"send_{cid}"))
    bot.send_message(admin,f"""
#{dict_cid_countryname[cid]}
آی دی بازیکن:@{m.from_user.username}
نام بازیکن : {m.chat.first_name}
*ارتباط با ادمین👤
- - - - - - - - - - - - - - - - - -
{text}
""",reply_markup=markup)
    markup=ReplyKeyboardMarkup()
    markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
    markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
    markup.add("خرید یورو🛍️")  
    markup.add("ارتباط با ادمین👤")
    userStep[cid]=0
    bot.send_message(cid,"پیام شما با موفقیت  برای ادمین ارسال شد و تا چند دقیقه دیگر برسی میشود",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==10)
def send_music(m):
    cid=m.chat.id
    text=m.text
    bot.send_message(uid_for_send_message,'🔴 پیام از طرف ادمین👇')
    bot.send_message(uid_for_send_message,text)
    userStep[cid]=0
    bot.send_message(cid,"پیام برای کاربر ارسال شد")

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==11)
def send_music(m):
    cid=m.chat.id
    text=m.text
    if m.chat.type == 'private':
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید",callback_data=f"sends_brodcast_{m.message_id}"))
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
        bot.send_message(cid,"پیام شما دریافت شد برای ارسال همگانی تایید را بزنید",reply_markup=markup)
        userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==12)
def send_music(m):
    cid=m.chat.id
    text=m.text
    if m.chat.type == 'private':
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید",callback_data=f"sends_brodcast_{m.message_id}"))
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="back_panel"))
        bot.send_message(cid,"پیام شما دریافت شد برای فوروارد همگانی تایید را بزنید",reply_markup=markup)
        userStep[cid]=0

@bot.message_handler(content_types=['photo'])
def panel_set_photo(m):
    cid = m.chat.id
    mid = m.message_id
    if m.chat.type=="private":
        caption=m.caption
        photo_id=m.photo[-1].file_id
        print(photo_id)
        print(get_user_step(m.chat.id))
        if get_user_step(m.chat.id)==1:
            bot.send_photo(chanel_id,photo_id,f"""
#{dict_cid_countryname[cid]}
*خرید زیرساخت و تجاری🏗️*
- - - - - - - - - - - - - - - - - -
{caption}
""")
            markup=ReplyKeyboardMarkup()
            markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
            markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
            markup.add("خرید یورو🛍️")  
            markup.add("ارتباط با ادمین👤")
            userStep[cid]=0
            bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

        elif get_user_step(m.chat.id)==2:
            bot.send_photo(chanel_id,photo_id,f"""
#{dict_cid_countryname[cid]}
*خرید نظامی 🪖*
- - - - - - - - - - - - - - - - - -
{caption}
""")
            markup=ReplyKeyboardMarkup()
            markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
            markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
            markup.add("خرید یورو🛍️")  
            markup.add("ارتباط با ادمین👤")
            userStep[cid]=0
            bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

        elif get_user_step(m.chat.id)==3:
            bot.send_photo(chanel_id,photo_id,f"""
#{dict_cid_countryname[cid]}

{caption}
""")
            markup=ReplyKeyboardMarkup()
            markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
            markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
            markup.add("خرید یورو🛍️")  
            markup.add("ارتباط با ادمین👤")
            userStep[cid]=0
            bot.send_message(cid,"پیام شما با موفقیت ارسال شد",reply_markup=markup)

@bot.message_handler(func=lambda m: True )
def country(m):
    cid = m.chat.id
    country_name=m.text
    if m.chat.type == 'private':
        if country_name in list_country:
            if cid not in dict_cid_countryname:
                # list_country.remove(country_name)
                list_country_selecting.append(country_name)
                dict_cid_countryname.setdefault(cid,country_name)
                list_mid_info=dict_country_mid[country_name]
                markup=ReplyKeyboardMarkup()
                markup.add("خرید زیرساخت و تجاری🏗️","خرید نظامی 🪖")
                markup.add("بیانیه کشور🗺️","اختراعات و سناریو📝")
                markup.add("خرید یورو🛍️")  
                markup.add("ارتباط با ادمین👤")
                image=bot.copy_message(cid,chanel_info_id,60)
                for i in list_mid_info:
                    bot.copy_message(cid,chanel_info_id,i)
                bot.send_message(cid,"کشور شما تایید شد ، صبر کنید بازی از طرف ادمین شروع بشه🗺️",reply_markup=markup)
            else:
                bot.send_message(cid,"شما قبلا کشور خود را انتخاب کرده اید")
        else:
            bot.send_message(cid,"مقدار وارد شده نامعتبر است")




bot.infinity_polling()
