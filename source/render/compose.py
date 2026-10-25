from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def panel(f, cap, w):
    im=Image.open(f).convert('RGB'); s=w/im.width; im=im.resize((w,int(im.height*s)),Image.LANCZOS)
    if cap:
        d=ImageDraw.Draw(im); f=ImageFont.truetype(B,30); bb=d.textbbox((24,18),cap,font=f); d.rectangle([bb[0]-10,bb[1]-8,bb[2]+10,bb[3]+8],fill='white'); d.text((24,18),cap,font=f,fill=(60,60,60))
    return im
def sheet(rows, title, sub, out, W=1700):
    ims=[]
    for row in rows:
        w=(W-20*(len(row)-1))//len(row); ps=[panel(f,c,w) for f,c in row]; h=max(p.height for p in ps)
        r=Image.new('RGB',(W,h),'white'); x=0
        for p in ps: r.paste(p,(x,0)); x+=w+20
        ims.append(r)
    H=120+sum(i.height for i in ims)+20*(len(ims)-1)+10
    S=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(S)
    d.rectangle([10,10,W-10,108],fill=(255,243,196)); d.text((28,18),title,font=ImageFont.truetype(B,36),fill='black'); d.text((28,66),sub,font=ImageFont.truetype(R,26),fill=(50,50,50))
    y=120
    for i in ims:
        S.paste(i,(0,y)); y+=i.height
        if i is not ims[-1]: d.line([(30,y+10),(W-30,y+10)],fill=(220,220,220),width=2); y+=20
    S.save(out, optimize=True); print(out, S.size)
O='out/'
import os; os.makedirs(O,exist_ok=True)
sheet([[('raw_ov_front.png','Front'),('raw_ov_back.png','Back')]],'Pi Touch Display 2 — voice satellite stand','Remix of MegaAndy\'s Guition 4" frame + stand, stretched for a 7" landscape display with a Pi 5 inside',O+'overview.png')
sheet([[('back-features.png',None)]],'Back of the stand','Everything on the outside of the back wall',O+'back-features.png')
sheet([[('raw_mute_out.png','Outside (back of the stand)')],[('raw_mute_in.png','Inside, bare'),('raw_mute_in2.png','Inside, ReSpeaker fitted (shown see-through)')]],
      'MUTE button, USR button and mics','Close-ups of the back wall around the ReSpeaker',O+'mute-button.png')
sheet([[('raw_in_bare.png','Mounts (stand only)')],[('raw_in_full.png','Parts fitted')]],'Inside the stand','Looking in through the open front, display and frame removed',O+'inside-mounts.png')
sheet([[('raw_spk_ex.png','Exploded: parts go in from the front, before the display')],[('raw_spk_back.png','Screws from the back')]],'Speaker assembly','Foam ring, speaker, box; four M3 screws through the back wall into the box',O+'speaker-assembly.png')
sheet([[('raw_pc_closed.png','Fitted'),('raw_pc_open.png','Removed')]],'Pi ports cover','Clip-on cover over the USB / Ethernet end of the Pi (right side as you face the screen)',O+'pi-ports-cover.png')
sheet([[('raw_box.png','Rim side (faces the back wall)'),('raw_box_cut.png','Section through the fitted box')]],'Speaker box','Sealed ~160 cm³ box, screwed to the back wall from outside',O+'speaker-box-sections.png')
