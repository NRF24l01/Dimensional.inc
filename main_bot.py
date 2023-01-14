#Importing lib`s
import telebot
import sqlite3

#Import token, and name database
from config import token, data

#Import antimat funcktion
from antimat import is_mat

#Create bot
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["sendtopodcast"])
def send_pod(message):
    if is_mod(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте айди статьи которую хотите отправить в подкаст:")
        restat(message, "stp")
    else:
        bot.send_message(message.from_user.id, "Недостаточно прав")

@bot.message_handler(commands=["del"])
def del1(message):
    if is_mod(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте айди статьи которую хотите удалить:")
        restat(message, "del")
    else:
        bot.send_message(message.from_user.id, "Недостаточно прав")

@bot.message_handler(commands=["veri"])
def veri(message):
    if is_mod(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте айди пользователя которого хотите верифнуть :")
        restat(message, "veri")
    else:
        bot.send_message(message.from_user.id, "Недостаточно прав")

@bot.message_handler(commands=["wfor"])
def wread(message):
    ids = []
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        count = cursor.execute("SELECT COUNT(*) FROM To_mod").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error sql7: ", error)

    finally:
        if (conn):
            conn.close()
    print(count)
    for i in range(1, count+1):
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            count = cursor.execute("SELECT status FROM To_mod WHERE id ='"+str(i)+"'").fetchall()
            if len(count)==0:
                break
            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        if count == "mod":
            ids.append(i)
    print(ids)
    for i in ids:
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            id = i
            for1 = cursor.execute("SELECT for FROM To_mod WHERE id ='"+str(i)+"'").fetchall()[0][0]
            txt = cursor.execute("SELECT txt FROM To_mod WHERE id ='" + str(i) + "'").fetchall()[0][0]
            user = cursor.execute("SELECT autor FROM To_mod WHERE id ='" + str(i) + "'").fetchall()[0][0]
            print(id, for1, txt, user)

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        if for1 == "veri":
            bot.send_message(message.from_user.id,'id: '+str(id)+" Автор: "+ user+"""
"""+txt)

@bot.message_handler(commands=["rerules"])
def rerules(message):
    if is_mod(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте новые правила:")
        restat(message, "rerules")
    else:
        bot.send_message(message.from_user.id, "Недостаточно прав")

@bot.message_handler(commands=["rules"])
def rules(message):
    bot.send_message(message.from_user.id, get_rules())

@bot.message_handler(commands=["cawr"])
def cawr(message):
    bot.send_message(message.from_user.id,"Отлично. Отправте нам кратко о себе и мы её проверем.")
    restat(message, "cawr")

@bot.message_handler(commands=["wread"])
def wread(message):
    ids = []
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        count = cursor.execute("SELECT COUNT(*) FROM txt").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error sql7: ", error)

    finally:
        if (conn):
            conn.close()
    print(count)
    for i in range(1, count+1):
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            count = cursor.execute("SELECT status FROM txt WHERE id ='"+str(i)+"'").fetchall()[0][0]

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        if count != "ban":
            ids.append(i)
    print(ids)
    for i in ids:
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            id = i
            txt = cursor.execute("SELECT txt FROM txt WHERE id ='"+str(i)+"'").fetchall()[0][0]
            user = cursor.execute("SELECT autor FROM txt WHERE id ='" + str(i) + "'").fetchall()[0][0]

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        bot.send_message(message.from_user.id, 'id: '+str(id)+" Автор: "+ user+"""
"""+txt)


@bot.message_handler(commands=["sb"])
def cb(message):
    bot.send_message(message.from_user.id, "Отлично. Отправте нам ваш день рождения в формате ДД:ММ (пример: 31.01):")
    restat(message, "cb")

@bot.message_handler(commands=["new"])
def new(message):
    if is_verif(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте нам вашу статью:")
        restat(message, "write")
    else: bot.send_message(message.from_user.id, "Ты писатель без галочки.")

@bot.message_handler(commands=["start"])
def start(message, res=False):
    if is_new_us(message):
        new_user(message)
    bot.send_message(message.from_user.id, get_hello())

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.from_user.id, get_help())

@bot.message_handler(commands=["rehelp"])
def rehelp(message):
    if is_mod(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте новое сообщение поддержки:")
        restat(message, "rehelp")
    else:
        bot.send_message(message.from_user.id, "Недостаточно прав")

@bot.message_handler(commands=["restart"])
def rehelp(message):
    if is_mod(message):
        bot.send_message(message.from_user.id, "Отлично. Отправте новое приветствие:")
        restat(message, "restart")
    else:
        bot.send_message(message.from_user.id, "Недостаточно прав")

@bot.message_handler(content_types=["text"])
def text_handl(message):
    if what_st(message) == "rehelp":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            count = cursor.execute("UPDATE Tech SET txt='"+message.text+"' WHERE for = 'help'")

            count_m = count.fetchall()

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
        bot.send_message(message.from_user.id, "Новое сообшение подержки: "+get_help())
    elif what_st(message) == "restart":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            count = cursor.execute("UPDATE Tech SET txt='" + message.text + "' WHERE for = 'start'")

            count_m = count.fetchall()

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
        bot.send_message(message.from_user.id, "Новое приветствие: " + get_hello())
    elif what_st(message) == "write":
        if not is_mat(message.text):
            try:
                conn = sqlite3.connect(data)
                cursor = conn.cursor()

                cursor.execute("INSERT INTO txt (autor, us_id, txt, likes) VALUES ('"+str(message.from_user.username)+"', '"+str(message.from_user.id)+"', '"+message.text+"', '0')")

                conn.commit()

            except sqlite3.Error as error:
                print("Error sql10: ", error)

            finally:
                if (conn):
                    conn.close()
            restat(message, "none")
            bot.send_message(message.from_user.id, "Ваша статья: " + message.text)
        else:
            bot.send_message(message.from_user.id, "С плохими словами не принимаем!")
            restat(message, "none")
    elif what_st(message) == "cb":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("UPDATE Users SET birtsday_time='"+message.text+"' WHERE us_id ='"+str(message.from_user.id)+"'")

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql10: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
        bot.send_message(message.from_user.id, "Ваш др: " + message.text)
    elif what_st(message) == "cawr":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO To_mod (for, txt, status, autor) VALUES ('veri', '"+str(message.text)+"', 'mod', '"+str(message.from_user.id)+"')")

            conn.commit()

        except sqlite3.Error as error:
            print("Error sql10: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
        bot.send_message(message.from_user.id, "Ваша заявка принята: " + message.text)
    elif what_st(message) == "rerules":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("UPDATE Tech SET txt='" + message.text + "' WHERE for = 'rules'")
            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
        bot.send_message(message.from_user.id, "Ваша правка правил принята: " + get_rules())
    elif what_st(message) == "veri":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("UPDATE users SET verif='1' WHERE us_id = '"+ message.text +"'")
            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM To_mod WHERE autor = '"+ str(message.from_user.id) +"'")
            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
    elif what_st(message) == "del":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("UPDATE txt SET status='ban' WHERE id = '"+ message.text +"'")
            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")
    elif what_st(message) == "stp":
        try:
            conn = sqlite3.connect(data)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Podcast (type_task, txt_task, st_task, w_or_m) VALUES ('announcement', '"+str(message.text)+"', 'go', 'men')")
            conn.commit()

        except sqlite3.Error as error:
            print("Error sql7: ", error)

        finally:
            if (conn):
                conn.close()
        restat(message, "none")



def is_new_us(message):
    count_m = []
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        count = cursor.execute("SELECT hz FROM Users WHERE us_id == '" + str(message.from_user.id) + "'")

        count_m = count.fetchall()

        conn.commit()

    except sqlite3.Error as error:
        print("Error sql1: ", error)

    finally:
        if (conn):
            conn.close()
    if len(count_m) == 0:
        return True

def new_user(message):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Users (us_id, username, hz, created_txt, rangWR, rangRE, you_like, name, you_liked, verif) VALUES ('" + str(message.from_user.id) + "', '" +str(message.from_user.username) + "', '117', '0', 'макро', 'макро', '0', 'Человек с Земли', '0', '0')")
        # cursor.execute("INSERT INTO profiles (compleat_ideas, status, dt_st) VALUES ('0', 'NONE', 'NONE')")
        # resultee = str(current_datetime) + " " + message.from_user.username + " Предложил новую идею: '" + message.text + "'"
        # print(resultee)

        conn.commit()
    except sqlite3.Error as error:
        print("Error sql2: ", error)

    finally:
        if (conn):
            conn.close()

def get_hello():
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT txt FROM Tech WHERE for == 'start'")

        txt = txt.fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error sql3: ", error)
        txt = "Error sql3: "+ str(error)

    finally:
        if (conn):
            conn.close()
    return txt

def get_help():
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT txt FROM Tech WHERE for == 'help'")

        txt = txt.fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error sql3: ", error)
        txt = "Error sql3: "+ str(error)

    finally:
        if (conn):
            conn.close()
    return txt

def is_owner(message):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT rangWR FROM Users WHERE us_id == '" + str(message.from_user.id) + "'").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error4: ", error)

    finally:
        if (conn):
            conn.close()
    if txt == "OWNER":
        return True
    else:
        return False

def is_mod(message):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT rangWR FROM Users WHERE us_id == '" + str(message.from_user.id) + "'").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error5: ", error)

    finally:
        if (conn):
            conn.close()
    if txt == "MOD" or is_owner(message):
        return True
    else:
        return False

def restat(message, txt):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        cursor.execute("UPDATE Users SET status='"+txt+"'  WHERE us_id == '" + str(message.from_user.id) + "'")

        conn.commit()

    except sqlite3.Error as error:
        print("Error6: ", error)

    finally:
        if (conn):
            conn.close()

def what_st(message):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT status FROM Users  WHERE us_id == '" + str(message.from_user.id) + "'").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error7: ", error)

    finally:
        if (conn):
            conn.close()
    return txt

def is_verif(message):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT verif FROM Users  WHERE us_id == '" + str(message.from_user.id) + "'").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error7: ", error)

    finally:
        if (conn):
            conn.close()
    if txt == "1": return True
    else: return False

def restat(message, txt):
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        cursor.execute("UPDATE Users SET status='"+txt+"'  WHERE us_id == '" + str(message.from_user.id) + "'")

        conn.commit()

    except sqlite3.Error as error:
        print("Error6: ", error)

    finally:
        if (conn):
            conn.close()

def get_rules():
    try:
        conn = sqlite3.connect(data)
        cursor = conn.cursor()

        txt = cursor.execute("SELECT txt FROM Tech WHERE for == 'rules'")

        txt = txt.fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error sql3: ", error)
        txt = "Error sql3: "+ str(error)

    finally:
        if (conn):
            conn.close()
    return txt

#Run, without stop
bot.polling(none_stop=True)