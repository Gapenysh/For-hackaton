import os
import pydub
import pysrt
import speech_recognition as sr
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from pytube import YouTube

from deep_translator import GoogleTranslator





def format_time(seconds):
    return str(pysrt.SubRipTime(seconds=seconds))


def proccess():
    video_url = "https://www.youtube.com/watch?v=acUrHVgKmWA"


    yt = YouTube(video_url)
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
    video_file = video_stream.download()


    # Путь к выходному видеофайлу с субтитрами
    output_path = "output_video.mp4"

    # Загрузить видеофайл и разделить аудиодорожку на фрагменты
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = "temp_audio.wav"
    audio.write_audiofile(audio_file)
    audio_segment = pydub.AudioSegment.from_wav(audio_file)
    chunk_length_ms = 5000  # 5 seconds
    chunks = [audio_segment[i * chunk_length_ms: (i + 1) * chunk_length_ms] for i in
              range(len(audio_segment) // chunk_length_ms)]

    # Преобразовать аудиофрагменты в текст с помощью SpeechRecognition
    r = sr.Recognizer()
    subtitles = []
    for i, chunk in enumerate(chunks):
        chunk.export("temp_chunk.wav", format="wav")
        with sr.AudioFile("temp_chunk.wav") as f:
            audio_data = r.record(f)
        try:
            text = r.recognize_google(audio_data, language="ru-RU")
            translated_text = GoogleTranslator(source="auto", target="tt").translate(text)
            subtitles.append((i * chunk_length_ms / 1000, (i + 1) * chunk_length_ms / 1000, translated_text))
        except sr.UnknownValueError:
            print(f"Error: Could not understand audio chunk {i}")
        except sr.RequestError:
            print(f"Error: Could not request results from speech recognition service")

    # Создать файл субтитров в формате .srt
    subtitles_list = []
    for i, (start, end, text) in enumerate(subtitles, 1):
        start_time = format_time(start)
        end_time = format_time(end)
        subtitle_entry = pysrt.SubRipItem(index=i, start=start_time, end=end_time, text=text)
        subtitles_list.append(subtitle_entry)

    srt_file = pysrt.SubRipFile(subtitles_list)
    srt_file.save("temp_subtitle.srt", encoding="utf-8")

    # Наложить субтитры на видео и сохранить выходной файл

    #video_with_subtitles = video.set_audio(video.audio)

    #for i, (start, end, text) in enumerate(subtitles):
        #txt_clip = TextClip(text, font='Arial', fontsize=20, color='white').set_duration(end - start)
     #   txt_clip = txt_clip.set_start(start)
      #  txt_clip = txt_clip.set_position(('center', 'bottom'))
       # video_with_subtitles = CompositeVideoClip([video_with_subtitles, txt_clip])

    #video_with_subtitles.write_videofile(output_path, audio=True, codec='libx264')



    # Удалить временные файлы
    os.remove(audio_file)

    os.remove("temp_chunk.wav")

proccess()