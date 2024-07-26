#!/bin/bash

magick convert jis_half.png -crop 6x12 +repage +adjoin glyphs/half%d.png
magick convert jis_full.png -crop 12x12 +repage +adjoin glyphs/full%d.png
