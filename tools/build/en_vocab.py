"""英語詳解加「單字」：在每題詳解最後一行前加一行單字表；發音題加「放進去唸唸看」。可重複執行。"""
import json,re,sys
sys.path.insert(0,'/home/claude/work/zh'); from en_tr import TR
P='/home/claude/repo-xuefu/english/data/questions.json'
GL=dict(x.split(':') for x in """apple:蘋果 apples:蘋果 art:美術 bag:袋子 banana:香蕉 bananas:香蕉 bathroom:浴室 bed:床 bedroom:臥室 big:大的 bike:腳踏車 bird:鳥 birds:鳥
black:黑色 blue:藍色 book:書 books:書 bookstore:書店 box:盒子 boy:男孩 brother:哥哥／弟弟 bus:公車 cake:蛋糕 car:汽車 cars:汽車 cat:貓 chinese:國語 close:關上 cold:冷的
color:顏色 come:來 cook:廚師 cool:涼爽的 dance:跳舞 dancing:跳舞 doctor:醫生 dog:狗 dogs:狗 doing:做 down:向下 draw:畫畫 drawing:畫畫 dress:洋裝 ear:耳朵 ears:耳朵 eat:吃 eating:吃
egg:蛋 eggs:蛋 eight:8 eleven:11 english:英語 exit:出口 eye:眼睛 eyes:眼睛 father:爸爸 fish:魚 five:5 fly:飛 flying:飛 four:4 girl:女孩 going:去 good:好的 green:綠色
hamburger:漢堡 hand:手 happy:開心的 have:有 head:頭 heads:頭 here:這裡 home:家 hot:熱的 how:怎樣 hurry:趕快 jacket:外套 job:工作 juice:果汁 kitchen:廚房 know:知道 late:遲到的
like:喜歡 line:排隊 lion:獅子 listen:聽 living:客廳（living-room） long:長的 look:看 lunch:午餐 marker:彩色筆 math:數學 milk:牛奶 morning:早上 mother:媽媽 mouth:嘴巴 mouths:嘴巴
music:音樂 name:名字 nine:9 no:不 nose:鼻子 not:不是 nurse:護理師 old:老的；…歲 one:1 open:打開 out:外面 park:公園 pen:原子筆 pencil:鉛筆 pie:派 pies:派 pig:豬 pizza:披薩 pizzas:披薩
play:玩 playing:玩 put:放 quiet:安靜的 rabbit:兔子 rabbits:兔子 rainy:下雨的 read:讀 reading:讀 ready:準備好的 red:紅色 rice:飯 ride:騎 riding:騎 ruler:尺 sad:難過的 school:學校
see:看到 seven:7 shoe:鞋子 short:矮的；短的 sing:唱歌 singing:唱歌 sister:姐姐／妹妹 sit:坐 six:6 skirt:裙子 sleep:睡覺 sleeping:睡覺 small:小的 sorry:對不起 stand:站 student:學生
sunny:晴天的 supermarket:超級市場 swim:游泳 swimming:游泳 tall:高的 tea:茶 teacher:老師 ten:10 thank:謝謝 three:3 tiger:老虎 time:時間 tired:累的 tv:電視 twelve:12 two:2 under:在…下面
up:向上 walk:走路 want:想要 warm:溫暖的 watch:看 watching:看 water:水 weather:天氣 welcome:歡迎 white:白色 worry:擔心 write:寫 writing:寫 wrong:錯的 year:年 years:年 yellow:黃色
yes:是 zoo:動物園 can:會 can't:不會 don't:不 this:這個 that:那個 what:什麼 where:哪裡 he:他 she:她 in:在…裡面 on:在…上面 t-shirt:T恤 my:我的 your:你的 thin:瘦的 fat:胖的
o'clock:…點鐘 sky:天空 hat:帽子 cup:杯子 fan:電扇 desk:書桌 chair:椅子 window:窗戶 door:門 thank-you:謝謝 taiwan:臺灣 let's:我們來… bear:熊 monkey:猴子 elephant:大象 duck:鴨子
cow:牛 horse:馬 run:跑 jump:跳 cry:哭 cloudy:陰天的 windy:颳風的 snowy:下雪的 day:天 night:晚上 face:臉 arm:手臂 leg:腿 foot:腳 sun:太陽 moon:月亮 star:星星 tree:樹 flower:花
house:房子 room:房間 bread:麵包 cookie:餅乾 candy:糖果 orange:柳橙；橘色 grape:葡萄 grapes:葡萄 hungry:餓的 thirsty:口渴的 sick:生病的 angry:生氣的 boat:船 train:火車 plane:飛機
ball:球 kite:風箏 doll:娃娃 robot:機器人 brown:咖啡色 pink:粉紅色 purple:紫色 gray:灰色 grandpa:爺爺 grandma:奶奶 baby:寶寶 friend:朋友 man:男人 woman:女人 family:家人
basketball:籃球 baseball:棒球 jog:慢跑 cut:剪；切 wash:洗 clean:乾淨的；打掃 nice:好的 fine:很好的 great:很棒的 hello:哈囉 hi:嗨 bye:再見 goodbye:再見 please:請 meet:見面
sit-down:坐下 stand-up:站起來 there:那裡 who:誰 old-:老 eraser:橡皮擦 crayon:蠟筆 notebook:筆記本 lamp:燈 sofa:沙發 table:桌子 clock:時鐘 phone:電話 computer:電腦 cap:帽子
sweater:毛衣 shorts:短褲 pants:長褲 socks:襪子 coat:大衣 umbrella:雨傘 hospital:醫院 library:圖書館 store:商店 restaurant:餐廳 police:警察 farmer:農夫 driver:司機 singer:歌手
dancer:舞者 cook-:廚師 hen:母雞 frog:青蛙 ant:螞蟻 bee:蜜蜂 sheep:羊 goat:山羊 mouse:老鼠 panda:貓熊 koala:無尾熊 zebra:斑馬 giraffe:長頸鹿 away:離開（put-away＝收起來） having:吃；有""".split())
STOP=set('a an the is are am it it\'s i i\'m you you\'re he\'s she\'s that\'s what\'s how\'s let\'s do to and but me his her its they we our of for at with be not'.split())-{'not'}
STOP|={'not','o\'clock','my','your','ing'}
EXP={"it's":[],"what's":['what'],"that's":['that'],"he's":['he'],"she's":['she'],"i'm":[],"you're":[],"how's":['how'],"let's":["let's"],"can't":["can't"],"don't":["don't"]}
NAMES={'amy','ann','ben','bob','jack','john','ken','mary','tom','ivy','sam','black','lion'}
def words(text):
    out=[]
    for w in re.findall(r"[A-Za-z][A-Za-z'\-]*",text):
        lw=w.lower()
        if lw in EXP: out+=EXP[lw]; continue
        out.append(lw)
    return out
