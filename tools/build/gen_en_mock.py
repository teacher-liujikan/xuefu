#!/usr/bin/env python3
"""英語閱讀 模擬卷 A（四～六年級，各 15 題）：照 113、114 年篩選測驗閱讀題的題型自編，圖用表情符號字型排出來。"""
import json, sys, os
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='/home/claude/repo-xuefu/english/'
def E(ch,size=110,style=''): return f'<span class="em" style="font-size:{size}px;{style}">{ch}</span>'
def box(inner,w=230,h=190,style=''): return f'<div class="pic" style="width:{w}px;height:{h}px;flex:none;{style}">{inner}</div>'
ARROW='<span class="ar">➜</span>'
def near(obj): return box(f'<div style="position:relative;width:180px;height:170px">{E(obj,96,"position:absolute;left:62px;top:0")}{E("👆",64,"position:absolute;left:40px;top:96px;transform:rotate(35deg)")}</div>',200,180)
def far(obj): return box(f'<div style="position:relative;width:180px;height:170px">{E(obj,44,"position:absolute;right:4px;top:0")}{E("👉",64,"position:absolute;left:6px;top:96px;transform:rotate(-38deg)")}<span style="position:absolute;left:78px;top:70px;font-size:26px;color:#888;transform:rotate(-38deg);letter-spacing:6px">· · ·</span></div>',200,180)
def sw(c,border='#222'): return box(f'<span style="display:block;width:120px;height:120px;border-radius:14px;background:{c};border:3px solid {border}"></span>')
def tbl(rows): return box('<table class="ox">'+''.join(f'<tr><td>{E(a,54)}</td><td class="m">{m}</td></tr>' for a,m in rows)+'</table>',190,60*len(rows)+20)
def W(pic,opts,ans,ex): return dict(k='W',pic=pic,opts=opts,ans=ans,ex=ex,tag='R1')
def S1(sent,pics,labels,ans,ex): return dict(k='S1',sent=sent,pics=pics,opts=labels,ans=ans,ex=ex,tag='R2')
def S2(pic,opts,ans,ex): return dict(k='S2',pic=pic,opts=opts,ans=ans,ex=ex,tag='R2')
def D(sent,opts,ans,ex): return dict(k='D',sent=sent,opts=opts,ans=ans,ex=ex,tag='R2')
G={}
G[4]=[
W(box(E('🍌')),['apple','banana','book'],2,['圖是一根香蕉。','香蕉是 banana。apple 是蘋果，book 是書。']),
W(box(E('🐦')),['bird','blue','book'],1,['圖是一隻鳥。','鳥是 bird。blue 是藍色，book 是書。三個字都是 b 開頭，要看清楚。']),
W(sw('#f6d21c'),['white','red','yellow'],3,['圖是黃色的色塊。','黃色是 yellow。white 是白色，red 是紅色。']),
W(box(E('📏')),['ruler','rabbit','red'],1,['圖是一把尺。','尺是 ruler。rabbit 是兔子，red 是紅色。']),
W(box(E('🐷')),['pig','dog','cat'],1,['圖是一隻豬。','豬是 pig。dog 是狗，cat 是貓。']),
W(box(E('✏️')),['pen','pencil','egg'],2,['圖是一枝鉛筆。','鉛筆是 pencil。pen 是原子筆，egg 是蛋。']),
W(box(E('🐈‍⬛')),['a black dog','a white cat','a black cat'],3,['圖是一隻黑色的貓。','black 是黑色，cat 是貓。dog 是狗，white 是白色。']),
S1(["It's a cake."],[box(E('🎂')),box(E('🥚')),box(E('🥛'))],['圖 (1) 蛋糕','圖 (2) 蛋','圖 (3) 牛奶'],1,["It's a cake. 意思是「它是蛋糕」。",'圖 (2) 是 egg（蛋），圖 (3) 是 milk（牛奶）。']),
S1(['A: What color is it?',"B: It's green."],[sw('#e03a2f'),sw('#2fa84f'),sw('#2f6fe0')],['圖 (1) 紅色','圖 (2) 綠色','圖 (3) 藍色'],2,['A 問：What color is it?（它是什麼顏色？）',"B 答：It's green.（它是綠色。）"]),
S1(["It's a book. It's blue."],[box(E('📕')),box(E('🐟')),box(E('📘'))],['圖 (1) 紅色的書','圖 (2) 藍色的魚','圖 (3) 藍色的書'],3,["It's a book.（它是書。）It's blue.（它是藍色的。）",'要找「藍色的書」。圖 (1) 是紅色的；圖 (2) 是藍色的，可是牠是魚。']),
S1(["A: What's that?","B: It's an apple."],[near('🍎'),far('🍎'),far('🍌')],['圖 (1) 摸著蘋果','圖 (2) 指著遠處的蘋果','圖 (3) 指著遠處的香蕉'],2,["A 問：What's that?（那是什麼？）that 是指遠的東西。","B 答：It's an apple.（是蘋果。）",'圖 (1) 手碰著蘋果，要用 this；圖 (3) 是香蕉。']),
S1(['A: Is this a tiger?',"B: No, it's not."],[near('🐯'),near('🦁'),far('🐯')],['圖 (1) 摸著老虎','圖 (2) 摸著獅子','圖 (3) 指著遠處的老虎'],2,['A 問：Is this a tiger?（這是老虎嗎？）this 是指近的東西。',"B 答：No, it's not.（不，牠不是。）",'要找「在手邊」而且「不是老虎」的圖。圖 (2) 手碰著的是獅子。']),
S2(box(E('🦁')),["It's a lion.","It's a tiger.","It's a rabbit."],1,['圖是一隻獅子，臉的四周有一圈毛。','獅子是 lion。tiger 是老虎，rabbit 是兔子。']),
S2(near('🐶'),["A: What's this?<br>B: It's a dog.","A: What's that?<br>B: It's a dog.","A: Is this a cat?<br>B: Yes, it is."],1,['圖裡的手碰著一隻狗，東西就在手邊，用 this。',"① What's this?（這是什麼？）It's a dog.（是狗。）對。",'② 用 that（那個），是指遠的東西。③ 說牠是貓，不對。']),
S2(box(E('📕')),["It's a book. It's blue.","It's red. It's not a book.","It's red. It's not an apple."],3,['圖是一本紅色的書。','① 說它是藍色的，不對。② 說它不是書，不對。',"③ It's red.（它是紅色的。）It's not an apple.（它不是蘋果。）兩句都對。"]),
]
def two(a,sa,b,sb,arrow=0,gap=18):
    ar=f'<span class="ar" style="position:absolute;top:-6px;left:{"8px" if arrow==0 else "auto"};right:{"8px" if arrow==1 else "auto"};transform:rotate(60deg)">➜</span>'
    return box(f'<div style="position:relative;display:flex;align-items:flex-end;gap:{gap}px;height:170px">{E(a,sa)}{E(b,sb)}{ar}</div>',240,200)
