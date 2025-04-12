import asyncio
import platform
from fileinput import filename
import nextcord
from nextcord.ext import commands
from nextcord import FFmpegAudio, FFmpegPCMAudio
from gtts import gTTS # type: ignore
import random
import webserver # นำเข้า webserver.py ที่คุณสร้างไว้
import discord
import yt_dlp
import os
import subprocess

# ตรวจสอบ FFmpeg
ffmpeg_path = r"C:\ffmpeg\bin"  # เปลี่ยนเป็น path ที่คุณเก็บ ffmpeg.exe
ffmpeg_full_path = os.path.join(ffmpeg_path, "ffmpeg.exe")
if os.path.exists(ffmpeg_full_path):
    os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_path)
    print(f"พบ FFmpeg ที่: {ffmpeg_full_path}")
else:
    print(f"ไม่พบ FFmpeg ที่: {ffmpeg_full_path}")
    exit()

# ✅ แก้ปัญหา asyncio บน Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# กำหนด intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.messages = True
import nextcord
from nextcord.ext import commands
# และ import อื่นๆ ตามปกติ

bot = commands.Bot(command_prefix="j", intents=intents)

texts = ["กูขอดมตูดหน่อยถอดกางเกงมา!!!", "ถกกางเกงมากูจะระเบิดดาก!!!", "ไปไกลๆไปไอหน้าตูด!!!", "กูชอบตูดมึงเข้าใจไหมกูชอบตูดดดดดด!!!", "ตูดคือที่สุดของในโลกกกกกกกก!!!", "กูนี่แหละเจ้าของดิสตัวจริงง!!!", "กูคือเกย์ King เว้ยยยย!!!", "หันตูดมาซะดีๆ!!!", "สวัสดีไอพวกชอบตูดทั้งหลายฮะฮิๆๆๆ", "ดากของนายอะสวยดีนะพ่อหนุ่ม!!!"]
ball = ["100%", "พีคิดว่าดีแน่นอน", "ไม่มีใครเถียงหรอก", "จำเป็นแน่", "พี่ว่าต้องทำ", "จากที่พี่ดู ดีมาก", "ผลที่พี่ดู ดีเยี่ยม", "ดีมาก", "ทุกอย่างดูดี", "ถามอีกรอบหน่อย พี่ฟังไม่ชัด", "ไม่บอกหรอก", "พี่ไม่รู้อ่ะ", "พี่ทำนายอนาคตไม่ได้นะ", "ฮะ ไรนะ", "อย่าเลยน้อง", "พี่ว่าไม่ดี", "จากที่วิเคราห์ดูแล้วพี่ว่าไม่น่าดี", "อย่าาาาา", "อย่าเลย"]

speak = ["มีไรหรือ","เรียกทำไมอะ","สวัสดี","อ้าวสวัสดี", "สบายดีไหม", "พี่เป็นไงบ้าง", "ไง", "ดี", "หวัดดี", "เจอกันอีกเล้วนะ", "อ้าวเป็นไง"]
answer = ["ก็ดีนะ" , "ดีอยู่" ,"เอาเลย" , "ไม่ดีกว่า","ใจเย็นกูคิดว่าไม่หน้าดี","อย่าดีกว่า","เยี่ยม","เอาดิ","ว้าวววว","ทำเลย","ฮะ ม่ายยยยย"]
complement = ["ทำได้ดีมาก", "สวยมาก" ,"ดีแล้ว","เจ๋ง","เก่งมาก","ว้าวววว","เก่งมากคับ","เราเก่งจังอ่ะ", "โห้ เก่งมากๆ"]
ask = ["ทำไมฉันต้องไป","ไหนคำขอโทษของฉัน","กลับไปทำไม"]
insult = ["ฉันด่าคนไม่เป็นอะ","ไม่เอาน่า", "อย่าเลย", "E3","ไม่อยากจะพูด","งอนแล้วนะ","ไม่อยากอ่ะ","ไอ้เ-ี้ย",">:)"]
help = ["ไม่เป็นไรนะ","มึงทำดีแล้ว","มึงอะทำถูกแล้ว","มึงเป็นคนดี","ทำดีที่สุดแล้ว","ไม่เป็นไรนะ","ไม่มีอะไรต้องกลัวนะ","ก็ได้นะก็ดีขึ้นเอง","ฉันอยู่ที่นี่เสมอเป็นกำลังใจให้นะ","ทุกสิ่งมีทางออกเสมออดทนไว้นะ","ไม่ว่าอะไรจะเกิดขึ้นเธอก็ไม่ได้นะนะ", "วันนี้อาจจะแย่แต่พรุ่งนี้วันที่ดีได้นะ"]
sorry = ["ขอโทษนะ ฉันไม่ได้ตั้งใจจริงๆ","ฉันผิดไปแล้ว ยกโทษให้ฉันได้ไหม?","ขอโทษนะ ถ้าทำให้เธอรู้สึกแย่","ฉันเสียใจที่ทำให้เกิดเรื่องแบบนี้","ฉันจะพยายามไม่ให้มันเกิดขึ้นอีก ขอโทษนะ"]
sad = ["ฉันรู้สึกแย่จัง… ขอโทษนะ","ฉันทำพลาดไปใช่ไหม… เสียใจจริงๆ","ไม่อยากให้เป็นแบบนี้เลย… ฉันเสียใจ","ฉันไม่น่าทำให้เธอรู้สึกแบบนี้เลย ขอโทษนะ","ฉันอาจจะเป็นแค่บอท แต่ฉันก็เสียใจจริงๆ นะ"]
hate = ["อึ๋ย! ไม่ชอบเลยจริงๆ!","ขออยู่ให้ห่างจากสิ่งนี้ได้ไหม...","แค่คิดก็ขนลุกแล้ว!","โอ๊ย! ไม่เอา ไม่อยากเจอเลย!","ขอไม่พูดถึงได้ไหม มันแย่สุดๆ!"]

