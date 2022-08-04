import json
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled,  VideoUnavailable # doesn't work

def get_base_url(port:int) -> str:
    '''
    Returns the base URL to the webserver if available.
    
    i.e. if the webserver is running on coding.ai-camp.org port 12345, then the base url is '/<your project id>/port/12345/'
    
    Inputs: port (int) - the port number of the webserver
    Outputs: base_url (str) - the base url to the webserver
    '''
    
    try:
        info = json.load(open(os.path.join(os.environ['HOME'], '.smc', 'info.json'), 'r'))
        project_id = info['project_id']
        base_url = f'/{project_id}/port/{port}/'
    except Exception as e:
        print(f'Server is probably running in production, so a base url does not apply: \n{e}')
        base_url = '/'
    return base_url
    
#function to add correct and or comma
def and_syntax(alist):
    if len(alist) == 1:
        alist = "".join(alist)
        return alist
    elif len(alist) == 2:
        alist = " and ".join(alist)
        return alist
    elif len(alist) > 2:
        alist[-1] = "and " + alist[-1]
        alist = ", ".join(alist)
        return alist
    else:
        return

def dict_to_str(dictlist):
    """transform dict transcript to a whole string"""
    str = ''
    for i in dictlist:
        str +=(i['text'])
        str +=(',')
    return str

# HELPER FUNCTIONS
def fetch_transcript(vid_id, language='en'):
  """
  Return the transcript of a video in a given language if it is found,
  otherwise pass. 
      
      Arguments:
      vid_id {String} -- the video id (at the end of the url v=<video_id>)
      language(str): the language of transcript, 2 character string (e.g. 'en', 'de')

      Returns:
      transcript(list[json]): {duration(float), start(float), text(str)}

  """
  transcript_obj = YouTubeTranscriptApi.list_transcripts(vid_id)
  try: 
    transcript = transcript_obj.find_transcript([language])
    return transcript.fetch()
  except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
    pass

