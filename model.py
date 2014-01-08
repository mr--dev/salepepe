import math
import config

class Model():
    
    def __init__(self, db):
        self.db = db
    
    def salva_ricetta(self, _ric):
        response_dict = dict()
        if int(_ric['id_ricetta']) == 0:
            _rec = ( _ric['nome'], _ric['numero_rivista'], int(_ric['anno_rivista']), _ric['pagina'], _ric['preferito'], int(_ric['id_categoria']), 
                    int(_ric['id_sezione']), _ric['tags'] )
            _sql = "INSERT INTO ricetta(nome, numero_rivista, anno_rivista, pagina, preferito, id_categoria, id_sezione, tags) values (?, ?, ?, ?, ?, ?, ?, ?)"
        else: 
            _rec = ( _ric['nome'], _ric['numero_rivista'], int(_ric['anno_rivista']), _ric['pagina'], _ric['preferito'], _ric['tags'], int(_ric['id_categoria']), 
                    int(_ric['id_sezione']), int(_ric['id_ricetta']) )
            _sql = "UPDATE ricetta SET nome = ?, numero_rivista = ?, anno_rivista = ?, pagina = ?, preferito = ?, tags = ?, id_categoria = ?, id_sezione = ? \
                    WHERE id_ricetta = ?"
        try: 
            cur = self.db.cursor()
            cur.execute(_sql, _rec)
            self.db.commit()
            stato = 0
            messaggio = "OK"
        except:
            stato = 1
            messaggio = "KO"
        
        response_dict['stato'] = stato
        response_dict['messaggio'] = messaggio
        return response_dict
    
    def delete_ricetta(self, id_ricetta):
        response_dict = dict()
        _sql = "DELETE FROM ricetta WHERE id_ricetta = ? ;"
        try: 
            cur = self.db.cursor()
            cur.execute(_sql, (id_ricetta, ))
            self.db.commit()
            stato = 0
            messaggio = "OK"
        except:
            stato = 1
            messaggio = "KO"
        
        response_dict['stato'] = stato
        response_dict['messaggio'] = messaggio
        return response_dict

    def get_ricette(self, keyword='', categoria='', search_index=1):
        limit = config.pagination
        
        _sql = "SELECT \
                    COUNT (ric.id_ricetta) \
                FROM \
                    ricetta ric \
                        JOIN \
                    categoria cat USING(id_categoria) \
                        JOIN \
                    sezione sez USING(id_sezione)\
                WHERE \
                    (ric.nome like ? OR tags LIKE ?) AND id_categoria like ? "
        cur = self.db.cursor()
        cur.execute(_sql, ('%'+keyword+'%', '%'+keyword+'%', '%'+categoria+'%'))
        count = cur.fetchone()[0]
        search_total = max(1, int( math.ceil( count / float(limit) ) ))
        
        # Trick: If I deleted the only record of a page, check for index
        if count % limit == 0 and search_index > search_total: search_index -= 1
        skip = (int(search_index)-1)*limit
        
        ricette_list = list()
        _sql = "SELECT \
                    ric.id_ricetta, ric.nome, ric.numero_rivista, ric.anno_rivista, ric.pagina, ric.preferito, cat.nome, sez.nome \
                FROM \
                    ricetta ric \
                        JOIN \
                    categoria cat USING(id_categoria) \
                        JOIN \
                    sezione sez USING(id_sezione)\
                WHERE \
                    (ric.nome like ? OR tags LIKE ?) AND id_categoria like ? \
                ORDER BY \
                    ric.anno_rivista DESC, ric.numero_rivista DESC, ric.pagina \
                LIMIT (?), (?); "
        for row in cur.execute(_sql, ('%'+keyword+'%', '%'+keyword+'%', '%'+categoria+'%', skip, limit)):
            r = dict()
            r['id_ricetta'] = row[0]
            r['nome'] = row[1]
            r['numero_rivista'] = row[2]
            r['anno_rivista'] = row[3]
            r['pagina'] = row[4]
            r['preferito'] = row[5]
            r['categoria'] = row[6]
            r['sezione'] = row[7]
            ricette_list.append(r)
        
        return ricette_list, search_total, search_index
    
    def get_ricetta(self, id_ricetta):
        _sql = "SELECT \
                    ric.id_ricetta, ric.nome, ric.numero_rivista, ric.anno_rivista, ric.pagina, ric.preferito, ric.tags, ric.id_categoria, ric.id_sezione \
                FROM \
                    ricetta ric \
                WHERE \
                    id_ricetta = ? ;"
        cur = self.db.cursor()
        cur.execute(_sql, (id_ricetta, ))
        row = cur.fetchone()
        r = dict()
        r['id_ricetta'] = row[0]
        r['nome'] = row[1]
        r['numero_rivista'] = row[2]
        r['anno_rivista'] = row[3]
        r['pagina'] = row[4]
        r['preferito'] = row[5]
        r['tags'] = row[6]
        r['id_categoria'] = row[7]
        r['id_sezione'] = row[8]
        return r

    def salva_categoria(self, _cat):
        response_dict = dict()
        if int(_cat['id_categoria']) == 0:
            _rec = ( _cat['nome'], )
            _sql = "INSERT INTO categoria(nome) values ( ? ); "
        else: 
            _rec = ( _cat['nome'], int(_cat['id_categoria']) )
            _sql = "UPDATE categoria SET nome = ? \
                    WHERE id_categoria = ? ;"
        try: 
            cur = self.db.cursor()
            cur.execute(_sql, _rec)
            self.db.commit()
            stato = 0
            messaggio = "OK"
        except:
            stato = 1
            messaggio = "KO"
        
        response_dict['stato'] = stato
        response_dict['messaggio'] = messaggio
        return response_dict
        
    def delete_categoria(self, id_categoria):
        """ Non elimino le categorie associate ad una ricetta """
        
        response_dict = dict()
        _sql = "SELECT COUNT(id_ricetta) FROM ricetta WHERE id_categoria = ? ;"
        cur = self.db.cursor()
        cur.execute(_sql, (id_categoria, ))
        row = cur.fetchone()
        if row[0] == 0:        
            _sql = "DELETE FROM categoria WHERE id_categoria = ? ;"
            try: 
                cur.execute(_sql, (id_categoria, ))
                self.db.commit()
                stato = 0
                messaggio = "OK"
            except:
                stato = 1
                messaggio = "KO"
        else:
            stato = 1
            messaggio = "Impossibile eliminare una categoria associata ad una ricetta."
            
        response_dict['stato'] = stato
        response_dict['messaggio'] = messaggio
        return response_dict
    
    def get_categorie(self):
        categorie_list = list()
        _sql = "SELECT id_categoria, nome FROM categoria ORDER BY nome; "
        cur = self.db.cursor()
        for row in cur.execute(_sql):
            c = dict()
            c['id_categoria'] = row[0]
            c['nome'] = row[1]
            categorie_list.append(c)
        return categorie_list
        
    def salva_sezione(self, _sez):
        response_dict = dict()
        if int(_sez['id_sezione']) == 0:
            _rec = ( _sez['nome'], )
            _sql = "INSERT INTO sezione(nome) values ( ? ); "
        else: 
            _rec = ( _sez['nome'], int(_sez['id_sezione']) )
            _sql = "UPDATE sezione SET nome = ? \
                    WHERE id_sezione = ? ;"
        try: 
            cur = self.db.cursor()
            cur.execute(_sql, _rec)
            self.db.commit()
            stato = 0
            messaggio = "OK"
        except:
            stato = 1
            messaggio = "KO"
        
        response_dict['stato'] = stato
        response_dict['messaggio'] = messaggio
        return response_dict
        
    def delete_sezione(self, id_sezione):
        """ Non elimino le sezioni associate ad una ricetta """
        
        response_dict = dict()
        _sql = "SELECT COUNT(id_ricetta) FROM ricetta WHERE id_sezione = ? ;"
        cur = self.db.cursor()
        cur.execute(_sql, (id_sezione, ))
        row = cur.fetchone()
        if row[0] == 0:        
            _sql = "DELETE FROM sezione WHERE id_sezione = ? ;"
            try: 
                cur.execute(_sql, (id_sezione, ))
                self.db.commit()
                stato = 0
                messaggio = "OK"
            except:
                stato = 1
                messaggio = "KO"
        else:
            stato = 1
            messaggio = "Impossibile eliminare una sezione associata ad una ricetta."
            
        response_dict['stato'] = stato
        response_dict['messaggio'] = messaggio
        return response_dict
        
    def get_sezioni(self):
        sezioni_list = list()
        _sql = "SELECT id_sezione, nome FROM sezione ORDER BY nome; "
        cur = self.db.cursor()
        for row in cur.execute(_sql):
            s = dict()
            s['id_sezione'] = row[0]
            s['nome'] = row[1]
            sezioni_list.append(s)
        return sezioni_list
