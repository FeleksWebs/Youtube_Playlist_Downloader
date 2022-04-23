# Install modules required
try:
    import os
    import pkg_resources
    import subprocess
    import sys
    import youtube_dl

except Exception as e:
    required = {'pip', 'choco'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        python = sys.executable
        subprocess.check_call(
            [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


# run youtube-dl install if choco is not installed
installed = {pkg.key for pkg in pkg_resources.working_set}
if("youtube-dl" not in installed):
    try:
        os.system('choco install -y youtube-dl ffmpeg')
    except Exception as e:
        cmdString = '@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString(' + \
            "https://chocolatey.org/install.ps1" + \
            '))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"'
        os.system(cmdString)
        os.system('choco install -y youtube-dl ffmpeg')


print('Enter your Youtube PlayList:')
URL = input()
print('Enter your file extension (eg. mp3,mp4,mov...)')
EXT = input()

options = {
    'verbose': True,
    'format': 'bestaudio/best',
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': EXT,
    }],
}

try:
    with youtube_dl.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(URL, download=False)
        title = info_dict['entries'][0]['title']
        new_name = "%s.mp3" % title
        options['outtmpl'] = new_name
        ydl.prepare_filename(info_dict)
        ydl.download([URL])
except Exception as e:
    print(e)
    exit()
