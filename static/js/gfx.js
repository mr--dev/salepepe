function showRicetta(id_ricetta) {
    $("#id-ricetta").val(id_ricetta);
    $("#main-div").hide("slide",{direction: 'up'});
    $("#scheda-ricetta-div").show("slide",{direction: 'down'});
    _form.resetForm();
}

function hideRicetta() {
    clearRicetta();
    $("#scheda-ricetta-div").hide("slide",{direction: 'down'});
    $("#main-div").show("slide",{direction: 'up'});
}

function clearRicetta() {
    $("#ricetta-form input").val('')
    $("#ricetta-form select").val('')
    $("#ricetta-form input[type=checkbox]").removeAttr('checked');
    checkRicettaForm();
}
function checkRicettaForm() {
    if ( $("#ricetta-form").valid() ) {
        $("#check-ricetta-form").removeClass('glyphicon-exclamation-sign').addClass('glyphicon-ok');
    } else {
        $("#check-ricetta-form").removeClass('glyphicon-ok').addClass('glyphicon-exclamation-sign');
    }
}

function makeTableRicette(ricette) {
    var html = '';
    for (ii=0; ii<ricette.length; ii++) {
        var r = ricette[ii];
        var htmlPreferito = r.preferito == 1 ? '<span class="glyphicon glyphicon-star-empty"></span>' : '';
        html += '<tr>'+
        '    <td>'+r.nome+'</td>'+
        '    <td class="text-center">'+r.numero_rivista+'</td>'+
        '    <td class="text-center">'+r.anno_rivista+'</td>'+
        '    <td>'+r.categoria+'</td>'+
        '    <td>'+r.sezione+'</td>'+
        '    <td class="text-center">'+htmlPreferito+'</td>'+
        '    <td class="text-center cursor-pointer" onclick="javascript:editRicetta('+r.id_ricetta+')">'+
        '       <span class="glyphicon glyphicon-pencil"></span>'+
        '    </td>'+
        '    <td class="text-center cursor-pointer" onclick="javascript:deleteRicetta('+r.id_ricetta+')">'+
        '       <span class="glyphicon glyphicon-remove"></span>'+
        '    </td>'+
        '</tr>'
    }
    $("#ricette-table tbody").html(html);
}

function makeCategorie(categorie) {
    var htmlSelect = '<option value="">Seleziona</option>';
    var htmlTable = '';
    for (ii=0; ii<categorie.length; ii++){
        var c = categorie[ii];
        htmlSelect += '<option value="'+c.id_categoria+'">'+c.nome+'</option>';
        htmlTable += '<tr>'+
            '   <td style="width: 80%">'+c.nome+'</td>'+
            '   <td style="width: 10%" class="cursor-pointer" onclick="javascript:editCategoria('+c.id_categoria+', \''+c.nome+'\');">'+
            '       <span class="glyphicon glyphicon-pencil"></span>'+
            '   </td>'+
            '   <td style="width: 10%" class="cursor-pointer" onclick="javascript:deleteCategoria('+c.id_categoria+')">'+
            '       <span class="glyphicon glyphicon-remove"></span>'+
            '   </td>'+
            '</tr>';
    }
    $("#categoria-filtra").html(htmlSelect);
    $("#categoria").html(htmlSelect);
    $("#categorie-table tbody").html(htmlTable);
}

function makeSezioni(sezioni) {
    htmlSelect = '<option value="">Seleziona</option>';
    var htmlTable = '';
    for (ii=0; ii<sezioni.length; ii++) {
        var s = sezioni[ii];
        htmlSelect += '<option value="'+s.id_sezione+'">'+s.nome+'</option>';
        htmlTable += '<tr>'+
            '   <td style="width: 80%">'+s.nome+'</td>'+
            '   <td style="width: 10%" class="cursor-pointer" onclick="javascript:editSezione('+s.id_sezione+', \''+s.nome+'\')">'+
            '       <span class="glyphicon glyphicon-pencil"></span>'+
            '   </td>'+
            '   <td style="width: 10%" class="cursor-pointer" onclick="javascript:deleteSezione('+s.id_sezione+')">'+
            '       <span class="glyphicon glyphicon-remove"></span>'+
            '   </td>'+
            '</tr>';
    }
    $("#sezione").html(htmlSelect);
    $("#sezioni-table").html(htmlTable);
}
function showImpostazioni() {
    $("#impostazioni-div").show("slide",{direction: 'up'});
}

function hideImpostazioni() {
    $("#impostazioni-div").hide("slide",{direction: 'up'});
}

function clearFiltri() {
    $("#parola-chiave-filtra").val('');
    $("#categoria-filtra").val('');
}
