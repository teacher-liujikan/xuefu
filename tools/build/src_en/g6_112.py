import sys; sys.path.insert(0,'/home/claude/work/zh/src_en')
from rd_helpers import W,S
OPT={11:['doctor','brother','teacher'],12:['ride','write','dance'],13:['head','ear','egg'],14:['box','bed','bus'],15:['boy','bag','shoe'],16:['zoo','home','school'],17:['a long skirt','a short skirt','a long T-shirt'],
18:["I'm a teacher.","I'm in the bathroom.","I'm singing in the bathroom."],19:["I'm going to the bookstore.","I'm reading English books.",'I have three books.'],20:['I like cars.','I have a car.',"It's in the box."],
21:['I have a small nose.','I have a big mouth.','I have three eyes.'],22:['He is swimming to Taiwan.','He is going to Taiwan.','He is in Taiwan.'],23:["It's 1:30. Amy is eating rice.","It's 2:15. Amy is riding a bike.","It's 4:30. Amy is drawing."],24:["I see a cat. It's watching TV.","The cat is on the TV. It's sleeping.","The dog is in the kitchen. It's watching TV."],25:["I'm in the park. It's hot.","It's warm. I want a dress.","I'm in the park. I want a jacket."]}
ANS={11:1,12:1,13:1,14:3,15:2,16:2,17:1,18:3,19:1,20:3,21:3,22:2,23:3,24:2,25:3}
G={'doctor':'醫生','brother':'哥哥／弟弟','teacher':'老師','ride':'騎','write':'寫','dance':'跳舞','head':'頭','ear':'耳朵','egg':'蛋','box':'盒子','bed':'床','bus':'公車','boy':'男孩','bag':'袋子','shoe':'鞋子','zoo':'動物園','home':'家','school':'學校','a long skirt':'長裙','a short skirt':'短裙','a long T-shirt':'長的 T 恤'}
EX={
11:W('女人穿著白袍、掛著聽診器，她是醫生。',1,OPT[11],G),
12:W('女孩騎著機車。',1,OPT[12],G),
13:W('箭頭指的是頭。',1,OPT[13],G),
14:W('圖是一輛公車。',3,OPT[14],G),
15:W('圖是一個袋子。',2,OPT[15],G),
16:W('一家人在房子裡，這是家。',2,OPT[16],G),
17:W('箭頭指的是女人穿的長裙。',1,OPT[17],G),
18:S(['A 問：What are you doing?（你正在做什麼？）','要回答動作，用 -ing。',"③ I'm singing in the bathroom.（我在浴室唱歌。）是動作。",'① 是職業，② 只說在哪裡。'],3,OPT[18][2]),
19:S(['A 問：Where are you going?（你要去哪裡？）','要回答要去的地方。',"① I'm going to the bookstore.（我要去書店。）對。",'② 是正在做的事，③ 是有幾本書。'],1,OPT[19][0]),
20:S(['A 問：Where is my car?（我的車在哪裡？）','Where 是問地方。',"③ It's in the box.（在盒子裡。）對。",'①② 都沒有說在哪裡。'],3,OPT[20][2]),
21:S(['怪獸有三個眼睛、一個大鼻子、小小的嘴巴。','① 鼻子不小，② 嘴巴不大。','③ I have three eyes.（我有三個眼睛。）對。'],3,OPT[21][2]),
22:S(['男生坐在飛機上，飛機正往臺灣飛。','① 他不是游泳，③ 他還沒到臺灣。','② He is going to Taiwan.（他正要去臺灣。）對。'],2,OPT[22][1]),
23:S(['看 Amy 的星期一：1:00～2:00 吃漢堡、喝飲料，2:00～3:00 睡覺，3:00～4:00 騎腳踏車，4:00～5:00 畫畫。',"③ It's 4:30. Amy is drawing.（四點半，Amy 在畫畫。）對。",'① 她吃的是漢堡，不是飯；② 兩點十五分她在睡覺。'],3,OPT[23][2]),
24:S(['貓趴在電視上面睡覺，狗在旁邊看電視。','① 貓沒有在看電視，③ 狗不在廚房。',"② The cat is on the TV.（貓在電視上面。）It's sleeping.（牠在睡覺。）對。"],2,OPT[24][1]),
25:S(['女生在公園裡，冷得抱著手，心裡想著外套，樹葉在飄。','① 天氣不熱，② 她想要的是外套，不是洋裝。',"③ I'm in the park.（我在公園。）I want a jacket.（我想要外套。）對。"],3,OPT[25][2]),
}
