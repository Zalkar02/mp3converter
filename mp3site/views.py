from django.shortcuts import render
import youtube_dl
import smtplib

from mp3.celery import app

def youtube(url):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',}],}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info(url, download=False)
    return res['url']

@app.task
def send_mail(url, email):
    FROM = "azisuulu2002@gmail.com"
    body = "\r\n".join((
    f"From: {FROM}",
    f"To: {email}",
    "Subject: np3 converter",
    "",
    youtube(url)))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(FROM, 'PASSWORD')
        server.sendmail(FROM, [email], body)
        server.close()
    except:
        pass

def base(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        email = request.POST.get('email')
        if 'youtube' in url:
            send_mail.delay(url, email)
    return render(request, 'base.html')
