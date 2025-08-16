from pytubefix import YouTube, Playlist
import os
from pathlib import Path
from moviepy import AudioFileClip

def baixar_youtube(link, destino):
    # Garante que o diretório de destino existe
    music_dir = Path.home() / "Music" / "baixadas"
    playlist_dir = Path.home() / "Music" / "playlists"
    pasta_destino = music_dir / destino
    os.makedirs(pasta_destino, exist_ok=True)

    def fazer_download_audio_mp3(yt_obj, destino):
        try:
            audio_stream = yt_obj.streams.filter(only_audio=True).order_by('abr').desc().first()
            if audio_stream is None:
                print("Nenhum stream de áudio disponível.")
                return
            print(f"Baixando áudio: {yt_obj.title}")
            downloaded_file = audio_stream.download(output_path=destino)
            mp3_path = os.path.splitext(downloaded_file)[0] + ".mp3"
            audio_clip = AudioFileClip(downloaded_file)
            audio_clip.write_audiofile(mp3_path)
            audio_clip.close()
            os.remove(downloaded_file)
            print(f"Áudio salvo como MP3: {mp3_path}")
        except Exception as e:
            print(f"Erro ao baixar/converter áudio: {e}")

    # Detecta se é playlist ou vídeo avulso
    if 'playlist?' in link or '/playlist/' in link:
        pl = Playlist(link)
        nome_playlist = pl.title or "playlist"
        pasta_playlist = criar_pasta(nome_playlist,"playlist")
        print(f"Detectado playlist '{nome_playlist}' com {len(pl.videos)} vídeos.")
        for video in pl.videos:
            try:
                fazer_download_audio_mp3(video, pasta_playlist)
            except Exception as e:
                print(f"Erro ao baixar {video.title}: {e}")
    else:
        try:
            yt = YouTube(link)
            fazer_download_audio_mp3(yt, str(pasta_destino))
        except Exception as e:
            print(f"Erro ao baixar vídeo: {e}")

def criar_pasta(nome_pasta,tipo_pasta):
    music_dir = Path.home() / "Music" / "baixadas"
    if tipo_pasta == "playlist":
        music_dir = Path.home() / "Music"
    if not music_dir.exists(): #Primeiro checa se encontrou a pasta Musicas
        music_dir.mkdir(parents=True)
    nome_pasta = nome_pasta.replace("Album - ","")
    pasta = music_dir / nome_pasta
    if not pasta.exists(): #Depois checa se existe a pasta destino, se não, cria.
        pasta.mkdir()
    return str(pasta)


def listar_pastas_musicas():
    music_dir = Path.home() / "Music" / "baixadas"
    if not music_dir.exists():
        return []
    return [item.name for item in music_dir.iterdir() if item.is_dir()]
