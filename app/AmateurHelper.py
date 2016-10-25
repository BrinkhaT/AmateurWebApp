'''
Created on 11.10.2016

@author: brinkhth
'''
from app import db, models

def updateAmateur(old, new):
    old.name = parseFormData(new.name.data)
    
    twName = parseFormData(new.tw.data)
    if twName != None:
        twName = twName.lower()
        updateOrCreateTwitterFollower(old.tw, twName)
        old.tw = twName
        
    old.mdhId = parseFormData(new.mdhId.data)
    old.vxId = parseFormData(new.vxId.data)
    old.pmId = parseFormData(new.pmId.data)
    old.subDomain = parseFormData(new.subDomain.data)
        
    db.session.add(old)
    db.session.commit()
    
def parseFormData(data):
    if data:
        if data == '':
            return None
        else:
            return data
    else:
        return None
    
def createAmateur(new):
    
    twName = parseFormData(new.tw.data)
    if twName != None:
        twName = twName.lower()
    
    a = models.Amateur(name=parseFormData(new.name.data),
                   tw=twName,
                   mdhId=parseFormData(new.mdhId.data),
                   vxId=parseFormData(new.vxId.data),
                   pmId=parseFormData(new.pmId.data),
                   subDomain=parseFormData(new.subDomain.data))
    updateOrCreateTwitterFollower(None, twName)
    
    db.session.add(a)
    db.session.commit()
    
def createAmateurByTwitterName(twName):
    twName = twName.lower()
    a = models.Amateur(name=twName,
                   tw=twName)
    updateOrCreateTwitterFollower(None, twName)
    
    db.session.add(a)
    db.session.commit()
    
def updateOrCreateTwitterFollower(twNameOld, twNameNew):
    if twNameOld != None and twNameNew == None:
        t = db.session.query(models.TwitterFollower).filter(models.TwitterFollower.twName == twNameOld and models.TwitterFollower.twConfig == 2).first()
        db.session.delete(t)
        db.session.commit()
    elif twNameOld != None and twNameNew != None:
        t = db.session.query(models.TwitterFollower).filter(models.TwitterFollower.twName == twNameOld and models.TwitterFollower.twConfig == 2).first()
        
        if t == None:
            t = models.TwitterFollower(twName=twNameNew, twConfig=2)
        else:
            t.twName = twNameNew
        
        db.session.add(t)
        db.session.commit()
    elif twNameOld == None and twNameNew != None:
        t = models.TwitterFollower(twName=twNameNew, twConfig=2)
        db.session.add(t)
        db.session.commit()