from app import db

class PaperInfo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    paperID = db.Column(db.String(64))    
    paperName = db.Column(db.String(128))
     


class ImageInfo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    mirtronName = db.Column(db.String(64),db.ForeignKey('mitron.mirtronName'))
    img_path = db.Column(db.String(64))    
    imgType = db.Column(db.String(24))
    


mitron_paper_association = db.Table('mitron_paper_association',
    db.Column('mitron_BalID', db.Integer, db.ForeignKey('mitron.BalID')),
    db.Column('paper_info_id', db.Integer, db.ForeignKey('paper_info.id'))
)
  

class Mitron(db.Model):

    # primary key
    BalID = db.Column(db.Integer, index=True,primary_key=True) 
    
    # Mirtron name
    mirtronName = db.Column(db.String(12),unique=True)

    # Mirtron type: precursor | mature
    mirtronType = db.Column(db.String(9))  
 
    # species
    species = db.Column(db.String(32),index=True)
  
    # hairpin arm
    # only for mature,set '-' for precursors
    hairpin_arm = db.Column(db.String(1))
  
    #mirtron status: known|candidate,currently all set as "-"
    status = db.Column(db.String(12))

    #Sequence
    sequence =  db.Column(db.String(128))
    
    #Chromosome
    chromosome = db.Column(db.String(8))  

    #chromosome start
    start_seq = db.Column(db.Integer)
  
    #chromosome end 
    end_seq = db.Column(db.Integer)

    # Strand 
    strand = db.Column(db.String(1))

    # Host Gene
    host_gene = db.Column(db.String(16))
    
    # intron region
    intron_region = db.Column(db.String(4))
 
    # 3' mature: only for precuror and 5' mature
    arm_3_name = db.Column(db.String(36))


    # 5' mature: only for precuror and 3' mature
    arm_5_name = db.Column(db.String(36))

    # precursor_id: only for matures
    precursor_name = db.Column(db.String(36))

    # other info
    other_info = db.Column(db.String(128),nullable=True)
    
    # source information
    source = db.Column(db.String(36)) 

    # Paper and otherinfo
    #paper = db.relationship('PaperInfo',backref='mitron', lazy='dynamic')

    # mitron and paper: many-to-many relationship
    paper = db.relationship('PaperInfo', secondary=mitron_paper_association, backref='mitron',lazy='dynamic')
      
    imageInfo = db.relationship('ImageInfo',backref='mitron',lazy='dynamic')



    def __getitem__(self,item):
        return getattr(self,item)


    pass 