@bot.event
async def on_ready():
    print(f"[Bot] เข้าสู่ระบบสำเร็จแล้ว: {bot.user}")

    # เพิ่มคำสั่งตามเดิมของคุณได้ที่นี่ เช่น @bot.commands, @bot.event เป็นต้น
    # หรือสามารถใช้ @bot.add_command() เพื่อเพิ่มคำสั่งใหม่ได้
@bot.command(name="พูด")
async def bottext(ctx):
    random.shuffle(texts)
    await ctx.send(texts[0])
    await ctx.message.delete()

@bot.command(name="คิด")
async def botthink(ctx):
    random.shuffle(ball)
    await ctx.send(ball[0])
    await ctx.message.delete()

# คำสั่งเข้า voice channel
@bot.command(name="เข้า")
async def join(ctx):
    if ctx.author.voice:  # ตรวจสอบว่าผู้ใช้อยู่ใน Voice Channel
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
        await ctx.send(f"บอทเข้าร่วมในห้อง: {channel.name}")
    else:
        await ctx.send("คุณต้องอยู่ใน Voice Channel ก่อนถึงจะให้บอทเข้าห้องได้!")
    await ctx.message.delete()

# คำสั่งออกจาก Voice Channel
@bot.command(name="ออก")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("บอทออกจากห้องแล้วจ้า")
    else:
        await ctx.send("บอทยังไม่ได้เข้าห้องนะครับ")
    await ctx.message.delete()