def many(ch,n,size): return box(''.join(E(ch,size) for _ in range(n)),210,110,'gap:2px')
G[5]=[
W(box('<span class="num">5</span>'),['four','five','nine'],2,['圖是數字 5。','5 是 five。four 是 4，nine 是 9。']),
W(box(E('🏊')),['swim','sing','see'],1,['圖裡的人在游泳。','游泳是 swim。sing 是唱歌，see 是看見。']),
W(box(E('🍚')),['juice','pizza','rice'],3,['圖是一碗飯。','飯是 rice。juice 是果汁，pizza 是披薩。']),
W(box(E('☀️',80)+E('🥵',100)),['cold','hot','tall'],2,['大太陽，臉都熱紅了、流汗了。','熱是 hot。cold 是冷，tall 是高。']),
W(box(E('👧')),['boy','brother','girl'],3,['圖是一個女孩。','女孩是 girl。boy 是男孩，brother 是哥哥或弟弟。']),
W(two('🦒',130,'🦒',60,arrow=0),['tall','thin','ten'],1,['箭頭指的是比較高的那隻長頸鹿。','高是 tall。thin 是瘦的，ten 是 10。']),
W(box(E('👧',100)+E('😢',70)),['a sad girl','a happy girl','a sad boy'],1,['圖是一個女孩，她在哭，很難過。','sad 是難過的，girl 是女孩。happy 是開心的，boy 是男孩。']),
S1(['A: What do you want?','B: I want tea.'],[box(E('🥛')),box(E('🍵')),box(E('🧃'))],['圖 (1) 牛奶','圖 (2) 茶','圖 (3) 果汁'],2,['A 問：What do you want?（你想要什麼？）','B 答：I want tea.（我想要茶。）','圖 (1) 是 milk（牛奶），圖 (3) 是 juice（果汁）。']),
S1(["It's seven o'clock."],[box(E('🕔')),box(E('🕖')),box(E('🕘'))],['圖 (1) 五點','圖 (2) 七點','圖 (3) 九點'],2,["It's seven o'clock. 意思是「現在七點」。",'seven 是 7。看短針：圖 (1) 是五點，圖 (3) 是九點。']),
S1(["A: How's the weather?","B: It's rainy."],[box(E('🌧️')),box(E('☀️')),box(E('❄️'))],['圖 (1) 下雨','圖 (2) 晴天','圖 (3) 下雪'],1,["A 問：How's the weather?（天氣怎麼樣？）","B 答：It's rainy.（下雨。）",'圖 (2) 是 sunny（晴天）。']),
S1(["My sister can dance. She can't swim."],[tbl([('💃','✕'),('🏊','○')]),tbl([('🎤','○'),('🏊','✕')]),tbl([('💃','○'),('🏊','✕')])],['圖 (1) 跳舞 ✕、游泳 ○','圖 (2) 唱歌 ○、游泳 ✕','圖 (3) 跳舞 ○、游泳 ✕'],3,['My sister can dance.（我的姐姐／妹妹會跳舞。）','She can\'t swim.（她不會游泳。）','can 是「會」，畫 ○；can\'t 是「不會」，畫 ✕。要找跳舞 ○、游泳 ✕。']),
S1(['I see three big dogs.'],[many('🐕',2,70),many('🐕',3,36),many('🐕',3,64)],['圖 (1) 兩隻大狗','圖 (2) 三隻小狗','圖 (3) 三隻大狗'],3,['I see three big dogs.（我看到三隻大狗。）','three 是 3，big 是大的。圖 (1) 只有兩隻，圖 (2) 是小狗。']),
S2(box(E('❄️',80)+E('🥶',100)),["It's hot.","It's cold.","It's sunny."],2,['圖裡在下雪，臉都凍僵了。',"② It's cold.（天氣很冷。）對。",'hot 是熱，sunny 是晴天。']),
S2(box('<div style="display:flex;flex-direction:column;align-items:center;gap:4px"><div>'+E('👦',84)+E('📖',64)+'</div><span class="cake"><b>8</b>'+E('🎂',60)+'</span></div>',230,225),['The boy is eight years old. He can read.','The girl is eight years old. She can read.','The boy is ten years old. He can sing.'],1,['圖裡是一個男孩在看書，生日蛋糕上面的數字是 8，表示他八歲。','② 說的是女孩（girl），不對。③ 說十歲、會唱歌，不對。','① The boy is eight years old.（男孩八歲。）He can read.（他會讀書。）對。']),
S2(box(E('☀️',64)+E('🕙',64)+E('👧',76)+E('😀',56),230,200,'flex-wrap:wrap'),["It's rainy. The girl is happy.","It's ten o'clock. The girl is sad.","It's sunny. The girl is happy."],3,['圖裡有太陽，時鐘是十點，女孩很開心。','① 說下雨（rainy），不對。② 說女孩很難過（sad），不對。',"③ It's sunny.（晴天。）The girl is happy.（女孩很開心。）對。"]),
]
def stack(top,mid,bot,ts=64,ms=110,bs=56):
    return box(f'<div style="display:flex;flex-direction:column;align-items:center;line-height:1">{E(top,ts) if top else ""}{E(mid,ms)}{E(bot,bs) if bot else ""}</div>',230,250 if (top and bot) else 215)
