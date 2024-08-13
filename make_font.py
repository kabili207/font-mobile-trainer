import fontforge
import subprocess
import os
import unicodedata
from sys import argv

hw_chars = (
" !\"#$%&'()*+,-./"
"0123456789:;<=>?"
"@ABCDEFGHIJKLMNO"
"PQRSTUVWXYZ[\\]^_"
"`abcdefghijklmno"
"pqrstuvwxyz{|}~\u007f"
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

# Allows us to manually add path splines
manual_full = {
	#'■': [[(1200,1000), (1200,-100), (100,-100), (100,1000)]]
}
manual_half = {
	'\u00a0': []
}

root = os.path.dirname(os.path.abspath(__file__))
glyph_root = os.path.join(root, 'glyphs')

if not os.path.exists(glyph_root):
	os.makedirs(glyph_root)

subprocess.run([
	'magick', 'convert', os.path.join(root, 'jis_half.png'),
	'-crop', '6x12', '+repage', '+adjoin', '-define', 'png:color-type=3',
	os.path.join(glyph_root, 'half%d.png')
	])
	
subprocess.run([
	'magick', 'convert', os.path.join(root, 'jis_full.png'),
	'-crop', '12x12', '+repage', '+adjoin', '-define', 'png:color-type=3',
	os.path.join(glyph_root, 'full%d.png')
	])

sfd_name = argv[1]
font_name = argv[2]

if os.path.exists(sfd_name):
	font = fontforge.open(sfd_name)
else:
	font = fontforge.font()
font.ascent = 1000
font.descent = 200
font.encoding = "Unicode"
	
total_chars = len(hw_chars) + len(fw_chars) + len(manual_full) + len(manual_half)
curr_index = 0

def create_glyph(char, is_full):
	global curr_index
	curr_index += 1
	try:
		name = unicodedata.name(char)
	except:
		name = f"CONTROL CHARACTER {ord(char)}"
	gl = font.createChar(ord(char))
	gl.clear()
	if is_full:
		gl.width = 1200
	else:
		gl.width = 600
	return gl, name

def finish_glyph(gl):
	gl.simplify()
	gl.validate()

def add_character(char, index, is_full):
	gl, name = create_glyph(char, is_full)
	if is_full:
		sprite = 'full%d.png'
	else:
		sprite = 'half%d.png'
	gl.importOutlines(os.path.join(glyph_root, sprite % index))
	print(f'[{curr_index:>3}/{total_chars}] Tracing {name}...')
	gl.autoTrace()
	gl.clear(0) # Remove background
	finish_glyph(gl)

def add_manually(char, splines, is_full):
	gl, name = create_glyph(char, is_full)
	print(f'[{curr_index:>3}/{total_chars}] Manually drawing {name}...')
	pen = gl.glyphPen();
	for path in splines:
		pen.moveTo(path[0])
		for point in path[1:]:
			pen.lineTo(point)
		pen.closePath()
	pen = None
	finish_glyph(gl)

for i, c in enumerate(hw_chars):
	add_character(c, i, False)

for c, s in manual_half.items():
	add_manually(c, s, False)

for i, c in enumerate(fw_chars):
	add_character(c, i, True)

for c, s in manual_full.items():
	add_manually(c, s, True)

# Keep these down here, they seem to mess with the image tracing
font.upos = -150
font.uwidth = 100

font.encoding = 'compacted'
font.fontname = font_name.replace(' ','')
font.fullname = font_name
font.familyname = font_name
font.version = '1.03'
font.copyright = 'Copyright (c) 2001 Nintendo.'

font.save(sfd_name)
font.close()
