# coding: utf-8
from vendor import web
import urllib2
from google.appengine.api import urlfetch
import urllib
from django.utils import simplejson as json
import base64
import unicodedata
from google.appengine.ext import db
from models import *
from datetime import datetime

urls = (
  '/','info',
  '/atualizarotwitter', 'index',
  '/rios', 'rios',
  '/status', 'status'
)

render = web.template.render('templates')

class info:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return "app de niveis de rios para twitter <a href='http://twitter.com/niveisrios'>@niveisrios</a>"

class index:
    def GET(self):
        try:
            url = "http://sibi.furb.br/alerta/Alerta/controllers/consultaJSON.php?tipo=tabela"
            result = urllib2.urlopen(url).read()

            rios = json.loads(result)

            dados = {}

            contador = 0
            for rio in rios:
                nome = unicodedata.normalize('NFKD', rio['ds_estacao']).encode('ascii','ignore')
                nivel = str(rio['vlr_nivel'])
                status = rio['status']
                precipitacao12 = rio['vlr_precipitacao_12hr']
                hora = rio['dt_leitura'].split(' ')[1]

                if not nivel == "Sem sensor":
                    msg = ""+nome+" "+hora+" nivel do rio: "+nivel+" - precipitacao ultimas 12h: "+precipitacao12+" - status: #"+status+" #"+nome.replace(' ','')+""
                    dados[contador] = msg
                    contador += 1

            msg = ""
            for twit in dados:
                msg = dados[twit]
                self.update(msg)

            return msg
        except Exception,e:
            return e

    def update(self, msg):
        login =  "niveisrios"
        password = ""
        payload= {'status' : msg,  'source' : "API"}
        payload= urllib.urlencode(payload)

        base64string = base64.encodestring('%s:%s' % (login, password))[:-1]
        headers = {'Authorization': "Basic %s" % base64string}

        url = "http://twitter.com/statuses/update.xml"
        result = urlfetch.fetch(url, payload=payload, method=urlfetch.POST, headers=headers)

        return result.content

class rios:
    def GET(self):
        try:
            url = "http://sibi.furb.br/alerta/Alerta/controllers/consultaJSON.php?tipo=tabela"
            result = urllib2.urlopen(url).read()

            rios = json.loads(result)

            dados = {}

            contador = 0
            for rio in rios:
                if rio['vlr_nivel'] != "Sem sensor":
                    info = Rio()
                    info.id = rio['cd_estacao']
                    info.cidade = unicodedata.normalize('NFKD', rio['ds_estacao']).encode('ascii','ignore')
                    dt_leitura = datetime.strptime(rio['dt_leitura'], "%d/%m/%Y %H:%M")
                    info.datahora = dt_leitura
                    info.nivel = float(rio['vlr_nivel'])
                    info.precipitacao = float(rio['vlr_precipitacao'])
                    info.status = rio['status']
                    info.precipitacao12 = float(rio['vlr_precipitacao_12hr'])
                    info.precipitacao24 = float(rio['vlr_precipitacao_24hr'])
                    info.precipitacao48 = float(rio['vlr_precipitacao_48hr'])
                    info.put()

            return "true"
        except Exception, e:
            return e

class status:
    def GET(self):
        try:
            rios = db.GqlQuery("SELECT * FROM Rio ")
            return render.status(rios)
        except Exception, e:
            return e

app = web.application(urls, globals())
main = app.cgirun()


