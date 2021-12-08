import subprocess
import re
import time

import requests


def Ex1():
    # https://trac.ffmpeg.org/wiki/Debug/MacroblocksAndMotionVectors
    command = ["ffmpeg", "-flags2", "+export_mvs", "-i", "BBBcuted.mp4", "-vf", "codecview=mv=pf+bf+bb", "BBBmv.mp4"]
    subprocess.call(command)

    rep = input("Vols reproduir el video (Y/N)\t")
    if rep == "Y" or rep == "y":
        com = ["ffplay", "BBBmv.mp4"]
        subprocess.call(com)


def Ex2():
    # https://qastack.mx/superuser/215430/would-like-to-change-audio-codec-but-keep-video-settings-with-ffmpeg

    command = ["ffmpeg", "-ss", "0", "-i", "BBB.mp4", "-c", "copy", "-t", "60", "BBB1mcut.mp4"]
    subprocess.call(command)

    # extreiem la part d'audio a mp3 sense tocar el bitrate
    command = ["ffmpeg", "-i", "BBB1mcut.mp4", "-c:a", "libmp3lame", "BBBmp3.mp3"]
    subprocess.call(command)

    # extreiem la part d'audio a aac pero reduim el bitrate a 45kb
    command = ["ffmpeg", "-i", "BBB1mcut.mp4", "-b:a", "45k", "-c:a", "aac", "BBBaac.aac"]
    subprocess.call(command)

    # https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg
    command = ["ffmpeg", "-i", "BBB1mcut.mp4", "-i", "BBBmp3.mp3", "-i", "BBBaac.aac", "-c", "copy", "-map", "0:v:0",
               "-map", "1:a:0", "-map", "2:a:0", "BBBex2.mp4"]
    subprocess.call(command)
    rep = input("Vols veure les propietats del video is soroll? (Y/N)\t")
    if rep == "Y" or rep == "y":
        com = ["ffmpeg", "-i", "BBBex2.mp4", "-hide_banner"]
        subprocess.call(com)
        time.sleep(5)


def Ex3():
    # https://stackoverflow.com/questions/49621540/finding-a-word-after-a-specific-word-in-python-using-regex-from-text-file/49621730
    com = ["ffmpeg", "-i", "BBBcuted.mp4", "-hide_banner"]
    x = subprocess.run(com, capture_output=True).stderr

    DVB = False
    ATSC = False
    ISDB = False
    DTMB = False

    DVBa = False
    ATSCa = False
    ISDBa = False
    DTMBa = False

    DVBv = False
    ATSCv = False
    ISDBv = False
    DTMBv = False

    BS = []

    with open('data.txt', 'w') as f:
        f.write(x.decode("utf-8"))

    AuC = []
    ViC = []
    with open('data.txt') as fd:

        # Iterate over the lines
        for line in fd:

            matchVideo = re.search(r' Video: (\S+)', line)
            matchAudio = re.search(r' Audio: (\S+)', line)

            if matchVideo:
                VideoCodec = matchVideo.group(1)
                ViC.append(VideoCodec)

            if matchAudio:
                AudioCodec = matchAudio.group(1)
                AuC.append(AudioCodec)
    # depenent de quin codec tingui el video i audio es podra utilitzar un broadcast
    for i in ViC:
        if i == 'h264' or i == 'mpeg2video':
            DVBv = True
            ATSCv = True
            ISDBv = True
            DTMBv = True
        elif i == 'avs' or i == 'avs+':
            DTMBv = True

    for i in AuC:
        if i == 'mp3':
            DVBa = True
            DTMBa = True
        elif i == 'aac':
            DVBa = True
            DTMBa = True
            ISDBa = True
        elif i == 'ac3':
            DVBa = True
            DTMBa = True
            ATSCa = True
        elif i == 'mp2':
            DTMBa = True
        elif i == 'dra':
            DTMBa = True
    # si els codecs de audio i video compleixen amb el estandar de difusió aquest sera un possible candidat.
    if DVBa:
        if DVBa == DVBv:
            DVB = True
            BS.append('DVB')
    if ISDBa:
        if ISDBa == ISDBv:
            ISDB = True
            BS.append("ISDB")
    if ATSCa:
        if ATSCa == ATSCv:
            ATSC = True
            BS.append("ATSC")
    if DTMBa:
        if DTMBa == DTMBv:
            DTMB = True
            BS.append("DTMB")

    if not DVB and not ISDB and not ATSC and not DTMB:
        print("ERROR. No encaixa en cap broadcast standard")
    print("El video podria ser utilitzat en aquests estàndards de difusió")
    print(BS)


def Ex4():
    # https://stackoverflow.com/questions/8672809/use-ffmpeg-to-add-text-subtitles
    # opensubtitles.org

    # si vols canviar els subtituls afegeix el link de descarga aqui, (tingues an compte que el link a vegades caduca!)
    url = 'https://dl.opensubtitles.org/es/download/file/1952038313'
    req = requests.get(url, allow_redirects=True)
    open('subtitles.srt', 'wb').write(req.content)

    com = ["ffmpeg", "-i", "BBB1mcut.mp4", "-vf", "subtitles=subtitles.srt", "BBBsub.mp4"]

    subprocess.call(com)

    rep = input("Vols reproduir el video (Y/N)\t")
    if rep == "Y" or rep == "y":
        com = ["ffplay", "BBBsub.mp4"]
        subprocess.call(com)


if __name__ == "__main__":
    Option = 0
    while Option != 5:
        Option = int(input("\n\nBENVINGUT AL SEMINARI 2 DE SCAV\n\nSiusplau, selecciona la opció que vulguis"
                           "\n\n\t [1] -Visualitzar els macroblocs i el motion vector"
                           "\n\n\t [2] -Exportar els audios en mp3 i aac i empaquetar-ho en un mp4"
                           "\n\n\t [3] -Saber quin broadcast standard pot ser utilitzat per un video"
                           "\n\n\t [4] -Afegir subtitols al video\n\n\t [5] -Sortir\n\n\t"))

        if Option == 1:
            Ex1()
        elif Option == 2:
            Ex2()
        elif Option == 3:
            Ex3()
        elif Option == 4:
            Ex4()
