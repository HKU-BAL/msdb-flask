from app.main import bp
from flask import Response,url_for,request,send_file,render_template, flash, redirect
from app import db
from flask_babel import _
import os
from datetime import datetime
from collections import OrderedDict
from app.models import Mitron,PaperInfo,mitron_paper_association
from app.main.utils import *
from app.main.form import *
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from app import email


from flask import current_app



prefix = '/msdb'
@bp.route(prefix+'/')
def index():
    """ Displays the index page accessible at '/'
    """

    stat_dict = {"precursor":1569,"mature":2640,"species":25,"papers":46}
  
    return render_template('home.html',title='Home',stat_dict=stat_dict)


@bp.route(prefix+'/tutorial')
def tutorial():

    '''
    '''



    return render_template('tutorial.html',title='Tutorial')
    
@bp.route(prefix+'/updates')
def updates():
    

    return render_template('base.html',title='Updates')



@bp.route(prefix+'/contact',methods=['GET',"POST"])
def contact():
    form = contactForm()

    
    if form.validate_on_submit():       

        # Send an email to the administrators
        msg = "Name:"+form.name.data+'\nE-mail:'+form.email.data+'\n'+form.question.data

        email.send_email("MirtronDB user messages", "mitronDB-BAL",current_app.config['ADMINS'] , msg, msg,sync=False)

        flash('Message was sent successfully. An email has been sent to the administrators.')
        return redirect(url_for('main.index'))
 
        pass

    return render_template('contact.html',title='Contact',form=form)



@bp.route(prefix+'/browser_main')  
def browser_main():


    curMitronInfo = db.session.query(Mitron).order_by(Mitron.species).all()    
    curData  = {"species":[],"mature":[],"precursor":[]}

    for curItem in curMitronInfo:
        if(curItem.species=='-'):
            continue 
        if(curItem.species not in curData["species"]):
            curData["species"].append(curItem.species)
            curData["mature"].append(0)
            curData["precursor"].append(0)

        curIndex = curData["species"].index(curItem.species)
        
        if(curItem.mirtronType.replace(" ","")=="precursor"):
            curData["precursor"][curIndex] += 1
        elif(curItem.mirtronType.replace(" ","")=="mature"):
            curData["mature"][curIndex] += 1
    
    return render_template('speciesGallery.html',title='Browser-main',speciesInfo=curData)
    

@bp.route(prefix+'/download_high_res/<mirtronName>/<imgType>')
def download_high_res(mirtronName,imgType):

    svg_root = current_app.config['IMG_DIR']
    cur_svg_path = os.path.join(svg_root,mirtronName+'_'+imgType.split(' ')[0]+'.svg')

    if(not os.path.exists(cur_svg_path)):
        if(imgType.startswith('Fold')):
            cur_svg_path = os.path.join(svg_root,mirtronName+'_'+imgType.split(' ')[-1]+'.svg')
        
    return send_file(cur_svg_path)
    

