
name := Mobile Trainer
out := MobileTrainer
sfd_out := ${out}.sfd

all: sfd web

sfd: make_font.py jis_half.png jis_full.png
	fontforge -script make_font.py "${sfd_out}" "${name}"

web: ttf woff woff2

ttf woff woff2: ${sfd_out}
	fontforge -c 'open(argv[1]).generate(argv[2])' "${sfd_out}" "${out}.$@"

full_clean: clean
	rm -rf "${sfd_out}"

clean:
	rm -rf "${out}".{ttf,woff,woff2} glyphs/*
