SalePepeManager
=============

Qualche tempo fa mi è stato chiesto di sviluppare un semplice applicativo che consentisse la catalogazione delle riviste di Sale e Pepe.  
Tale software doveva consentire l'inserimento delle ricette presenti nella rivista in modo da favorirne l'operazione di consultazione w ricerca.  
Ho deciso di rendere pubblico questo piccolo progettino, scritto nel tempo libero.  
SalePepeManager è stato sviluppato utilizzando:  
* [Tornado](http://www.tornadoweb.org/en/stable/): framework Python
* [Amelia](http://bootswatch.com/amelia/): tema basato su [Bootstrap](http://getbootstrap.com/)
* [jQuery](http://jquery.com/download/)
* [jQuery Validation Plugin](http://jqueryvalidation.org/) per la validazione dei form
* SQLite
* il CSS per il loading page utilizzato nelle operazioni di salvataggio, modifica, elimina è stato ispirato dal progetto GitHub [SpinKit](https://github.com/tobiasahlin/SpinKit)

La struttura base del database è nel file `salepepe.struct.sql` presente nella home di questo progetto.
Le configurazioni dell'applicativo (porta, numero paginazione, nome database) si trovano nel file `config.py`.
