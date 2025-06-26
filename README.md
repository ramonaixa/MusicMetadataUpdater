# Music Metadata Updater

Este script en Python utiliza la API de Spotify para obtener información sobre canciones (género, BPM, clave, fecha de lanzamiento) y actualiza los metadatos de archivos de música en formatos MP3 y FLAC.

## Requisitos

- Python 3.x
- Bibliotecas: `spotipy`, `mutagen`, `pandas`

Puedes instalar las bibliotecas necesarias con el siguiente comando:

```bash
pip install spotipy mutagen pandas
```

## Configuración de Spotify

1. **Crea una aplicación en Spotify Developer Dashboard:**
    - Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    - Inicia sesión con tu cuenta de Spotify.
    - Haz clic en "Create an App".
    - Ingresa un nombre y una descripción para tu aplicación.
    - Acepta los términos y condiciones y haz clic en "Create".
    - Una vez creada la aplicación, obtén el `Client ID` y `Client Secret`.

2. **Configura las credenciales en el script:**

    Abre el script y reemplaza `TU_CLIENT_ID` y `TU_CLIENT_SECRET` con los valores de Client ID y Client Secret que obtuviste del Spotify Developer Dashboard:

    ```python
    # Configurar las credenciales de Spotify
    client_id = 'TU_CLIENT_ID'
    client_secret = 'TU_CLIENT_SECRET'
    ```

## Uso del Script

1. **Prepara tu archivo CSV:**

    El archivo CSV debe tener los siguientes campos sin cabeceras:

    ```sql
    title;artist;album;track;year;genre;bpm;initialkey;duration;fullfilenameext
    ```

    Donde:

    - title: Título de la canción.
    - artist: Artista de la canción.
    - album: Álbum de la canción.
    - track: Número de pista (opcional).
    - year: Año de lanzamiento (solo año).
    - genre: Género inicial (puede estar vacío).
    - bpm: BPM inicial (puede estar vacío).
    - initialkey: Clave inicial (puede estar vacío).
    - duration: Duración en formato mm:ss.
    - fullfilenameext: Ruta absoluta del archivo de música con nombre y extensión.

2. **Ejecuta el script:**

    El script cargará el archivo CSV, buscará información de cada canción en la API de Spotify y actualizará los metadatos de los archivos de música en tu computadora.

    ```python
    # Ejecutar el script
    python update_music_metadata.py
    ````

3. **Revisa el archivo CSV actualizado:**

    El script generará un nuevo archivo CSV llamado `TrackList_final.csv` con la información obtenida de Spotify.

## Actualización de Metadatos

El script actualiza los metadatos de los archivos de música de la siguiente manera:

- Archivos MP3: Utiliza etiquetas ID3.
- Archivos FLAC: Utiliza etiquetas Vorbis/FLAC.

Los metadatos actualizados incluyen:

- Título (title)
- Artista (artist)
- Álbum (album)
- Género (genre)
- BPM (bpm)
- Clave (initialkey)
- Fecha de lanzamiento (release_date)
- Número de pista (tracknumber, si está disponible)

## Errores Comunes

- **Formato de archivo no soportado:** El script solo soporta archivos MP3 y FLAC.
- **Credenciales incorrectas:** Asegúrate de haber configurado correctamente el `client_id` y `client_secret`.
- **Archivo CSV malformado:** Verifica que el archivo CSV tenga el formato correcto y que las rutas de los archivos de música sean válidas.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias o encuentras errores, por favor abre un issue o envía un pull request.
