from copy import deepcopy
from enum import Enum
import json 
import shutil
import os
from pathlib import Path
from typing import Any

class ControlType(Enum):
    label               ={'type' : ''}
    image               ={'type' : ''}
    button              ={'type' : ''}
    panel               ={'type' : ''}
    stack_panel         ={'type' : ''}
    input_panel         ={'type' : ''}
    collection_panel    ={'type' : ''}
    toggle              ={'type' : ''}
    dropdown            ={'type' : ''}
    slider              ={'type' : ''}
    slider_box          ={'type' : ''}
    edit_box            ={'type' : ''}
    factory             ={'type' : ''}
    grid                ={'type' : ''}
    scroll_view         ={'type' : ''}
    scroll_track        ={'type' : ''}
    scrollbar_box       ={'type' : ''}
    selection_wheel     ={'type' : ''}
    screen              ={'type' : ''}
    custom              ={'type' : ''}
    image_cycler        ={'type' : ''}
    text_cycler         ={'type' : ''}
    grid_page_indicator ={'type' : ''}
    
    @classmethod
    def init(cls):
        with open('ControlType.json', 'r') as f:
            config_data = json.load(f)
            for member in cls:
                config_data[member.name].pop('//',None)
                member._value_ = config_data[member.name]
ControlType.init()
    
class Button:
    def __init__(self, name: str, type: ControlType = ControlType.image) -> None:
        self.name = name
        self.info: dict[str,Any] = type.value
        
    def __setitem__(self, key, val):
        self.info[key] = val
    
    def __getitem__(self, key):
        return self.info[key]
    
    def pop(self, key):
        self.info.pop(key,None)

class UI:
    def __init__(self, path: str) -> None:
        if os.path.exists(path) and os.path.isfile(path):
            with open(path,'r') as f:
                self.ui: dict[str,Any] = json.load(f)
        else :
            with open('template/ui/start_screen.json', 'r') as f:
                self.ui: dict[str,Any] = json.load(f)   
                
            for name,info in self.ui.items():
                if 'texture' in info:
                    info['texture'] = f"template/{info['texture']}" 
            
        self.path = path
        
    def clear(self) -> None:
        self.ui = {"namespace": "start"}
            
    def add(self, button : Button) -> None:
        self.ui[button.name] = button.info
        
    def remove(self, button : Button|str) -> None:
        self.ui.pop(button.name if isinstance(button,Button) else button,None)
        
    def save(self) -> None:
        with open(self.path,'w') as f:
            json.dump(self.ui,f,indent=4)
            
    def pick(self, aim_dir: str = None):
        if aim_dir is None:
            aim_dir = self.path[:-5]
            
        ui = deepcopy(self.ui)
        shutil.copytree('template', aim_dir,dirs_exist_ok=True, ignore=shutil.ignore_patterns(
            "template.png", "start_screen.json"))
        
        target_dir = Path(aim_dir)
        
        textures_src: list[str] = []
        textures_dst: list[str] = []
        for name,info in ui.items():
            if 'texture' in info:
                textures_src.append(info['texture'])
                textures_dst.append(str(target_dir/'textures'/'ui'/info['texture'].split('/')[-1]))
                info['texture'] = textures_dst[-1]
                
        with open(target_dir/'ui'/'start_screen.json','w') as f:
            json.dump(ui,f,indent=4)
            
        for src,dst in zip(textures_src,textures_dst):
            shutil.copyfile(src,dst)
            
        print(f'succeeded pick to dir: {target_dir}')
                
            
if __name__ == '__main__':
    ui = UI('test.json')
    ui.clear()
    button = Button('test_button')
    ui.add(button)
    
    ui.pick()
    ui.save()