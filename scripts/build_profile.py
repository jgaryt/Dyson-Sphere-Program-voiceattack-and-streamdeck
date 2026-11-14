import uuid
from xml.sax.saxutils import escape
rows = [
("Tesla Tower","1","F1","tesla tower"),
("Wireless Power Tower","1","F2","wireless [power;] tower"),
("Wind Turbine","1","F4","wind turbine"),
("Thermal Power Plant","1","F5","thermal [power;] plant"),
("Solar Panel","1","F6","solar panel"),
("Geothermal Power Station","1","F7","geothermal [power station;station;]"),
("Mining Machine","2","F1","[mining machine;miner]"),
("Water Pump","2","F3","water pump"),
("Oil Extractor","2","F4","oil extractor"),
("Conveyor Belt Mk I","3","F1","[conveyor belt;conveyor;belt] [one;mark one]"),
("Conveyor Belt Mk II","3","F2","[conveyor belt;conveyor;belt] [two;mark two]"),
("Conveyor Belt Mk III","3","F3","[conveyor belt;conveyor;belt] [three;mark three]"),
("Sorter Mk I","3","F4","sorter [one;mark one]"),
("Sorter Mk II","3","F5","sorter [two;mark two]"),
("Sorter Mk III","3","F6","sorter [three;mark three]"),
("Splitter","3","F8","splitter"),
("Traffic Monitor","3","F9","traffic monitor"),
("Spray Coater","3","F10","spray coater"),
("Depot Mk I","4","F1","[depot;storage;container] [one;mark one]"),
("Depot Mk II","4","F2","[depot;storage;container] [two;mark two]"),
("Storage Tank","4","F3","[storage;] tank"),
("Arc Smelter","5","F1","[arc;] smelter"),
("Assembling Machine Mk I","5","F3","assembler [one;mark one]"),
("Assembling Machine Mk II","5","F4","assembler [two;mark two]"),
("Oil Refinery","5","F6","[oil;] refinery"),
("Chemical Plant","5","F7","[chemical;chem] plant"),
("Gauss Turret","7","F1","gauss turret"),
("Missile Turret","7","F2","missile turret"),
("Implosion Cannon","7","F3","implosion cannon"),
("Signal Tower","7","F9","signal tower"),
("Matrix Lab","8","F1","[matrix;research] lab"),
("Foundation","9","F1","foundation"),
]
REPLY = {'Tesla Tower': 'Deploying tesla tower;Constructing tesla tower', 'Wireless Power Tower': 'Deploying wireless tower;Constructing wireless tower', 'Wind Turbine': 'Deploying wind turbine;Constructing wind turbine', 'Thermal Power Plant': 'Deploying thermal plant;Constructing thermal plant', 'Solar Panel': 'Deploying solar panel;Constructing solar panel', 'Geothermal Power Station': 'Deploying geothermal station;Constructing geothermal station', 'Mining Machine': 'Deploying mining machine;Constructing mining machine', 'Water Pump': 'Deploying water pump;Constructing water pump', 'Oil Extractor': 'Deploying oil extractor;Constructing oil extractor', 'Conveyor Belt Mk I': 'Deploying belt mark one;Constructing belt mark one', 'Conveyor Belt Mk II': 'Deploying belt mark two;Constructing belt mark two', 'Conveyor Belt Mk III': 'Deploying belt mark three;Constructing belt mark three', 'Sorter Mk I': 'Deploying sorter mark one;Constructing sorter mark one', 'Sorter Mk II': 'Deploying sorter mark two;Constructing sorter mark two', 'Sorter Mk III': 'Deploying sorter mark three;Constructing sorter mark three', 'Splitter': 'Deploying splitter;Constructing splitter', 'Traffic Monitor': 'Deploying traffic monitor;Constructing traffic monitor', 'Spray Coater': 'Deploying spray coater;Constructing spray coater', 'Depot Mk I': 'Deploying depot mark one;Constructing depot mark one', 'Depot Mk II': 'Deploying depot mark two;Constructing depot mark two', 'Storage Tank': 'Deploying storage tank;Constructing storage tank', 'Arc Smelter': 'Deploying arc smelter;Constructing arc smelter', 'Assembling Machine Mk I': 'Deploying assembler mark one;Constructing assembler mark one', 'Assembling Machine Mk II': 'Deploying assembler mark two;Constructing assembler mark two', 'Oil Refinery': 'Deploying oil refinery;Constructing oil refinery', 'Chemical Plant': 'Deploying chemical plant;Constructing chemical plant', 'Gauss Turret': 'Deploying gauss turret;Constructing gauss turret', 'Missile Turret': 'Deploying missile turret;Constructing missile turret', 'Implosion Cannon': 'Deploying implosion cannon;Constructing implosion cannon', 'Signal Tower': 'Deploying signal tower;Constructing signal tower', 'Matrix Lab': 'Deploying matrix lab;Constructing matrix lab', 'Foundation': 'Deploying foundation;Constructing foundation'}
codes = {str(i):48+i for i in range(1,10)}
codes.update({f"F{i}":111+i for i in range(1,11)})
codes.update({"U":85,"X":88,"ESC":27,"SPACE":32,"LALT":164,"LSHIFT":160,"H":72,"T":84,"R":82,"F11":122,"I":73,"V":86,"M":77,"N":78,"C":67,"P":80,"E":69,"F":70})
G=lambda: str(uuid.uuid4())
def press(key, ordinal):
    return f"""        <CommandAction>
          <Ordinal>{ordinal}</Ordinal>
          <Id>{G()}</Id>
          <ActionType>PressKey</ActionType>
          <Duration>0.05</Duration>
          <Delay>0</Delay>
          <KeyCodes><unsignedShort>{codes[key]}</unsignedShort></KeyCodes>
          <Context />
          <Disabled>false</Disabled>
        </CommandAction>
"""
def pause(sec, ordinal):
    return f"""        <CommandAction>
          <Ordinal>{ordinal}</Ordinal>
          <Id>{G()}</Id>
          <ActionType>Pause</ActionType>
          <Duration>{sec}</Duration>
          <Delay>0</Delay>
          <KeyCodes />
          <Context />
          <Disabled>false</Disabled>
        </CommandAction>
"""
def say(text, ordinal):
    return f"""        <CommandAction>
          <Ordinal>{ordinal}</Ordinal>
          <Id>{G()}</Id>
          <ActionType>Say</ActionType>
          <Duration>0</Duration>
          <Delay>0</Delay>
          <KeyCodes />
          <Context>{escape(text)}</Context>
          <Context2>[Azure] Blue (en-US)</Context2>
          <X>100</X>
          <Y>0</Y>
          <Disabled>false</Disabled>
        </CommandAction>
"""
def keydown(key, ordinal):
    return press(key, ordinal).replace("<ActionType>PressKey</ActionType>", "<ActionType>KeyDown</ActionType>")
