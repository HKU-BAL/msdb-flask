from PIL import Image
import io
import base64
import PIL

from collections import OrderedDict
import pandas as pd


def convertIMG(img_path):


    '''
    resize the image and convert the image to base64

    '''
    mywidth = 200

    img = Image.open(img_path)
    wpercent = (mywidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
    buffer = io.BytesIO()
    img.save(buffer, format="png")
    img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
    
    return img_str




def makeCSV(selectedItems):

    colNames = ["BalID","Mirtron name","Species","Mirtron type","Chromosome","Start Sequence","End Sequence","Strand","Sequence","Host gene","Paper"]
        
    myKeys_original = {"BalID":"BalID","Mirtron name":"mirtronName",
       "Species":"species",  "Mirtron status":"status","Mirtron type":"mirtronType",
       "Sequence":"sequence","Hairpin Arm":"hairpin_arm",
       "Chromosome":"chromosome", "Start Sequence":"start_seq", "End Sequence":"end_seq", "Strand":"strand",
       "Host gene":"host_gene", "Source":"source", "Other info":"other_info",\
       "Mature 3\'":"arm_3_name","Mature 5\'":"arm_5_name","Precursor":"precursor_name"}
 

    curCSV = OrderedDict({x:[] for x in colNames} )

    for curItem in selectedItems:
        for key in colNames:
            if(key!='Paper'):
                attr_name = myKeys_original[key]
                attr_val = curItem.__getitem__(attr_name)
            else:
                paper_list = curItem.paper.all()
                paper_dois = [tmp.paperID for tmp in paper_list]
                attr_val = ';'.join(paper_dois) 
                pass
            curCSV[key].append(attr_val)

    curCSV = pd.DataFrame(curCSV)
    return curCSV
    

def readRowtoOrderedDict(mitronRow):
   
   
    myKeys_original = {"BalID":"BalID","Mirtron name":"mirtronName",
       "Species":"species",  "Mirtron status":"status","Mirtron Type":"mirtronType",
       "Sequence":"sequence","Hairpin Arm":"hairpin_arm", 
       "Chromosome":"chromosome", "Start Sequence":"start_seq", "End Sequence":"end_seq", "Strand":"strand",
       "Host Gene":"host_gene", "Source":"source", "Other info":"other_info",\
       "Mature 3\'":"arm_3_name","Mature 5\'":"arm_5_name","Precursor":"precursor_name"}

    myOrderedKeys_precursor = ["BalID","Mirtron name",
       "Species","Mirtron Type",
       "Mature 3\'", "Mature 5\'",
       "Chromosome", "Start Sequence", "End Sequence", "Strand","Sequence",
       "Host Gene", "Source","Other info"] 
   
    myOrderedKeys_mature = ["BalID","Mirtron name",
       "Species","Mirtron Type","Hairpin Arm",
       "Mature 3\'", "Mature 5\'",
       "Chromosome", "Start Sequence", "End Sequence", "Strand","Sequence",
       "Host Gene", "Source","Other info"]
    myOrderedKeys_unknown =  ["BalID","Mirtron name",
       "Species","Mirtron Type",
       "Mature 3\'", "Mature 5\'",
       "Chromosome", "Start Sequence", "End Sequence", "Strand","Sequence",
       "Host Gene", "Source","Other info"]

     
    if(mitronRow.mirtronType.replace(" ","")=="precursor"):
        myOrderedKeys = myOrderedKeys_precursor
    elif(mitronRow.mirtronType.replace(" ","")=="mature"):
        myOrderedKeys = myOrderedKeys_mature
    else:
        myOrderedKeys = myOrderedKeys_unknown 
    myOrderedDict = OrderedDict()
    for k in myOrderedKeys:
               
        if(k==''):
            pass
        else:
            cur_item = myKeys_original[k]
           
            myOrderedDict[k] = mitronRow.__getitem__(cur_item)
     
    return myOrderedDict



