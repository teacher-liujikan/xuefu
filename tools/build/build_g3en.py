"""英語三年級（113、114）：字母聽寫 1–15、聽辨語音 16–21、聽辨常用語 22–25，每題附切好的音檔。"""
import json,re,os
from audio_cut import items,cut
OUT='/home/claude/repo-xuefu/english/'
SRC={'111':'/mnt/user-data/uploads/Downloads/11105_英語篩選測驗3年級紙本聽力檔.mp3','112':'/mnt/user-data/uploads/Downloads/11205_英語篩選測驗3年級紙本聽力檔.mp3','113':'/mnt/user-data/uploads/Downloads/113年篩選測驗英語科3年級試卷聽力檔.mp3','114':'/mnt/user-data/uploads/Downloads/114年篩選測驗英語科3年級試卷聽力檔.mp3'}
TR={'111':'/home/claude/work/audio/t3_111.json','112':'/home/claude/work/audio/t3_112.json','113':'/home/claude/work/audio/t113.json','114':'/home/claude/work/audio/t114.json'}
LET={'111':'DLIVYQJRN','112':'UYIFDLPHRNSZGEQ','113':'ZECHJKXMPQTRGVB','114':'VNJTCPFGSYUDQLH'}
OX={'111':[2,1,2,1,1],'112':[1,2,2,1,1,2],'113':[2,1,1,2,1,2],'114':[1,1,2,1,2,1]}          # 1=O 2=X
PIC={'111':[3,2,1],'112':[2,3,1,1],'113':[2,3,2,1],'114':[3,1,3,3]}
# 16–21：兩個字開頭的音（依音檔整理）
OXEX={'111':[('b','v','buff、vet'),('w','w','wet、weed'),('th','t','theme、tell'),('m','m','mill、mug'),('p','p','pit、pun')],
      '112':[('b','b','bam、boot'),('h','n','hug、nod'),('l','j','lap、jug'),('th','th','thin、thought'),('y','y','yem、yoke'),('sh','th','shell、thick')],
      '114':[('j','j',''),('sh','sh',''),('d','l',''),('h','h',''),('z','d',''),('th','th','')],
      '113':[('g','d',''),('m','m',''),('sh','sh',''),('f','v',''),('h','h',''),('s','ch','')]}
PICEX={'111':[('Close your book.','把書闔上。','圖 (3) 對話框裡的箭頭表示把書闔起來。','(1) 是舉手，(2) 是把書打開。'),
              ('Look!','你看！','圖 (2) 女孩拿著望遠鏡在看。','(1) 是在聽，(3) 是比讚。'),
              ('Stand up.','站起來。','圖 (1) 箭頭往上，男孩從椅子上站起來。','(2) 是坐下，(3) 是把書打開。')],
       '112':[('Be quiet.','安靜一點。','圖 (2) 寶寶在睡覺，女孩比「噓」請弟弟安靜。','(1) 是說好吃，(3) 是指著風箏叫人看。'),
              ('Listen.','仔細聽。','圖 (3) 男孩把手放在耳朵旁邊在聽。','(1) 是指著星星，(2) 是摸肚子。'),
              ('Sit down.','坐下。','圖 (1) 男孩的手往下比，小狗坐了下來。','(2) 小狗站起來，(3) 小狗躺在地上。'),
              ('Good morning!','早安！','圖 (1) 天上有太陽，是早上在打招呼。','(2) 是晚上，(3) 是在幫忙搬書。')],
       '114':[('Good job!','做得好！','圖 (3) 女孩摸摸小狗、稱讚牠。','(1) 女孩和小狗在拉扯，(2) 小狗對著女孩叫。'),
              ('Be quiet.','安靜一點。','圖 (1) 小男孩在旁邊敲鼓，爸爸在講電話，請他安靜。','(2) 小狗在睡覺，(3) 小狗在叫。'),
              ('Look!','你看！','圖 (3) 男孩指著地上的錢，叫朋友看。','(1) 鳥在叫，(2) 大家在看書。'),
              ('Open your book.','把書打開。','圖 (3) 箭頭表示把書翻開。','(1) 是打開盒子，(2) 是把書闔上。')],
       '113':[('Thank you.','謝謝你。','圖 (2) 男孩幫朋友包紮傷口，朋友向他道謝。','(1) 大家在打招呼，(3) 有人在咳嗽、打噴嚏。'),
              ('Close your book.','把書闔上。','圖 (3) 箭頭表示把書闔起來。','(1) 是把書打開，(2) 是把書收進書包。'),
              ('Sit down.','坐下。','圖 (2) 老師指著椅子，請男孩坐下。','(1) 是揮手，(3) 是把東西放下。'),
              ('Listen!','仔細聽！','圖 (1) 小朋友用紙杯電話聽對方說話。','(2) 是用望遠鏡看，(3) 是在說話、遞東西。')]}
