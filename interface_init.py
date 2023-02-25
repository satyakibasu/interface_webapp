# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 16:38:59 2022

@author: ADMIN
"""

from draw_interface_catalogue_class import DrawInterfaceCatalogue
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', type=str, required=True,help="input interface registry")
    parser.add_argument('-g','--group', type=str, required=False,help="data flow group (optional)")
    parser.add_argument('-c','--config', type=str, required=False,help="configuration file (optional)")
    parser.add_argument('-m','--mapping', type=str, required=False,help= "maping configuration file (optional)")
    
    args = parser.parse_args() 
    
    file = args.file
    group = args.group
    config = args.config
    mapping = args.mapping
    
    if not config:
        config = "default_config.json"
    
    if not mapping:
        mapping = "default_mapping.json"
    
    obj = DrawInterfaceCatalogue("files/"+file,group,"config/"+config,"mapping/"+mapping)
    
    image = obj.draw_image()
    image.show()
