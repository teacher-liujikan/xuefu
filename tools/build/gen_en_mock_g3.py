"""英語三年級 模擬卷 A（25 題，含聽力）：版面照 112～114 年（字母聽寫 1–15、聽辨語音 16–21、聽辨常用語 22–25）。
音檔用 Piper 語音合成（en_US amy），圖用表情符號字型排出。要在 gen_en_mock.py 之後執行。"""
import json,sys,subprocess,os
sys.path.insert(0,'/home/claude/work/audio/tts'); sys.path.insert(0,'/home/claude/work/zh')
from tts import build
from gen_en_mock import CSS,E,box
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='/home/claude/repo-xuefu/english/'
NUM=['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','twenty-one','twenty-two','twenty-three','twenty-four','twenty-five']
LET='WDHBMNPGJYSFRAI'
OX=[('cat','cup','k','k',1),('dog','bed','d','b',2),('pig','ten','p','t',2),('sun','six','s','s',1),('map','milk','m','m',1),('fox','box','f','b',2)]
PIC=[('Good morning.','早安！',[('🌅|👋','早上打招呼'),('🌙|😴','晚上睡覺'),('🎂|🥳','慶生')],1,'圖 (1) 太陽剛出來，女孩舉手打招呼，是早上說的話。','圖 (2) 是晚上睡覺，要說 Good night.（晚安）；圖 (3) 是慶生，要說 Happy birthday.（生日快樂）。',['🌅','🌙','🎂']),
     ('Raise your hand.','把手舉起來。',[('🧍','站著'),('🙋','舉手'),('🙇','鞠躬')],2,'圖 (2) 的人把手舉得高高的。','圖 (1) 只是站著，圖 (3) 是在鞠躬。',None),
     ('Be quiet.','安靜一點。',[('📣|😆','大聲喊'),('🎵|🎤','唱歌'),('🤫','比「噓」')],3,'圖 (3) 手指放在嘴巴前面比「噓」，請大家安靜。','圖 (1) 拿著大聲公在喊，圖 (2) 在唱歌。',None),
     ('Goodbye.','再見。',[('🙏','說謝謝'),('👋|🎒','揮手道別'),('🍽️|😋','吃飯')],2,'圖 (2) 背著書包揮手，要回家了，說再見。','圖 (1) 是在道謝，要說 Thank you.（謝謝）；圖 (3) 是在吃飯。',None)]
PICEN=[['morning（早上）','night（晚上）','birthday（生日）'],['stand（站）','hand（手）','bow（鞠躬）'],['shout（大叫）','sing（唱歌）','quiet（安靜的）'],['thank you（謝謝）','goodbye（再見）','eat（吃）']]
def mp3(parts,dst):
    wav=dst+'.wav'; build(parts,wav)
    subprocess.run(['ffmpeg','-v','error','-y','-i',wav,'-ac','1','-ar','22050','-b:a','40k',dst],check=True); os.remove(wav)
def pics_html(items):
    cells=''.join(f'<div class="cell" style="flex:1">({i+1}){box(''.join(E(x,90 if '|' not in e else 62) for x in e.split('|')),210,150,'flex-wrap:nowrap')}</div>' for i,(e,_) in enumerate(items))
    return f'<div class="q col"><div class="row">{cells}</div></div>'
def main():
    QS=json.load(open(OUT+'data/questions.json')); QS=[q for q in QS if not (q['grade']==3 and q['year']=='mA')]
    def num(n): return f'Number {NUM[n-1]}.'
    for n in range(1,16):
        L=LET[n-1]; aud=f'audio/g3-mA-{n}.mp3'; mp3([num(n),1.2,L+'.',2.0,L+'.',2.0,L+'.'],OUT+aud)
        QS.append(dict(id=f'g3-mA-{n}',grade=3,year='mA',no=n,audio=aud,listen=True,type='fill',stem='聽一聽，把聽到的字母寫出來：先寫大寫，再寫小寫。',blanks=[L,L.lower()],blabels=['大寫','小寫'],
            xf=['L-3-0'],sec='字母聽寫',ex=[f'音檔唸了三次字母 {L}。',f'大寫寫成 {L}，小寫寫成 {L.lower()}。','小心：大寫和小寫要分清楚，格子裡要分別寫。',f'所以答案是 {L}、{L.lower()}']))
    for i,(w1,w2,p,q,ans) in enumerate(OX):
        n=16+i; aud=f'audio/g3-mA-{n}.mp3'; mp3([num(n),1.2]+sum([[w1+'.',0.8,w2+'.',1.8] for _ in range(3)],[]),OUT+aud)
        ex=[f'音檔唸了兩個字：{w1} 和 {w2}。', f'{w1} 開頭的音是 {p}，{w2} 開頭的音是 {q}，不一樣。' if p!=q else f'{w1} 和 {w2} 開頭的音都是 {p}，一樣。']
        if (w1,w2)==('cat','cup'): ex.append('cat 的 c 唸 /k/，和 cup 的 c 一樣。')
        QS.append(dict(id=f'g3-mA-{n}',grade=3,year='mA',no=n,audio=aud,listen=True,type='choice',stem='聽兩個字：開頭的音一樣選 O，不一樣選 X。',options=['O','X'],answer=ans,xf=['L-3-1'],sec='聽辨語音',
            ex=ex+['開頭的音一樣選 O，不一樣選 X。',f"所以選 {'①②'[ans-1]} {'OX'[ans-1]}"]))
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={'width':900,'height':500},device_scale_factor=1.6)
        for i,(s,zh,items,ans,why,other,_) in enumerate(PIC):
            n=22+i; aud=f'audio/g3-mA-{n}.mp3'; mp3([num(n),1.2,s,2.2,s,2.2,s],OUT+aud)
            pg.set_content(f'<style>{CSS}</style>{pics_html(items)}'); pg.wait_for_timeout(80)
            name=f'img/g3-mA-{n}.png'; pg.query_selector('.q').screenshot(path=OUT+name)
            im=Image.open(OUT+name).convert('RGB'); im.quantize(96,method=Image.Quantize.MEDIANCUT).save(OUT+name,optimize=True)
            opts=[f'圖 ({k+1}) {d}' for k,(_,d) in enumerate(items)]
            QS.append(dict(id=f'g3-mA-{n}',grade=3,year='mA',no=n,audio=aud,listen=True,type='choice',stem='聽一句話，選出最適合的圖片。',options=opts,answer=ans,img=name,iw=im.width,ih=im.height,xf=['L-3-3'],sec='聽辨常用語',
                ex=[f'音檔唸的是：{s}（{zh}）',why,other,'三張圖的英文：'+'、'.join(f'圖 ({k+1}) {w}' for k,w in enumerate(PICEN[i])),f"所以選 {'①②③'[ans-1]} {opts[ans-1]}"]))
        b.close()
    json.dump(QS,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1); print('total',len(QS))
if __name__=='__main__': main()
