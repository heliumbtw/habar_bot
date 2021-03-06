from vk_api.bot_longpoll import VkBotEventType

from auth import Auth
from functions import Functions
from settings import flex_groups, dmc_groups, salem_group_id, parrot_group_id, anime_group_id, winx_group_id
from words import secret_trigger, smile_trigger


class Listen:
    def __init__(self):
        self.event = None

    def choose(self):
        try:
            for self.event in Auth.longpoll.listen():
                if self.event.type == VkBotEventType.MESSAGE_NEW:
                    f = Functions(self.event)
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
                    elif response in ['хабар мудрость']:
                        f.mudrost()
                    elif response in ['хабар крипота']:
                        f.creepy()
                    elif response in ['хабар меладзе']:
                        f.get_meladze()
                    elif response in ['хабар флекс']:
                        f.send_wallpost_things(flex_groups, text='text', photo='photo')
                    elif response in ['хабар павер']:
                        f.send_wallpost_things(dmc_groups, text='text', photo='photo')
                    elif response in ['хабар сэйлем', 'хабар сайлем', 'хабар сейлем']:
                        f.send_wallpost_things(salem_group_id, text='text', photo='photo')
                    elif response in ['хабар живец']:
                        f.send_wallpost_things(parrot_group_id, text='text', photo='photo')
                    elif response in ['хабар аниме']:
                        f.send_wallpost_things(anime_group_id, text='text', photo='photo')
                    elif response in ['хабар винкс']:
                        f.send_wallpost_things(winx_group_id, text='text', photo='photo')
                    elif 'хабар оцени ' in response:
                        f.habar_oceni()
                    elif self.event.obj.attachments:
                        if any(attach_type in self.event.obj.attachments[0]['type']
                               for attach_type in ['wall', 'photo']):
                            f.random_rate_message()
                    elif 'хабар скажи ' in response:
                        f.habar_say(response)
                    elif ('альянс' in response) or ('alliance' in response):
                        f.send_alliance()
                    elif any(trigger in response for trigger in secret_trigger):
                        f.secret_trigger()
        except Exception:
            pass
