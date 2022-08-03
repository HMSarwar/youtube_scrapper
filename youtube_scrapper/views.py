
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings
import datetime
from django.db import connection
from django.core import serializers
from .models import ChannelWiseLastSync, Video, VideoPerformance, VideoTags
from django.http import HttpResponse
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def sync_uploaded_videos(*args, **kwargs):
    channel_list = get_channel_list()
    sync_history = get_channel_wise_last_updated()
    for channel in channel_list:
        save_latest_uploaded_videos(channel, sync_history)
    update_channel_wise_sync_data(channel_list)


def sync_video_performance(*args, **kwargs):
    videos = Video.objects.filter(next_sync__lte=datetime.datetime.now()).all()
    youtube = get_youtube()
    for video in videos:
        video_statistics = video_details(youtube, video.videoId, part='statistics')['items'][0]['statistics']
        video_statistics.update({'published_at': video.published_at})
        save_video_performance(video, video_statistics, video.videoId)



def save_latest_uploaded_videos(chanelID, sync_history):
    youtube = get_youtube()
    last_sync = sync_history.get(chanelID) or datetime.datetime.now().replace(year=1971)
    upload_id = get_upload_id_by_channel(chanelID, youtube)
    videos = get_videos_by_upload_id(upload_id, youtube, last_sync)
    for video in videos:
        video_info = video_details(youtube, video.get('videoId'))['items'][0]['snippet']
        video_statistics = video_details(youtube, video.get('videoId'), part='statistics')['items'][0]['statistics']
        save_video_info(video_info,video_statistics, video.get('videoId'))
        save_video_tags(video_info,video.get('videoId'))
        save_video_performance(video_info,video_statistics,video.get('videoId'))


def get_videos_by_upload_id(upload_id, youtube,last_sync):
    videos = []
    next_page = ''
    while True:
        playlist_items = youtube.playlistItems().list(part='contentDetails', playlistId=upload_id, pageToken=next_page or None, maxResults=50).execute()
        next_page = playlist_items.get('nextPageToken') or ''
        video_ = [{'videoId': x.get('contentDetails', {}).get('videoId'), 'videoPublishedAt': x.get('contentDetails', {}).get('videoPublishedAt').replace('T', ' ').replace('Z', '')} for x in playlist_items.get('items')]
        for video in video_:
            if datetime.datetime.strptime(video.get('videoPublishedAt'), '%Y-%m-%d %H:%M:%S') < last_sync:
                break
            videos.append(video)
        if not next_page:
            break
    return videos


def video_details(youtube, videoID, part='snippet'):
    video= youtube.videos().list(part=part, id=videoID).execute()
    return video



def get_upload_id_by_channel(channel_id,youtube):
    channel_data = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    upload_id = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return upload_id

def save_video_info(video_data,statistics_data, videoID):
    video = Video(
        title=video_data.get('title'),
        videoId = videoID,
        channelID = video_data.get('channelId'),
        published_at = video_data.get('publishedAt').replace('T', ' ').replace('Z', ''),
        view_count=statistics_data.get('viewCount') or 0,
        like_count=statistics_data.get('likeCount') or 0,
        favorite_count=statistics_data.get('favoriteCount') or 0,
        comment_count=statistics_data.get('commentCount') or 0,
        next_sync = max(datetime.datetime.strptime(video_data.get('publishedAt').replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1), datetime.datetime.now())
    )
    video.save()


