from ._base import YoutubeBaseInfoExtractor


class YoutubeStudioIE(YoutubeBaseInfoExtractor):
    IE_NAME = 'youtube:studio'
    IE_DESC = "YouTube Studio"
    _VALID_URL = r'^https?://studio\.youtube\.com/video/(?P<id>[0-9A-Za-z_-]{11})(/edit)?$'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        yt_query = {
            'videoId': video_id,
            'ttsTrackId': {
              'kind': 'asr',
              'lang': 'en'
            },
            'preferredFormat': 'vtt'
        }

        response = self._extract_response(
            default_client='web_creator',
            ep='globalization/download_caption_track',
            item_id=video_id,
            query=yt_query,
            note='Downloading subtitles',
            fatal=True
        )

        subtitles = {}

        if response['content']:
            captions = base64.urlsafe_b64decode(response['content']).decode('utf-8')

            subtitles['en'] = [
                {
                  'data': captions,
                  'ext': 'vtt'
                }
            ]

        formats = [{ 'url': url }]

        return {
            'formats': formats,
            'id': video_id,
            'title': 'captions',
            'subtitles': subtitles
        }
