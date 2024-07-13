import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.easyid3 import EasyID3

# Configurar las credenciales de Spotify
client_id = 'TU_CLIENT_ID'
client_secret = 'TU_CLIENT_SECRET'

# Autenticación con Spotify
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# Ruta a tu archivo CSV
csv_file_path = 'TrackList.csv'

# Cargar el archivo CSV sin cabeceras
columns = ['title', 'artist', 'album', 'track', 'year', 'genre', 'bpm', 'initialkey', 'duration', 'fullfilenameext']
tracks_df = pd.read_csv(csv_file_path, delimiter=';', header=None, names=columns)

# Mapeo de claves
key_map_major = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_map_minor = ['Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm']

# Función para convertir la duración de minutos:segundos a milisegundos
def duration_to_milliseconds(duration):
    minutes, seconds = map(int, duration.split(':'))
    return (minutes * 60 + seconds) * 1000

# Función para obtener el género, BPM, clave y fecha de lanzamiento de una canción
def get_track_info(title, artist, duration):
    query = f'track:{title} artist:{artist}'
    result = sp.search(q=query, type='track', limit=10)  # Buscar las primeras 10 coincidencias
    duration_ms = duration_to_milliseconds(duration)
    for track in result['tracks']['items']:
        if abs(track['duration_ms'] - duration_ms) < 5000:  # Permitir una diferencia de 5 segundos
            artist_id = track['artists'][0]['id']
            track_id = track['id']
            artist_info = sp.artist(artist_id)
            genres = artist_info['genres']
            
            # Obtener características de audio
            track_features = sp.audio_features(track_id)[0]
            bpm = track_features['tempo']
            key = track_features['key']
            mode = track_features['mode']
            
            if key is not None and mode is not None:
                if mode == 1:  # Menor
                    musical_key = key_map_minor[key]
                else:  # Mayor
                    musical_key = key_map_major[key]
            else:
                musical_key = None

            # Obtener la fecha completa de lanzamiento
            release_date = track['album']['release_date']
            
            return genres, bpm, musical_key, release_date
    return [], None, None, None

# Obtener la información de las canciones
tracks_df['genres'], tracks_df['bpm'], tracks_df['key'], tracks_df['release_date'] = zip(*tracks_df.apply(lambda row: get_track_info(row['title'], row['artist'], row['duration']), axis=1))

# Guardar el archivo CSV actualizado
updated_file_path = 'TrackList_final.csv'
tracks_df.to_csv(updated_file_path, index=False, sep=';')

# Función para actualizar los metadatos de una canción
def update_metadata(file_path, title, artist, album, genre, bpm, key, release_date, track):
    try:
        audio = EasyID3(file_path)
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio['genre'] = genre
        audio['bpm'] = str(bpm)
        audio['key'] = key
        audio['date'] = release_date
        if pd.notna(track):
            audio['tracknumber'] = str(track)
        audio.save()
        print(f"Metadatos actualizados para {file_path}")
    except Exception as e:
        print(f"Error al actualizar metadatos para {file_path}: {e}")

# Recorrer las filas del DataFrame y actualizar los metadatos de las canciones
for index, row in tracks_df.iterrows():
    file_path = row['fullfilenameext']
    title = row['title']
    artist = row['artist']
    album = row['album']
    genre = ', '.join(row['genres']) if row['genres'] else row['genre']
    bpm = row['bpm']
    key = row['key']
    release_date = row['release_date']
    track = row['track']

    # Actualizar los metadatos del archivo de música
    update_metadata(file_path, title, artist, album, genre, bpm, key, release_date, track)
