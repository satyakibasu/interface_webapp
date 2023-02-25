# -*- coding: utf-8 -*-
from flask import Flask,request,render_template, redirect, url_for
from draw_interface_catalogue_class import DrawInterfaceCatalogue
import os
import pandas as pd

#from google.cloud import storage
#from PIL import Image




app = Flask(__name__,static_url_path='/static')


@app.route('/')
def main():
    cwd = os.getcwd()
    files = os.listdir(cwd+'/files')
    print(cwd)
    return render_template("list.html", files=files)

@app.route('/upload')
def uploader():
    return render_template("upload.html")


@app.route('/uploader', methods = ["POST"])
def upload_file():
   if request.method == 'POST':
       f = request.files['filename']
       f.save('./files/'+f.filename)
   
   return render_template("display.html",file=f.filename)

@app.route('/display', methods = ["POST","GET"])
def display():
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        #print("i am here")
        
        
        try:
            
                
            if request.form['display']:
                filename = request.form['display']
                print(filename)
                config = request.form['color_scheme']
                
                groups = request.form.getlist('group')
                print(set(groups))
                group_list = list(set(groups))
                print(group_list)
                group_list = list(filter(None,group_list))
                if group_list:
                    group = group_list[0]
                else:
                    group = ""
        
                
                print("group in :",group)
                f_name = filename.split('.')[0]
                print(f_name)
                #config = "config/white_config.json"
                mapping = "mapping/default_mapping.json"
                print(config)
                obj = DrawInterfaceCatalogue("files/"+filename,group=group, config="config/"+config,mapping=mapping)
                image = obj.draw_image()
                #image.show()
                cwd = os.getcwd()
                if group:
                    image_name = f_name+"_"+group+".png"
                else:
                    image_name = f_name+".png"
                print(image_name)  
                image.save(cwd+"/static/images/"+image_name)
                
                
                files = os.listdir(cwd+'/files')
                return render_template("list.html",files=files, image_name = image_name)
        except:
            group = request.form['group']
            request.form['display_data']
            filename = request.form['display_data']
            print("filename",filename)
            df = pd.read_csv("files/"+filename)
            
            if group:
                df = df[(df['data_flow_group'] == group)]
        
            return render_template('display_data.html',  tables=[df.to_html(classes='data', header="true")])
        

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='images/'+filename), code=301)

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT',8080))
    app.run(debug=True)
