import fontforge

hw_chars = (
" !\"#$%&'()*+,-./"
"0123456789:;<=>?"
"@ABCDEFGHIJKLMNO"
"PQRSTUVWXYZ[\\]^_"
"`abcdefghijklmno"
"pqrstuvwxyz{|}~"
)


fw_chars = (
"¢£§¨¬°±´¶×÷Α"
"ΒΓΔΕΖΗΘΙΚΛΜΝ"
"ΞΟΠΡΣΤΥΦΧΨΩα"
"βγδεζηθικλμν"
"ξοπρστυφχψωЁ"
"АБВГДЕЖЗИЙКЛ"
"МНОПРСТУФХЦЧ"
"ШЩЪЫЬЭЮЯабвг"
"дежзийклмноп"
"рстуфхцчшщъы"
"ьэюяё‐‖‘’“”†"
"‡‥…‰′″※℃Å←↑→"
"↓⇒⇔∀∂∃∇∈∋−√∝"
"∞∠∧∨∩∪∫∬∴∵∽≒"
"≠≡≦≧≪≫⊂⊃⊆⊇⊥⌒"
"─━│┃┌┏┐┓└┗┘┛"
"├┝┠┣┤┥┨┫┬┯┰┳"
"┴┷┸┻┼┿╂╋■□▲△"
"▼▽◆◇○◎●◯★☆♀♂"
"♪♭♯　、。〃々〆〇〈〉"
"《》「」『』【】〒〓〔〕"
"〜ぁあぃいぅうぇえぉおか"
"がきぎくぐけげこごさざし"
"じすずせぜそぞただちぢっ"
"つづてでとどなにぬねのは"
"ばぱひびぴふぶぷへべぺほ"
"ぼぽまみむめもゃやゅゆょ"
"よらりるれろゎわゐゑをん"
"゛゜ゝゞァアィイゥウェエ"
"ォオカガキギクグケゲコゴ"
"サザシジスズセゼソゾタダ"
"チヂッツヅテデトドナニヌ"
"ネノハバパヒビピフブプヘ"
"ベペホボポマミムメモャヤ"
"ュユョヨラリルレロヮワヰ"
"ヱヲンヴヵヶ・ーヽヾ一！"
"＃＄％＆（）＊＋，．／０"
"１２３４５６７８９：；＜"
"＝＞？＠ＡＢＣＤＥＦＧＨ"
"ＩＪＫＬＭＮＯＰＱＲＳＴ"
"ＵＶＷＸＹＺ［＼］＾＿｀"
"ａｂｃｄｅｆｇｈｉｊｋｌ"
"ｍｎｏｐｑｒｓｔｕｖｗｘ"
"ｙｚ｛｜｝￣￥"
)

mkr = fontforge.font()
mkr.ascent = 1000
mkr.descent = 200
mkr.encoding = "Unicode"

sprite_root = '/home/kabili/Projects/Fonts/REON/MobileTrainer/glyphs/'

for i in range(0, len(hw_chars)):
	s = hw_chars[i]
	if not s in mkr:
		gl = mkr.createChar(ord(s))
	else:
		gl = mkr[s]
	sprite = "uni%04X.png" % ord(s)
	gl.importOutlines(sprite_root + sprite)
	gl.autoTrace()
	gl.width = 600
	
for i in range(0, len(fw_chars)):
	s = fw_chars[i]
	if not s in mkr:
		gl = mkr.createChar(ord(s))
	else:
		gl = mkr[s]
	sprite = "uni%04X.png" % ord(s)
	gl.importOutlines(sprite_root + sprite)
	gl.autoTrace()
	gl.width = 1200
