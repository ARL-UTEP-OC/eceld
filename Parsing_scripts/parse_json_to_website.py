# -*- coding: utf-8 -*-
"""
Created on ~

@author: Gerardo Cervantes
"""
import datetime

panel_id = 0
def parse_action(content):
     content_list = content.split(',')
     action = content_list[0].lower()
     if action == 'click':
         return get_image_panel_html(parse_image_path(content_list[1]), 'Mouse click')
     if action == 'key':
         return 'Key press ' + content_list[1]
     if action == 'timed':
         return get_image_panel_html(parse_image_path(content_list[1]), 'Timed image')
     if action == 'log':
         return 'System log ' + content_list[1]
     return ''
         
 #<img src="raw\pykeylogger\click_images\a.png" width="750" height="450">
def parse_image_path(image_path):
    image_path = image_path[image_path.find('raw'):] #Removes everything before keyword raw
    image_path = image_path.replace('raw/', 'raw/pykeylogger/') #Link in data comes broken, this corrects the link
    return image_path
        
def get_image_panel_html(image_path, panel_title):
    import random
    panel_id = str(random.randint(1, 2 ** 30))
    panel_id_with_quotes = '"' + panel_id + '"'
    panel_start = """<div class="panel panel-default">
        <div class="panel-heading">
            <h4 class="panel-title">
                <a class="accordion-toggle text-normalize" data-toggle="collapse" data-parent="#accordion" href="#""" + panel_id + '"' + """><i class="fa fa-minus text-primary"></i> """ + panel_title + """</a>
            </h4>
        </div>
        <div id="""
    panel_end = """ class="panel-collapse collapse">
    <img src=""" + '"' + image_path + '"' + """ width="750" height="450">
        </div>
        </div>"""
    panel_image_html = panel_start + panel_id_with_quotes + panel_end
    return panel_image_html

def create_panel_syslogs_html():
    import random
    panel_id = str(random.randint(1, 2 ** 30))
    panel_id_with_quotes = '"' + panel_id + '"'
    panel_title = 'System logs'
    panel_start = """<div class="panel panel-default">
        <div class="panel-heading">
            <h4 class="panel-title">
                <a class="accordion-toggle text-normalize" data-toggle="collapse" data-parent="#accordion" href="#""" + panel_id + '"' + """><i class="fa fa-minus text-primary"></i> """ + panel_title + """</a>
            </h4>
        </div>
        <div id=""" + panel_id_with_quotes + """class="panel-collapse collapse">"""
    panel_end = """
        </div>
        </div>"""
    return panel_start, panel_end
    

def create_website(ordered_times, ordered_contents, bug_date):
    file_name = 'index.html'
    
    cleaned_html_contents = []
    for i, time_secs in enumerate(ordered_times):
        str_time = str(datetime.timedelta(seconds = time_secs))
        clean_str = '<h4>' + str_time + ' ' +  parse_action(ordered_contents[i]) + '</h4><br>'
        cleaned_html_contents.append(clean_str)

    body_html_clicks = [html_line for html_line in cleaned_html_contents if 'click' in html_line.lower() or 'timed image' in html_line.lower() ]
    body_html_clicks = ''.join(body_html_clicks)
    body_html_keys = [html_line for html_line in cleaned_html_contents if 'key press' in html_line.lower() ]
    body_html_keys = ''.join(body_html_keys)
    
    body_html_syslogs = [html_line for html_line in cleaned_html_contents if 'system log' in html_line.lower() ]
    body_html_syslogs = ''.join(body_html_syslogs)
    
    panel_start, panel_end = create_panel_syslogs_html()
    is_in_log = False
    mod_html_contents = []
    for html_line in cleaned_html_contents:
        if 'system log' in html_line.lower():
            if not is_in_log:
                panel_start, panel_end = create_panel_syslogs_html()
                mod_html_contents.append(panel_start + html_line)
            else:
                mod_html_contents.append(html_line)
                
            is_in_log = True
        else:
            if is_in_log:
                mod_html_contents.append(panel_end + html_line)
                is_in_log = False
            else:
                mod_html_contents.append(html_line)
                
    body_html_code = ''.join(mod_html_contents)
    end_html_code = """
        </div>
      </div>
    </div>
    
    </body>
    </html>
    
        """
                 
    start_html_code = """
        <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Bug Report</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
      <style>
      .fakeimg {
        height: 200px;
        background: #aaa;
      }
      </style>
    </head>
    
    
    
    
    
    <body>
    
    <div class="jumbotron text-center" style="margin-bottom:0">
      <h1>Bug Recreation Summary</h1>
    </div>
    
    
    
    <nav class="navbar navbar-inverse">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>                        
          </button>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li class="active"><a href="index.html">Main Summary</a></li>
            <li><a href="keys.html">Keyboard strokes</a></li>
            <li><a href="screenshots.html">Screenshot images</a></li>
            <li><a href="syslogs.html">System logs</a></li>
          </ul>
        </div>
      </div>
    </nav>
    
    
    
    <div class="container">
      <div class="row">
        
        <div class="col-sm-8">
        """
    body_title_html = """
      <h1>Bug encounter summary</h1><h3>""" + bug_date +"""</h3>"""
    index_html_code = start_html_code + body_title_html + body_html_code + end_html_code
    screenshots_html_code = start_html_code + body_html_clicks + end_html_code 
    keys_html_code = start_html_code + body_html_keys + end_html_code
    syslogs_html_code = start_html_code + body_html_syslogs + end_html_code
    
    print(index_html_code)
    with open(file_name,'w') as file:
        file.write(index_html_code)    
    with open('screenshots.html','w') as file:
        file.write(screenshots_html_code)
    with open('keys.html','w') as file:
        file.write(keys_html_code)
    with open('syslogs.html','w') as file:
        file.write(syslogs_html_code)
                    
        

if __name__ == '__main__':
    create_website([1],["You have to run __init__.py not this file"])