import random

import requests

from secrets import randbelow
from auth import Auth
from settings import service_app_key, mudrost_group_id, creepy_group_id, meladze_playlist
from words import secret_trigger_answer, meladze_songs, shar_answers, smile_answer, spoki_answer, spoki_answer_msg, \
    poka_answer, privet_answer, ratings
from db_functions import tts_db


class functions:
    def __init__(self, event):
        self.event = event
        self.first_name = self.get_name()

    def get_name(self):
        user_info = (Auth.vk_session_group.method('users.get', {'user_ids': self.event.obj.from_id}))
        name = user_info[0]['first_name']
        return str(name)

    def habar_oceni(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', '
                                                       + ratings[(random.randint(0, 10))],
                                                       'random_id': random.randint(0, 100000000)})

    def privet(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', '
                                                       + random.choice(privet_answer),
                                                       'random_id': random.randint(0, 100000000)})

    def poka(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', '
                                                       + random.choice(poka_answer),
                                                       'random_id': random.randint(0, 1000000000)})

    def spoki(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': random.choice(spoki_answer_msg)
                                                       + ', ' + self.first_name,
                                                       'attachment': random.choice(spoki_answer),
                                                       'random_id': random.randint(0, 1000000000)})

    def spasibo(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', Это моя работа 😎',
                                                       'random_id': random.randint(0, 1000000000)})

    def smile(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': random.choice(smile_answer),
                                                       'random_id': random.randint(0, 1000000000)})

    def gadanie(self):
        answers = (random.choice(list(open('prinakaz.txt', encoding="utf-8"))))
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', ' + answers,
                                                       'random_id': random.randint(0, 1000000000)})

    def shar(self, response):
        lastword = response.replace('хабар шар ', '')
        if str(lastword) not in '':
            Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                           'message': self.first_name + ', '
                                                           + random.choice(shar_answers),
                                                           'random_id': random.randint(0, 1000000000)})

    def help(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name +
                                                       ', Статья с функциями скоро будет(наверное)',
                                                       'random_id': random.randint(0, 1000000000)})

    def send_wallpost_things(self, groups_dict, text=None, photo=None):
        data = []
        access_keys = []
        owner_id = []
        text = self.first_name + ", "
        grp = random.choice(groups_dict)
        max_num = (Auth.vk_session_user.method('wall.get', {'owner_id': grp,
                                                            'count': 0, 'access_token': service_app_key}))['count']
        num = random.randint(0, max_num)
        wallpost = Auth.vk_session_user.method('wall.get', {'owner_id': grp,
                                                            'album_id': 'wall', 'count': 1, 'offset': num,
                                                            'access_token': service_app_key})
        try:
            if 'copy_history' not in wallpost['items'][0].keys():
                if text == 'text':
                    text = text + wallpost['items'][0]['text']
                if photo == 'photo':
                    if wallpost['items'][0]['attachments'][0]['type'] == "photo":
                        i = 0
                        while True:
                            owner_id.append(wallpost['items'][0]['attachments'][i]['photo']['owner_id'])
                            data.append(wallpost['items'][0]['attachments'][i]['photo']['id'])
                            access_keys.append(wallpost['items'][0]['attachments'][i]['photo']['access_key'])
                            i += 1
                            if i == len(wallpost['items'][0]['attachments']):
                                break
        except:
            return self.send_wallpost_things(groups_dict, text, photo)
        photos_string = ""
        if photo == 'photo':
            if data:
                i = 0
                while True:
                    data[i] = 'photo%s_%s_%s' % (str(owner_id[i]), str(data[i]), str(access_keys[i]))
                    i += 1
                    if i == len(data):
                        break
                photos_string = ','.join(data)
            else:
                return self.send_wallpost_things(groups_dict, text, photo)
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id, 'message': text,
                                                       'random_id': random.randint(0, 1000000000),
                                                       'attachment': photos_string})

    def mudrost(self):
        max_num = (Auth.vk_session_user.method('wall.search', {'owner_id': mudrost_group_id, 'query': '#мудрость',
                                                               'count': 0, 'access_token': service_app_key}))['count']
        num = random.randint(0, max_num)
        mudrost = Auth.vk_session_user.method('wall.search', {'owner_id': mudrost_group_id, 'query': '#мудрость',
                                                              'count': 1, 'offset': num,
                                                              'access_token': service_app_key})['items'][0]['text']
        if 'Маяковский' in mudrost:
            return self.mudrost()
        else:
            Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                           'message': self.first_name + ', ' + str(mudrost),
                                                           'random_id': random.randint(0, 1000000000)})

    def creepy(self):
        max_num = (Auth.vk_session_user.method('wall.search', {'owner_id': creepy_group_id, 'query': '#крипи',
                                                               'count': 0, 'access_token': service_app_key}))['count']
        num = random.randint(0, max_num)
        creepy = Auth.vk_session_user.method('wall.search', {'owner_id': creepy_group_id, 'query': '#крипи',
                                                             'count': 1, 'offset': num,
                                                             'access_token': service_app_key})
        wallpost = 'wall%s_%s' % (str(creepy['items'][0]['owner_id']), str(creepy['items'][0]['id']))
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', ',
                                                       'random_id': random.randint(0, 1000000000),
                                                       "attachment": wallpost})

    @staticmethod
    def get_page_tokens(playlist_id):
        a = [""]
        playlistitems_max = Auth.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=0,
            playlistId=playlist_id
        ).execute()['pageInfo']['totalResults']
        playlistitems = Auth.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlist_id
        ).execute()
        while True:
            a.append(playlistitems['nextPageToken'])
            playlistitems = Auth.youtube_client.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=50,
                playlistId=playlist_id,
                pageToken=a[len(a) - 1]
            ).execute()
            playlistitems_max -= 50
            if playlistitems_max < 50:
                break
        return a

    def send_meladze(self, title, link):
        a = Auth.vk_session_user.method('video.save',
                                        {'is_private': 1, 'link': 'https://www.youtube.com/watch?v=' + link})
        owner_id = a['owner_id']
        video_id = a['video_id']
        access_key = a['access_key']
        upload_url = a['upload_url']
        requests.post(upload_url)
        try:
            quantity_strings = len(meladze_songs[title])
            if 0 < quantity_strings < 8:
                n_string = meladze_songs[title][(random.randint(0, (quantity_strings - 1)))]
            else:
                n_string = meladze_songs.get(title)
            Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                           'message': self.first_name + ', ' + title + '\n' + n_string,
                                                           'random_id': random.randint(0, 1000000000),
                                                           'attachment': 'video%s_%s_%s' % (
                                                               str(owner_id), str(video_id), str(access_key))})
        except:
            Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                           'message': self.first_name + ', ' + title,
                                                           'random_id': random.randint(0, 1000000000),
                                                           'attachment': 'video%s_%s_%s' % (str(owner_id),
                                                                                            str(video_id),
                                                                                            str(access_key))})

    def get_meladze(self):
        playlistitems_max = Auth.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=0,
            playlistId=meladze_playlist,
        ).execute()['pageInfo']['totalResults']
        random_position = random.randint(0, playlistitems_max - 1)
        p_tokens = self.get_page_tokens(meladze_playlist)
        i = 0
        while random_position > 49:
            random_position -= 50
            i += 1
        title = Auth.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=meladze_playlist,
            pageToken=p_tokens[i]
        ).execute()['items'][random_position]['snippet']['title']
        link = Auth.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=meladze_playlist,
            pageToken=p_tokens[i]
        ).execute()['items'][random_position]['snippet']['resourceId']['videoId']
        self.send_meladze(title, link)

    def send_alliance(self):
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': self.first_name + ', ЗА АЛЬЯНС!!!',
                                                       'random_id': random.randint(0, 1000000000),
                                                       'attachment': 'video-176071592_456239239'})

    def secret_trigger(self):
        if random.randint(0, 1):
            message = secret_trigger_answer[0] + self.first_name
        else:
            message = secret_trigger_answer[1] + self.first_name + ' ?'
        Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                       'message': message,
                                                       'random_id': random.randint(0, 1000000000)})

    def aws_tts(self, text_to_say):
        if str(text_to_say) not in ('', ' ', '  '):
            if len(text_to_say) < 3000:
                tts = tts_db()
                if tts.check_tts(len(text_to_say)):
                    answer = Auth.polly_client.synthesize_speech(VoiceId='Maxim', OutputFormat='ogg_vorbis',
                                                                 Text=text_to_say)
                    file = open('speech.ogg', 'wb')
                    file.write(answer['AudioStream'].read())
                    tts_url = Auth.vk_session_group.method('docs.getMessagesUploadServer',
                                                           {'type': 'audio_message',
                                                            'peer_id': self.event.obj.peer_id
                                                            })['upload_url']
                    file = {'file': ('speech.ogg', open('speech.ogg', 'rb'))}
                    upload_speech = requests.post(tts_url, files=file)
                    r = Auth.vk_session_group.method('docs.save',
                                                     {'file': upload_speech.json()['file']})
                    Auth.vk_session_group.method('messages.send',
                                                 {'peer_id': self.event.obj.peer_id,
                                                  'message': self.first_name + ', ',
                                                  'random_id': random.randint(0, 1000000000),
                                                  'attachment': 'audio_message%s_%s' % (r['audio_message']['owner_id'],
                                                                                        r['audio_message']['id'])})
                else:
                    Auth.vk_session_group.method('messages.send',
                                                 {'peer_id': self.event.obj.peer_id,
                                                  'message': self.first_name + ', на сегодня осталось ' +
                                                  tts.check_tts(len(text_to_say)) + ' символов',
                                                  'random_id': random.randint(0, 1000000000)})

            else:
                Auth.vk_session_group.method('messages.send',
                                             {'peer_id': self.event.obj.peer_id,
                                              'message': self.first_name + ', до 2999 символов в 1 сообщении.\n'
                                                                           'В твоем сейчас ' + str(len(text_to_say))
                                                                           + ' символов',
                                              'random_id': random.randint(0, 1000000000)})

    def habar_say(self, response):
        text_for_aws = response.replace('хабар скажи ', '')
        return self.aws_tts(text_for_aws)

    def random_rate_message(self):
        if randbelow(10) in [3, 5, 7, 9]:
            Auth.vk_session_group.method('messages.send', {'peer_id': self.event.obj.peer_id,
                                                           'message': self.first_name + ', '
                                                           + ratings[(random.randint(0, 10))],
                                                           'random_id': random.randint(0, 100000000)})
        else:
            pass
