from googleapiclient.discovery import build

def create_youtube_service(youtube_key):
    """Crée un objet de service pour interagir avec l'API YouTube."""
    return build('youtube', 'v3', developerKey=youtube_key)

def get_video_details(youtube, video_ids):
    """Récupère les détails des vidéos, y compris le nombre de vues."""
    request = youtube.videos().list(
        part='statistics',
        id=','.join(video_ids)  # Joint les ID avec des virgules
    )
    response = request.execute()
    return response.get('items', [])

def search_videos(youtube, max_results=20, channel_id='UC4JX40jDee_tINbkjycV4Sg'):
    """Recherche les dernières vidéos d'une chaîne et récupère leurs détails."""
    request = youtube.search().list(
        part='snippet',  # On récupère le snippet pour les infos de base
        channelId=channel_id,
        type='video',
        order="date",
        maxResults=max_results
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response.get('items', [])]
    return response.get('items', []), video_ids
