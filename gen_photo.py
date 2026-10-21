#!/usr/bin/env python3
"""Fotós 1:1 hirdetéskép: python3 gen_photo.py "Cím = kiemelt rész" <unsplash_photo_id> <kimenet.jpg>"""
import sys, io, urllib.request, textwrap
from PIL import Image, ImageDraw, ImageFont
S=1080
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BORD=(123,28,62); GOLD=(201,151,58); DARK=(34,26,28)
def font(sz): return ImageFont.truetype(BOLD,sz)
def load(pid):
    url=f"https://images.unsplash.com/photo-{pid}?w=1400&q=85&fit=crop&crop=entropy&h=1400"
    data=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read()
    im=Image.open(io.BytesIO(data)).convert("RGB"); w,h=im.size; m=min(w,h)
    im=im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m)).resize((S,S)); return im
def wrap(words,d,f,maxw):
    lines=[];cur=[]
    for i,w in enumerate(words):
        t=" ".join([x for x,_ in cur]+[w[0]])
        if cur and d.textlength(t,font=f)>maxw: lines.append(cur);cur=[w]
        else: cur.append(w)
    lines.append(cur);return lines
def make(title,pid,out):
    t=title.upper().rstrip(".").split()
    k=len(t)-2
    if "=" in t: k=t.index("=")+1; t.remove("=")
    words=[(w,i>=k) for i,w in enumerate(t)]
    img=load(pid).convert("RGBA")
    ov=Image.new("RGBA",(S,S),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for x in range(S):
        a=int(235*max(0,1-x/760)**1.2); od.line([(x,0),(x,S)],fill=(30,22,25,a))
    img=Image.alpha_composite(img,ov); d=ImageDraw.Draw(img)
    # felső jelvény
    f=font(34); label="INGYENES ELŐADÁS"; w=d.textlength(label,font=f)
    d.rounded_rectangle([70,70,70+w+60,140],35,fill=GOLD); d.text((100,86),label,font=f,fill=DARK)
    # cím
    maxw=640
    for sz in (88,80,72,64,56):
        f=font(sz); lines=wrap(words,d,f,maxw)
        if len(lines)*sz*1.28<=520: break
    lh=int(sz*1.28); y=int(500-len(lines)*lh/2)+40
    for line in lines:
        x=70
        for w_,acc in line:
            ww=d.textlength(w_,font=f)
            if acc:
                d.rounded_rectangle([x-12,y-4,x+ww+12,y+sz*1.05],10,fill=GOLD); d.text((x,y),w_,font=f,fill=DARK)
            else: d.text((x,y),w_,font=f,fill=(255,255,255))
            x+=ww+d.textlength(" ",font=f)
        y+=lh
    # alszöveg
    f2=font(34); d.text((70,y+24),"Jelentkezz az ingyenes előadásra.",font=f2,fill=(240,232,222))
    # CTA gomb
    f3=font(36); lab="JELENTKEZZ INGYEN"; ww=d.textlength(lab,font=f3)
    d.rounded_rectangle([70,900,70+ww+150,986],43,fill=BORD)
    d.rectangle([104,925,136,955],outline=(255,255,255),width=3); d.line([(104,934),(136,934)],fill=(255,255,255),width=3)
    d.text((158,926),lab,font=f3,fill=(255,255,255)); d.text((158+ww+14,922),"›",font=font(46),fill=(255,255,255))
    img.convert("RGB").save(out,quality=92); print(out,Image.open(out).size)
if __name__=="__main__": make(sys.argv[1],sys.argv[2],sys.argv[3])