G[6]=[
W(box(E('🚴')),['ride','walk','eat'],1,['圖裡的人在騎腳踏車。','騎是 ride。walk 是走路，eat 是吃。']),
W(box(E('👃')),['ear','mouth','nose'],3,['圖是鼻子。','鼻子是 nose。ear 是耳朵，mouth 是嘴巴。']),
W(box(E('👕')),['jacket','T-shirt','dress'],2,['圖是一件 T 恤。','T 恤是 T-shirt。jacket 是外套，dress 是洋裝。']),
W(box(E('🎨')),['math','music','art'],3,['圖是調色盤和畫筆，是美術課用的。','美術是 art。math 是數學，music 是音樂。']),
W(box(E('👩‍🏫')),['teacher','cook','student'],1,['圖裡的人站在黑板前面上課，她是老師。','老師是 teacher。cook 是廚師，student 是學生。']),
W(box(E('🛏️')),['kitchen','bedroom','bathroom'],2,['圖是一張床，有床的房間是臥室。','臥室是 bedroom。kitchen 是廚房，bathroom 是浴室。']),
W(two('🚌',120,'🚌',56,arrow=1),['a long bus','a small box','a small bus'],3,['箭頭指的是比較小的那輛公車。','small 是小的，bus 是公車。long 是長的，box 是盒子。']),
D(['A: Where is your mother?','B: ______________'],["She's a nurse.","She's in the kitchen.","She's tall."],2,['A 問：Where is your mother?（你的媽媽在哪裡？）','Where 是問「地方」。',"② She's in the kitchen.（她在廚房。）是地方。",'① 是職業，③ 是身高，都不是地方。']),
D(['A: What is she doing?','B: ______________'],["She's watching TV.","She's a teacher.","She's at school."],1,['A 問：What is she doing?（她正在做什麼？）','問「正在做什麼」，要回答動作，用 -ing。',"① She's watching TV.（她在看電視。）對。",'② 是職業，③ 是地方，都不是動作。']),
D(['A: Do you like music?','B: ______________'],['Yes. I like math.','No. I can sing.','Yes. I like music.'],3,['A 問：Do you like music?（你喜歡音樂嗎？）','① 回答 Yes，後面卻說喜歡數學，前後不合。② can sing 是「會唱歌」，沒有回答喜不喜歡。','③ Yes. I like music.（是的，我喜歡音樂。）前後合理。']),
S2(stack('🐱','📦',None,70,120),['The cat is in the box.','The cat is on the box.','The cat is under the box.'],2,['圖裡的貓在盒子的上面。','on 是「在……上面」。in 是「在……裡面」，under 是「在……下面」。']),
S2(box('<div style="display:flex;flex-direction:column;align-items:center">'+E('👨‍🍳',110)+'<span class="tag">Sam</span></div>'+E('🍳',60),230,200),['He is Sam. He is a cook.','He is Tom. He is a cook.','He is Sam. He is a teacher.'],1,['圖裡的人戴著廚師帽，名牌寫 Sam。','② 名字不對，他是 Sam，不是 Tom。③ 他是廚師（cook），不是老師（teacher）。','① He is Sam. He is a cook.（他是 Sam，他是廚師。）對。']),
S2(tbl([('🎵','○'),('🔢','✕'),('🎨','○')]),["I like math. I don't like art.","I like music. I don't like math.","I don't like music. I like art."],2,['看表格：音樂是 ○（喜歡），數學是 ✕（不喜歡），美術是 ○（喜歡）。','① 說喜歡數學，不對。③ 說不喜歡音樂，不對。',"② I like music.（我喜歡音樂。）I don't like math.（我不喜歡數學。）對。"]),
S2(box(E('🕗',70)+'<div style="display:flex;align-items:flex-end;gap:6px">'+E('🚶‍♀️',76,'transform:scaleX(-1)')+'<span class="ar" style="font-size:34px">➜</span>'+E('🏫',76)+'</div>',230,200,'flex-direction:column'),["It's eight o'clock. The girl is going to school.","It's eight o'clock. The girl is in the kitchen.","It's six o'clock. The girl is going to the zoo."],1,['時鐘是八點，女孩正走向學校。','② 她不是在廚房。③ 時間不是六點，她也不是要去動物園（zoo）。',"① It's eight o'clock.（八點了。）The girl is going to school.（女孩正要去學校。）對。"]),
S2(stack('👗','🛏️','👟',64,130,50),['I have a dress. It\'s under the bed.','I have a jacket. It\'s on the bed.','I have a dress. It\'s on the bed.'],3,['圖裡洋裝在床的上面，鞋子在床的下面。','① 洋裝不是在床下（under）。② 床上的是洋裝，不是外套（jacket）。',"③ I have a dress.（我有一件洋裝。）It's on the bed.（它在床上。）對。"]),
]
CSS='''*{box-sizing:border-box}body{margin:0;background:#fff;font-family:"DejaVu Sans","Noto Sans",sans-serif;color:#111}
.em{font-family:"Noto Color Emoji";line-height:1.05}
.q{display:flex;gap:26px;padding:10px 12px;align-items:flex-start;width:680px}
.q.col{flex-direction:column;gap:10px}
.pic{display:flex;align-items:center;justify-content:center;gap:6px}
.opts{display:flex;flex-direction:column;gap:14px;font-size:27px;padding-top:6px}
.opts.sm{font-size:23px;gap:14px;flex:1}
.opts div{display:flex;gap:8px}.opts i{font-style:normal;font-family:"DejaVu Serif",serif}
.sent{font-size:26px;line-height:1.55}
.row{display:flex;gap:10px}.cell{display:flex;flex-direction:column;align-items:center;font-size:24px;font-family:"DejaVu Serif",serif;gap:2px}
.num{font-size:150px;font-family:"DejaVu Serif",serif;line-height:1}
.ar{font-size:46px;color:#111;font-family:"DejaVu Sans"}
table.ox{border-collapse:collapse}table.ox td{border:2.5px solid #222;padding:2px 14px;text-align:center}table.ox td.m{font-size:38px;font-weight:700;font-family:"DejaVu Sans"}
.cake{position:relative;display:inline-flex;align-items:center}.cake{flex-direction:column}.cake b{font-size:40px;font-family:"DejaVu Serif",serif;line-height:1;color:#c62a1f;margin:0}
.tag{border:2px solid #222;border-radius:6px;padding:0 10px;font-size:22px;margin-top:-6px;background:#fff}'''
def html(q):
    o=lambda sm='':'<div class="opts'+sm+'">'+''.join(f'<div><i>({i+1})</i><span>{t}</span></div>' for i,t in enumerate(q['opts']))+'</div>'
    if q['k']=='W': return f'<div class="q">{q["pic"]}{o()}</div>'
    if q['k']=='S2': return f'<div class="q">{q["pic"]}{o(" sm")}</div>'
    if q['k']=='D': return f'<div class="q col"><div class="sent">{"<br>".join(q["sent"])}</div>{o()}</div>'
    cells=''.join(f'<div class="cell" style="flex:1">({i+1}){p}</div>' for i,p in enumerate(q['pics']))
    return f'<div class="q col"><div class="sent">{"<br>".join(q["sent"])}</div><div class="row">{cells}</div></div>'
