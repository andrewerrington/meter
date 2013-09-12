#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Program to draw d'Arsonval meter scales with SVG
# By Andrew Errington ZL3AME
# December 2012

"""Build an SVG file to draw a d'Arsonval meter scale."""

import math
import sys


class Meter:
    def __init__(self, **args):
        self.label_width=args['label_width']
        self.label_height=args['label_height']
        self.label_offset=args['label_offset']

        if 'cutout_radius' in args:
            self.cutout_radius=args['cutout_radius']

        if 'screw_centres' in args:
            self.screw_centres=args['screw_centres']
            self.screw_offset=args['screw_offset']
            self.screw_radius=args['screw_radius']

        self.fsd=args['fsd']

        self.d=args.get('d',0)

        self.landscape=args.get('landscape',True)

        self.items=[]

    def add(self,item):
        item.fsd=self.fsd
        item.d=self.d
        self.items.append(item)

    def svg(self):
        # SVG for Meter label

        # tick marks for cutting
        # horizontal
        buf=[]
        buf.append(SVGpath('M %.2f %.2f h -2'%(-(self.label_width/2)-1,-self.label_offset),'none','black',0.1))
        buf.append(SVGpath('M %.2f %.2f h -2'%\
            (-(self.label_width/2)-1,-self.label_offset-self.label_height),'none','black',0.1))
        buf.append(SVGpath('M %.2f %.2f h 2'%((self.label_width/2)+1,-self.label_offset),'none','black',0.1))
        buf.append(SVGpath('M %.2f %.2f h 2'%\
            ((self.label_width/2)+1,-self.label_offset-self.label_height),'none','black',0.1))

        #vertical
        buf.append(SVGpath('M %.2f %.2f v 2'%(-self.label_width/2,-self.label_offset+1),'none','black',0.1))
        buf.append(SVGpath('M %.2f %.2f v -2'%\
            (-self.label_width/2,-self.label_offset-self.label_height-1),'none','black',0.1))
        buf.append(SVGpath('M %.2f %.2f v 2'%(self.label_width/2,-self.label_offset+1),'none','black',0.1))
        buf.append(SVGpath('M %.2f %.2f v -2'%\
            (self.label_width/2,-self.label_offset-self.label_height-1),'none','black',0.1))

        # Meter movement centre is at origin
        buf.append(SVGpath('M -2 0 h 4','none','black',0.1))
        buf.append(SVGpath('M 0 -2 v 4','none','black',0.1))

        # Add reference mark for 'flattened' scale origin
        if self.d<>0:
            buf.append(SVGpath('M -2 %.2f h 4'%self.d,'none','black',0.1))
            buf.append(SVGpath('M 0 %.2f v 4'%(self.d-2),'none','black',0.1))

        # Meter cutout
        if hasattr(self,'cutout_radius'):
            buf.append(SVGpath('M %.2f 0 A %.2f %.2f 0 0,0 -%.2f,0'%\
                (self.cutout_radius,self.cutout_radius,self.cutout_radius,self.cutout_radius),'none','black',0.1))

        # screw holes
        if hasattr(self,'screw_centres'):
            buf.append(SVGcircle( (-self.screw_centres/2, -self.screw_offset),\
                self.screw_radius,'none','black',0.1) )
            buf.append(SVGcircle( (self.screw_centres/2, -self.screw_offset),\
                self.screw_radius,'none','black',0.1) )
            # centre dots for screw holes
            buf.append(SVGcircle( (-self.screw_centres/2, -self.screw_offset),\
                0.1,'none','black',0.1) )
            buf.append(SVGcircle( (self.screw_centres/2, -self.screw_offset),\
                0.1,'none','black',0.1) )

        return ''.join(buf)

    def write_svg(self):
        """Write SVG to draw the meter face"""
        # Hard code A4 sized paper here.
        if self.landscape:
            width=297
            height=210
        else:
            width=210
            height=297

        # Build the SVG XML header.  Set the viewBox to the same size as the document
        # so that there is a 1:1 ratio between document units (mm) and internal units.
        buf=[]
        buf.append('<?xml version="1.0" encoding="UTF-8"?>\n')
        buf.append('<svg width="%dmm" height="%dmm" viewBox="0 0 %d %d" version="1.1"\n'%(width,height,width,height))
        buf.append('xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        buf.append('<g style="fill-opacity:1.0; stroke:black; stroke-width:0.1;" ')
        buf.append('transform="translate(%d,%d)">\n'%(width/2,height/2))    # Translate (0,0) to centre of the sheet.

        buf.append(self.svg())

        for item in (self.items):
            buf.append(item.svg())

        buf.append('</g>\n</svg>\n')

        return ''.join(buf)


class Scale:
    def __init__(self, **args):
        self.radius=args['radius']
        self.min_value=args['min_value']
        self.max_value=args['max_value']

        self.show_arc=args.get('show_arc',True)
        self.scale_stroke=args.get('scale_stroke','black')
        self.scale_stroke_width=args.get('scale_stroke_width',0.1)

        self.tick_direction=args.get('tick_direction',1.0)

        if 'scale_label_radius' in args:
            self.scale_label_radius=args['scale_label_radius']
            self.scale_label_font=args['scale_label_font']
            self.scale_label_font_size=args['scale_label_font_size']
            self.scale_label_fill=args['scale_label_fill']
            self.scale_label_stroke=args['scale_label_stroke']
            self.scale_labels=args['scale_labels']

        self.function=args['function']

        if 'label_text' in args:
            self.label_text=args['label_text']
            self.label_radius=args['label_radius']
            self.label_font=args['label_font']
            self.label_font_size=args['label_font_size']

        if 'minor_ticks' in args:
            self.minor_ticks=args['minor_ticks']
            self.minor_tick_length=args['minor_tick_length']
            self.minor_tick_stroke=args.get('minor_tick_stroke','black')
            self.minor_tick_width=args.get('minor_tick_width',0.1)

        if 'major_ticks' in args:
            self.major_ticks=args['major_ticks']
            self.major_tick_length=args['major_tick_length']
            self.major_tick_stroke=args.get('major_tick_stroke','black')
            self.major_tick_width=args.get('major_tick_width',0.1)

    def svg(self):
        # SVG for scale
        theta_min=self.fsd*self.function(x=self.min_value,min_x=self.min_value,max_x=self.max_value)
        theta_max=self.fsd*self.function(x=self.max_value,min_x=self.min_value,max_x=self.max_value)

        left=flatten((self.radius,theta_min),self.fsd,self.d)
        flat_radius=left[0] # Keep the 'flattened' radius
        right=flatten((self.radius,theta_max),self.fsd,self.d)

        left=degree_to_scale(left,self.d)
        right=degree_to_scale(right,self.d)

        buf=[]

        if self.show_arc:
            # Start of scale arc
            path='M %.2f %.2f '%(left[0],left[1])
            # End of scale arc
            path+='A %.2f %.2f 0 0,1 %.2f,%.2f'%(flat_radius,flat_radius,right[0],right[1])

            buf.append(SVGpath(path,'none',self.scale_stroke,self.scale_stroke_width))

        # minor tick marks
        if hasattr(self,'minor_ticks'):
            for tick in self.minor_ticks:
                theta=self.fsd*self.function(x=tick,min_x=self.min_value,max_x=self.max_value)
                tickstart = degree_to_scale(flatten((self.radius,theta),self.fsd,self.d),self.d)
                tickend= degree_to_scale(flatten((self.radius+(self.minor_tick_length*self.tick_direction),theta)\
                    ,self.fsd,self.d),self.d)
                buf.append(SVGline((tickstart ),(tickend),self.minor_tick_stroke,self.minor_tick_width))

        # major tick marks
        if hasattr(self,'major_ticks'):
            for tick in self.major_ticks:
                theta=self.fsd*self.function(x=tick,min_x=self.min_value,max_x=self.max_value)
                tickstart = degree_to_scale(flatten((self.radius,theta),self.fsd,self.d),self.d)
                tickend= degree_to_scale(flatten((self.radius+(self.major_tick_length*self.tick_direction),theta)\
                    ,self.fsd,self.d),self.d)
                buf.append(SVGline((tickstart ),(tickend),self.major_tick_stroke,self.major_tick_width))

        # scale mark labels
        if hasattr(self,'scale_label_radius'):
            for tick in self.scale_labels:
                theta=self.fsd*self.function(x=tick[0],min_x=self.min_value,max_x=self.max_value)
                tickpos = degree_to_scale(flatten((self.scale_label_radius,theta),self.fsd,self.d),self.d)
                buf.append(SVGtext(tickpos,tick[1],self.scale_label_font,self.scale_label_font_size,\
                    self.scale_label_fill,self.scale_label_stroke))

        # scale label
        if hasattr(self,'label_text'):
            tick=degree_to_scale(flatten((self.label_radius,self.fsd/2),self.fsd,self.d),self.d)
            buf.append(SVGtext(tick,self.label_text,self.scale_label_font,self.label_font_size))

        return ''.join(buf)


class Segment:
    def __init__(self, **args):
        self.inner_radius=args['inner_radius']
        self.outer_radius=args['outer_radius']
        self.left=args['left']
        self.right=args['right']
        self.segment_stroke=args['segment_stroke']
        self.segment_fill=args['segment_fill']

        if 'label_text' in args:
            self.label_text=args['label_text']
            self.label_radius=args['label_radius']
            self.label_font=args['label_font']
            self.label_font_size=args['label_font_size']
            self.label_stroke=args['label_stroke']
            self.label_fill=args['label_fill']

    def svg(self):
        # SVG for scale segment
        # fsd and d are added by Meter class
        start_degree=self.fsd*self.left
        end_degree=self.fsd*self.right

        left_inner=flatten((self.inner_radius,start_degree),self.fsd,self.d)
        left_outer=flatten((self.outer_radius,start_degree),self.fsd,self.d)

        r_inner=left_inner[0]
        r_outer=left_outer[0]
        left_inner=degree_to_scale(left_inner,self.d)
        left_outer=degree_to_scale(left_outer,self.d)

        right_inner=flatten((self.inner_radius,end_degree),self.fsd,self.d)
        right_outer=flatten((self.outer_radius,end_degree),self.fsd,self.d)

        right_inner=degree_to_scale(right_inner,self.d)
        right_outer=degree_to_scale(right_outer,self.d)

        # Left inner to left outer
        path='M %.2f %.2f L %.2f %.2f '%(left_inner[0],left_inner[1],left_outer[0],left_outer[1])
        # Left outer to right outer
        path+='A %.2f %.2f 0 0,1 %.2f,%.2f '%(r_outer,r_outer,right_outer[0],right_outer[1])
        # Right outer to right inner
        path+='L %.2f %.2f L %.2f %.2f '%(right_outer[0],right_outer[1],right_inner[0],right_inner[1])
        # Right inner to left inner
        path+='A %.2f %.2f 0 0,0 %.2f,%.2f Z'%(r_inner,r_inner,left_inner[0],left_inner[1])

        buf=[]
        buf.append(SVGpath(path,self.segment_fill,self.segment_stroke,0.1))

        # Make a path for the text
        if hasattr(self,'label_text'):
            left=flatten((self.label_radius,start_degree),self.fsd,self.d)
            radius=left[0]
            right=flatten((self.label_radius,end_degree),self.fsd,self.d)

            left=degree_to_scale(left,self.d)
            right=degree_to_scale(right,self.d)

            # Start of text path
            path='M %.2f %.2f '%(left[0],left[1])
            # End of text path
            path+='A %.2f %.2f 0 0,1 %.2f,%.2f'%(radius,radius,right[0],right[1])

            path_id='%s%s%s'%(start_degree,end_degree,radius)   # Build a (probably) unique ID

            buf.append(SVGdef('path id="%s" d="%s"'%(path_id,path)))

            buf.append(SVGtextonpath(path_id,self.label_text,self.label_font,\
                self.label_font_size,self.label_fill,self.label_stroke,50)) #50 is 50%, or half way along the path

        return ''.join(buf)


# General meter drawing functions
def degree_to_scale(p,d=0):
    # p=(r,theta)
    # r= radius (mm) from meter origin (or offset origin if specified)
    # theta= degrees (0-180) 0 is horizontal to the right, 90 is vertically straight up
    # d= offset (mm) positive offset below meter origin.

    x= p[0] * math.cos(math.radians(p[1]))
    y= -p[0] * math.sin(math.radians(p[1]))+d

    return (x,y)

def flatten(p, fsd, d):
    # p=(r,theta)
    # r= radius (mm)
    # theta= degrees (0-fsd) Number of degrees along meter scale.  0 is left side of meter scale.
    # Return a polar coordinate tuple for the polar coordinate p
    # on a meter with f.s.d. fsd degrees, flattened by offset d mm below meter origin

    r=p[0]
    # Calculate the radius (r2) of the 'flattened' scale
    x=float(r) * math.sin(math.radians(float(fsd)/2))
    y=float(r) * math.cos(math.radians(float(fsd)/2))
    r2=math.sqrt((x*x)+(y+d)**2)

    # Calculate the new angle subtended by the meter needle based on the offset origin.
    theta2=math.degrees(2.0*math.acos((y+d)/r2))

    # Now we can use proportions to map the meter deflection to the offset, and
    # adjust it for the conventional zero degree reference.
    theta=90+(theta2/2)-((p[1]/float(fsd))*theta2)
    return (r2, theta)

def linear(**args):
    # Linear scale function.  Returns the proportion of full scale.
    x=float(args['x'])
    min_x=float(args['min_x'])
    max_x=float(args['max_x'])
    return x/(max_x-min_x)

# SVG elements
def SVGpath(path,fill,stroke,width):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" />\n'%(path,fill,stroke,width)

def SVGcircle(centre,radius,fill,stroke,width):
    return '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" stroke-width="%s"/>\n'\
            %(centre[0],centre[1],radius,fill,stroke,width)

def SVGline(start,end,stroke='black',width=0.1):
    return '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" width="%.2f" />\n'%\
            (start[0],start[1],end[0],end[1],stroke,width)

def SVGtext(origin,text,font,size,fill='black',stroke='black'):
    return '<text x="%.2f" y="%.2f" font-size="%g" fill="%s" stroke="%s" font-family="%s" style="text-anchor:middle;dominant-baseline:middle">\n%s\n</text>\n'%\
        (origin[0],origin[1],size,fill,stroke,font,text)

def SVGdef(definition):
    return '<defs>\n  <%s />\n</defs>\n' %definition

def SVGtextonpath(path_id,text,font,size,fill,stroke,startOffset=0):
    return '<text font-size="%g" fill="%s" stroke="%s" font-family="%s" style="text-anchor:middle;dominant-baseline:middle">\n<textPath xlink:href="#%s" startOffset="%g%%">\n%s\n</textPath>\n</text>\n'\
        %(size,fill,stroke,font,path_id,startOffset,text)

def main():
    print __doc__
    return 0

if __name__=='__main__':
    status=main()
    sys.exit(status)