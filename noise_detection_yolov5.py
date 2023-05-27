def noise_detection_yolov5(path):
    #takes dir as input, 
    #output =  list of prediction of same length as number of files in dir
    
    #import all functions
    import torch
    from PIL import Image
    from torchvision import transforms as T
    import pathlib
    import pandas as pd
    import os
    import warnings
    
    warnings.filterwarnings('ignore')
    
    #ad-hoc to avoid PosixPath error
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath
    
    #set device to Cude, if not available, use CPU
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    
    #get all files in path
    file_list = os.listdir(path)
    
    #create output dict
    output = {
        "Filename": [],
        "Noise": []}
    
    for i in file_list:
        # path to the image or video
        imagename = path + "/" + i
        
        #open the image from given path
        image = Image.open(imagename)
    
        #use mean/std from imagenet
        # NOT THE BEST APPROACH, since Imagenet parameters are for natural focus picture. Noise in image falls into unnatural pixels.

        #ref: https://github.com/ultralytics/yolov5/issues/9030
        IMAGENET_MEAN = 0.485, 0.456, 0.406
        IMAGENET_STD = 0.229, 0.224, 0.225
        def classify_transforms(size=224): 
             # Transforms to apply if albumentations not installed 
             return T.Compose([T.ToTensor(), T.Resize(size), T.CenterCrop(size), T.Normalize(IMAGENET_MEAN, IMAGENET_STD)])


        #convert image into tensor of 1x3x224x224 (batch,channel,height,width)
        transformations = classify_transforms()
        convert_tensor = transformations(image)
        convert_tensor = convert_tensor.unsqueeze(0) #create value for batch
        #print(convert_tensor.shape)

        #send input to device
        convert_tensor = convert_tensor.to(DEVICE)

        #load model from local weight and Pytorch Hub
        model = torch.hub.load('yolov5','custom', path='yolo5s_best_apr_4.pt',autoshape = False, force_reload=True, source='local')

        #feed image into model for inference
        results = model(convert_tensor)  # inference

        #use softmax on output and argmax to get the result
        sm = torch.nn.Softmax(dim=1)
        prediction = torch.argmax(sm(results)).item()
        
        #append prediction to dict
        output["Filename"].append(i)
        output["Noise"].append(prediction)
        
        
    output = pd.DataFrame.from_dict(output)
    return(output)