def main():
    QS=json.load(open(OUT+'data/questions.json')); QS=[q for q in QS if q['year']!='mA']
    import re
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':900,'height':700},device_scale_factor=1.6)
        for g,qs in G.items():
            assert len(qs)==15
            from collections import Counter; print(g,Counter(q['ans'] for q in qs))
            for n,q in enumerate(qs,1):
                pg.set_content(f'<style>{CSS}</style>{html(q)}'); pg.wait_for_timeout(60)
                name=f'img/g{g}-mA-{n}.png'; pg.query_selector('.q').screenshot(path=OUT+name)
                im=Image.open(OUT+name).convert('RGB'); im.quantize(96,method=Image.Quantize.MEDIANCUT).save(OUT+name,optimize=True)
                opts=[re.sub(r'<br>',' / ',t) for t in q['opts']]
                ex=q['ex']+[f"所以選 {'①②③'[q['ans']-1]} {opts[q['ans']-1]}"]
                QS.append(dict(id=f'g{g}-mA-{n}',grade=g,year='mA',no=n,type='choice',stem='',options=opts,answer=q['ans'],img=name,iw=im.width,ih=im.height,xf=[f"R-{g}-{q['tag'][1]}"],listen=False,sec='辨識單字' if q['tag']=='R1' else '辨識句子',ex=ex))
        b.close()
    json.dump(QS,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1); print('total',len(QS))
if __name__=='__main__': main()
