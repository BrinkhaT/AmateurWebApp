from app import db, models
import bitly_api
        
def shortenUrl(url):
    bApiKey = db.session.query(models.SysProp).filter(models.SysProp.key == 'BitlyApiKey').first()
    
    if bApiKey:
        try:
            c = bitly_api.Connection(access_token=bApiKey.value)
            data = c.shorten(url)
            return data['url']
        except:
            pass
    
    return url
    