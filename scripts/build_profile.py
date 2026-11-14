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
("Matrix Lab","8","F1","[matrix;research] lab"),
("Foundation","9","F1","foundation"),
]
REPLY = {'Tesla Tower': 'Tesla tower;Tesla tower ready;Placing tesla tower', 'Wireless Power Tower': 'Wireless tower;Wireless tower ready', 'Wind Turbine': 'Wind turbine;Turbine ready;Placing turbine', 'Thermal Power Plant': 'Thermal plant;Thermal plant ready', 'Solar Panel': 'Solar panel;Solar ready;Placing solar', 'Geothermal Power Station': 'Geothermal;Geothermal ready', 'Mining Machine': 'Miner;Mining machine ready;Placing miner', 'Water Pump': 'Water pump;Pump ready', 'Oil Extractor': 'Oil extractor;Extractor ready', 'Conveyor Belt Mk I': 'Belt one;Belt mark one', 'Conveyor Belt Mk II': 'Belt two;Belt mark two', 'Conveyor Belt Mk III': 'Belt three;Belt mark three', 'Sorter Mk I': 'Sorter one;Sorter mark one', 'Sorter Mk II': 'Sorter two;Sorter mark two', 'Sorter Mk III': 'Sorter three;Sorter mark three', 'Splitter': 'Splitter;Splitter ready', 'Traffic Monitor': 'Traffic monitor;Monitor ready', 'Spray Coater': 'Spray coater;Coater ready', 'Depot Mk I': 'Depot one;Depot mark one', 'Depot Mk II': 'Depot two;Depot mark two', 'Storage Tank': 'Storage tank;Tank ready', 'Arc Smelter': 'Smelter;Smelter ready;Placing smelter', 'Assembling Machine Mk I': 'Assembler one;Assembler mark one', 'Assembling Machine Mk II': 'Assembler two;Assembler mark two', 'Oil Refinery': 'Refinery;Refinery ready', 'Chemical Plant': 'Chemical plant;Chem plant ready', 'Gauss Turret': 'Gauss turret;Turret ready;Defense online', 'Matrix Lab': 'Matrix lab;Lab ready', 'Foundation': 'Foundation;Foundation ready'}
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
out.append(cmd("[cancel;stop building;exit build mode]", say("Build cancelled;Standing down;Cancelled",0)+press("ESC",1), "Cancel build mode: Escape"))
out.append(cmd("[fly;take off;lift off]", say("Thrusters engaged;Airborne;Lifting off",0)+press("SPACE",1)+pause(0.1,2)+press("SPACE",3), "Fly: double-tap Space"))
out.append(cmd("land", say("Landing;Touchdown;Descending",0)+press("LALT",1), "Land: Left Alt"))
PANELS = [
    ("Mecha Panel", "C", "[open;show;close;hide;] mecha [panel;]", "Mecha panel;Mecha status"),
    ("Statistics Panel", "P", "[open;show;close;hide;] [statistics;stats] [panel;]", "Statistics;Stats panel"),
    ("Inventory Panel", "E", "[open;show;close;hide;] inventory [panel;]", "Inventory;Inventory open"),
    ("Replicator", "F", "[open;show;close;hide;] replicator", "Replicator;Replicator online"),
    ("Details Display", "H", "[open;show;close;hide;toggle;] [detail;details] display", "Details display;Overlay toggled"),
    ("Technology Tree", "T", "[open;show;close;hide;] [technology tree;tech tree]", "Tech tree;Technology tree"),
    ("Interplanetary Logistics", "I", "[open;show;close;hide;] [interplanetary logistics;logistics]", "Logistics;Logistics panel"),
    ("Starmap", "V", "[open;show;close;hide;] [starmap;star map;system map]", "Starmap;Star map"),
    ("Planet View", "M", "[open;show;close;hide;] planet [view;]", "Planet view;Planet"),
    ("Face North", "N", "[face;rotate;point] north", "Facing north;North"),
]
for pname, pkey, pphrase, preply in PANELS:
    out.append(cmd(pphrase, say(preply,0)+press(pkey,1), f"{pname}: {pkey}"))
out.append(cmd("[copy;duplicate]", say("Copied;Duplicating",0)+keydown("LSHIFT",1)+pause(0.05,2)+mouse("LC",3)+pause(0.05,4)+keyup("LSHIFT",5), "Copy selected build: Shift + left click"))
out.append(cmd("[screenshot;take screenshot;capture screen]", say("Screenshot;Image captured",0)+keydown("LSHIFT",1)+pause(0.05,2)+press("F11",3)+pause(0.05,4)+keyup("LSHIFT",5), "Screenshot: Shift + F11"))
out.append(cmd("upgrade [mode;]", say("Upgrade mode;Upgrade ready",0)+press("U",1), "Upgrade mode: U"))
out.append(cmd("[dismantle;demolish] [mode;]", say("Dismantle mode;Demolition ready",0)+press("X",1), "Dismantle mode: X"))
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
