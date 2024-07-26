import fontforge
import subprocess
import os
import unicodedata

hw_chars = (
" !\"#$%&'()*+,-./"
"0123456789:;<=>?"
"@ABCDEFGHIJKLMNO"
"PQRSTUVWXYZ[\\]^_"
"`abcdefghijklmno"
"pqrstuvwxyz{|}~\u00a0"
# Mobile Trainer does not support the half-width kana
)

# The first half of these are typically rendered as half-width
# on most systems, but Mobile Trainer renders them as full-width
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

root = os.path.dirname(os.path.abspath(__file__))
glyph_root = os.path.join(root, 'glyphs')

if not os.path.exists(glyph_root):
	os.makedirs(glyph_root)

subprocess.run([
	'magick', 'convert', os.path.join(root, 'jis_half.png'),
	'-crop', '6x12', '+repage', '+adjoin',
	os.path.join(glyph_root, 'half%d.png')
	])
	
subprocess.run([
	'magick', 'convert', os.path.join(root, 'jis_full.png'),
	'-crop', '12x12', '+repage', '+adjoin',
	os.path.join(glyph_root, 'full%d.png')
	])

font = fontforge.font()
font.ascent = 1000
font.descent = 200
font.encoding = "Unicode"
	
total_chars = len(hw_chars) + len(fw_chars)
curr_index = 0

def add_character(char, index, is_full):
	global curr_index
	if not char in font:
		gl = font.createChar(ord(char))
	else:
		gl = font[char]
	if is_full:
		gl.width = 1200
		path = 'full%d.png'
	else:
		gl.width = 600
		path = 'half%d.png'
	gl.importOutlines(os.path.join(glyph_root, path % index))
	name = unicodedata.name(char)
	curr_index += 1
	print(f'[{curr_index:>3}/{total_chars}] Tracing {name}...')
	gl.autoTrace()
	gl.clear(0)
	gl.validate()

for i, c in enumerate(hw_chars):
	add_character(c, i, False)
	
for i, c in enumerate(fw_chars):
	add_character(c, i, True)

# Keep these down here, they seem to mess with the image tracing
font.upos = -150
font.uwidth = 100

font.encoding = 'compacted'
font.fontname = "MobileTrainer" # no spaces!
font.fullname = "Mobile Trainer"
font.familyname = "Mobile Trainer"
font.version = '1.01'
font.copyright = 'Copyright (c) 2001 Nintendo.'

font.save("MobileTrainer.sfd")
font.close()
