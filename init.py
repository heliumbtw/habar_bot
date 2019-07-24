from vk_api.bot_longpoll import VkBotEventType
import random
import functions
from words import *
from auth import *

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response = event.obj.text.lower()
                first_name = functions.get_name(event)
                if 'привет' in response:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': str(first_name) + ', '
                                                                                   + random.choice(privet_answer),
                                                        'random_id': random.randint(0, 10000000)})
                elif response in ['пока']:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': str(first_name) + ', ' + random.choice(poka_answer),
                                                        'random_id': random.randint(0, 10000000)})
                elif ('споки' in response) or ('спокойной ночи' in response):
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': random.choice(spoki_answer_msg) + ', '
                                                        + str(first_name),
                                                        'attachment': random.choice(spoki_answer),
                                                        'random_id': random.randint(0, 10000000)})
                elif response in ['хабар спасибо']:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': str(first_name) + ', Это моя работа 😎',
                                                        'random_id': random.randint(0, 10000000)})
                elif ('🌚' in response) or ('🌝' in response) or\
                        ('😎' in response) or ('🌖' in response) or ('😏' in response):
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': random.choice(smile_answer),
                                                        'random_id': random.randint(0, 10000000)})
                elif response in ['хабар гадай', 'хабар гадай.']:
                    answers = (random.choice(list(open('prinakaz.txt', encoding="utf-8"))))
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': str(first_name) + ', ' + answers,
                                                        'random_id': random.randint(0, 10000000)})
                elif 'хабар шар ' in response:
                    lastword = response.replace('хабар шар ', '')
                    if str(lastword) not in '':
                        vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                            'message': str(first_name) + ', '
                                                            + random.choice(shar_answers),
                                                            'random_id': random.randint(0, 10000000)})
                elif response in ['хабар помощь']:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': str(first_name) +
                                                        ', Статья с функциями скоро будет',
                                                        'random_id': random.randint(0, 10000000)})
                elif response in ['хабар флекс']:
                    functions.get_flex_picture(event, first_name)
                elif response in ['хабар мудрость']:
                    functions.send_mudrost(vk_session, event, first_name)
                elif response in ['хабар крипота']:
                    functions.send_creepy(vk_session, event, first_name)
                elif response in ['хабар меладзе']:
                    functions.get_random_meladze(yt_client, event, first_name)
                elif response in ['хабар павер']:
                    functions.send_wallpost_things(vk_session_access, event, dmc_groups, first_name, 1, 1)
                elif response in ['хабар сэйлем', 'хабар сайлем', 'хабар сейлем']:
                    functions.send_wallpost_things(vk_session_access, event, salem_group_id, first_name, 1, 1)
                elif response in ['хабар живец']:
                    functions.send_wallpost_things(vk_session_access, event, parrot_group_id, first_name, 1, 1)
                elif response in ['хабар аниме']:
                    functions.send_wallpost_things(vk_session_access, event, anime_group_id, first_name, 1, 1)
                elif response in ['хабар винкс']:
                    functions.send_wallpost_things(vk_session_access, event, winx_group_id, first_name, 1, 1)
                elif 'хабар скажи ' in response:
                    functions.habar_say(vk_session, polly_client, response, first_name, event)
                elif response in ['хабар оцени']:
                    functions.habar_oceni(vk_session, event, first_name)
                elif ('альянс' in response) or ('alliance' in response):
                    functions.send_alliance(vk_session, event, first_name)
                elif 'пидор' in response:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': 'Сам пидор, ' + str(first_name),
                                                        'random_id': random.randint(0, 10000000)})
                elif response in mbtipidor:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': str(first_name) + ', А может ты пидор ?',
                                                        'random_id': random.randint(0, 10000000)})
    except:
        pass
