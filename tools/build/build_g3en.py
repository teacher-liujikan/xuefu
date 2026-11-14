"""英語三年級（113、114）：字母聽寫 1–15、聽辨語音 16–21、聽辨常用語 22–25，每題附切好的音檔。"""
import json,re,os
from audio_cut import items,cut
OUT='/home/claude/repo-xuefu/english/'
SRC={'113':'/mnt/user-data/uploads/Downloads/113年篩選測驗英語科3年級試卷聽力檔.mp3','114':'/mnt/user-data/uploads/Downloads/114年篩選測驗英語科3年級試卷聽力檔.mp3'}
TR={'113':'/home/claude/work/audio/t113.json','114':'/home/claude/work/audio/t114.json'}
LET={'113':'ZECHJKXMPQTRGVB','114':'VNJTCPFGSYUDQLH'}
OX={'113':[2,1,1,2,1,2],'114':[1,1,2,1,2,1]}          # 1=O 2=X
PIC={'113':[2,3,2,1],'114':[3,1,3,3]}
# 16–21：兩個字開頭的音（依音檔整理）
OXEX={'114':[('j','j',''),('sh','sh',''),('d','l',''),('h','h',''),('z','d',''),('th','th','')],
      '113':[('g','d',''),('m','m',''),('sh','sh',''),('f','v',''),('h','h',''),('s','ch','')]}
PICEX={'114':[('Good job!','做得好！','圖 (3) 女孩摸摸小狗、稱讚牠。','(1) 女孩和小狗在拉扯，(2) 小狗對著女孩叫。'),
              ('Be quiet.','安靜一點。','圖 (1) 小男孩在旁邊敲鼓，爸爸在講電話，請他安靜。','(2) 小狗在睡覺，(3) 小狗在叫。'),
              ('Look!','你看！','圖 (3) 男孩指著地上的錢，叫朋友看。','(1) 鳥在叫，(2) 大家在看書。'),
              ('Open your book.','把書打開。','圖 (3) 箭頭表示把書翻開。','(1) 是打開盒子，(2) 是把書闔上。')],
       '113':[('Thank you.','謝謝你。','圖 (2) 男孩幫朋友包紮傷口，朋友向他道謝。','(1) 大家在打招呼，(3) 有人在咳嗽、打噴嚏。'),
              ('Close your book.','把書闔上。','圖 (3) 箭頭表示把書闔起來。','(1) 是把書打開，(2) 是把書收進書包。'),
              ('Sit down.','坐下。','圖 (2) 老師指著椅子，請男孩坐下。','(1) 是揮手，(3) 是把東西放下。'),
              ('Listen!','仔細聽！','圖 (1) 小朋友用紙杯電話聽對方說話。','(2) 是用望遠鏡看，(3) 是在說話、遞東西。')]}
IMGS=json.load(open('/home/claude/work/zh/g3en_imgs.json'))
def build(y,extra=None):
    segs=json.load(open(TR[y])); its={n:(a,b,body) for n,a,b,body in items(segs)}
    miss=[n for n in range(1,26) if n not in its]
    assert not miss,(y,'missing',miss)
    QS=[]
    for n in range(1,26):
        a,b,body=its[n]; aud=f'audio/g3-{y}-{n}.mp3'; cut(SRC[y],a,b,OUT+aud)
        base=dict(id=f'g3-{y}-{n}',grade=3,year=y,no=n,audio=aud,listen=True)
        if n<=15:
            L=LET[y][n-1]
            QS.append(dict(base,type='fill',stem='聽一聽，把聽到的字母寫出來：先寫大寫，再寫小寫。',blanks=[L,L.lower()],blabels=['大寫','小寫'],
                xf=['L-3-0'],sec='字母聽寫',ex=[f'音檔唸了三次字母 {L}。',f'大寫寫成 {L}，小寫寫成 {L.lower()}。','小心：大寫和小寫要分清楚，格子裡要分別寫。',f'所以答案是 {L}、{L.lower()}']))
        elif n<=21:
            k=n-16; ans=OX[y][k]; info=(OXEX.get(y) or [None]*6)[k]
            if info:
                p,q,eg=info
                ex=[f'音檔唸了兩個字{"（"+eg+"）" if eg else ""}。', f'第一個字開頭的音是 {p}，第二個字開頭的音是 {q}。' if p!=q else f'兩個字開頭的音都是 {p}。', '開頭的音一樣選 O，不一樣選 X。']
            else: ex=['音檔唸了兩個字，仔細聽兩個字開頭的音。','開頭的音一樣選 O，不一樣選 X。']
            QS.append(dict(base,type='choice',stem='聽兩個字：開頭的音一樣選 O，不一樣選 X。',options=['O','X'],answer=ans,xf=['L-3-1'],sec='聽辨語音',
                ex=ex+[f"所以選 {'①②'[ans-1]} {'OX'[ans-1]}"]))
        else:
            k=n-22; ans=PIC[y][k]; nm,w,h=IMGS[f'{y}-{n}']; info=(PICEX.get(y) or [None]*4)[k]
            ex=[f'音檔唸的是：{info[0]}（{info[1]}）',info[2],info[3]] if info else ['仔細聽音檔的句子，選出最符合的圖。']
            QS.append(dict(base,type='choice',stem='聽一句話，選出最適合的圖片。',options=['圖 (1)','圖 (2)','圖 (3)'],answer=ans,img='img/'+nm,iw=w,ih=h,xf=['L-3-3'],sec='聽辨常用語',
                ex=ex+[f"所以選 {'①②③'[ans-1]} 圖 ({ans})"]))
    return QS
if __name__=='__main__':
    Q=json.load(open(OUT+'data/questions.json')); Q=[q for q in Q if q['grade']!=3]
    for y in ('114','113'):
        if os.path.exists(TR[y]): Q+=build(y); print('g3',y,'ok')
    json.dump(Q,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1); print(len(Q))
