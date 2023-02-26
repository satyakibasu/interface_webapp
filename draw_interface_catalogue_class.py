# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:42:17 2022

@author: ADMIN
"""

from PIL import Image, ImageDraw, ImageFont
import math
import pandas as pd
import datetime
import json

class DrawInterfaceCatalogue:
    #declare the class attributes
    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    width_of_rec =	200 #default values
    height_of_rec =	60 #default values
    dist_between_from_to_box = 100 #default values
    dist_between_from_box =	50 #default values
    init_x = 100 #default values
    init_y = 40 #default values

    
    def __init__(self,file,group,config,mapping):
       #declare object attributes
       self.ly = []
       self.group_list = []
       self.IMG_WIDTH = 0
       self.IMG_HEIGHT = 0
       self._cord_df = 0
       
       
       #read the config file
       with open(config) as fp:
           config_dict = json.load(fp)
       
       #set the config parameters
       self.background_color = config_dict['background_color']
       self.width_of_rec = config_dict['width_of_rec']
       self.height_of_rec = config_dict['height_of_rec']
       self.dist_between_from_to_box = config_dict['dist_between_from_to_box']
       self.dist_between_from_box = config_dict['dist_between_from_box']
       DrawInterfaceCatalogue.init_x = config_dict['init_x_coordinates']
       DrawInterfaceCatalogue.init_y = config_dict['init_y_coordinates']
       self.heading_text = config_dict['heading_text']
       self.heading_text_color = config_dict['heading_text_color']
       self.node_color = config_dict['node_color']
       self.node_text_color = config_dict['node_text_color']
       self.other_node_color = config_dict['other_node_color']
       self.other_node_text_color = config_dict['other_node_text_color']
       self.arrow_color = config_dict['arrow_color']
       self.text_color = config_dict['text_color']
       self.group_name_color = config_dict['group_name_color']
       self.node_id_color = config_dict['node_id_color']
       self.other_node_id_color = config_dict['other_node_id_color']
     
      #read the input file
       df = pd.read_csv(file)
       with open(mapping) as fp:
           mapping_dict = json.load(fp)
         
      #this looks up the mapping json
       new_col = []
       '''
       for col in df.columns:
            #print(col)
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
               

       '''
       print(df.columns)   
       new_col = []
       for col in df.columns:
            temp_col = [i for i in mapping_dict if mapping_dict[i] == col]
            new_col.append(temp_col[0])
       '''
      
       df.columns = new_col

       
       if group:
           #df = df[(df['data_flow_group'] == "fin_fpsl_grp")] 
           df = df[(df['data_flow_group_name'] == group)]
        
       if df.empty:
            raise Exception("Error: Group not found")
        
       df = df.sort_values(by=['data_flow_group_name','sequence_group_id'],ascending=True)
       df.columns = [i.lower() for i in df.columns]
        
       (rows,cols) = df.shape
       max_grp_count = df[['data_flow_group_name','sequence_group_id']]\
                               .groupby(["data_flow_group_name","sequence_group_id"])\
                               .size().groupby(level=1).max()\
                               .sort_values(ascending = False).tolist()[0]
       
       self.IMG_WIDTH = int(self.init_x + (max_grp_count+1)*self.width_of_rec + max_grp_count*self.dist_between_from_to_box+self.init_x)
       self.IMG_HEIGHT = int(self.init_y + rows*self.height_of_rec +(rows*self.dist_between_from_box)) 
       
       self._cord_df = df
       
 
    
    def _generate_coordinates(self):
        #Step 1: Set the base co-ordinates. Every row is mapped as 1-2-1 
        #self._cord_df = self.df.apply(self._set_coordinates,axis=1,result_type='expand')
        self._cord_df = self._cord_df.apply(self._set_coordinates,axis=1,result_type='expand')

      
        #Step 2: Set the other other main co-ordinates
        self._set_other_coordinates(flag="M") #'M' is main co-ordinates
        
        #Step 3: This function checks if there is a sequence that the boxes needs to be plotted
        # in the same line. This aligns the co-ordinates
        #self._check_sequence_group()
        
            ####Option 1: using list#####
        #self._check_sequence_group_new()
        
            ####Option 2 - using generator####
        dfs = self._check_sequence_group_new()
        self._cord_df = pd.concat([df for df in dfs], axis=0)
        
        
        
        #Step 4: This checks if there are any inputs to the main data flow
        #self._check_input_to_group_new()
        self._check_input_to_group_new()
        
        #Step 5: This reduces the gap occured due to the input boxes to the main flow
        # This can be optional
        self._reduce_gap_between_boxes()
        #self._reduce_gap()        
        self._reduce_gap_group()
        
        #Step 6: Set other main co-ordinates
        self._set_other_coordinates(flag="O") #'O' other optional co-ordinates
        
   
    def draw_image(self, coordinates=pd.DataFrame()):
        if not coordinates.empty:
           self._cord_df = coordinates
        else:
            self._generate_coordinates()
        
        int_img = Image.new('RGB', (self.IMG_WIDTH, self.IMG_HEIGHT), self.background_color)
        self.draw = ImageDraw.Draw(int_img)
        
        sig_font = ImageFont.truetype("Arial.ttf")
        #sig_font = ImageFont.load_default()
        
        heading_font = ImageFont.truetype("Arial.ttf",14)
        #heading_font = ImageFont.load_default()
        
        #Heading
        signature = "created by: Satyaki Basu (mail2samratbasu@gmail.com)"

        self.draw.text((self.IMG_WIDTH/2-30, DrawInterfaceCatalogue.init_y-30), self.heading_text, font=heading_font,fill=self.heading_text_color)
        self.draw.text((self.IMG_WIDTH/2, self.IMG_HEIGHT-25), signature, fill=self.heading_text_color, font=sig_font)
        self.draw.text((DrawInterfaceCatalogue.init_x, self.IMG_HEIGHT-25), "Date created: "+self.date_string, fill=self.heading_text_color, font=sig_font)
        
        self._cord_df.apply(self._generate_diagram,axis=1)
        
        return int_img
   
    #This reduces the gap occured due to the input boxes to the main flow for a given sequence group
    def _reduce_gap_between_boxes(self):
        _cord_df = self._cord_df
        sequence_list = list()
        data_flow_group_name = list(set(_cord_df['data_flow_group_name'].tolist()))
        
        for name, group in _cord_df.groupby(['data_flow_group_name','sequence_group_id']):
            input_flow_values = group['input_to_main_flow'].values
            from_y0 = group['from_y0'].values[0]
            sequence_list.append(from_y0)
        
            
            #This condition is for multiple level input flow where one of them is 'Y'. This only supports 'n' levels
            if len(input_flow_values) > 1 and ['Y'] in input_flow_values:
                if name[0] in data_flow_group_name:
                    new_from_y0 = sequence_list[-2]+self.dist_between_from_box+self.height_of_rec
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
                    
                    new_from_y0 = sequence_list[-2]+self.dist_between_from_box+self.height_of_rec
                    new_counter = from_y0-new_from_y0
                    sequence_list.remove(from_y0)
                    sequence_list.append(new_from_y0)
                    index_values = group.index.values
                
                    #Apply the changes at the index values for single 'from' box
                    _cord_df.at[index_values[0],'from_y0'] = _cord_df.at[index_values[0],'from_y0'] - new_counter
                    _cord_df.at[index_values[0],'from_y1'] = _cord_df.at[index_values[0],'from_y1'] - new_counter
            

        self._cord_df = _cord_df
   
     #This reduces the gap between functional groups
    def _reduce_gap_group(self):
        _cord_df = self._cord_df
        group_list = list()
        group_list.append(DrawInterfaceCatalogue.init_y)
       
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
            new_min_from_y0 = prev_from_y0 + 2*(self.dist_between_from_box+self.height_of_rec) 
            
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
        
        #override the Height of the image due to the reduction of group
        self.IMG_HEIGHT = group_list[0]+200

        self._cord_df = _cord_df
        
        
     #This reduces the gap occured due to the input boxes to the main flow for a given sequence group
    def _reduce_gap_new(self):
        _cord_df = self._cord_df

        counter = 1 #used to find the count of input to main flow
        counter_dict = dict()

        
        data_flow_group_name = list(set(_cord_df['data_flow_group_name'].tolist()))
  
        #initialize the counter dict    
        for i in data_flow_group_name:
            counter_dict[i] = 1
        
        print("counter dict before for loop", counter_dict)
        for name, group in _cord_df.groupby(['data_flow_group_name','sequence_group_id']):
            input_flow_values = group['input_to_main_flow'].values
            
            print("name:", name)
            print("group:\n",group)
            print("input flow values:", input_flow_values)
        
            #This is used to find out the sequence group levels
            if len(set(input_flow_values)) == 1 and len(input_flow_values) > 1:
                counter = len(input_flow_values)-1
                counter_dict[name[0]] = counter

            print("counter dict after for loop", counter_dict)
            
            #This condition is for multiple level input flow where one of them is 'Y'. This only supports 'n' levels
            if len(input_flow_values) > 1 and ['Y'] in input_flow_values:
                if name[0] in data_flow_group_name:
                    counter = counter_dict[name[0]] + 1
                    counter_dict[name[0]] = counter
                    index_values = group.index.values
                    
                    print("new counter:", counter_dict)
                    print(index_values)
                    print("calc:",(self.height_of_rec+self.dist_between_from_box)*(counter-1))
                    

                    for i in index_values:
                        if index_values[-1] == i:
                            #Apply the changes at the index values for both the levels 
                            _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                        else:
                            _cord_df.at[i,'from_y0'] = _cord_df.at[i,'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'from_y1'] = _cord_df.at[i,'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'to_y0'] = _cord_df.at[i,'to_y0'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                            _cord_df.at[i,'to_y1'] = _cord_df.at[i,'to_y1'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                    
                    #_cord_df.at[index_values[1],'from_y0'] = _cord_df.at[index_values[1],'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
                    #_cord_df.at[index_values[1],'from_y1'] = _cord_df.at[index_values[1],'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(counter-1)
            
                    counter = counter + 1
                    print(_cord_df[_cord_df['sequence_group_id']==name[1]])
                
            #This is for solo input level to the main flow where the only value is 'Y'
            elif len(input_flow_values) == 1 and ['Y'] in input_flow_values:
                 if name[0] in data_flow_group_name:
                    counter = counter_dict[name[0]]
                    counter_dict[name[0]] = counter
                    index_values = group.index.values
                 
                 
                    #Apply the changes at the index values for single 'from' box
                    _cord_df.at[index_values[0],'from_y0'] = _cord_df.at[index_values[0],'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(counter)
                    _cord_df.at[index_values[0],'from_y1'] = _cord_df.at[index_values[0],'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(counter)
            

        self._cord_df = _cord_df
   
    
    #This reduces the gap occured due to the input boxes to the main flow for a given sequence group
    def _reduce_gap(self):
        _cord_df = self._cord_df
        temp_max = 0

        for name, group in _cord_df.groupby(['data_flow_group_name','sequence_group_id']):
            
            max_grp = group['sequence_group_id'].value_counts().max()
            if max_grp > temp_max:
                temp_max = max_grp
                a = temp_max-1
        
            input_flow_values = group['input_to_main_flow'].values
        
            if len(input_flow_values) > 1 and ['Y'] in input_flow_values:
                index_values = group.index.values
 
                _cord_df.at[index_values[0],'from_y0'] = _cord_df.at[index_values[0],'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(a)
                _cord_df.at[index_values[0],'from_y1'] = _cord_df.at[index_values[0],'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(a)
                _cord_df.at[index_values[0],'to_y0'] = _cord_df.at[index_values[0],'to_y0'] - (self.height_of_rec+self.dist_between_from_box)*(a)
                _cord_df.at[index_values[0],'to_y1'] = _cord_df.at[index_values[0],'to_y1'] - (self.height_of_rec+self.dist_between_from_box)*(a)
                
                _cord_df.at[index_values[1],'from_y0'] = _cord_df.at[index_values[1],'from_y0'] - (self.height_of_rec+self.dist_between_from_box)*(a)
                _cord_df.at[index_values[1],'from_y1'] = _cord_df.at[index_values[1],'from_y1'] - (self.height_of_rec+self.dist_between_from_box)*(a)
        
                a = temp_max

        self._cord_df = _cord_df
    
  
    #This function checks if there is a sequence that the boxes needs to be plotted
    # in the same line. This aligns the co-ordinates
    def _check_sequence_group(self):
        self.group_list = []
        self._cord_df['match'] = self._cord_df['sequence_group_id'].eq(self.df['sequence_group_id'].shift())
        
        self._cord_df = self._cord_df.apply(self._get_sequence_coordinates,axis=1)
        
        #self._cord_df.to_csv('old_func.csv')

    
    #This function checks if there is a sequence that the boxes needs to be plotted
    # in the same line. This aligns the co-ordinates
    def _check_sequence_group_new(self):
        #dfs = [] #uncomment this for using Option 1: using list
        cord_df = self._cord_df
        
        for name, group in cord_df.groupby('data_flow_group_name'):
            group['in_sequence'] = group['sequence_group_id'].eq(group['sequence_group_id'].shift())
            group = group.apply(self._get_sequence_coordinates,axis=1)
            group.drop(['in_sequence'],axis=1)
            #Option 1 - using list
            #dfs.append(group)
 
            #Option 2 - using generator
            yield group

        #Option 1 - using list (uncomment the below lines)
        #cord_df = pd.concat([df for df in dfs], axis=0)
        #self._cord_df = cord_df

    #This function is called by _check_sequence_group and returns the
    #new set of co-ordinates
    def _get_sequence_coordinates(self,row):
        if row['in_sequence']: 
            from_x0,from_y0,from_x1,from_y1 = self.group_list[len(self.group_list)-1]
            self.group_list.pop()
            row['from_x0'] = from_x0
            row['from_y0'] = from_y0
            row['from_x1'] = from_x1
            row['from_y1'] = from_y1
        
            row['to_x0'] = row['from_x1'] + self.dist_between_from_to_box
            row['to_y0'] = row['from_y0']
            row['to_x1'] = row['to_x0'] + self.width_of_rec
            row['to_y1'] = row['from_y1']
        
            self.group_list.append((row['to_x0'], row['to_y0'],row['to_x1'], row['to_y1']))
        else:
            self.group_list.append((row['to_x0'], row['to_y0'],row['to_x1'], row['to_y1']))
        
        return row
 
    
    #This functions checks if there are any input systems to the sequence group flow. The to sys
    #co-ordinates is mapped to the main 'to system' in the main data flow

    def _check_input_to_group_new(self):
            cord_df = self._cord_df

            for name, group in cord_df.groupby('data_flow_group_name'):
    
             filter_input = group['input_to_main_flow']=='Y'
             #to_sys_index_list = group[filter_input]['to_node'].index.tolist()
             #to_sys_list = group[filter_input]['to_node'].tolist()
             #resultdict = dict(zip(to_sys_index_list, to_sys_list))
             
             max_grp = group['sequence_group_id'].value_counts().max()
             
             #This code is to reduce the gap between the boxes which are inputs to main flow  
             group.loc[group['input_to_main_flow'] == 'Y', 'from_y0'] = group['from_y0'] - (max_grp-1)*(self.height_of_rec + self.dist_between_from_box)
             group.loc[group['input_to_main_flow'] == 'Y', 'from_y1'] = group['from_y1'] - (max_grp-1)*(self.height_of_rec + self.dist_between_from_box)
            
             #This code maps to the 'to' box in main flow
             #Ref: test_grp_2, test_grp_3
             #option: 1
             to_sys_d = group[filter_input][['to_node']]
             to_sys_d['index1'] = to_sys_d.index

             group_temp = group[group['input_to_main_flow'] == 'N']
             group_temp = group_temp.drop_duplicates(subset='to_node', keep="first")
                      
             group_temp = group_temp[['sequence_group_id','to_node','to_x0','to_y0','to_x1','to_y1']]
             temp_df = pd.merge(to_sys_d,group_temp,how='inner',left_on=['to_node'],right_on=['to_node'])
             
             if not temp_df.empty:
                for index_value in temp_df['index1'].values:
                    
                    cord_df.at[index_value,'to_x0'] = temp_df[temp_df['index1'] == index_value]['to_x0']
                    cord_df.at[index_value,'to_y0'] = temp_df[temp_df['index1'] == index_value]['to_y0']
                    cord_df.at[index_value,'to_x1'] = temp_df[temp_df['index1'] == index_value]['to_x1']
                    cord_df.at[index_value,'to_y1'] = temp_df[temp_df['index1'] == index_value]['to_y1']
            
                    #set the from_y0 and from_y1 to reduce the gap between the 'input' boxes 
                    
                    #cord_df.at[index_value,'from_y0'] = group.at[index_value,'from_y0']
                    #cord_df.at[index_value,'from_y1'] = group.at[index_value,'from_y1']
            
            self._cord_df = cord_df
         
    
    def _check_input_to_group(self):
        _cord_df = self._cord_df
        
       
        for name, group in _cord_df.groupby('data_flow_group_name'):

            filter_input = group['input_to_main_flow']=='Y'
            #to_sys_index_list = group[filter_input]['to_node'].index.tolist()
            #to_sys_list = group[filter_input]['to_node'].tolist()
            #resultdict = dict(zip(to_sys_index_list, to_sys_list))
            
            max_grp = group['sequence_group_id'].value_counts().max()
            
            #This code is to reduce the gap between the boxes which are inputs to main flow  
            group.loc[group['input_to_main_flow'] == 'Y', 'from_y0'] = group['from_y0'] - (max_grp-1)*(self.height_of_rec+self.dist_between_from_box)
            group.loc[group['input_to_main_flow'] == 'Y', 'from_y1'] = group['from_y1'] - (max_grp-1)*(self.height_of_rec+self.dist_between_from_box)
           
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
                    
                    
                    _cord_df.at[index_value,'to_x0'] = temp_df[temp_df['index1'] == index_value]['to_x0']
                    _cord_df.at[index_value,'to_y0'] = temp_df[temp_df['index1'] == index_value]['to_y0']
                    _cord_df.at[index_value,'to_x1'] = temp_df[temp_df['index1'] == index_value]['to_x1']
                    _cord_df.at[index_value,'to_y1'] = temp_df[temp_df['index1'] == index_value]['to_y1']
            
                    #set the from_y0 and from_y1 to reduce the gap between the 'input' boxes 
                    
                    _cord_df.at[index_value,'from_y0'] = group.at[index_value,'from_y0']
                    _cord_df.at[index_value,'from_y1'] = group.at[index_value,'from_y1']
                    
            
            #option 2
            '''
            for i in resultdict:
                g = group[group['to_sys'] == resultdict[i]]
                g = g[g['input_to_flow'] == 'N']
                new_cord = g[['to_x0','to_y0','to_x1','to_y1']]
                
               
                _cord_df.at[i,'to_x0'] = new_cord['to_x0']
                _cord_df.at[i,'to_y0'] = new_cord['to_y0']
                _cord_df.at[i,'to_x1'] = new_cord['to_x1']
                _cord_df.at[i,'to_y1'] = new_cord['to_y1']
                
                #set the from_y0 and from_y1 to reduce the gap between the 'input' boxes 
                _cord_df.at[i,'from_y0'] = group.at[i,'from_y0']
                _cord_df.at[i,'from_y1'] = group.at[i,'from_y1']
             '''  
            
            
            #This code checks if in a sequence group, the last of the box is an input to the main flow. Then the co-ordinates needs to be changed
            #Ref: test_grp_4
            from_sys_d = group[filter_input][['from_node','sequence_group_id']]
            from_sys_d['index1'] = from_sys_d.index
           
            group_temp = group[['to_node','sequence_group_id','to_x0','to_y0','to_x1','to_y1']]
            temp_df = pd.merge(from_sys_d,group_temp,how='inner',left_on=['from_node','sequence_group_id'],right_on=['to_node','sequence_group_id'])
            
            if not temp_df.empty:
                index_value = temp_df['index1'].values[0]
                _cord_df.at[index_value,'from_x0'] = temp_df['to_x0']
                _cord_df.at[index_value,'from_y0'] = temp_df['to_y0']
                _cord_df.at[index_value,'from_x1'] = temp_df['to_x1']
                _cord_df.at[index_value,'from_y1'] = temp_df['to_y1']
             
        self._cord_df = _cord_df
    

    def _set_other_coordinates(self,flag):
        _cord_df = self._cord_df
        if flag == "M":
        
            #set the other co-ordinates 
            _cord_df['to_x0'] = _cord_df['from_x1'] + self.dist_between_from_to_box
            _cord_df['to_y0'] = _cord_df['from_y0']
            _cord_df['to_x1'] = _cord_df['to_x0'] + self.width_of_rec
            _cord_df['to_y1'] = _cord_df['from_y1']
        
        elif flag == 'O':
            _cord_df['from_text_x'] = _cord_df['from_x0'] + self.width_of_rec/3
            _cord_df['from_text_y'] = _cord_df['from_y0'] + self.height_of_rec/3
            _cord_df['to_text_x'] = _cord_df['to_x0'] + self.width_of_rec/3
            _cord_df['to_text_y'] = _cord_df['to_y0'] + self.height_of_rec/3
        
            #set Dataflow group co-ordinates
            _cord_df['dataflow_group_x'] = 10
            temp = _cord_df.drop_duplicates(subset='data_flow_group_name', keep="first")
            for i in temp.index.values:
                _cord_df.at[i,'dataflow_group_y'] = temp.at[i,'from_y0']
                    
            #cond = _cord_df['input_to_main_flow'] == 'Y'
            #_cord_df['dataflow_group_y'] = _cord_df['from_y0']
            #_cord_df.loc[cond,'dataflow_group_y']= 0
            
            
            #set the interface id co-ordinates
            _cord_df['interface_id_x'] = _cord_df['from_x0'] + self.width_of_rec + 10
            _cord_df['interface_id_y'] = _cord_df['from_y0'] + self.height_of_rec/2 - 15
            
            #set the data_entity co-ordinates
            _cord_df['data_entity_x'] = _cord_df['from_x0'] + self.width_of_rec + 10
            _cord_df['data_entity_y'] = _cord_df['from_y0'] + self.height_of_rec/2 + 10
            
            '''
            #set the desc co-ordinates
            _cord_df['description_x'] = _cord_df['from_x0'] + width_of_rec/2
            _cord_df['description_y'] = _cord_df['from_y1'] + 15
            '''
                   
            #set the node_id co-ordinates
            _cord_df['from_node_id_x'] = _cord_df['from_text_x'] - 15
            _cord_df['from_node_id_y'] = _cord_df['from_text_y'] + 20 
            
            _cord_df['to_node_id_x'] = _cord_df['to_text_x'] - 15
            _cord_df['to_node_id_y'] = _cord_df['to_text_y'] + 20 
       
        self._cord_df = _cord_df
    
     #This function will generate the main co-ordinates    
    def _set_coordinates(self,row):
           
        if self.ly:
            self.init_y = self.ly.pop()+self.dist_between_from_box
    
        #set the from upper left co-ordinates
        from_x0 = self.init_x
        from_y0 = self.init_y
        self.ly.append(from_y0)
        
        #set the from lower right co-ordinates
        from_x1 = from_x0 + self.width_of_rec
        from_y1 = from_y0 + self.height_of_rec
        self.ly.append(from_y1)
        
        row_dict = dict(row)
        new_dict = {'from_x0':from_x0,'from_y0':from_y0,'from_x1':from_x1,'from_y1':from_y1}
        
        d = {**row_dict,**new_dict}
        
        return(d)
    
    
    def _arrowedLine(self,ptA, ptB, color, width=1):
        """Draw line from ptA to ptB with arrowhead at ptB"""
        # Get drawing context
        #draw = ImageDraw.Draw(im)
        # Draw the line without arrows
        self.draw.line((ptA,ptB), width=width, fill=color)
    
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
        self.draw.polygon([vtx0, vtx1, ptB], fill=color)
 
        
    def _generate_diagram(self,row):
        #text to display
        data_flow_group = row['data_flow_group_name']
        from_sys = row['from_node']
        to_sys = row['to_node']
        interface_id = row['interface_id']
        data_entity = row['data_entity']
        #description = row['description']
        from_node_id = row['from_node_id']
        to_node_id = row['to_node_id']
        input_flag = row['input_to_main_flow']
        from_node_other = row['from_node_other']
        to_node_other = row['to_node_other']
        reverse_flow = row['reverse_flow']
    
        box_font = ImageFont.truetype("Arial.ttf")
        #box_font = ImageFont.load_default()
        
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
         
        interface_id_x = row['interface_id_x']
        interface_id_y = row['interface_id_y']
    
        data_entity_x = row['data_entity_x']
        data_entity_y = row['data_entity_y']
    
        #description_x = row['description_x']
        #description_y = row['description_y']
    
        from_node_id_x = row['from_node_id_x']
        from_node_id_y = row['from_node_id_y']
    
        to_node_id_x = row['to_node_id_x']
        to_node_id_y = row['to_node_id_y']
        
        #From box
        if from_node_other == "Y":
            self.draw.rectangle([from_x0,from_y0,from_x1,from_y1], fill =self.other_node_color, outline ="red")
            self.draw.text((from_text_x, from_text_y), from_sys, fill=self.other_node_text_color,font=box_font)
        else:
            self.draw.rectangle([from_x0,from_y0,from_x1,from_y1], fill = self.node_color, outline ="red")
            self.draw.text((from_text_x, from_text_y), from_sys, fill=self.node_text_color,font=box_font)
        
        #To box
        if to_node_other == 'Y':
           self.draw.rectangle([to_x0,to_y0,to_x1,to_y1], fill =self.other_node_color, outline ="red")
           self.draw.text((to_text_x, to_text_y), to_sys, fill=self.other_node_text_color,font=box_font)
        else:
            self.draw.rectangle([to_x0,to_y0,to_x1,to_y1], fill =self.node_color, outline ="red")
            self.draw.text((to_text_x, to_text_y), to_sys, fill=self.node_text_color,font=box_font)
            
        
        #Connecting arrow
        if input_flag == 'N':
            ptA = (from_x1,(from_y1-from_y0)/2+from_y0)
            ptB = (from_x0+self.width_of_rec+self.dist_between_from_to_box,(from_y1-from_y0)/2+from_y0)
            self._arrowedLine(ptA,ptB,self.arrow_color)
        else:
            ptA = (from_x1,(from_y1-from_y0)/2+from_y0)
            ptB = (to_x0,to_y0+self.height_of_rec)
            self._arrowedLine(ptA,ptB,self.arrow_color)
        
        if reverse_flow == 'Y':
            ptB = (from_x0+self.width_of_rec+self.dist_between_from_to_box,(from_y1-from_y0)*2/3+from_y0)
            ptA = (from_x1,(from_y1-from_y0)*2/3+from_y0)
            self._arrowedLine(ptB,ptA,self.arrow_color)
             #self._arrowedLine((from_x1,(from_y1-from_y0)/2+from_y0),(from_x0+self.width_of_rec+self.dist_between_from_to_box,(from_y1-from_y0)/2+from_y0))

        
        #Data Flow Group
        if input_flag == 'N':
            self.draw.text((data_flow_group_x, data_flow_group_y), data_flow_group, fill=self.group_name_color,font=box_font)
        
        
        #JIRA No
        self.draw.text((interface_id_x, interface_id_y), interface_id, fill=self.text_color,font=box_font)
        
        #Data Entity
        self.draw.text((data_entity_x, data_entity_y), data_entity, fill=self.text_color,font=box_font)
        
        #Description
        #draw.text((description_x, description_y), description, fill=(0,255,0))
        
        #Node ID
        if from_node_other == "Y":
            self.draw.text((from_node_id_x, from_node_id_y), '('+from_node_id+')', fill=self.other_node_id_color,font=box_font)
        else:
            self.draw.text((from_node_id_x, from_node_id_y), '('+from_node_id+')', fill=self.node_id_color,font=box_font)
            
        if to_node_other == 'Y':
            self.draw.text((to_node_id_x, to_node_id_y), '('+to_node_id+')', fill=self.other_node_id_color,font=box_font)
        else:
            self.draw.text((to_node_id_x, to_node_id_y), '('+to_node_id+')', fill=self.node_id_color,font=box_font)

    
        
if __name__ == "__main__":
    file = 'files/all_patterns.csv'
    group = ""
    config = "config/default_config.json"
    mapping = "mapping/default_mapping.json"
    
    obj = DrawInterfaceCatalogue(file,group,config,mapping)
    #coordinates = pd.read_csv("cord.csv")


    #image = obj.draw_image(coordinates)
    image = obj.draw_image()
    cordinates = obj._cord_df
    #print(cordinates[["from_node","from_x0","from_y0","from_x1","from_y1","to_node","to_x0","to_y0","to_x1","to_y1"]])       

    #cordinates.to_csv("cord_new.csv")

    image.show()
    


    