import os

def check_input(input_path):
    
    #Global variable to store data type and format 
    dict = {}
    
    # Checking if the input path exists
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist")
        return

    # Checking if the input path is a file
    if os.path.isfile(input_path):
        # Check if the input is structured 
        file_extension = os.path.splitext(input_path)[1]
        if file_extension in ['.csv', '.xlsx','xls']:
            dict['classification'] = 'structured'
            dict['extension'] = file_extension
            return dict
            
        #Checking in the input is unstructured    
        elif file_extension in ['.txt']:
            dict['classification'] = 'unstructured'
            dict['extension'] = file_extension
            return dict
            
        #Checking is the input is semi-structured    
        elif file_extension in ['.json']:
            dict['classification'] = 'semi-structured'
            dict['extension'] = file_extension
            return dict
        
        else:
            dict['unknown'] = file_extension
            return dict
            #print(f"{input_path} does not fit any current criteria")
            
    # Check if the input path is a directory
    elif os.path.isdir(input_path):
        # Check if the directory contains images or videos
        contains_images = False
        contains_videos = False
        for filename in os.listdir(input_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                contains_images = True
                
            elif filename.endswith(('.mp4', '.avi', '.mov', '.wmv')):
                contains_videos = True
                
        if contains_images and contains_videos:
            dict['unstructured']='image & video'
            return dict
           
        elif contains_images:
            dict['unstructured']='image'
            return dict
            
        elif contains_videos:
            dict['unstructured']='video'
            return dict
            
        else:
            print(f"{input_path} is an empty directory")
            
    else:
        print(f"{input_path} is not a file or directory")