def keyup(key, ordinal):
    return press(key, ordinal).replace("<ActionType>PressKey</ActionType>", "<ActionType>KeyUp</ActionType>")
def mouse(code, ordinal):
    return f"""        <CommandAction>
          <Ordinal>{ordinal}</Ordinal>
          <Id>{G()}</Id>
          <ActionType>MouseAction</ActionType>
          <Duration>0</Duration>
          <Delay>0</Delay>
          <KeyCodes />
          <Context>{code}</Context>
          <Disabled>false</Disabled>
        </CommandAction>
"""
def cmd(phrase, actions, desc):
    return f"""    <Command>
      <Id>{G()}</Id>
      <BaseId>{G()}</BaseId>
      <CommandString>{escape(phrase)}</CommandString>
      <Description>{escape(desc)}</Description>
      <ActionSequence>
{actions}      </ActionSequence>
      <Async>true</Async>
      <Enabled>true</Enabled>
      <Category>Dyson Sphere Program</Category>
      <UseShortcut>false</UseShortcut>
      <UseSpokenPhrase>true</UseSpokenPhrase>
      <UseJoystick>false</UseJoystick>
      <UseMouse>false</UseMouse>
    </Command>
"""
out=[]
for name,cat,fk,phrase in rows:
    other = "8" if cat=="9" else "9"
    acts = say(REPLY[name],0)+press(other,1)+pause(0.1,2)+press(cat,3)+pause(0.1,4)+press(fk,5)
    out.append(cmd(f"[build;place;] {phrase}", acts, f"{name}: {cat} then {fk}"))
