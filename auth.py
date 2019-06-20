from vk_api.bot_longpoll import VkBotLongPoll
import vk_api
from yandex.Translater import Translater
from googleapiclient.discovery import build
import boto3
from settings import *


vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()
tr = Translater()
tr.set_key(ya_tr_token)
vk_session_access = vk_api.VkApi(token=access_token)
polly_client = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name='eu-central-1').client('polly')
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
yt_client = build(API_SERVICE_NAME, API_VERSION, developerKey=yt_api_key)
