import random

import requests

from auth import *
from words import *


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


def send_meladze(title, link, event, first_name):
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
        Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                       'message': first_name + ', ' + title + '\n' + n_string,
                                                       'random_id': random.randint(0, 10000000),
                                                       'attachment': 'video%s_%s_%s' % (
                                                           str(owner_id), str(video_id), str(access_key))})
    except:
        Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                       'message': first_name + ', ' + title,
                                                       'random_id': random.randint(0, 10000000),
                                                       'attachment': 'video%s_%s_%s' % (
                                                           str(owner_id), str(video_id), str(access_key))})
        pass


def get_random_meladze(event, first_name):
    playlistitems_max = Auth.youtube_client.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=0,
        playlistId=meladze_playlist,
    ).execute()['pageInfo']['totalResults']
    random_position = random.randint(0, playlistitems_max - 1)
    p_tokens = get_page_tokens(meladze_playlist)
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
    send_meladze(title, link, event, first_name)


def send_alliance(event, first_name):
    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                   'message': first_name + ', ЗА АЛЬЯНС!!!',
                                                   'random_id': random.randint(0, 10000000),
                                                   'attachment': 'video-176071592_456239239'})


def get_wallpost_things(groups_dict, text_flag, photo_flag):
    data = []
    access_keys = []
    owner_id = []
    text = ""
    grp = random.choice(groups_dict)
    max_num = (Auth.vk_session_user.method('wall.get', {'owner_id': grp,
                                                        'count': 0, 'access_token': service_app_key}))['count']
    while True:
        num = random.randint(0, max_num)
        wallpost = Auth.vk_session_user.method('wall.get', {'owner_id': grp,
                                                            'album_id': 'wall', 'count': 1, 'offset': num,
                                                            'access_token': service_app_key})
        try:
            if 'copy_history' not in wallpost['items'][0].keys():
                if text_flag == 1:
                    text = '' + wallpost['items'][0]['text']
                if photo_flag == 1:
                    if wallpost['items'][0]['attachments'][0]['type'] == "photo":
                        photo = wallpost['items'][0]['attachments']
                        i = 0
                        while True:
                            owner_id = photo[i]['photo']['owner_id']
                            data.append(photo[i]['photo']['id'])
                            access_keys.append(photo[i]['photo']['access_key'])
                            i += 1
                            if i == len(photo):
                                break
                return data, text, owner_id, access_keys
        except:
            continue


def send_wallpost_things(groups_dict, text_flag, photo_flag, event, first_name):
    s, t, owner_id, access_keys = get_wallpost_things(groups_dict, text_flag, photo_flag)
    if photo_flag == 1:
        i = 0
        while True:
            s[i] = 'photo%s_%s_%s' % (str(owner_id), str(s[i]), str(access_keys[i]))
            i += 1
            if i == len(s):
                break
        photos_string = ','.join(s)
    else:
        photos_string = ''
    if text_flag == 1:
        t = first_name + ', ' + t
    else:
        t = ''
    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id, 'message': t,
                                                   'random_id': random.randint(0, 10000000),
                                                   "attachment": photos_string})


def habar_oceni(event, first_name):
    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                   'message': first_name + ', '
                                                   + str(random.randint(0, 10)) + '/10',
                                                   'random_id': random.randint(0, 10000000)})


def random_mudrost(event, first_name):
    max_num = (Auth.vk_session_user.method('wall.search', {'owner_id': mudrost_group_id, 'query': '#мудрость',
                                                           'count': 0, 'access_token': service_app_key}))['count']
    num = random.randint(0, max_num)
    mudrost = Auth.vk_session_user.method('wall.search', {'owner_id': mudrost_group_id, 'query': '#мудрость',
                                                          'count': 1, 'offset': num,
                                                          'access_token': service_app_key})['items'][0]['text']

    if 'Маяковский' in mudrost:
        random_mudrost(event, first_name)
    else:
        Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                       'message': first_name + ', ' + str(mudrost),
                                                       'random_id': random.randint(0, 10000000)})


