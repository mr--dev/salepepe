function salvaRicetta() {
    var _ric = {}
    _ric.id_ricetta = $("#id-ricetta").val();
    _ric.nome = $("#ricetta").val();
    _ric.numero_rivista = $("#numero-rivista").val();
    _ric.anno_rivista = $("#anno-rivista").val();
    _ric.pagina = $("#pagina").val();
    _ric.preferito = $("#preferito").is(":checked") ? 1 : 0;
    _ric.id_categoria = $("#categoria").val();
    _ric.id_sezione = $("#sezione").val();
    var tags = Array();
    $("#tag span").each(function(ind, el){
        tags.push(el.getAttribute('value'));
    });
    _ric.tags = tags.join("|");
    $.post('/', {'azione': 'salvaRicetta', 'ricetta': JSON.stringify(_ric)}, function(response){
        var response = JSON.parse(response);
        if (response.stato == 0) {
            makeTableRicette(response.ricette);
            hideRicetta();
        }
        else
            alert('Errore durante il salvataggio.');
    })
}

function editRicetta(id_ricetta) {
    $.post('/', {'azione': 'editRicetta', 'id_ricetta': id_ricetta}, function(response){
        var response = JSON.parse(response);
        var r = response.ricetta;
        $("#id-ricetta").val(r.id_ricetta);
        $("#ricetta").val(r.nome);
        $("#numero-rivista").val(r.numero_rivista);
        $("#anno-rivista").val(r.anno_rivista);
        $("#pagina").val(r.pagina);
        if (r.preferito == 1) $("#preferito").attr('checked', 'checked');
        var tags = r.tags.split('|');
        if (tags.length != 0 && tags[0] != '') {
            for (ii = 0; ii < tags.length; ii++) {
                addLabelTag(tags[ii].trim());
            }
        }
        $("#categoria").val(r.id_categoria);
        $("#sezione").val(r.id_sezione);
        showRicetta(id_ricetta);
    })
}

function deleteRicetta(id_ricetta) {
    result = confirm('Sei sicuro di voler eliminare questa ricetta?');
    if (result) {
        $.post('/', {'azione': 'deleteRicetta', 'id_ricetta': id_ricetta}, function(response){
            var response = JSON.parse(response);
            if (response.stato == 0) {
                makeTableRicette(response.ricette);
            }
            else
                alert('Errore durante l\'eliminazione.');
        });
    }
}

function addTag() {
    var tags = $("#inserisci-tag").val().split(',');
    for (ii = 0; ii < tags.length; ii++) {
        addLabelTag(tags[ii].trim());
    }
    $("#inserisci-tag").val('');
}

/* CATEGORIE */
function editCategoria(id_categoria, nome){
    // Per il solo nome, non ha senso una chiamata Ajax.
    $("#id-categoria").val(id_categoria);
    $("#impostazioni-categorie").val(nome);
}
function annullaCategoria() {
    $("#id-categoria").val(0);
    $("#impostazioni-categorie").val('');
}
function salvaCategoria() {
    var _cat = {};
    _cat.id_categoria = $("#id-categoria").val();
    _cat.nome = $("#impostazioni-categorie").val();
    
    if (_cat.nome == '') {
        alert('Inserire il nome della categoria.');
    } else {
        $.post('/', {'azione': 'salvaCategoria', 'categoria': JSON.stringify(_cat)}, function(response){
            var response = JSON.parse(response);
            if (response.stato == 0) {
                annullaCategoria();
                refreshAll();
            }
            else
                alert('Errore durante il salvataggio.');
        });
    }
}
function deleteCategoria(id_categoria) {
    result = confirm('Sei sicuro di voler eliminare questa categoria?');
    if (result) {
        $.post('/', {'azione': 'deleteCategoria', 'id_categoria': id_categoria}, function(response){
            var response = JSON.parse(response);
            if (response.stato == 0) {
                makeCategorie(response.categorie);
            }
            else
                alert(response.messaggio);
        });
    }
}

/* SEZIONI */
function editSezione(id_sezione, nome){
    // Per il solo nome, non ha senso una chiamata Ajax.
    $("#id-sezione").val(id_sezione);
    $("#impostazioni-sezioni").val(nome);
}
function annullaSezione() {
    $("#id-sezione").val(0);
    $("#impostazioni-sezioni").val('');
}
function salvaSezione() {
    var _sez = {};
    _sez.id_sezione = $("#id-sezione").val();
    _sez.nome = $("#impostazioni-sezioni").val();
    
    if (_sez.nome == '') {
        alert('Inserire il nome della sezione.');
    } else {
        $.post('/', {'azione': 'salvaSezione', 'sezione': JSON.stringify(_sez)}, function(response){
            var response = JSON.parse(response);
            if (response.stato == 0) {
                annullaSezione();
                refreshAll();
            }
            else
                alert('Errore durante il salvataggio.');
        });
    }
}
function deleteSezione(id_sezione) {
    result = confirm('Sei sicuro di voler eliminare questa sezione?');
    if (result) {
        $.post('/', {'azione': 'deleteSezione', 'id_sezione': id_sezione}, function(response){
            var response = JSON.parse(response);
            if (response.stato == 0) {
                makeSezioni(response.sezioni);
            }
            else
                alert(response.messaggio);
        });
    }
}


function refreshAll(){
    $.post('/', {'azione': 'caricaContenuti'}, function(response){
        var response = JSON.parse(response);
        makeTableRicette(response.ricette);
        makeCategorie(response.categorie);
        makeSezioni(response.sezioni);
        // TODO: hide loading page;
    });
}

$(document).ready(function(){
    
    refreshAll();
    
    // Bind Listener For Check Form
    $("#ricetta-form input[type=text]").bind('keyup', checkRicettaForm);
    $("#ricetta-form select").bind('change', checkRicettaForm);
    
    _form = $("#ricetta-form").validate({
        'rules': {
            'ricetta': 'required',
            'numero-rivista': 'required',
            'anno-rivista': {
                'required': true,
                'number': true,
            },
            'categoria': 'required',
            'sezione': 'required',
        },
        'messages': {
            'ricetta': '',
            'numero-rivista': '',
            'anno-rivista': '',
            'categoria': '',
            'sezione': '',
        },
    })
})
