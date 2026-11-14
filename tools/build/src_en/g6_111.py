import sys; sys.path.insert(0,'/home/claude/work/zh/src_en')
from rd_helpers import W,S
OPT={11:['brother','student','doctor'],12:['ride','walk','watch'],13:['Chinese','English','math'],14:['car','bus','cat'],15:['supermarket','school','home'],16:['bag','box','TV'],17:['short','long','tall'],
18:["She's in the park.",'She can sing.',"She's flying."],19:['I have a T-shirt.',"It's a small T-shirt.","It's in the bathroom."],20:['Yes, I can draw.','No, I like math.',"No, I can't."],
21:["She's playing.","She's at home.","She's sad."],22:['I see two big heads.','I see two small ears.','I see three small eyes.'],23:["He's a doctor. He's reading.","He's a teacher. He's reading.","He's a doctor. He's drawing."],24:["I have a lion. It's in the living room.","I have a cat. It's under the skirt.","I see a lion. It's sleeping."],25:["I don't like art. I like math.","I don't like math. I like art.","I don't like art. I like Chinese."]}
ANS={11:2,12:3,13:2,14:1,15:1,16:3,17:2,18:3,19:3,20:2,21:1,22:3,23:1,24:2,25:3}
G={'brother':'哥哥／弟弟','student':'學生','doctor':'醫生','ride':'騎','walk':'走路','watch':'看','Chinese':'國語','English':'英語','math':'數學','car':'汽車','bus':'公車','cat':'貓','supermarket':'超級市場','school':'學校','home':'家','bag':'袋子','box':'盒子','TV':'電視','short':'短的','long':'長的','tall':'高的'}
EX={
11:W('女孩穿著制服、背著書包，她是學生。',2,OPT[11],G),
12:W('男孩拿著望遠鏡在看。',3,OPT[12],G),
13:W('箭頭圈起來的是英文字 EXIT（出口）。',2,OPT[13],G),
14:W('圖是一輛汽車。',1,OPT[14],G),
15:W('女人推著購物車買蔬果，這裡是超級市場。',1,OPT[15],G),
16:W('圖是電視和遙控器。',3,OPT[16],G),
17:W('箭頭指的是比較長的那把尺。',2,OPT[17],G),
18:S(['A 問：What is she doing?（她正在做什麼？）','問「正在做什麼」，要回答動作，用 -ing。',"③ She's flying.（她在飛。）是動作。",'① 是地方，② 是會不會，都沒有回答正在做什麼。'],3,OPT[18][2]),
19:S(['A 問：Where is my T-shirt?（我的 T 恤在哪裡？）','Where 是問地方。',"③ It's in the bathroom.（在浴室裡。）是地方。",'①② 都沒有說在哪裡。'],3,OPT[19][2]),
20:S(['A 問：Do you like music?（你喜歡音樂嗎？）','② No, I like math.（不，我喜歡數學。）有回答喜不喜歡。','① 和 ③ 是在說會不會（can），沒有回答喜不喜歡。'],2,OPT[20][1]),
21:S(['女孩在海邊開心的堆沙堡。',"① She's playing.（她在玩。）對。",'② 她不在家，③ 她並不難過。'],1,OPT[21][0]),
22:S(['放大鏡裡的外星人有一個頭、三個小眼睛。','① 不是兩個頭，② 看不到耳朵。','③ I see three small eyes.（我看到三個小眼睛。）對。'],3,OPT[22][2]),
23:S(['圖裡的人戴著口罩、掛著聽診器，在看手上的板子。','② 他不是老師，③ 他沒有在畫畫。',"① He's a doctor.（他是醫生。）He's reading.（他在看東西。）對。"],1,OPT[23][0]),
24:S(['電視上有一隻獅子，地上有一隻貓躲在裙子下面睡覺。','① 和 ③ 的獅子只是在電視上，不在客廳，也沒有在睡覺。',"② I have a cat.（我有一隻貓。）It's under the skirt.（牠在裙子下面。）對。"],2,OPT[24][1]),
25:S(['看表格：數學 ✕、國語 ♥、美術 ✕。','① 說喜歡數學，② 說喜歡美術，都不對。',"③ I don't like art.（我不喜歡美術。）I like Chinese.（我喜歡國語。）對。"],3,OPT[25][2]),
}
OPT.update({1:['od','ude','ode'],2:['ep','eep','ipe'],3:['ate','ea','ay'],
4:['圖 (1) 在黑板寫字','圖 (2) 在黑板畫畫','圖 (3) 看書'],5:['圖 (1) 書店','圖 (2) 超級市場','圖 (3) 學校'],6:['圖 (1) 外套','圖 (2) 裙子','圖 (3) T 恤'],
7:['圖 (1) 送花','圖 (2) 慶生','圖 (3) 安慰難過的男孩'],8:['圖 (1) 兔子在袋子裡','圖 (2) 兔子在盒子裡','圖 (3) 兔子在帽子上'],9:['圖 (1) 在家吃飯','圖 (2) 在學校吃飯','圖 (3) 在學校黑板寫字'],10:['圖 (1) 騎腳踏車回家','圖 (2) 溜滑板車回家','圖 (3) 騎腳踏車去動物園']})
ANS.update({1:3,2:2,3:3,4:2,5:1,6:1,7:3,8:1,9:2,10:1})
EX.update({
1:['音檔唸的是 mode，三遍。','m 後面接 ode，o 唸長音「歐」，結尾的 e 不發音。','所以選 ③ ode'],
2:['音檔唸的是 bleep，三遍。','bl 後面接 eep，ee 唸長音「伊」。','所以選 ② eep'],
3:['音檔唸的是 chay，三遍。','ch 後面接 ay，ay 唸「欸」，後面沒有 t 的音。','所以選 ③ ay'],
4:['音檔唸的是 draw（畫畫）。','圖 (2) 男孩在黑板上畫熊。圖 (1) 是寫字，圖 (3) 是看書。','所以選 ② 圖 (2) 在黑板畫畫'],
5:['音檔唸的是 bookstore（書店）。','圖 (1) 招牌上畫著書。圖 (2) 是超級市場，圖 (3) 是學校。','所以選 ① 圖 (1) 書店'],
6:['音檔唸的是 jacket（外套）。','圖 (2) 是 skirt（裙子），圖 (3) 是 T-shirt（T 恤）。','所以選 ① 圖 (1) 外套'],
7:["音檔唸的是 Don't worry.（別擔心。）",'圖 (3) 男孩看起來很難過，媽媽拍拍他、安慰他。','圖 (1) 是收到花，圖 (2) 是在慶生。','所以選 ③ 圖 (3) 安慰難過的男孩'],
8:["音檔唸的是：Where is my rabbit?（我的兔子在哪裡？）It's in the bag.（在袋子裡。）",'圖 (1) 兔子在袋子裡。圖 (2) 是盒子（box），圖 (3) 在帽子上。','所以選 ① 圖 (1) 兔子在袋子裡'],
9:["音檔唸的是：She's at school.（她在學校。）She's eating.（她在吃東西。）",'要「在學校」又「在吃東西」。圖 (2) 有佈告欄、課桌，她在吃飯。','圖 (1) 在家裡吃飯，圖 (3) 在學校但是在寫黑板。','所以選 ② 圖 (2) 在學校吃飯'],
10:["音檔唸的是：I'm riding a bike.（我在騎腳踏車。）I'm going home.（我要回家。）",'圖 (1) 騎腳踏車往家裡去。圖 (2) 溜的是滑板車，圖 (3) 要去的是動物園。','所以選 ① 圖 (1) 騎腳踏車回家'],
})