IMGS=json.load(open('/home/claude/work/zh/g3en_imgs.json'))
AUDFIX={'111':{1:(106.0,124.8),2:(124.8,143.6),3:(143.6,162.3),10:(361.5,374.5),11:(374.5,386.9),13:(399.9,412.8),15:(452.8,465.7),16:(465.7,480.4),20:(617.4,634.3),21:(634.3,650.6)}}
# 每年的版面：(題號起, 題號迄, 類型)
LAY={'111':[(1,9,'dict'),(10,13,'let'),(14,16,'pic'),(17,21,'ox'),(22,25,'read')]}
LAYDEF=[(1,15,'dict'),(16,21,'ox'),(22,25,'pic')]
LETOPT={'111':{10:(['D','C','G'],2),11:(['T','E','F'],3),12:(['x','f','s'],1),13:(['v','n','u'],3)}}
READ={'111':{22:('T',['i','t','j'],2),23:('B',['d','p','b'],3),24:('h',['H','K','L'],1),25:('e',['F','I','E'],3)}}
def kind(y,n):
    for a,b,k in LAY.get(y,LAYDEF):
        if a<=n<=b: return k,n-a
def build(y,extra=None):
    segs=json.load(open(TR[y])); its={n:(a,b,body) for n,a,b,body in items(segs)}
    for n,(a,b) in AUDFIX.get(y,{}).items(): its[n]=(a,b,[])
    miss=[n for n in range(1,26) if n not in its and kind(y,n)[0]!='read']
    assert not miss,(y,'missing',miss)
    QS=[]
    for n in range(1,26):
        k,i=kind(y,n)
        if k=='read':
            up,opts,ans=READ[y][n]; other='大寫' if up.islower() else '小寫'; c=opts[ans-1]
            QS.append(dict(id=f'g3-{y}-{n}',grade=3,year=y,no=n,type='choice',stem=f'選出和 {up} 對應的{other}字母。',options=opts,answer=ans,ansSrc='self',xf=['R-3-0'],sec='辨識字母',
                ex=[f'{up} 的{other}是 {c}。','其他兩個是不同的字母。',f"所以選 {'①②③'[ans-1]} {c}"])); continue
        a,b,body=its[n]; aud=f'audio/g3-{y}-{n}.mp3'; cut(SRC[y],a,b,OUT+aud)
        base=dict(id=f'g3-{y}-{n}',grade=3,year=y,no=n,audio=aud,listen=True)
        if y in ('111','112'): base['ansSrc']='self'
        if k=='let':
            opts,ans=LETOPT[y][n]; c=opts[ans-1]
            QS.append(dict(base,type='choice',stem='聽一聽，選出聽到的字母。',options=opts,answer=ans,xf=['L-3-4'],sec='聽辨字母',
                ex=[f'音檔唸了三次字母 {c.upper()}。',f'選項裡的 {c} 就是這個字母。',f"所以選 {'①②③'[ans-1]} {c}"]))
        elif k=='dict':
            L=LET[y][i]
            QS.append(dict(base,type='fill',stem='聽一聽，把聽到的字母寫出來：先寫大寫，再寫小寫。',blanks=[L,L.lower()],blabels=['大寫','小寫'],
                xf=['L-3-0'],sec='字母聽寫',ex=[f'音檔唸了三次字母 {L}。',f'大寫寫成 {L}，小寫寫成 {L.lower()}。','小心：大寫和小寫要分清楚，格子裡要分別寫。',f'所以答案是 {L}、{L.lower()}']))
        elif k=='ox':
            ans=OX[y][i]; info=(OXEX.get(y) or [None]*6)[i]
            if info:
                p,q,eg=info
                ex=[f'音檔唸了兩個字{"（"+eg+"）" if eg else ""}。', f'第一個字開頭的音是 {p}，第二個字開頭的音是 {q}。' if p!=q else f'兩個字開頭的音都是 {p}。', '開頭的音一樣選 O，不一樣選 X。']
            else: ex=['音檔唸了兩個字，仔細聽兩個字開頭的音。','開頭的音一樣選 O，不一樣選 X。']
            QS.append(dict(base,type='choice',stem='聽兩個字：開頭的音一樣選 O，不一樣選 X。',options=['O','X'],answer=ans,xf=['L-3-1'],sec='聽辨語音',
                ex=ex+[f"所以選 {'①②'[ans-1]} {'OX'[ans-1]}"]))
        else:
            ans=PIC[y][i]; nm,w,h=IMGS[f'{y}-{n}']; info=(PICEX.get(y) or [None]*4)[i]
            ex=[f'音檔唸的是：{info[0]}（{info[1]}）',info[2],info[3]] if info else ['仔細聽音檔的句子，選出最符合的圖。']
            QS.append(dict(base,type='choice',stem='聽一句話，選出最適合的圖片。',options=['圖 (1)','圖 (2)','圖 (3)'],answer=ans,img='img/'+nm,iw=w,ih=h,xf=['L-3-3'],sec='聽辨常用語',
                ex=ex+[f"所以選 {'①②③'[ans-1]} 圖 ({ans})"]))
    return QS
if __name__=='__main__':
    Q=json.load(open(OUT+'data/questions.json')); Q=[q for q in Q if q['grade']!=3]
    for y in ('114','113','112','111'):
        if os.path.exists(TR[y]): Q+=build(y); print('g3',y,'ok')
    json.dump(Q,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1); print(len(Q))