@bp.route(prefix+'/download_main',methods=['GET','POST'])
def download_main():


    '''
    download page
    '''
    mitron_alias = aliased(Mitron)
    paper_info_alias = aliased(PaperInfo)


    base_query = db.session.query(Mitron).join(mitron_alias, Mitron.mirtronName == mitron_alias.mirtronName).join(
        mitron_paper_association, mitron_alias.BalID == mitron_paper_association.c.mitron_BalID).join(
        paper_info_alias, paper_info_alias.id == mitron_paper_association.c.paper_info_id)


    form = downloadForm()
    if form.validate_on_submit():


        selected_species = request.form.getlist("species")
        selected_papers = request.form.getlist("paper")
        select_precursor = request.form.get('precursorCheckbox')
        select_mature = request.form.get("matureCheckbox")        
        query = db.session.query(Mitron)

        if('all' not in selected_species):
            query = query.filter(Mitron.species.in_(selected_species))
            
        if('all' not in selected_papers):
            pass
        selected_mitron_type = [] 
        if(select_precursor == 'checked'):
            selected_mitron_type.append("precursor")
        if(select_mature == 'checked'):
            selected_mitron_type.append("mature")
        query = query.filter(Mitron.mirtronType.in_(selected_mitron_type))
        selectedItems = query.all()
        
        # make CSV files
        prepared_csv = makeCSV(selectedItems)

        # Assuming you have the 'prepared_csv' DataFrame
        csv_data = prepared_csv.to_csv(index=False)

        # Create a response with the CSV data
        response = Response(csv_data, content_type='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        return response
 
    curMitronInfo = db.session.query(Mitron).all()
    unique_species = []
    unique_papers = []

    for curItem in curMitronInfo:
        unique_species.append(curItem.species)

    curAllPaperInfo = db.session.query(PaperInfo).all()
    for curPaper in curAllPaperInfo:
        unique_papers.append(curPaper.paperName)

    unique_species = sorted(list(set(unique_species)))
    unique_species.remove('-')
    unique_papers = sorted(list(set(unique_papers)))


    
    return render_template('downloadMain.html',title="Download-main",form=form,species_list=unique_species,paper_list=unique_papers)
    


@bp.route(prefix+'/download_select/<species>/<balID>',methods=["GET","POST"])
def download_select(species,balID):



    # Create aliases for the 'mitron' and 'paper_info' tables
    mitron_alias = aliased(Mitron)
    paper_info_alias = aliased(PaperInfo)


    base_query = db.session.query(Mitron).join(mitron_alias, Mitron.mirtronName == mitron_alias.mirtronName).join(
        mitron_paper_association, mitron_alias.BalID == mitron_paper_association.c.mitron_BalID).join(
        paper_info_alias, paper_info_alias.id == mitron_paper_association.c.paper_info_id)


    if(balID!='all'):

        # individual item 
        curItems = base_query.filter(Mitron.BalID == balID).all()
         
        
    elif(species=='all'):
        curItems = base_query.all()
    
    else:
        # download specific species
        curItems = base_query.filter(Mitron.species == species).all()
        pass

    
    # make CSV files
    prepared_csv = makeCSV(curItems) 

    # Assuming you have the 'prepared_csv' DataFrame
    csv_data = prepared_csv.to_csv(index=False)

    # Create a response with the CSV data
    response = Response(csv_data, content_type='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"



    return response
    pass


@bp.route(prefix+'/searchMain',methods=['GET','POST'])
def searchMain():

    form = searchForm()
    
    if form.validate_on_submit():
        
        
        selected_species = request.form.get("species") 
        selected_sources = request.form.get("sources").replace("/","&")
        # search by key words
        cur_key_word = request.form.get('keyword').replace('/',"&")
        
        if(cur_key_word==''):
            cur_key_word='None'
         
        # jump to the list page
        return redirect(url_for('main.mitronSearchResult',keywords=cur_key_word,species=selected_species,sources=selected_sources))
        
         
    curMitronInfo = db.session.query(Mitron).all()
    unique_species = []
    unique_papers = []
    
    for curItem in curMitronInfo:
        unique_species.append(curItem.species)
    
    curAllPaperInfo = db.session.query(PaperInfo).all()
    for curPaper in curAllPaperInfo:
        unique_papers.append(curPaper.paperName)
        
    unique_species = set(unique_species)
    unique_papers = set(unique_papers)
     
    return render_template('searchMain.html',title='Search',form=form,unique_species=unique_species,unique_papers=unique_papers,curItemList=[])
    

@bp.route(prefix+'/mirtronDetails/<mitronName>')
def mirtronDetails(mitronName):

    curMitronInfo = db.session.query(Mitron).filter_by(mirtronName=mitronName).first() 
    if(not curMitronInfo):
        return render_template('errors/404.html')

        
    curMitronInfo2 = readRowtoOrderedDict(curMitronInfo)
    
    # load RNA structure images
    curImgInfo = curMitronInfo.imageInfo.all()
    # iterate and convert the RNA structure images
    curImgDict = OrderedDict()
    for i in range(len(curImgInfo)):
        curImageItem = convertIMG(curImgInfo[i].img_path)
        curImageType = curImgInfo[i].imgType
        curImgDict[curImageType] = curImageItem 


    curPaperInfo = curMitronInfo.paper.all()
    
    num_img = len(list(curImgDict.keys()))
    return render_template('mitronDetails2.html',title='MitronDetails',num_img=num_img,curImgDict=curImgDict,curMitronInfo=curMitronInfo2,curPaperInfo=curPaperInfo)  



@bp.route(prefix+'/mitronList/<mitronGroup>')
def mitronGroups(mitronGroup):
    ROWS_PER_PAGE = 20
    page = request.args.get('page', 1, type=int)

    if(mitronGroup!='all'):
        curMitronList = db.session.query(Mitron).filter_by(species=mitronGroup).paginate(page=page, per_page=ROWS_PER_PAGE) 
    else:
        curMitronList = db.session.query(Mitron).all().paginate(page=page, per_page=ROWS_PER_PAGE) 
    return render_template('mitronList.html',title='MitronList',curMitronList=curMitronList,mitronGroup=mitronGroup)
    



@bp.route(prefix+'/mitronSearchResult/<keywords>/<species>/<sources>')
def mitronSearchResult(keywords,species,sources):
    
    # Create aliases for the 'mitron' and 'paper_info' tables
    mitron_alias = aliased(Mitron)
    paper_info_alias = aliased(PaperInfo)


    # all items in the database 
    curItems = db.session.query(Mitron)
   
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get("per-page", 20, type=int)
    sources = sources.replace("&","/")
    
    ROWS_PER_PAGE = 50  
    if(species!='all'):
        
        curItems = curItems.filter(Mitron.species==species)
     
    if(sources!='all'):
        curItems = curItems.filter(Mitron.source==sources)

     
    cur_key_word = keywords.replace("&",'/')      
    if(cur_key_word!='None'):
        
        or_conditions = [
        Mitron.BalID.like("%" + cur_key_word + "%"),
        Mitron.arm_3_name.like("%" + cur_key_word + "%"),
        Mitron.arm_5_name.like("%" + cur_key_word + "%"),
        Mitron.mirtronName.like("%" + cur_key_word + "%"),
        Mitron.species.like("%" + cur_key_word + "%"),
        Mitron.host_gene.like("%" + cur_key_word + "%"),
        Mitron.source.like("%" + cur_key_word + "%"),
        paper_info_alias.paperID.like("%" + cur_key_word + "%"),
        paper_info_alias.paperName.like("%" + cur_key_word + "%")]
        
        # Add the join conditions
        curItems = curItems.join(mitron_alias, Mitron.mirtronName == mitron_alias.mirtronName).join(
        mitron_paper_association, mitron_alias.BalID == mitron_paper_association.c.mitron_BalID).join(
        paper_info_alias, paper_info_alias.id == mitron_paper_association.c.paper_info_id)

        # Apply the OR conditions to the query
        curItems = curItems.filter(or_(*or_conditions))
        
    curMitronList = curItems.paginate(page=page, per_page=per_page)
    
    return render_template('mitronList.html',title='MitronList',keywords=keywords,species=species,sources=sources,curMitronList=curMitronList,mitronTotalNum=len(curItems.all()))
    
    




