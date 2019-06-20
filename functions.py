import random
from words import *
import requests
from auth import *


def get_page_tokens(client, playlist_id):
    a = [""]
    playlistitems_max = client.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=0,
        playlistId=playlist_id
    ).execute()['pageInfo']['totalResults']
    playlistitems = client.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id
    ).execute()
    while True:
        a.append(playlistitems['nextPageToken'])
        playlistitems = client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlist_id,
            pageToken=a[len(a) - 1]
        ).execute()
        playlistitems_max -= 50
        if playlistitems_max < 50:
            break
    return a


def send_miladze(vk_s, event, first_name, title, link, vk_s_a):
    a = vk_s_a.method('video.save', {'is_private': 1, 'link': 'https://www.youtube.com/watch?v='+link})
    owner_id = a['owner_id']
    video_id = a['video_id']
    access_key = a['access_key']
    upload_url = a['upload_url']
    requests.post(upload_url)
    try:
        quantity_strings = len(meladze_songs[title])
        if 0 < quantity_strings < 8:
            n_string = meladze_songs[title][(random.randint(0, (quantity_strings-1)))]
        else:
            n_string = meladze_songs.get(title)
        vk_s.method('messages.send', {'peer_id': event.obj.peer_id,
                                      'message': str(first_name) + ', ' + title + '\n' + n_string,
                                      'random_id': random.randint(0, 10000000),
                                      'attachment': 'video%s_%s_%s' % (str(owner_id), str(video_id), str(access_key))})
    except:
        vk_s.method('messages.send', {'peer_id': event.obj.peer_id,
                                      'message': str(first_name) + ', ' + title,
                                      'random_id': random.randint(0, 10000000),
                                      'attachment': 'video%s_%s_%s' % (str(owner_id), str(video_id), str(access_key))})
        pass


def get_random_meladze(client, event, first_name):
    playlistitems_max = client.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=0,
        playlistId=meladze_playlist,
        ).execute()['pageInfo']['totalResults']
    random_position = random.randint(0, playlistitems_max - 1)
    p_tokens = get_page_tokens(client, meladze_playlist)
    i = 0
    while random_position > 49:
        random_position -= 50
        i += 1
    title = client.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=meladze_playlist,
        pageToken=p_tokens[i]
    ).execute()['items'][random_position]['snippet']['title']
    link = client.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=meladze_playlist,
        pageToken=p_tokens[i]
    ).execute()['items'][random_position]['snippet']['resourceId']['videoId']
    send_miladze(vk_session, event, first_name, title, link, vk_session_access)


def send_alliance(vk_s, event, first_name):
    vk_s.method('messages.send', {'peer_id': event.obj.peer_id,
                                  'message': str(first_name) + ', ЗА АЛЬЯНС!!!',
                                  'random_id': random.randint(0, 10000000),
                                  'attachment': 'video-176071592_456239239'})


def get_random_wall_picture(photo_group_id, a_token, access_vk_session):
    max_num = (access_vk_session.method('photos.get', {'owner_id': photo_group_id, 'album_id': 'wall',
                                                       'count': 0, 'access_token': a_token}))['count']
    num = random.randint(1, max_num)
    photo = access_vk_session.method('photos.get', {'owner_id': str(photo_group_id), 'album_id': 'wall', 'count': 1,
                                                    'offset': num, 'access_token': a_token})['items'][0]['id']
    attachment = 'photo' + str(photo_group_id) + '_' + str(photo)
    return attachment


def get_wallpost_things(access_vk_session, groups_dict, text_flag, photo_flag):
    data = []
    access_keys = []
    owner_id = []
    text = ""
    grp = random.choice(groups_dict)
    max_num = (access_vk_session.method('wall.get', {'owner_id': grp,
                                                     'count': 0, 'access_token': service_token}))['count']
    while True:
        num = random.randint(0, max_num)
        wallpost = access_vk_session.method('wall.get', {'owner_id': grp,
                                                         'album_id': 'wall', 'count': 1, 'offset': num,
                                                         'access_token': service_token})
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


def send_wallpost_things(access_vk_session, event, groups_dict, first_name, text_flag, photo_flag):
    s, t, owner_id, access_keys = get_wallpost_things(access_vk_session, groups_dict, text_flag, photo_flag)
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
        t = str(first_name) + ', ' + t
    else:
        t = ''
    vk_session.method('messages.send', {'peer_id': event.obj.peer_id, 'message': t,
                                        'random_id': random.randint(0, 10000000), "attachment": photos_string})


def get_random_mudrost(access_vk_session):
    max_num = (access_vk_session.method('wall.search', {'owner_id': mudrost_group_id, 'query': '#мудрость',
                                                        'count': 0, 'access_token': service_token}))['count']
    num = random.randint(0, max_num)
    mudrost = access_vk_session.method('wall.search', {'owner_id': mudrost_group_id, 'query': '#мудрость',
                                                       'count': 1, 'offset': num,
                                                       'access_token': service_token})['items'][0]['text']
    return str(mudrost)


