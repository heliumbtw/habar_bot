from vk_api.bot_longpoll import VkBotEventType

from functions import *


def get_name():
    user_info = (Auth.vk_session_group.method('users.get', {'user_ids': event.obj.from_id}))
    name = user_info[0]['first_name']
    return str(name)


while True:
    try:
        for event in Auth.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response = event.obj.text.lower()
                first_name = get_name()
                if 'привет' in response:
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': first_name + ', '
                                                                   + random.choice(privet_answer),
                                                                   'random_id': random.randint(0, 10000000)})
                elif response in ['пока']:
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': str(first_name) + ', '
                                                                   + random.choice(poka_answer),
                                                                   'random_id': random.randint(0, 10000000)})
                elif ('споки' in response) or ('спокойной ночи' in response):
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': random.choice(spoki_answer_msg)
                                                                   + ', ' + str(first_name),
                                                                   'attachment': random.choice(spoki_answer),
                                                                   'random_id': random.randint(0, 10000000)})
                elif response in ['хабар спасибо']:
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': str(first_name) + ', Это моя работа 😎',
                                                                   'random_id': random.randint(0, 10000000)})
                elif ('🌚' in response) or ('🌝' in response) or \
                        ('😎' in response) or ('🌖' in response) or ('😏' in response):
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': random.choice(smile_answer),
                                                                   'random_id': random.randint(0, 10000000)})
                elif response in ['хабар гадай']:
                    answers = (random.choice(list(open('prinakaz.txt', encoding="utf-8"))))
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': str(first_name) + ', ' + answers,
                                                                   'random_id': random.randint(0, 10000000)})
                elif 'хабар шар ' in response:
                    lastword = response.replace('хабар шар ', '')
                    if str(lastword) not in '':
                        Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                       'message': str(first_name) + ', '
                                                                       + random.choice(shar_answers),
                                                                       'random_id': random.randint(0, 10000000)})
                elif response in ['хабар помощь']:
                    Auth.vk_session_group.method('messages.send', {'peer_id': event.obj.peer_id,
                                                                   'message': str(first_name) +
                                                                   ', Статья с функциями скоро будет',
                                                                   'random_id': random.randint(0, 10000000)})
                elif response in ['хабар флекс']:
                    send_wallpost_things(flex_groups, 1, 1, event, first_name)
                elif response in ['хабар мудрость']:
                    random_mudrost(event, first_name)
                elif response in ['хабар крипота']:
                    random_creepy(event, first_name)
                elif response in ['хабар меладзе']:
                    get_random_meladze(event, first_name)
                elif response in ['хабар павер']:
                    send_wallpost_things(dmc_groups, 1, 1, event, first_name)
                elif response in ['хабар сэйлем', 'хабар сайлем', 'хабар сейлем']:
                    send_wallpost_things(salem_group_id, 1, 1, event, first_name)
                elif response in ['хабар живец']:
                    send_wallpost_things(parrot_group_id, 1, 1, event, first_name)
                elif response in ['хабар аниме']:
                    send_wallpost_things(anime_group_id, 1, 1, event, first_name)
                elif response in ['хабар винкс']:
                    send_wallpost_things(winx_group_id, 1, 1, event, first_name)
                elif 'хабар скажи ' in response:
                    habar_say(response, event, first_name)
                elif 'хабар оцени ' in response:
                    habar_oceni(event, first_name)
                elif ('альянс' in response) or ('alliance' in response):
                    send_alliance(event, first_name)
                elif 'пидор' in response:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': 'Сам пидор, ' + first_name,
                                                        'random_id': random.randint(0, 10000000)})
                elif response in mbtipidor:
                    vk_session.method('messages.send', {'peer_id': event.obj.peer_id,
                                                        'message': first_name + ', А может ты пидор ?',
                                                        'random_id': random.randint(0, 10000000)})
    except:
        raise
