import sys; sys.path.insert(0,'/home/claude/work/zh/src_en')
from rd_helpers import W,S
OPT={11:['apple','cake','milk'],12:['white rabbit','white bird','red rabbit'],13:['tiger','cat','dog'],14:['tiger','lion','pig'],15:['blue','black','green'],16:['yes','no','it'],17:['ruler','pencil','marker'],
18:['圖 (1) 貓','圖 (2) 獅子','圖 (3) 老虎'],19:['圖 (1) 魚','圖 (2) 尺','圖 (3) 魚形狀的尺'],20:['圖 (1) 紅色','圖 (2) 綠色','圖 (3) 黃色'],21:['圖 (1) 藍色彩色筆','圖 (2) 綠色彩色筆','圖 (3) 綠色鉛筆'],22:['圖 (1) 遠處的豬','圖 (2) 指著近處的豬','圖 (3) 指著狗'],
23:["What is it? / It's an egg.","Is it an egg? / No. It's a bird.","Is it an egg? / Yes. It's an egg."],24:["Is that a cake? / No, it's not.","What's this? / It's a cake.","What's that? / It's a cake."],25:['Is this green? / No. It\'s black.',"What color is it? / It's black.","What's your name? / My name is Black."]}
ANS={11:3,12:1,13:3,14:1,15:1,16:2,17:1,18:2,19:1,20:1,21:2,22:2,23:2,24:3,25:3}
G={'apple':'蘋果','cake':'蛋糕','milk':'牛奶','white rabbit':'白色的兔子','white bird':'白色的鳥','red rabbit':'紅色的兔子','tiger':'老虎','cat':'貓','dog':'狗','lion':'獅子','pig':'豬','blue':'藍色','black':'黑色','green':'綠色','yes':'是','no':'不','it':'它','ruler':'尺','pencil':'鉛筆','marker':'彩色筆'}
EX={
11:W('圖是一盒牛奶。',3,OPT[11],G),
12:W('圖是一隻白色的兔子。',1,OPT[12],G),
13:W('圖是一隻狗。',3,OPT[13],G),
14:W('圖是一隻老虎。',1,OPT[14],G),
15:W('油漆桶上寫著「藍色」。',1,OPT[15],G),
16:W('男生看到打針哭了，雙手抱胸拒絕，像在說「不要！」。',2,OPT[16],G),
17:W('圖是一把尺。',1,OPT[17],G),
18:S(["It's a lion.（牠是獅子。）",'圖 (1) 是貓，圖 (3) 是老虎。'],2,OPT[18][1]),
19:S(["It's a fish.（它是魚。）It's not a ruler.（它不是尺。）",'圖 (1) 是真的魚。圖 (3) 雖然是魚的形狀，但它是一把尺。'],1,OPT[19][0]),
20:S(['A 問：What color is it? Yellow?（它是什麼顏色？黃色嗎？）',"B 答：No. It's red.（不是，是紅色。）"],1,OPT[20][0]),
21:S(["It's not a pencil.（它不是鉛筆。）It's a marker.（它是彩色筆。）It's green.（它是綠色的。）",'圖 (1) 是藍色的，圖 (3) 是鉛筆。'],2,OPT[21][1]),
22:S(["男孩問：What's this? Is it a pig?（這是什麼？是豬嗎？）this 是指近的東西。",'女孩答：Yes, it is.（是的。）','圖 (2) 男孩指著旁邊的豬。圖 (1) 的豬在遠處，圖 (3) 是狗。'],2,OPT[22][1]),
23:S(['圖是一隻剛從蛋殼裡出來的小鳥。',"② Is it an egg?（是蛋嗎？）No. It's a bird.（不是，是鳥。）對。",'① 和 ③ 都說是蛋，不對。'],2,OPT[23][1]),
24:S(['蛋糕在遠遠的桌上，遠的東西用 that。',"③ What's that?（那是什麼？）It's a cake.（是蛋糕。）對。",'① 說不是蛋糕，② 用 this（這個），都不對。'],3,OPT[24][2]),
25:S(['男生拿著寫有「Black」的名牌，女生拿著麥克風在問他。',"③ What's your name?（你叫什麼名字？）My name is Black.（我叫 Black。）對。",'這裡的 Black 是名字，不是在說顏色。'],3,OPT[25][2]),
}
