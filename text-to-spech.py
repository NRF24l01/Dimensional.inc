#Importing libraries
import os
import torch
import random
import sqlite3
import time

#Setting up silero (text-to-speech library)
speakers_men = ['aidar','eugene']
speakers_women = ['kseniya','xenia','baya']

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)
sample_rate = 48000

#This is an example of saving a file
#audio_paths = model.save_wav(text=example_text,
#                             speaker=speaker,
#                             sample_rate=sample_rate,
#                             audio_path='eugene.wav')

# Main loop
while True:
    #print(time.strftime('%m.%d.%Y'))

    # Checking birthdays! :D
    if time.strftime('%H:%M') == '00:00':
        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            # Getting all the users that have their birthday today
            bd_bd = cursor.execute('SELECT name FROM Users WHERE birtsday_time="' + time.strftime('%m.%d') + '"')

            bd_bd = bd_bd.fetchall()

            # Making congratulations
            text = 'РЎРµРіРѕРґРЅСЏ РјС‹ РїРѕР·РґСЂР°РІР»СЏРµРј СЃ РґРЅС‘Рј СЂРѕР¶РґРµРЅРёСЏ СЃР»РµРґСѓСЋС‰РёС… СѓС‡РµРЅРёРєРѕРІ. ' + str(
                bd_bd) + 'Р–РµР»Р°РµРј РІСЃРµРј РІСЃРµРіРѕ РЅР°РёР»СѓС‡С€РµРіРѕ!'

            model.save_wav(text=text,
                           speaker='random',
                           sample_rate=sample_rate,
                           audio_path='congrats_' + str(time.strftime('%m_%d_%y')) + '.wav')

            # This is just because I'm too lazy to check if a congratulation file is already exists ;)
            time.sleep(61)



        except sqlite3.Error as error:
            print("Error in bds", error)

        finally:
            if (conn):
                conn.close()


    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Getting the first task ID of current tasks
        id_bd = cursor.execute('SELECT id FROM Podcast WHERE st_task="go"')

        id_bd = id_bd.fetchall()
        if len(id_bd) == 0:
            continue
        else:
            id_bd = id_bd[0][0]

    except sqlite3.Error as error:
        print("Error in 1", error)

    finally:
        if (conn):
            conn.close()




    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Getting the type of the task
        typetask_bd = cursor.execute('SELECT type_task FROM Podcast WHERE id=' + str(id_bd))

        typetask_bd = typetask_bd.fetchall()[0][0]

        # print(txt)

    except sqlite3.Error as error:
        print("Error in 2", error)

    finally:
        if (conn):
            conn.close()

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Getting and editing the text to pronounce
        text_bd = cursor.execute('SELECT txt_task FROM Podcast WHERE id=' + str(id_bd))

        text_bd = text_bd.fetchall()[0][0]

        # print(txt)

    except sqlite3.Error as error:
        print("Error in 3", error)

    finally:
        if (conn):
            conn.close()

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Getting the type of gender of the task sender/user who this message is dedicated to (yes i know my english level 99999)
        gender_bd = cursor.execute('SELECT w_or_m FROM Podcast WHERE id=' + str(id_bd))

        gender_bd = gender_bd.fetchall()[0][0]

        # print(txt)

    except sqlite3.Error as error:
        print("Error in 4", error)

    finally:
        if (conn):
            conn.close()

    # Checking task type
    if gender_bd == 'men':
        voice = random.choice(speakers_men)
    elif gender_bd == 'women':
        voice = random.choice(speakers_women)
    else:
        voice = 'random'
    text = text_bd
    if typetask_bd == 'forDR':
        model.save_wav(text=text,
                       speaker=voice,
                       sample_rate=sample_rate,
                       audio_path='congrats_of_'+str(id_bd)+'.wav')
    elif typetask_bd == 'announcement':
        model.save_wav(text=text,
                       speaker=voice,
                       sample_rate=sample_rate,
                       audio_path='announcement_' + str(id_bd) + '.wav')

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Changing task state
        cursor.execute('UPDATE Podcast SET st_task = "render" WHERE id=' + str(id_bd))
        conn.commit()

    except sqlite3.Error as error:
        print("Error in final", error)

    finally:
        if (conn):
            conn.close()
    print(id_bd)