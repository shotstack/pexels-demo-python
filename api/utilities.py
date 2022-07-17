from dotenv import load_dotenv

import shotstack_sdk as shotstack
import os

from pexelsapi.pexels                import Pexels
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.title_asset import TitleAsset
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.soundtrack  import Soundtrack
from shotstack_sdk.model.transition  import Transition

load_dotenv()

shotstack_url           = os.getenv("SHOTSTACK_HOST")
shotstack_api_key       = os.getenv("SHOTSTACK_API_KEY")
shotstack_assets_url    = os.getenv("SHOTSTACK_ASSETS_URL")
pexels_api_key          = os.getenv("PEXELS_API_KEY")

api                     = Pexels(pexels_api_key)

configuration = shotstack.Configuration(host = shotstack_url)
configuration.api_key['DeveloperKey'] = shotstack_api_key

def submit(data):
    min_clips   = 4.0
    max_clips   = 8.0
    clip_length = 2.0
    video_start = 4.0

    search_videos = api.search_videos(
        query           = data.get("search"),
        orientation     = '', size='', color='', locale='', page=1,
        per_page        = max_clips
    )
    
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)
        video_clips  = []

        title_asset = TitleAsset(
            text        = data.get('title'),
            style       = "minimal",
            size        = "small"
        )

        title_transition = Transition(
            _in="fade",
            out="fade"
        )

        title_clip = Clip(
            asset       = title_asset,
            length      = video_start,
            start       = 0.0,
            transition  = title_transition,
            effect      = "zoomIn"
        )

        for index, video in enumerate(search_videos.get('videos')):
            if index >= max_clips:
                break
            
            hd_file = None
            videos  = video.get('video_files')

            for entry in videos:
                if entry.get('height') == 720 or entry.get('width') == 1920:
                    hd_file = entry

            if hd_file is None:
                hd_file = videos[0]

            video_asset = VideoAsset(
                src = hd_file.get('link'),
                trim= 1.0
            )

            video_clip = Clip(
                asset = video_asset,
                start = video_start + (index * clip_length),
                length= clip_length
            )

            video_clips.append(video_clip)

            title_transition = Transition(
                _in="fade",
                out="fade"
            )

        soundtrack = Soundtrack(
            src         = f"{shotstack_assets_url}music/{data.get('soundtrack')}.mp3",
            effect      = "fadeOut"
        )

        timeline = Timeline(
            background  = "#000000",
            soundtrack  = soundtrack,
            tracks      = [Track(clips=[title_clip]), Track(clips=video_clips)]
        )

        output = Output(
            format      = "mp4",
            resolution  = "sd"
        )

        edit = Edit(
            timeline    = timeline,
            output      = output
        )

        try:
            return api_instance.post_render(edit)['response']
        except Exception as e:
            print(f"Unable to resolve API call: {e}") 

def status(render_id):
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        try:
            return api_instance.get_render(render_id, data=False, merged=True)['response']
        except Exception as e:
            print(f"Unable to resolve API call: {e}") 