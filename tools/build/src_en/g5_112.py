import sys; sys.path.insert(0,'/home/claude/work/zh/src_en')
from rd_helpers import W,S
OPT={11:['tiger','mother','brother'],12:['tea','two','three'],13:['red','tired','read'],14:['write','what','white'],15:['sad','tall','happy'],16:['rice','juice','ruler'],17:['cold','short','sunny'],
18:['圖 (1) 時鐘 4:00','圖 (2) 時鐘 5:00','圖 (3) 5 歲蛋糕'],19:['圖 (1) 兩杯冰紅茶','圖 (2) 兩盒熱牛奶','圖 (3) 兩杯熱茶'],20:['圖 (1) 冷得發抖','圖 (2) 熱得吹電扇','圖 (3) 微風涼涼的'],21:['圖 (1) 瘦瘦的男孩','圖 (2) 胖胖的男孩','圖 (3) 女孩'],22:['圖 (1) 女孩開心游泳','圖 (2) 女孩哭著游泳','圖 (3) 男孩哭著游泳'],
23:["It's four o'clock. It's rainy.","It's six o'clock. It's sunny.","It's eight o'clock. It's rainy."],24:['I see two rabbits. The rabbits are white.',"I like the black rabbit. It's happy.","I like the white rabbit. It's thin."],25:["John can dance. He can't sing.","Ann can sing. She can't dance.","Bob can dance. He can't sing."]}
ANS={11:2,12:2,13:3,14:1,15:1,16:1,17:3,18:2,19:3,20:3,21:1,22:2,23:3,24:2,25:1}
G={'tiger':'老虎','mother':'媽媽','brother':'哥哥／弟弟','tea':'茶','two':'2','three':'3','red':'紅色','tired':'累的','read':'讀','write':'寫','what':'什麼','white':'白色','sad':'難過的','tall':'高的','happy':'開心的','rice':'飯','juice':'果汁','ruler':'尺','cold':'冷的','short':'矮的；短的','sunny':'晴天的'}
EX={
11:W('箭頭指的是抱著小孩的女人，她是媽媽。',2,OPT[11],G),
12:W('圖是數字 2。',2,OPT[12],G),
13:W('女孩在看書。',3,OPT[13],G,'小心：read（讀）和 red（紅色）字很像，要看清楚。'),
14:W('男孩在本子上寫字。',1,OPT[14],G,'小心：write（寫）、white（白色）、what（什麼）長得很像。'),
15:W('男孩看到打針，哭得很難過。',1,OPT[15],G),
16:W('圖是一碗飯。',1,OPT[16],G),
17:W('太陽笑咪咪的，是晴天。',3,OPT[17],G),
18:S(['A 問：What time is it?（現在幾點？）',"B 答：Five o'clock.（五點。）",'圖 (2) 的時鐘是 5:00。圖 (1) 是四點，圖 (3) 是 5 歲的蛋糕。'],2,OPT[18][1]),
19:S(['A 問：What do you want?（你想要什麼？）','B 答：Two hot tea.（兩杯熱茶。）','圖 (3) 是兩杯冒著熱氣的茶。圖 (1) 是冰的，圖 (2) 是牛奶。'],3,OPT[19][2]),
20:S(["A 問：How's the weather?（天氣怎麼樣？）","B 答：It's cool.（涼涼的。）",'圖 (1) 太冷，圖 (2) 太熱，圖 (3) 有微風吹，涼涼的。'],3,OPT[20][2]),
21:S(['My brother is ten years old.（我的哥哥十歲。）He is thin.（他很瘦。）','brother 是男生，而且要瘦的。圖 (2) 胖胖的，圖 (3) 是女孩。'],1,OPT[21][0]),
22:S(['男孩問：Can you swim?（你會游泳嗎？）',"女孩答：No, I can't.（我不會。）",'圖裡游泳圈上的人要找不會游泳的女孩，她嚇得哭了。圖 (3) 是男孩。'],2,OPT[22][1]),
23:S(['看表格：4:00、5:00 是晴天，6:00 是陰天，7:00、8:00 下雨。',"③ It's eight o'clock. It's rainy.（八點，下雨。）對。",'① 四點是晴天；② 六點是陰天，不是晴天。'],3,OPT[23][2]),
24:S(['圖裡有一隻白兔和一隻黑兔，黑兔笑咪咪的。','① 兩隻不都是白色。③ 白兔胖胖的，不瘦。',"② I like the black rabbit.（我喜歡那隻黑兔。）It's happy.（牠很開心。）對。"],2,OPT[24][1]),
25:S(['表格第一欄是唱歌，第二欄是跳舞。John 唱歌 ✕、跳舞 ✓。',"① John can dance. He can't sing.（John 會跳舞，不會唱歌。）對。",'② Ann 兩個都不會；③ Bob 是會唱歌、不會跳舞。'],1,OPT[25][0]),
}
