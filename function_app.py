import azure.functions as func
import json
import logging

from youtube_service import create_youtube_service, get_video_details, search_videos
from keyvault_service import get_youtube_api_key

app = func.FunctionApp()

@app.route(route="Youtubefunction", auth_level=func.AuthLevel.FUNCTION)
def Youtubefunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Récupérer la clé API depuis Key Vault test
    youtube_key = get_youtube_api_key()

    # Créer l'objet de service YouTube
    youtube = create_youtube_service(youtube_key)

    # Recherche des vidéos
    videos_data, video_ids = search_videos(youtube)
    video_details = get_video_details(youtube, video_ids)

    # Créer un dictionnaire pour stocker le nombre de vues par ID de vidéo
    view_counts = {item['id']: item['statistics']['viewCount'] for item in video_details}

    response_data = []

    for video in videos_data:
        video_id = video['id']['videoId']
        title = video['snippet']['title']
        url = f'https://www.youtube.com/watch?v={video_id}'
        description = video['snippet']['description']
        thumbnail = video['snippet']['thumbnails']['default']['url']
        view_count = view_counts.get(video_id, 'N/A')  # Récupérer le nombre de vues

        # Formater les données à envoyer dans la réponse
        video_info = {
            'Titre': title,
            'Description': description,
            'URL': url,
            'Thumbnail': thumbnail,
            'Nombre de vues': view_count
        }
        response_data.append(video_info)

    return func.HttpResponse(
        json.dumps(response_data, indent=2),
        mimetype="application/json",
        status_code=200
    )