out.append(cmd("[cancel;stop building;exit build mode]", say("Build cancelled;Standing down",0)+press("ESC",1), "Cancel build mode: Escape"))
out.append(cmd("[fly;take off;lift off]", say("Thrusters engaged;Airborne;Lifting off",0)+press("SPACE",1)+pause(0.1,2)+press("SPACE",3), "Fly: double-tap Space"))
out.append(cmd("land", say("Landing;Descending",0)+press("LALT",1), "Land: Left Alt"))
PANELS = [
    ("Mecha Panel", "C", "[open;show;close;hide;] mecha [panel;]", "Displaying mecha status;Mecha status"),
    ("Statistics Panel", "P", "[open;show;close;hide;] [statistics;stats] [panel;]", "Displaying statistics"),
    ("Inventory Panel", "E", "[open;show;close;hide;] inventory [panel;]", "Displaying inventory"),
    ("Replicator", "F", "[open;show;close;hide;] replicator", "Replicator online;Displaying replicator"),
    ("Details Display", "H", "[open;show;close;hide;toggle;] [detail;details] display", "Overlay toggled;Displaying details"),
    ("Technology Tree", "T", "[open;show;close;hide;] [technology tree;tech tree]", "Displaying technology"),
    ("Interplanetary Logistics", "I", "[open;show;close;hide;] [interplanetary logistics;logistics]", "Displaying logistics"),
    ("Starmap", "V", "[open;show;close;hide;] [starmap;star map;system map]", "Displaying starmap;Charting stars"),
    ("Planet View", "M", "[open;show;close;hide;] planet [view;]", "Displaying planet"),
    ("Face North", "N", "[face;rotate;point] north", "Facing north;Heading north"),
]
for pname, pkey, pphrase, preply in PANELS:
    out.append(cmd(pphrase, say(preply,0)+press(pkey,1), f"{pname}: {pkey}"))
out.append(cmd("[copy;duplicate]", say("Copying settings;Duplicating",0)+keydown("LSHIFT",1)+pause(0.05,2)+mouse("LC",3)+pause(0.05,4)+keyup("LSHIFT",5), "Copy selected build: Shift + left click"))
out.append(cmd("[screenshot;take screenshot;capture screen]", say("Image captured;Capturing image",0)+keydown("LSHIFT",1)+pause(0.05,2)+press("F11",3)+pause(0.05,4)+keyup("LSHIFT",5), "Screenshot: Shift + F11"))
out.append(cmd("upgrade [mode;]", say("Upgrade engaged;Upgrading",0)+press("U",1), "Upgrade mode: U"))
out.append(cmd("[dismantle;demolish] [mode;]", say("Demolition engaged;Dismantling",0)+press("X",1), "Dismantle mode: X"))
import re as _rx
_re_cmds=_rx.compile(r"<CommandString>(.*?)</CommandString>")
_re_says=_rx.compile(r"<ActionType>Say</ActionType>.*?<Context>(.*?)</Context>", _rx.S)

def _expand(phrase):
    import itertools, re as _re
    parts=_re.split(r"(\[[^\]]*\])", phrase)
    opts=[[o for o in p[1:-1].split(";")] if p.startswith("[") else [p] for p in parts]
    return {" ".join("".join(c).split()).lower() for c in itertools.product(*opts)}
_spoken=set()
for _c in _re_cmds.findall("".join(out)):
    _spoken |= _expand(_c)
for _r in _re_says.findall("".join(out)):
    for _line in _r.split(";"):
        if _line.strip().lower() in _spoken:
            raise SystemExit(f"Reply '{_line}' matches a voice command and would cause a feedback loop")
xml = f"""<?xml version="1.0" encoding="utf-8"?>
<Profile xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <HasMB>false</HasMB>
  <Id>{G()}</Id>
  <Name>Dyson Sphere Program - Build Hotkeys</Name>
  <Commands>
{''.join(out)}  </Commands>
</Profile>
"""
open("profiles/DSP Build Hotkeys-Profile.vap","w",encoding="utf-8").write(xml)
print(len(out))
