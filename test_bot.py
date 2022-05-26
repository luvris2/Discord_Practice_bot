import discord
from discord.ext import commands # 명령어를 통해 수행하는 라이브러리
from youtube_dl import YoutubeDL # 유튜브의 영상을 추출하는 라이브러리
import time
import asyncio
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio

# 명령어로 사용 될 때 명령어 선언 접두사
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    # activity=discord.Game("연습봇 테스트") 봇 상태 표시, ~ 하는 중
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("연습봇 테스트"))

@bot.command()
async def 따라하기(ctx, *, text):
    #a wait ctx.send(text) #그냥 텍스트로 봇이 응답
    # embed가 포함되어 봇이 응답
    # title은 embed의 제목, description은 내용, color는 색상
    # description은 embed의 내용으로 입력받은 변수 text
    await ctx.send(embed=discord.Embed(title='따라하기', description=text, color=0x00ff00))

@bot.command()
async def 이리와(ctx):
    try:
        global vc
        # 음성채널에 봇이 들어갈 수 있게 만드는 코드
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            # 만약 유저가 접속해있지않으면
            # 다른 채널에는 없는지 확인한 다음에 이동
            await vc.move_to(ctx.message.author.voice.channel)      
        except:
            # 유저가 접속해있지 않으면 문구 출력
            await ctx.send("채널에 유저가 접속해있지 않아요.")
            
@bot.command()
async def 사라져(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("이미 채널에 나가있어요.")

# 음악 재생에 필요한 라이브러리
# pip install selenium
# pip install beautifulsoup4 (웹 크롤링)
# pip install youtube_dl (유튜브 컨텐츠)
# pip install requests
# 봇이 영상을 다운로드해서 소리를 재생하기 위한 라이브러리 ffmpeg
# 환경변수 추가 ffmpeg-5.0.1-full_build\bin

# 크롬 버전 확인후 chromedriver와 비슷한 버전으로 설치
# pip install lxml (셀레니움 크롤링에 필요)

# 유튜브URL을 입력하면 재생, 혹은 노래 제목을 쓰면 검색하여 재생
@bot.command()
async def 노래재생(ctx, *, msg):
    if not vc.is_playing():
        global entireText
        # YDL_OPTIONS, FFMPEG_OPTIONS는 ffmpeg와 youtube_dl의 기본설정
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        if msg.find('https://www.youtube.com/watch?') :
            pass
        else :
            # 옵션 변수를 이용하여 드라이브를 숨김
            options = webdriver.ChromeOptions()
            options.add_argument('headless')

            # 크롬드라이버와 셀레니움을 활용하여
            # 유튜브에서 영상 제목과 링크 등을 가져오는 코드
            # 크롬드라이버가 있는 경로로 설정
            chromedriver_dir = "E:\Program Files\Bot\chromedriver.exe"
            driver = webdriver.Chrome(chromedriver_dir, options=options)
            #driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
            driver.get("https://www.youtube.com/results?search_query="+msg)
            source = driver.page_source
            # 웹 크롤링
            bs = bs4.BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            entireText = entireNum.text.strip()
            musicurl = entireNum.get('href') # a href
            url = 'https://www.youtube.com'+musicurl 

            driver.quit() # 크롬드라이버 종료

        # 음악 재생 코드
        with YoutubeDL(YDL_OPTIONS) as ydl:
            # 유튜브의 url 추출
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

# 위의 노래 검색 코드와 같지만 멜론차트로 검색하여 멜론차트를 재생해주는 명령어 생성
@bot.command()
async def 멜론차트(ctx):
    # try:
    #     global vc
    #     # 음성채널에 봇이 들어갈 수 있게 만드는 코드
    #     vc = await ctx.message.author.voice.channel.connect()
    # except:
    #     try:
    #         # 만약 유저가 접속해있지않으면
    #         # 다른 채널에는 없는지 확인한 다음에 이동
    #         await vc.move_to(ctx.message.author.voice.channel)      
    #     except:
    #         pass

    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = "E:\Program Files\Bot\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

# 현재 재생중인 노래의 제목을 확인
@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))

# 디스코드 api에서 제공하는 기본 함수 사용 pause()
@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = entireText + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

# 디스코드 api에서 제공하는 기본 함수 사용 resume()
@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = entireText  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

# 디스코드 api에서 제공하는 기본 함수 사용 stop()
@bot.command()
async def 정지(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

bot.run('OTc4Mjc0NDg5NzMxMjgwOTU2.GdNrnN.TY6OBkiVZbqY-X6SXcXF1CFNjqaqY9ZCuLeu8o')


