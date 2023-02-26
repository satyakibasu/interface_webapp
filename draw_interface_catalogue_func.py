# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 10:16:33 2022

@author: basusat
"""

from PIL import Image, ImageDraw
import math
import pandas as pd
import datetime
#import argparse
import json

#This function draws the arrow line
def _arrowedLine(draw, ptA, ptB, width=1, color=(0,255,0)):
    """Draw line from ptA to ptB with arrowhead at ptB"""
    # Get drawing context
    #draw = ImageDraw.Draw(im)
    # Draw the line without arrows
    draw.line((ptA,ptB), width=width, fill=color)

    # Now work out the arrowhead
    # = it will be a triangle with one vertex at ptB
    # - it will start at 95% of the length of the line
    # - it will extend 8 pixels either side of the line
    x0, y0 = ptA
    x1, y1 = ptB
    # Now we can work out the x,y coordinates of the bottom of the arrowhead triangle
    xb = 0.95*(x1-x0)+x0
    yb = 0.95*(y1-y0)+y0

    # Work out the other two vertices of the triangle
    # Check if line is vertical
    if x0==x1:
       vtx0 = (xb-5, yb)
       vtx1 = (xb+5, yb)
    # Check if line is horizontal
    elif y0==y1:
       vtx0 = (xb, yb+5)
       vtx1 = (xb, yb-5)
    else:
       alpha = math.atan2(y1-y0,x1-x0)-90*math.pi/180
       a = 8*math.cos(alpha)
       b = 8*math.sin(alpha)
       vtx0 = (xb+a, yb+b)
       vtx1 = (xb-a, yb-b)

    #draw.point((xb,yb), fill=(255,0,0))    # DEBUG: draw point of base in red - comment out draw.polygon() below if using this line
    #im.save('DEBUG-base.png')              # DEBUG: save

    # Now draw the arrowhead triangle
    draw.polygon([vtx0, vtx1, ptB], fill=color)
    return draw

#This function renders the picture    
def generate_diagram(row, draw):

    #text to display
    data_flow_group = row['data_flow_group_name']
    from_sys = row['from_node']
    to_sys = row['to_node']
    jira = row['interface_id']
    data_entity = row['data_entity']
    #description = row['description']
    from_narid = row['from_node_id']
    to_narid = row['to_node_id']
    input_flag = row['input_to_main_flow']
    from_is_db_sys = row['from_node_other']
    to_is_db_sys = row['to_node_other']
    reverse_flow = row['reverse_flow']

    
    #co-ordinates
    from_x0 = row['from_x0']
    from_y0 = row['from_y0']
    from_x1 = row['from_x1']
    from_y1 = row['from_y1']
    
    to_x0 = row['to_x0']
    to_y0 = row['to_y0']
    to_x1 = row['to_x1']
    to_y1 = row['to_y1']

    from_text_x = row['from_text_x']
    from_text_y = row['from_text_y']
    
    to_text_x = row['to_text_x']
    to_text_y = row['to_text_y']
    
    data_flow_group_x = row['dataflow_group_x']
    data_flow_group_y = row['dataflow_group_y']
     
    jira_x = row['jira_x']
    jira_y = row['jira_y']

    data_entity_x = row['data_entity_x']
    data_entity_y = row['data_entity_y']

    #description_x = row['description_x']
    #description_y = row['description_y']

    from_narid_x = row['from_narid_x']
    from_narid_y = row['from_narid_y']

    to_narid_x = row['to_narid_x']
    to_narid_y = row['to_narid_y']
    
    

    #Heading    
    draw.text((IMG_WIDTH/2, init_y-30), "CF INTERFACE & DATA FLOW DIAGRAM", fill=(0,255,0))
    draw.text((IMG_WIDTH/2, IMG_HEIGHT-25), "Date created: "+date_string, fill=(0,255,0))
    draw.text((IMG_WIDTH/2+200, IMG_HEIGHT-25), "created by: satyaki.basu@dws.com", fill=(0,255,0))
    
    
    #From box
    if from_is_db_sys == "Y":
        draw.rectangle([from_x0,from_y0,from_x1,from_y1], fill =(0,48,143), outline ="red")
        draw.text((from_text_x, from_text_y), from_sys, fill='#FFFFFF')
    else:
        draw.rectangle([from_x0,from_y0,from_x1,from_y1], fill =(222,222,222), outline ="red")
        draw.text((from_text_x, from_text_y), from_sys, fill=(0, 0, 0))
    
    #To box
    if to_is_db_sys == 'Y':
       draw.rectangle([to_x0,to_y0,to_x1,to_y1], fill =(0,48,143), outline ="red")
       draw.text((to_text_x, to_text_y), to_sys, fill='#FFFFFF')
    else:
        draw.rectangle([to_x0,to_y0,to_x1,to_y1], fill =(222,222,222), outline ="red")
        draw.text((to_text_x, to_text_y), to_sys, fill=(0, 0, 0))
        
    
    #Connecting arrow
    if input_flag == 'N':
        ptA = (from_x1,(from_y1-from_y0)/2+from_y0)
        ptB = (from_x0+width_of_rec+dist_between_from_to_box,(from_y1-from_y0)/2+from_y0)
        _arrowedLine(draw,ptA,ptB)
    else:
        ptA = (from_x1,(from_y1-from_y0)/2+from_y0)
        ptB = (to_x0,to_y0+height_of_rec)
        _arrowedLine(draw,ptA,ptB)
    
    if reverse_flow == 'Y':
        ptB = (from_x0+width_of_rec+dist_between_from_to_box,(from_y1-from_y0)*2/3+from_y0)
        ptA = (from_x1,(from_y1-from_y0)*2/3+from_y0)
        _arrowedLine(draw,ptB,ptA)
         #self._arrowedLine((from_x1,(from_y1-from_y0)/2+from_y0),(from_x0+self.width_of_rec+self.dist_between_from_to_box,(from_y1-from_y0)/2+from_y0))

         
    
    #Data Flow Group
    if input_flag == 'N':
        draw.text((data_flow_group_x, data_flow_group_y), data_flow_group, fill=(237,135,45))
    
    
    #JIRA No
    draw.text((jira_x, jira_y), jira, fill=(0,255,0))
    
    #Data Entity
    draw.text((data_entity_x, data_entity_y), data_entity, fill=(0,255,0))
    
    #Description
    #draw.text((description_x, description_y), description, fill=(0,255,0))
    
    #NAR ID
    if from_is_db_sys == "Y":
        draw.text((from_narid_x, from_narid_y), '('+from_narid+')', fill='#FFFFFF')
    else:
        draw.text((from_narid_x, from_narid_y), '('+from_narid+')', fill=(0, 0, 0))
        
    if to_is_db_sys == 'Y':
        draw.text((to_narid_x, to_narid_y), '('+to_narid+')', fill='#FFFFFF')
    else:
        draw.text((to_narid_x, to_narid_y), '('+to_narid+')', fill=(0, 0, 0))
    
    
#This function will generate the co-ordinates    
def generate_coordinates(row,init_x,init_y):
   
    if ly:
        init_y = ly.pop()+dist_between_from_box

    #set the from upper left co-ordinates
    from_x0 = init_x
    from_y0 = init_y
    ly.append(from_y0)
    
    #set the from lower right co-ordinates
    from_x1 = from_x0 + width_of_rec
    from_y1 = from_y0 + height_of_rec
    ly.append(from_y1)
    
    row_dict = dict(row)
    new_dict = {'from_x0':from_x0,'from_y0':from_y0,'from_x1':from_x1,'from_y1':from_y1}
    
    d = {**row_dict,**new_dict}
    
    return(d)
    
#this function checks for grouping and aligns the boxes
def checkgroup(row):
    if row['match']: 
        from_x0,from_y0,from_x1,from_y1 = group_list[len(group_list)-1]
        group_list.pop()
        row['from_x0'] = from_x0
        row['from_y0'] = from_y0
        row['from_x1'] = from_x1
        row['from_y1'] = from_y1
        
        row['to_x0'] = row['from_x1'] + dist_between_from_to_box
        row['to_y0'] = row['from_y0']
        row['to_x1'] = row['to_x0'] + width_of_rec
        row['to_y1'] = row['from_y1']
        
        group_list.append((row['to_x0'], row['to_y0'],row['to_x1'], row['to_y1']))
    else:
        group_list.append((row['to_x0'], row['to_y0'],row['to_x1'], row['to_y1']))
        
    return row


#This functions checks if there are any input systems to the sequence group flow. The to sys
#co-ordinates is mapped to the main 'to system' in the main data flow

def check_input_to_group_new(df):
        cord_df = df
        for name, group in cord_df.groupby('data_flow_group_name'):

         filter_input = group['input_to_main_flow']=='Y'
         #to_sys_index_list = group[filter_input]['to_node'].index.tolist()
         #to_sys_list = group[filter_input]['to_node'].tolist()
         #resultdict = dict(zip(to_sys_index_list, to_sys_list))
         
         max_grp = group['sequence_group_id'].value_counts().max()
         
         #This code is to reduce the gap between the boxes which are inputs to main flow  
         group.loc[group['input_to_main_flow'] == 'Y', 'from_y0'] = group['from_y0'] - (max_grp-1)*(height_of_rec+dist_between_from_box)
         group.loc[group['input_to_main_flow'] == 'Y', 'from_y1'] = group['from_y1'] - (max_grp-1)*(height_of_rec+dist_between_from_box)
        
         #This code maps to the 'to' box in main flow
         #Ref: test_grp_2, test_grp_3
         #option: 1
         to_sys_d = group[filter_input][['to_node']]
         to_sys_d['index1'] = to_sys_d.index

         group_temp = group[group['input_to_main_flow'] == 'N']
         #print(group_temp)
         group_temp = group_temp.drop_duplicates(subset='to_node', keep="first")
         
         group_temp = group_temp[['sequence_group_id','to_node','to_x0','to_y0','to_x1','to_y1']]
         temp_df = pd.merge(to_sys_d,group_temp,how='inner',left_on=['to_node'],right_on=['to_node'])
         #print(temp_df)
         
         index_values = temp_df['index1'].values
         #print(index_values)
         
         if not temp_df.empty:
            for index_value in index_values:
                
                cord_df.at[index_value,'to_x0'] = temp_df[temp_df['index1'] == index_value]['to_x0']
                cord_df.at[index_value,'to_y0'] = temp_df[temp_df['index1'] == index_value]['to_y0']
                cord_df.at[index_value,'to_x1'] = temp_df[temp_df['index1'] == index_value]['to_x1']
                cord_df.at[index_value,'to_y1'] = temp_df[temp_df['index1'] == index_value]['to_y1']
        
                #set the from_y0 and from_y1 to reduce the gap between the 'input' boxes 
                
                #cord_df.at[index_value,'from_y0'] = group.at[index_value,'from_y0']
                #cord_df.at[index_value,'from_y1'] = group.at[index_value,'from_y1']
        
        
        return cord_df 
         

def check_input_to_group(df):
    cord_df = df
    
    for name, group in cord_df.groupby('data_flow_group_name'):
        filter_input = group['input_to_main_flow']=='Y'
        #to_sys_index_list = group[filter_input]['to_node'].index.tolist()
        #to_sys_list = group[filter_input]['to_node'].tolist()
        #resultdict = dict(zip(to_sys_index_list, to_sys_list))
        
        max_grp = group['sequence_group_id'].value_counts().max()
        
        #This code is to reduce the gap between the boxes which are inputs to main flow  
        group.loc[group['input_to_main_flow'] == 'Y', 'from_y0'] = group['from_y0'] - (max_grp-1)*(height_of_rec+dist_between_from_box)
        group.loc[group['input_to_main_flow'] == 'Y', 'from_y1'] = group['from_y1'] - (max_grp-1)*(height_of_rec+dist_between_from_box)
       
        #This code maps to the 'to' box in main flow
        #Ref: test_grp_2, test_grp_3
        #option: 1
        to_sys_d = group[filter_input][['to_node']]
        to_sys_d['index1'] = to_sys_d.index
        group_temp = group[group['input_to_main_flow'] == 'N']
        
        group_temp = group_temp[['sequence_group_id','to_node','to_x0','to_y0','to_x1','to_y1']]
        temp_df = pd.merge(to_sys_d,group_temp,how='inner',left_on=['to_node'],right_on=['to_node'])

        if not temp_df.empty:
            for index_value in temp_df['index1'].values:
                
                cord_df.at[index_value,'to_x0'] = temp_df[temp_df['index1'] == index_value]['to_x0']
                cord_df.at[index_value,'to_y0'] = temp_df[temp_df['index1'] == index_value]['to_y0']
                cord_df.at[index_value,'to_x1'] = temp_df[temp_df['index1'] == index_value]['to_x1']
                cord_df.at[index_value,'to_y1'] = temp_df[temp_df['index1'] == index_value]['to_y1']
        
                #set the from_y0 and from_y1 to reduce the gap between the 'input' boxes 
                
                cord_df.at[index_value,'from_y0'] = group.at[index_value,'from_y0']
                cord_df.at[index_value,'from_y1'] = group.at[index_value,'from_y1']
        
        #option 2
        '''
        for i in resultdict:
            g = group[group['to_sys'] == resultdict[i]]
            g = g[g['input_to_flow'] == 'N']
            new_cord = g[['to_x0','to_y0','to_x1','to_y1']]
            
           
            cord_df.at[i,'to_x0'] = new_cord['to_x0']
            cord_df.at[i,'to_y0'] = new_cord['to_y0']
            cord_df.at[i,'to_x1'] = new_cord['to_x1']
            cord_df.at[i,'to_y1'] = new_cord['to_y1']
            
            #set the from_y0 and from_y1 to reduce the gap between the 'input' boxes 
            cord_df.at[i,'from_y0'] = group.at[i,'from_y0']
            cord_df.at[i,'from_y1'] = group.at[i,'from_y1']
         '''  
         
        
        #This code checks if in a sequence group, the last of the box is an input to the main flow. Then the co-ordinates needs to be changed
        #Ref: test_grp_4
        from_sys_d = group[filter_input][['from_node','sequence_group_id']]
        from_sys_d['index1'] = from_sys_d.index
       
        group_temp = group[['to_node','sequence_group_id','to_x0','to_y0','to_x1','to_y1']]
        temp_df = pd.merge(from_sys_d,group_temp,how='inner',left_on=['from_node','sequence_group_id'],right_on=['to_node','sequence_group_id'])
        
        if not temp_df.empty:
            index_value = temp_df['index1'].values[0]
            cord_df.at[index_value,'from_x0'] = temp_df['to_x0']
            cord_df.at[index_value,'from_y0'] = temp_df['to_y0']
            cord_df.at[index_value,'from_x1'] = temp_df['to_x1']
            cord_df.at[index_value,'from_y1'] = temp_df['to_y1']
      
         
      
    return cord_df    

#This reduces the gap occured due to the input boxes to the main flow for a given sequence group
def _reduce_gap_between_boxes(cord_df):
     _cord_df = cord_df
     sequence_list = list()
     data_flow_group_name = list(set(_cord_df['data_flow_group_name'].tolist()))
     
     for name, group in _cord_df.groupby(['data_flow_group_name','sequence_group_id']):
         input_flow_values = group['input_to_main_flow'].values
         from_y0 = group['from_y0'].values[0]
         sequence_list.append(from_y0)
     
         
         #This condition is for multiple level input flow where one of them is 'Y'. This only supports 'n' levels
         if len(input_flow_values) > 1 and ['Y'] in input_flow_values:
             if name[0] in data_flow_group_name:
                 new_from_y0 = sequence_list[-2]+dist_between_from_box+height_of_rec
                 new_counter = from_y0-new_from_y0
                 sequence_list.remove(from_y0)
                 sequence_list.append(new_from_y0)
                 index_values = group.index.values
                 from_y0 = group['from_y0'].values
                 
             for i in index_values:
                     if index_values[-1] == i:
                         #Apply the changes for the from box only.
                         _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - new_counter
                         _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - new_counter
                     else:
                         #Apply the changes at the index values for both the levels 
                         _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - new_counter
                         _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - new_counter
                         _cord_df.at[i,'to_y0'] = _cord_df.at[i,'to_y0'] - new_counter
                         _cord_df.at[i,'to_y1'] = _cord_df.at[i,'to_y1'] - new_counter
                 
         #This is for solo input level to the main flow where the only value is 'Y'
         elif len(input_flow_values) == 1 and ['Y'] in input_flow_values:
              if name[0] in data_flow_group_name:
                 
                 new_from_y0 = sequence_list[-2]+dist_between_from_box+height_of_rec
                 new_counter = from_y0-new_from_y0
                 sequence_list.remove(from_y0)
                 sequence_list.append(new_from_y0)
                 index_values = group.index.values
             
                 #Apply the changes at the index values for single 'from' box
                 _cord_df.at[index_values[0],'from_y0'] = _cord_df.at[index_values[0],'from_y0'] - new_counter
                 _cord_df.at[index_values[0],'from_y1'] = _cord_df.at[index_values[0],'from_y1'] - new_counter
         

     return _cord_df

#This reduces the gap between functional groups
def _reduce_gap_group(cord_df):
     _cord_df = cord_df
     global IMG_HEIGHT
     group_list = list()
     group_list.append(init_y)
    
     df = _cord_df.groupby(['data_flow_group_name']).agg({"from_y0":['min','max']})
     df .columns = df.columns.droplevel(0)
     df = df.reset_index()
 
     #a = pd.melt(df , id_vars='data_flow_group_name', value_vars=['min','max'], value_name='key')
     #a = a.sort_values(by=['data_flow_group_name'],ascending=True)
     #a = a[a['variable'] == 'max']
     #print(a)
     
     for name, group in _cord_df.groupby('data_flow_group_name'):
         
         #get the previous group's max from_y0 value
         #prev_from_y0 = group_list[-1]
         prev_from_y0 = group_list.pop()
         
         #Estimated from_y0 value
         new_min_from_y0 = prev_from_y0 + 2*(dist_between_from_box+height_of_rec) 
         
         #Get the current group's min from_y0 value
         min_from_y0 = group['from_y0'].values.min()
         reduce_by = min_from_y0 - new_min_from_y0
         
         #Now apply this deviation to the group
         index_values = group.index.values
         for i in index_values:
             _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - reduce_by
             _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - reduce_by
             _cord_df.at[i,'to_y0'] = _cord_df.at[i,'to_y0'] - reduce_by
             _cord_df.at[i,'to_y1'] = _cord_df.at[i,'to_y1'] - reduce_by
         
         #Get the max value within the group and put it in the list
         g = _cord_df[_cord_df['data_flow_group_name'] == name]
         new_from_y0 = g['from_y0'].values.max()  
         group_list.append(new_from_y0)

     IMG_HEIGHT = group_list[0]+200 
     return _cord_df
  
 

def reduce_gap_new(cord_df):
        _cord_df = cord_df

        counter = 1 #used to find the count of input to main flow
        counter_dict = dict()

        
        data_flow_group_name = list(set(_cord_df['data_flow_group_name'].tolist()))
  
        #initialize the counter dict    
        for i in data_flow_group_name:
            counter_dict[i] = 1
        
        
        for name, group in _cord_df.groupby(['data_flow_group_name','sequence_group_id']):
            input_flow_values = group['input_to_main_flow'].values
        
            #This is used to find out the sequence group levels
            if len(set(input_flow_values)) == 1 and len(input_flow_values) > 1:
                counter = len(input_flow_values)-1
                counter_dict[name[0]] = counter

            
            #This condition is for multiple level input flow where one of them is 'Y'. This only supports 2 levels
            if len(input_flow_values) > 1 and ['Y'] in input_flow_values:
                if name[0] in data_flow_group_name:
                    counter = counter_dict[name[0]] + 1
                    counter_dict[name[0]] = counter
                    index_values = group.index.values

                    
                    for i in index_values:
                        if index_values[-1] == i:
                            #Apply the changes at the index values for both the levels 
                            _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - (height_of_rec+dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - (height_of_rec+dist_between_from_box)*(counter-1)
                        else:
                            _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - (height_of_rec+dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - (height_of_rec+dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'to_y0'] = _cord_df.at[i,'to_y0'] - (height_of_rec+dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'to_y1'] = _cord_df.at[i,'to_y1'] - (height_of_rec+dist_between_from_box)*(counter-1)
                    
                    #_cord_df.at[index_values[1],'from_y0'] = _cord_df.at[index_values[1],'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                    #_cord_df.at[index_values[1],'from_y1'] = _cord_df.at[index_values[1],'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
            
                    counter = counter + 1
                
            #This is for solo input level to the main flow where the onlyy value is 'Y'
            elif len(input_flow_values) == 1 and ['Y'] in input_flow_values:
                 #data_flow_len = len(data_flow_group_name)   
                 
                 if name[0] in data_flow_group_name:
                    counter = counter_dict[name[0]]
                    counter_dict[name[0]] = counter
                    index_values = group.index.values
                 
                 
                    #Apply the changes at the index values for single 'from' box
                    _cord_df.at[index_values[0],'from_y0'] = _cord_df.at[index_values[0],'from_y0'] - (height_of_rec+dist_between_from_box)*(counter)
                    _cord_df.at[index_values[0],'from_y1'] = _cord_df.at[index_values[0],'from_y1'] - (height_of_rec+dist_between_from_box)*(counter)
            

        return _cord_df

#This function reduces the gap between the boxes due to sequencing
def reduce_gap(cord_df):
    temp_max = 0
    for name, group in cord_df.groupby(['data_flow_group_name','sequence_group_id']):
        max_grp = group['sequence_group_id'].value_counts().max()
        
        if max_grp > temp_max:
            temp_max = max_grp
    
        
        input_flow_values = group['input_to_main_flow'].values
        
        if len(input_flow_values) > 1 and ['Y'] in input_flow_values:
                index_values = group.index.values
 
                cord_df.at[index_values[0],'from_y0'] = cord_df.at[index_values[0],'from_y0'] - (height_of_rec+dist_between_from_box)*(temp_max-1)
                cord_df.at[index_values[0],'from_y1'] = cord_df.at[index_values[0],'from_y1'] - (height_of_rec+dist_between_from_box)*(temp_max-1)
                cord_df.at[index_values[0],'to_y0'] = cord_df.at[index_values[0],'to_y0'] - (height_of_rec+dist_between_from_box)*(temp_max-1)
                cord_df.at[index_values[0],'to_y1'] = cord_df.at[index_values[0],'to_y1'] - (height_of_rec+dist_between_from_box)*(temp_max-1)
                
                cord_df.at[index_values[1],'from_y0'] = cord_df.at[index_values[1],'from_y0'] - (height_of_rec+dist_between_from_box)*(temp_max-1)
                cord_df.at[index_values[1],'from_y1'] = cord_df.at[index_values[1],'from_y1'] - (height_of_rec+dist_between_from_box)*(temp_max-1)
    
        
    
    return cord_df
    

def set_other_coordinates(df, flag='M'):
    
    cord_df = df
    if flag == "M":
        
        #set the other co-ordinates 
        cord_df['to_x0'] = cord_df['from_x1'] + dist_between_from_to_box
        cord_df['to_y0'] = cord_df['from_y0']
        cord_df['to_x1'] = cord_df['to_x0'] + width_of_rec
        cord_df['to_y1'] = cord_df['from_y1']
        
    elif flag == 'O':
        cord_df['from_text_x'] = cord_df['from_x0'] + width_of_rec/3
        cord_df['from_text_y'] = cord_df['from_y0'] + height_of_rec/3
        cord_df['to_text_x'] = cord_df['to_x0'] + width_of_rec/3
        cord_df['to_text_y'] = cord_df['to_y0'] + height_of_rec/3
        
        #set Dataflow group co-ordinates
        cord_df['dataflow_group_x'] = 10
        temp = cord_df.drop_duplicates(subset='data_flow_group_name', keep="first")
        for i in temp.index.values:
                cord_df.at[i,'dataflow_group_y'] = temp.at[i,'from_y0']
            
        #cond = cord_df['input_to_main_flow'] == 'Y'
        #cord_df['dataflow_group_y'] = cord_df['from_y0']
        #cord_df.loc[cond,'dataflow_group_y']= 0
        
        
        #set the jira co-ordinates
        cord_df['jira_x'] = cord_df['from_x0'] + width_of_rec + 10
        cord_df['jira_y'] = cord_df['from_y0'] + height_of_rec/2 - 15
        
        #set the data_entity co-ordinates
        cord_df['data_entity_x'] = cord_df['from_x0'] + width_of_rec + 10
        cord_df['data_entity_y'] = cord_df['from_y0'] + height_of_rec/2 + 10
        
        '''
        #set the desc co-ordinates
        cord_df['description_x'] = cord_df['from_x0'] + width_of_rec/2
        cord_df['description_y'] = cord_df['from_y1'] + 15
        '''
               
        #set the nar co-ordinates
        cord_df['from_narid_x'] = cord_df['from_text_x'] - 15
        cord_df['from_narid_y'] = cord_df['from_text_y'] + 20 
        
        cord_df['to_narid_x'] = cord_df['to_text_x'] - 15
        cord_df['to_narid_y'] = cord_df['to_text_y'] + 20 
   
    
    
    return cord_df


def draw_image(cord_df):
    
    int_img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(int_img)
   
    cord_df.apply(generate_diagram,axis=1, draw=draw)
   
    return int_img

##################### main program #################################
def main(file,group):
    
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', type=str, required=True,help="input interface registry")
    parser.add_argument('-g','--group', type=str, required=False,help="data flow group (optional)")
    args = parser.parse_args() 
    '''
    
    #set global values
    global date_string
    global width_of_rec
    global height_of_rec
    global dist_between_from_to_box
    global dist_between_from_box
    global IMG_WIDTH
    global IMG_HEIGHT
    global group_list
    global init_x
    global init_y
    global int_img
    global ly 
    
    
    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    
    #get the mappping document
    with open("mapping/default_mapping.json") as fp:
        mapping_dict = json.load(fp)

    
    #initiliaze the x,y co-ordinates
    init_x = 100
    init_y = 40
    
    #initialize a global list used in generate co-ordinate function
    ly = []
    
    #read the interface registry file
    #mandatory_col = ['data_flow_group','sequence_group','from_sys','from_nar_id','from_is_db_sys','input_to_flow','to_sys','to_nar_id','to_is_db_sys']
    df = pd.read_csv(file)
    #df = pd.read_csv('interface_master_v6.csv')
    
    #Filter to show only groups that you are interested
    if group:
        #df = df[(df['data_flow_group'] == "fin_fpsl_grp")] 
        df = df[(df['data_flow_group_name'] == group)]
        
    if df.empty:
        raise Exception("Error: Group not found")
    
    
    #replace the df columns with the standard columns
    new_col = []
    '''
    for col in df.columns:
        for k,v in mapping_dict.items():
            if col == v:
                new_col.append(k)
    '''
    key_list = list(mapping_dict.keys())
    val_list = list(mapping_dict.values())
        
    for col in df.columns:
        try: 
            position = val_list.index(col)
            key = key_list[position]
            new_col.append(key)
        except Exception as e:
            new_col.append(col)
            print("Warning: ",e.args)
 
    df.columns = new_col 
    
    #sort by group name and sequence id
    df = df.sort_values(by=['data_flow_group_name','sequence_group_id'],ascending=True)
    
    (rows,cols) = df.shape
    
    width_of_rec =	200
    height_of_rec =	60
    dist_between_from_to_box = 100
    dist_between_from_box =	50
    max_grp_count = df[['data_flow_group_name','sequence_group_id']]\
                               .groupby(["data_flow_group_name","sequence_group_id"])\
                               .size().groupby(level=1).max()\
                               .sort_values(ascending = False).tolist()[0]
    
    IMG_WIDTH = int(init_x + (max_grp_count+1)*width_of_rec + max_grp_count*dist_between_from_to_box+init_x)
    IMG_HEIGHT = int(init_y + rows*height_of_rec +(rows*dist_between_from_box)) 
    
    #convert all columns to lower case
    df.columns = [i.lower() for i in df.columns]
    
    #Main function to generate the co-ordinates
    cord_df = df.apply(generate_coordinates,axis=1,result_type='expand',init_x=init_x,init_y=init_y)
    
    #set other main co-ordinates
    cord_df = set_other_coordinates(cord_df,flag="M") #'M' is main co-ordinates
    
 
    #This will check for sequence of grouping by comparing with prev row. These needs to be in a single line
    cord_df['match'] = cord_df['sequence_group_id'].eq(df['sequence_group_id'].shift())
    group_list = []
    cord_df = cord_df.apply(checkgroup,axis=1)
    
    
    #This checks if there are any inputs to the main data flow
    #cord_df = check_input_to_group(cord_df)
    cord_df = check_input_to_group_new(cord_df)
    
    
    #This checks if there are any inputs to the main data flow
    #cord_df = reduce_gap(cord_df)
    cord_df = _reduce_gap_between_boxes(cord_df)
    cord_df = _reduce_gap_group(cord_df)
    
    #set other main co-ordinates
    cord_df = set_other_coordinates(cord_df,flag="O") #'O' other optional co-ordinates
    
    # Draw the image
    #int_img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (255,255,255,0))
    #draw = ImageDraw.Draw(int_img)
    
    #This is the main function which draws in the image row by row based on co-ordinates   
    #cord_df.apply(generate_diagram,axis=1, draw=draw)
    #int_img.show()
    
    return cord_df

    

if __name__ == "__main__":

    file = 'files/all_patterns.csv'
    group = ""
    coordinates = main(file,group) 
    image = draw_image(coordinates)
    image.show()
