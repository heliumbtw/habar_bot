from vk_api.bot_longpoll import VkBotEventType

from auth import Auth
from functions import functions
from settings import flex_groups, dmc_groups, salem_group_id, parrot_group_id, anime_group_id, winx_group_id
from words import secret_trigger, smile_trigger


class listen:
    def __init__(self):
        self.event = None

    def choose(self):
        try:
            for self.event in Auth.longpoll.listen():
                if self.event.type == VkBotEventType.MESSAGE_NEW:
                    f = functions(self.event)
                    response = self.event.obj.text.lower()
                    if 'хабар оцени ' in response:
                        f.habar_oceni()
                    elif (response in ['привет']) or (response in ['хабар привет']):
                        f.privet()
                    elif (response in ['пока']) or (response in ['хабар пока']):
                        f.poka()
                    elif ('споки' in response) or ('спокойной ночи' in response):
                        f.spoki()
                    elif response in ['хабар спасибо']:
                        f.spasibo()
                    elif any(trigger in response for trigger in smile_trigger):
                        f.smile()
                    elif response in ['хабар гадай']:
                        f.gadanie()
                    elif 'хабар шар ' in response:
                        f.shar(response)
                    elif response in ['хабар помощь', 'помощь', 'хабар функции', 'функции']:
                        f.help()
                    elif response in ['хабар флекс']:
                        f.send_wallpost_things(flex_groups, 1, 1)
                    elif response in ['хабар мудрость']:
                        f.mudrost()
                    elif response in ['хабар крипота']:
                        f.creepy()
                    elif response in ['хабар меладзе']:
                        f.get_meladze()
                    elif response in ['хабар павер']:
                        f.send_wallpost_things(dmc_groups, 1, 1)
                    elif response in ['хабар сэйлем', 'хабар сайлем', 'хабар сейлем']:
                        f.send_wallpost_things(salem_group_id, 1, 1)
                    elif response in ['хабар живец']:
                        f.send_wallpost_things(parrot_group_id, 1, 1)
                    elif response in ['хабар аниме']:
                        f.send_wallpost_things(anime_group_id, 1, 1)
                    elif response in ['хабар винкс']:
                        f.send_wallpost_things(winx_group_id, 1, 1)
                    elif 'хабар оцени ' in response:
                        f.habar_oceni()
                    #elif 'хабар скажи ' in response:
                    #    f.habar_say(response)
                    elif ('альянс' in response) or ('alliance' in response):
                        f.send_alliance()
                    elif any(trigger in response for trigger in secret_trigger):
                        f.secret_trigger()
        except Exception:
            raise