# คำสั่งเล่นเพลงจาก YouTube
@bot.command(name="เล่นยูทูป")
async def play_youtube(ctx, *, url):
    if not ctx.author.voice:
        await ctx.send("คุณต้องอยู่ใน Voice Channel ก่อนถึงจะเล่นเพลงได้!")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client
        await vc.move_to(channel)

    if vc.is_playing():
        vc.stop()

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': 'audio/temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            temp_path = "audio/temp.mp3"

        if not os.path.exists(temp_path):
            await ctx.send("ไม่สามารถดาวน์โหลดเพลงได้!")
            return

        source = FFmpegPCMAudio(temp_path)
        vc.play(source)
        await ctx.send(f"🎵 กำลังเปิดเพลง: {info.get('title', 'ชื่อเพลงไม่ระบุ')}")

        while vc.is_playing():
            await asyncio.sleep(1)

    except Exception as e:
        await ctx.send(f"เกิดข้อผิดพลาด: {e}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@bot.command(name="เล่นเพลง")
async def play_local(ctx, *, filename: str):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await channel.connect()
        else:
            vc = ctx.voice_client
            await vc.move_to(channel)

        filepath = f"audio/{filename}.mp3"

        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await ctx.send("❌ Bot ไม่ได้เชื่อมต่อกับ Voice Channel!")
            return
        
        if vc.is_playing():
            vc.stop()
        try:
            source = FFmpegPCMAudio(filepath)
            vc.play(source)
            await ctx.send(f"🎶 กำลังเล่นเพลง: {filename}")
            await ctx.send(f"เกิดข้อผิดพลาด: {e}")
            while vc.is_playing():
                await asyncio.sleep(1)

        except Exception as e:
            await ctx.send(f"เกิดข้อผิดพลาด: {e}")
    else:
        await ctx.send("คุณต้องอยู่ใน Voice Channel ก่อนใช้คำสั่งนี้!")

@bot.command(name="ตอบ")
async def botanswer(ctx):
    random.shuffle(answer)
    await ctx.send(answer[0])
    await ctx.message.delete()

@bot.command(name="ชม")
async def botcomplement(ctx):
    random.shuffle(complement)
    await ctx.send(complement[0])
    await ctx.message.delete()

@bot.command(name="ถาม")
async def botask(ctx):
    random.shuffle(ask)
    await ctx.send(ask[0])
    await ctx.message.delete()

@bot.command(name="ด่า")
async def botinsult(ctx):
    random.shuffle(insult)
    await ctx.send(insult[0])
    await ctx.message.delete()

@bot.command(name="ปลอบใจ")
async def bothelp(ctx):
    random.shuffle(help)
    await ctx.send(help[0])
    await ctx.message.delete()

@bot.command(name="ขอโทษ")
async def botsorry(ctx):
    random.shuffle(sorry)
    await ctx.send(sorry[0])
    await ctx.message.delete()

@bot.command(name="เสียใจ")
async def botsad(ctx):
    random.shuffle(sad)
    await ctx.send(sad[0])
    await ctx.message.delete()

@bot.command(name="เกลียด")
async def bothate(ctx):
    random.shuffle(hate)
    await ctx.send(hate[0])
    await ctx.message.delete()

@bot.command(name="สุ่ม")
async def botrandom(ctx):
    await ctx.send(random.randint(1, 10))
    await ctx.message.delete()
    
@bot.command(name="พูดerror")
async def tts(ctx, *, text: str):
    try:
        tts = gTTS(text=text, lang='th')
        tts.save("voice.mp3")

        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                vc = await channel.connect()
            else:
                vc = ctx.voice_client
                await vc.move_to(channel)

            if not vc.is_connected():
                await ctx.send("❌ บอทยังไม่ได้เชื่อมต่อ Voice Channel!")
                return

            vc.play(discord.FFmpegPCMAudio("voice.mp3"), after=lambda e: print("เล่นจบแล้ว"))
            await ctx.send(f"🎤 บอทกำลังพูด: {text}")
        else:
            await ctx.send("คุณต้องอยู่ใน Voice Channel ก่อนถึงจะใช้คำสั่งนี้ได้!")

    except Exception as e:
        await ctx.send(f"เกิดข้อผิดพลาด: {e}")
    finally:
        if os.path.exists("voice.mp3"):
            os.remove("voice.mp3")  # ลบไฟล์เสียงหลังจากเล่นเสร็จ
    
@bot.command(name="erroe")
async def play(ctx):
    if ctx.voice_client:
        source = discord.FFmpegPCMAudio("path/to/your/audio.mp3")
        ctx.voice_client.play(source)
        await ctx.send("🎶 กำลังเล่นเสียง...")
    else:
        await ctx.send("บอทยังไม่ได้เชื่อมต่อ Voice Channel!")

# 🟢 ฟังก์ชัน async สำหรับรัน 1 บอท
from dotenv import load_dotenv
load_dotenv()

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if token:
      asyncio.run(bot.start('MTM1OTg5NzM5NTIxOTEzNjU3Mg.GPQn8E.PlESsHVfgBAoG3neEkfiilvRbRaT8N_39FK9bg')),  # แทนที่ 'YOUR_BOT_TOKEN' ด้วย Token บอทตัวแรก
      bot.run('MTM1OTg5NzM5NTIxOTEzNjU3Mg.GPQn8E.PlESsHVfgBAoG3neEkfiilvRbRaT8N_39FK9bg')
    else:
        print("❌ ไม่พบ TOKEN")
    
if __name__ == "__main__":
    webserver.keep_alive()  # เรียกใช้งาน webserver เพื่อให้บอททำงานตลอดเวลา
    
       # ✅ ตัวอย่างที่แก้ปัญหา
    async def main():
        # Run your bot inside this async function
        await bot.start('MTM1OTg5NzM5NTIxOTEzNjU3Mg.GPQn8E.PlESsHVfgBAoG3neEkfiilvRbRaT8N_39FK9bg')  # Replace with your bot token
    
try:
    asyncio.run(main())
except KeyboardInterrupt:
  print(subprocess.getoutput("ffmpeg -version"))  # Ensure command matches ffmpeg installed version command
  print("ปิดบอทแล้ว")