def eng_parts(line):
    # 只取句子中的英文片段（中文說明裡夾的英文）
    return ' '.join(re.findall(r"[A-Za-z][A-Za-z'\-\.,!? ]*",line))
missing={}
DISP={'tv':'TV','t-shirt':'T-shirt','chinese':'Chinese','english':'English','taiwan':'Taiwan'}
def vocab(q):
    src=[]
    for l in q['ex'][:-1]: src+=words(eng_parts(l))
    for o in q.get('options',[]) or []:
        if isinstance(o,str) and re.match(r'^[A-Za-z]',o): src+=words(o)
    seen=[];
    for w in src:
        if w in STOP or w in seen: continue
        if w in GL: seen.append(w)
        elif len(w)>2 and w not in NAMES: missing.setdefault(w,q['id'])
    return seen
def phon(q):
    opts=q['options']; ans=q['answer']; m=re.search(r'音檔唸的是 ([a-z]+)',q['ex'][0])
    if not m: return None
    heard=m.group(1); o=opts[ans-1]
    i=heard.find(o)
    if i<0: return None
    pre,post=heard[:i],heard[i+len(o):]
    combos=[f'{pre}{"＋" if pre else ""}{x}{"＋" if post else ""}{post}＝{pre}{x}{post}' for x in opts]
    return f"把三個選項放進去唸唸看：{'、'.join(combos)}。和音檔一樣的是 {heard}。"
def run():
    Q=json.load(open(P)); n1=n2=0
    for q in Q:
        if not q.get('ex'): continue
        q['ex']=[l for l in q['ex'] if not l.startswith(('📖 單字：','把三個選項放進去唸唸看','三個選項的意思：','選項①','選項②','選項③'))]
        opts=q.get('options') or []
        if q.get('sec')=='字母聽寫' or q.get('type')!='choice': continue
        if opts and all(isinstance(o,str) and re.fullmatch(r'[a-z]{1,4}',o) for o in opts):   # 發音題
            l=phon(q)
            if l: q['ex'].insert(len(q['ex'])-1,l); n2+=1
            continue
        if opts==['O','X'] or q.get('sec') in ('聽辨字母','辨識字母'): continue
        # 辨識單字（選項是單字、詳解已逐一說明）不重複
        if opts and all(isinstance(o,str) and re.fullmatch(r"[A-Za-z\- ]+",o) and len(o.split())<=3 for o in opts) and not q.get('audio'): continue
        if opts and all(o in TR for o in opts):
            for i,o in reversed(list(enumerate(opts))): q['ex'].insert(0,f"選項{'①②③'[i]} {o}（{TR[o]}）")
        elif opts and any(isinstance(o,str) and re.match(r'^[A-Z]',o) and len(o.split())>=2 for o in opts): print('noTR',q['id'],[o for o in opts if o not in TR])
        v=vocab(q)
        if v: q['ex'].insert(len(q['ex'])-1,'📖 單字：'+'、'.join(f'{DISP.get(w,w)}（{GL[w]}）' for w in v)); n1+=1
    json.dump(Q,open(P,'w'),ensure_ascii=False,indent=1)
    print('vocab',n1,'phon',n2); print('missing',missing)
if __name__=='__main__': run()