def save_video_performance(video_data,statistics_data, videoID):
    published = statistics_data.get('published_at') or datetime.datetime.strptime(video_data.get('publishedAt').replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
    perf = VideoPerformance(
        videoId=videoID,
        view_count =statistics_data.get('viewCount') or 0,
        like_count =statistics_data.get('likeCount') or 0,
        favorite_count =statistics_data.get('favoriteCount') or 0,
        comment_count =statistics_data.get('commentCount') or 0,
        timeframe = ((datetime.datetime.now() - published).seconds) / 60
    )
    perf.save()



def save_video_tags(video_data, videoID):
    for tag_name in video_data.get('tags'):
        tag = VideoTags(
            tag=tag_name,
            videoID = videoID
        )
        tag.save()


def update_channel_wise_sync_data(channel_list=[]):
    if channel_list:
        query_ = """replace into `youtube_scrapper_channelwiselastsync` (`channelID`, `last_sync`) VALUES """
        for index, chan_ in enumerate(channel_list):
            if index:
                query_ += ""","""
            query_ += """('{}', '{}')""".format(chan_, str(datetime.datetime.now()))
        cursor = get_cursor()
        cursor.execute(query_+""";""")


def get_channel_wise_last_updated(*args, **kwargs):
    data_list = ChannelWiseLastSync.objects.all()
    return {x.channelID: x.last_sync for x in data_list}


def get_cursor():
    return connection.cursor()

def get_channel_list(*args):
    channel_list = []
    with open(settings.CHANNEL_FILE_PATH, 'r') as f:
        channel_list = f.readlines()
    return [x.strip('\n') for x in channel_list]


def get_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=settings.DEV_API_KEY)
    return youtube


def median_view_by_channel(channel_id):
    sub_query = """
            select sum(t.view_count) from
            (select max(youtube_scrapper_videoperformance.view_count) as view_count,youtube_scrapper_videoperformance.timeframe,youtube_scrapper_videoperformance.videoID   from youtube_scrapper_videoperformance join youtube_scrapper_video on youtube_scrapper_video.videoId = youtube_scrapper_videoperformance.videoId
            where timeframe < 60 {} group by youtube_scrapper_videoperformance.videoID) as t

        """.format(("and channelID=" + channel_id) if channel_id else '')
    curosor = get_cursor()
    curosor.execute(sub_query)
    result = curosor.fetchall()
    all_count = 0
    if result and len(result) > 0:
        result = result[0]
        if result and len(result) > 0:
            all_count = int(result[0])
    curosor.execute("""select count(id) from youtube_scrapper_video {}""").format(
        ("where channelID=" + channel_id) if channel_id else '')
    result = curosor.fetchall()
    len_of_vids = 1
    if result and len(result) > 0:
        result = result[0]
        if result and len(result) > 0:
            len_of_vids = int(result[0])
    median = all_count / len_of_vids
    return median


def get_videos_by_performance(channel_id, median):
    query = """
                select max(youtube_scrapper_videoperformance.view_count) as view_count,youtube_scrapper_video.channelID,youtube_scrapper_videoperformance.videoID   from youtube_scrapper_videoperformance join youtube_scrapper_video on youtube_scrapper_video.videoId = youtube_scrapper_videoperformance.videoId
                where timeframe < 60 {} group by youtube_scrapper_videoperformance.videoID having max(youtube_scrapper_videoperformance.view_count) > {}
        """.format(("and channelID=" + channel_id) if channel_id else '', median)
    cursor = get_cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_videos_by_tags(taglist):
    query = """
        select view_count,youtube_scrapper_video.channelID,youtube_scrapper_video.videoID  from youtube_scrapper_video join youtube_scrapper_videotags on youtube_scrapper_videotags.videoID = youtube_scrapper_video.videoID {} group by youtube_scrapper_video.videoID
    """.format("""where youtube_scrapper_videotags.tag in ({})""".format(taglist) if taglist else '')
    cursor = get_cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_video_performance_data(request, **kwargs):
    tag_list = ''
    if request.GET.get('tags'):
        tag_list = request.GET.get('tags')

    channel_id = request.GET.get('channel_id')
    video_performance = request.GET.get('video_performance')
    if video_performance:
        median = median_view_by_channel(channel_id)
        result = get_videos_by_performance(channel_id, median)
    else:
        result = get_videos_by_tags(channel_id)
    to_return = []
    if result:
        for row in result:
            to_return.append(dict(
                videoID=row[2],
                view_count=row[0],
                channelID=row[1],
            ))
    return HttpResponse(json.dumps(to_return))