def send_mudrost(vk_s, event, first_name):
    vk_s.method('messages.send', {'peer_id': event.obj.peer_id,
                                  'message': str(first_name) + ', ' + get_random_mudrost(vk_session_access),
                                  'random_id': random.randint(0, 10000000)})


def get_random_creepy(access_vk_session):
    max_num = (access_vk_session.method('wall.search', {'owner_id': creepy_group_id, 'query': '#крипи',
                                                        'count': 0, 'access_token': service_token}))['count']
    num = random.randint(0, max_num)
    print(num)
    creepy = access_vk_session.method('wall.search', {'owner_id': creepy_group_id, 'query': '#крипи',
                                                      'count': 1, 'offset': num,
                                                      'access_token': service_token})
    wall_post = 'wall%s_%s' % (str(creepy['items'][0]['owner_id']), str(creepy['items'][0]['id']))
    return wall_post


def send_creepy(vk_s, event, first_name):
    vk_s.method('messages.send', {'peer_id': event.obj.peer_id,
                                  'message': str(first_name) + ', ',
                                  'random_id': random.randint(0, 10000000),
                                  "attachment": get_random_creepy(vk_session_access)})


def get_flex_picture(event, first_name):
    attachment = get_random_wall_picture(random.choice(flex_groups), service_token, vk_session_access)
    vk_session.method('messages.send', {'peer_id': event.obj.peer_id, 'message': str(first_name) + ', лови флекс',
                                        'random_id': random.randint(0, 10000000), "attachment": attachment})


def get_name(event):
    user_info = (vk_session.method('users.get', {'user_ids': event.obj.from_id}))
    first_name = user_info[0]['first_name']
    return first_name


def aws_tts(vk_s, polly_cl, first_name, event, text_to_say):
    if str(text_to_say) not in ('', ' ', '  ', '   ', '    ', '     '):
        if len(text_to_say) <= 3000:
            answer = polly_cl.synthesize_speech(VoiceId='Maxim', OutputFormat='ogg_vorbis',
                                                Text=text_to_say)
            file = open('speech.ogg', 'wb')
            file.write(answer['AudioStream'].read())
            tts_url = vk_s.method('docs.getMessagesUploadServer',
                                  {'type': 'audio_message',
                                   'peer_id': event.obj.peer_id
                                   })['upload_url']

            file = {'file': ('speech.ogg', open('speech.ogg', 'rb'))}
            r = requests.post(tts_url, files=file)
            r_string = r.json()['file']
            r_2 = vk_s.method('docs.save', {'file': r_string})
            _id = r_2['audio_message']['id']
            owner_id = r_2['audio_message']['owner_id']
            vk_s.method('messages.send',
                        {'peer_id': event.obj.peer_id,
                         'message': str(first_name) + ', ',
                         'random_id': random.randint(0, 10000000),
                         'attachment': 'audio_message%s_%s' % (str(owner_id), str(_id))})
        else:
            vk_s.method('messages.send',
                        {'peer_id': event.obj.peer_id,
                         'message': str(first_name) + ', вы ввели слишком большую пасту',
                         'random_id': random.randint(0, 10000000)})
    del text_to_say
    return()


def habar_say(vk_s, polly_cl, response, first_name, event):
    text_for_aws = response.replace('хабар скажи ', '')
    aws_tts(vk_s, polly_cl, first_name, event, text_for_aws)


def habar_perevedi(vk_s, polly_cl, response, first_name, event):
    tolang = response.split(' ')[3]
    tolang_tr = valid_lang.get(tolang)
    if tolang_tr in iter(valid_lang.values()):
        lastword = response.replace('хабар переведи на ' + str(tolang), '')
        if str(lastword) not in ('', ' ', '  ', '   ', '    ', '     '):
            stext1 = tr.set_text(lastword)
            det_lang = tr.detect_lang()
            fleng = tr.set_from_lang(det_lang)
            to_lang = tr.set_to_lang(tolang_tr)
            stext2 = tr.set_text(lastword)
            if str(tr.translate()) not in ('', ' ', '  ', '   ', '    ', '     '):
                if len(tr.translate()) <= 3000:
                    answer = polly_cl.synthesize_speech(VoiceId='Maxim', OutputFormat='ogg_vorbis',
                                                        Text=tr.translate())
                    file = open('speech.ogg', 'wb')
                    file.write(answer['AudioStream'].read())
                    tts_url = vk_s.method('docs.getMessagesUploadServer',
                                          {'type': 'audio_message',
                                           'peer_id': event.obj.peer_id
                                           })['upload_url']
                    file = {'file': ('speech.ogg', open('speech.ogg', 'rb'))}
                    r = requests.post(tts_url, files=file)
                    r_string = r.json()['file']
                    r_2 = vk_s.method('docs.save', {'file': r_string})
                    _id = r_2['audio_message']['id']
                    owner_id = r_2['audio_message']['owner_id']
                    vk_s.method('messages.send', {'peer_id': event.obj.peer_id,
                                                  'message': str(first_name) + ', ' + tr.translate(),
                                                  'random_id': random.randint(0, 10000000),
                                                  'attachment': 'audio_message%s_%s' % (str(owner_id), str(_id))})
            del det_lang, to_lang, tolang_tr, stext1, stext2, fleng
