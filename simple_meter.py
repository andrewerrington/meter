#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math
import meter


# Create the meter object
SWRmeter = meter.Meter(
    # Dimensions for scale label
    label_width = 76,label_height = 45,label_offset = 4,

    # Radius of meter movement cutout (mm)
    cutout_radius = 13,

    # Screwholes at 31mm centres, 7mm from origin, dia 1.5mm
    screw_centres = 67.0,screw_offset = 7.0,screw_radius = 0.75,

    # fsd
    fsd = 90,

    # 'flattening' offset
    d = 40,
)


#Volts dc (upper) scale
SWRmeter.add(meter.Scale(radius=45, show_arc=True, tick_direction=1,

    scale_label_radius=50,
    min_value=0.0,
    max_value=30.0,
    scale_label_font="IsonormD",scale_label_font_size=3,
    scale_label_fill='black',
    scale_label_stroke='black',
    scale_stroke="black",function=meter.linear,
    label_radius=55,label_font="IsonormD",label_font_size=4,
    label_text='VOLTS DC',

    minor_ticks=[x for x in range(0,31)],
    minor_tick_length = 1,

    major_ticks=[x for x in range(0,31,5)],
    major_tick_length = 2,

    scale_labels=[(x,'%d'%x) for x in range(0,31,5)]
))

#Amps dc (lower) scale
SWRmeter.add(meter.Scale(radius=44.5, show_arc=True, tick_direction=-1,

    scale_label_radius=39.5,
    min_value=0.0,
    max_value=4.0,
    scale_label_font="IsonormD",scale_label_font_size=3,
    scale_label_fill='black',
    scale_label_stroke='black',
    scale_stroke="black",function=meter.linear,
    label_radius=34.5,label_font="IsonormD",label_font_size=4,
    label_text='AMPS DC',

    minor_ticks=[float(x)/10 for x in range(0,41)],
    minor_tick_length = 1,

    major_ticks=[x for x in range(0,5)],
    major_tick_length = 2,

    scale_labels=[(x,'%d'%x) for x in range(0,5)]
))



f=open("simple.svg",'w')
f.write(SWRmeter.write_svg())
f.close