def random_creepy(event, first_name):
    max_num = (Auth.vk_session_user.method('wall.search', {'owner_id': creepy_group_id, 'query': '#крипи',
                                                           'count': 0, 'access_token': service_app_key}))['count']
    num = random.randint(0, max_num)
    creepy = Auth.vk_session_user.method('wall.search', {'owner_id': creepy_group_id, 'query': '#крипи',
                                                         'count': 1, 'offset': num,
                                                         'access_token': service_app_key})
    wall_post = 'wall%s_%s' % (str(creepy['items'][0]['owner_id']), str(creepy['items'][0]['id']))
    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                   'message': first_name + ', ',
                                                   'random_id': random.randint(0, 10000000),
                                                   "attachment": wall_post})


def aws_tts(text_to_say, event, first_name):
    if str(text_to_say) not in ('', ' ', '  ', '   ', '    ', '     '):
        if len(text_to_say) <= 3000:
            answer = Auth.polly_client.synthesize_speech(VoiceId='Maxim', OutputFormat='ogg_vorbis',
                                                         Text=text_to_say)
            file = open('speech.ogg', 'wb')
            file.write(answer['AudioStream'].read())
            tts_url = Auth.vk_session_group.method('docs.getMessagesUploadServer',
                                                   {'type': 'audio_message',
                                                    'peer_id': event.obj.peer_id
                                                    })['upload_url']
            file = {'file': ('speech.ogg', open('speech.ogg', 'rb'))}
            r = requests.post(tts_url, files=file)
            r_string = r.json()['file']
            r_2 = Auth.vk_session_group.method('docs.save', {'file': r_string})
            _id = r_2['audio_message']['id']
            owner_id = r_2['audio_message']['owner_id']
            Auth.vk_session_group.method('messages.send',
                                         {'peer_id': event.obj.peer_id,
                                          'message': first_name + ', ',
                                          'random_id': random.randint(0, 10000000),
                                          'attachment': 'audio_message%s_%s' % (str(owner_id), str(_id))})
        else:
            Auth.vk_session_group.method('messages.send',
                                         {'peer_id': event.obj.peer_id,
                                          'message': first_name + ', вы ввели слишком большую пасту',
                                          'random_id': random.randint(0, 10000000)})
    del text_to_say


def habar_say(response, event, first_name):
    text_for_aws = response.replace('хабар скажи ', '')
    aws_tts(text_for_aws, event, first_name)


def habar_perevedi(response, event, first_name):
    tolang = response.split(' ')[3]
    tolang_tr = valid_lang.get(tolang)
    if tolang_tr in iter(valid_lang.values()):
        lastword = response.replace('хабар переведи на ' + str(tolang), '')
        if str(lastword) not in ('', ' ', '  ', '   ', '    ', '     '):
            stext1 = Auth.tr.set_text(lastword)
            det_lang = Auth.tr.detect_lang()
            fleng = Auth.tr.set_from_lang(det_lang)
            to_lang = Auth.tr.set_to_lang(tolang_tr)
            stext2 = Auth.tr.set_text(lastword)
            if str(Auth.tr.translate()) not in ('', ' ', '  ', '   ', '    ', '     '):
                if len(Auth.tr.translate()) <= 3000:
                    answer = Auth.polly_client.synthesize_speech(VoiceId='Maxim', OutputFormat='ogg_vorbis',
                                                                 Text=Auth.tr.translate())
                    file = open('speech.ogg', 'wb')
                    file.write(answer['AudioStream'].read())
                    tts_url = Auth.vk_session_group.method('docs.getMessagesUploadServer',
                                                           {'type': 'audio_message',
                                                            'peer_id': event.obj.peer_id
                                                            })['upload_url']
                    file = {'file': ('speech.ogg', open('speech.ogg', 'rb'))}
                    r = requests.post(tts_url, files=file)
                    r_string = r.json()['file']
                    r_2 = Auth.vk_session_group.method('docs.save', {'file': r_string})
                    _id = r_2['audio_message']['id']
                    owner_id = r_2['audio_message']['owner_id']
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': first_name + ', ' + Auth.tr.translate(),
                                                                   'random_id': random.randint(0, 10000000),
                                                                   'attachment': 'audio_message%s_%s' % (
                                                                    str(owner_id), str(_id))})
            del det_lang, to_lang, tolang_tr, stext1, stext2, fleng
