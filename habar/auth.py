import boto3
import vk_api
from googleapiclient.discovery import build
from vk_api.bot_longpoll import VkBotLongPoll


from settings import group_api_key, group_id, access_token, aws_access_key_id, aws_secret_access_key, yt_api_key


class Auth:
    vk_session_group = vk_api.VkApi(token=group_api_key)
    session_api = vk_session_group.get_api()
    longpoll = VkBotLongPoll(vk_session_group, group_id)
    vk = vk_session_group.get_api()
    vk_session_user = vk_api.VkApi(token=access_token)
    polly_client = boto3.Session(
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name='eu-central-1').client('polly')
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    youtube_client = build(API_SERVICE_NAME, API_VERSION, developerKey=yt_api_key)
