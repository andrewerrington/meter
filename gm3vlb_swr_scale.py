#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Program to draw SVG file for GM3VLB antenna analyser scale
# By Andrew Errington ZL3AME
# December 2012

import math
import meter


# Functions for special scales on this meter

def swr(**args):
    # Input x (SWR value)
    # Output, proportion of fsd represented by x
    swr=float(args['x'])
    return (swr-1)/(swr+1)

def rz(**args):
    # Input x (R or Z value)
    # Output, proportion of fsd represented by x
    rz=float(args['x'])
    Vfsd = 13.74    # fixme: describe source of this number
    V2=14.14*(rz/(rz+50.0))-0.2
    return V2/Vfsd


# Create the meter object
SWRmeter = meter.Meter(
    # Dimensions for scale label
    label_width = 60,label_height = 35,label_offset = 4,

    # Radius of meter movement cutout (mm)
    cutout_radius = 10,

    # Screwholes at 31mm centres, 7mm from origin, dia 1.5mm
    screw_centres = 31.0,screw_offset = 7.0,screw_radius = 0.75,

    # fsd
    fsd = 90,

    # 'flattening' offset
    d = 10,
)


#SWR (upper) scale
SWRmeter.add(meter.Scale(radius=31,

    scale_label_radius=35,
    min_value=1.0,
    max_value=1000000.0,
    scale_label_font="IsonormD",scale_label_font_size=2,
    scale_label_fill='black',
    scale_label_stroke='black',
    scale_stroke="black",function=swr,
    label_radius=39,label_font="IsonormD",label_font_size=3,
    label_text='SWR',

    minor_ticks=[1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,
        2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,
        3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,1000000.0],
    minor_tick_length = 1,

    major_ticks=[1.0,1.5,2.0,3.0,5.0,10.0,1000000.0],
    major_tick_length = 2,

    scale_labels=[(1.0,'1'),(1.5,'1.5'),(2.0,'2'),(3.0,'3'),(5.0,'5'),(10.0,'10'),(1000000.0,'∞')]
))


# R/Z (lower) scale
SWRmeter.add(meter.Scale(radius=30.5, show_arc=True, tick_direction=-1,

    scale_label_radius=27,
    min_value=0.0,
    max_value=10000000.0,
    scale_label_font="IsonormD",scale_label_font_size=2,
    scale_label_fill='red',
    scale_label_stroke='red',
    scale_stroke="red",
    function=rz,
    label_radius=24,label_font="IsonormD",label_font_size=3,
    label_text='R or Z (Ω)',

    minor_ticks=[0.0,5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,
        50.0,60.0,70.0,80.0,90.0,100.0,
        120.0,140.0,160.0,180.0,200.0,
        300.0,400.0,500.0,10000000.0],
    minor_tick_length = 1,
    minor_tick_stroke='red',

    major_ticks=[0.0,10.0,20.0,30.0,40.0,50.0,100.0,200.0,500.0,10000000.0],
    major_tick_length = 2,
    major_tick_stroke='red',

    scale_labels=[(0.0,'0'),(10.0,'10'),(20.0,'20'),(30.0,'30'),(40.0,'40'),(50.0,'50'),
        (100.0,'100'),(200.0,'200'),(500.0,'500'),(10000000.0,'∞')]
))


# Add 'Input OK' segment
SWRmeter.add(meter.Segment(inner_radius=18,outer_radius=22,left=0.44,right=1.0,
    segment_stroke='black',segment_fill='limegreen',
    label_radius=20.2,label_font="IsonormD",label_font_size=3,
    label_text='INPUT OK',label_stroke='white',label_fill='white'
))


f=open("swrscale.svg",'w')
f.write(SWRmeter.write_svg())
f.close
