import tornado.web
import sqlite3
from model import Model
import config

class MainHandler(tornado.web.RequestHandler):
    
    def initialize(self):
        self.db = self.application.db

    def get(self):
        self.render("index.html")
    
    def post(self):
        azione = self.get_argument('azione', default='')
        _model = Model(self.db)        
        response_dict = dict()
        
        if azione == 'caricaContenuti':
            ricette = _model.get_ricette()
            categorie = _model.get_categorie()
            sezioni = _model.get_sezioni()
            response_dict['ricette'] = ricette
            response_dict['categorie'] = categorie
            response_dict['sezioni'] = sezioni
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'getRicette':
            ricette = _model.get_ricette()
            response_dict['ricette'] = ricette
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'editRicetta':
            id_ricetta = int(self.get_argument('id_ricetta'))
            response_dict['ricetta'] = _model.get_ricetta(id_ricetta)
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'salvaRicetta':
            _ric = tornado.escape.json_decode(self.get_argument('ricetta'))
            response_dict = _model.salva_ricetta(_ric)
            # Se tutto OK, ritorno le ricette per il reload
            if response_dict['stato'] == 0: response_dict['ricette'] = _model.get_ricette()
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'deleteRicetta':
            id_ricetta = int(self.get_argument('id_ricetta'))
            response_dict = _model.delete_ricetta(id_ricetta)
            # Se tutto OK, ritorno le ricette per il reload
            if response_dict['stato'] == 0: response_dict['ricette'] = _model.get_ricette()
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'salvaCategoria':
            _cat = tornado.escape.json_decode(self.get_argument('categoria'))
            response_dict = _model.salva_categoria(_cat)
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'deleteCategoria':
            id_categoria = int(self.get_argument('id_categoria'))
            response_dict = _model.delete_categoria(id_categoria)
            # Se tutto OK, ritorno le categorie per il reload
            if response_dict['stato'] == 0: response_dict['categorie'] = _model.get_categorie()
            self.write(tornado.escape.json_encode(response_dict))
            
        elif azione == 'salvaSezione':
            _sez = tornado.escape.json_decode(self.get_argument('sezione'))
            response_dict = _model.salva_sezione(_sez)
            self.write(tornado.escape.json_encode(response_dict))
        
        elif azione == 'deleteSezione':
            id_sezione = int(self.get_argument('id_sezione'))
            response_dict = _model.delete_sezione(id_sezione)
            # Se tutto OK, ritorno le categorie per il reload
            if response_dict['stato'] == 0: response_dict['sezioni'] = _model.get_sezioni()
            self.write(tornado.escape.json_encode(response_dict))
            

""" Defining Application """
application = tornado.web.Application([
        (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=config.static_path)),
        (r"/(favicon.ico)", tornado.web.StaticFileHandler, dict(path=config.static_path)),
        (r"/", MainHandler),
    ],
    autoescape=None,
    debug=True,
)

""" MAIN """
if __name__ == "__main__":
    application.listen(config.port)
    application.db = sqlite3.connect('salepepe.db')
    tornado.ioloop.IOLoop.instance().start()
    tornado.autoreload.wait()
