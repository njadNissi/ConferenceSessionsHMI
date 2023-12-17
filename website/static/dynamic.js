// const userName = document.getElementById('name').value
const totalRows = document.getElementById('rows')
const totalCols = document.getElementById('cols')
const headers = document.getElementById('headers')
let tbody = document.getElementById('body')
indSC = 2 // index of session chair name, 3=3rd column
const keyword_chair = document.getElementById('keyword_chair')

function addRow(){
    let row = document.createElement('tr')
    let rows = parseInt(totalRows.value) + 1
    let cols = parseInt(totalCols.value)
    h = headers.value.slice(0, -1).split(',')

    for(let i=0; i < cols; i++){
        let td = document.createElement("td")

        if(i == 0){ td.innerText = "" + rows }
        else{
            let newField = document.createElement('input');
            newField.setAttribute('type','text');
            newField.setAttribute('id', h[i]);
            newField.setAttribute('name', h[i]);
            // newField.setAttribute('class','text');
            newField.setAttribute('size', 15);
            newField.setAttribute('placeholder', h[i]);
    
            td.appendChild(newField)
        }
        row.appendChild(td)
    }
     // add the save button to row
     let a = document.createElement('a')
     a.innerHTML = '<strong><font color=blue>save</font></strong>'
     a.href = ''
    //  a.addEventListener('click', () => { alert('saved') });
     row.appendChild(a)
     // add row to tbody
    tbody.appendChild(row);
    // alert('created ' + userName)
}

function removeRow(row_id){
    window.h
    let row = document.getElementById(row_id)
    tbody.removeChild(row)
}

// search in all the sessions of the whole conferenvce
function searchChair(){
    window.location.href = '/chair/sessions/search?keyword='+ keyword_chair.value
}



$(document).ready(function(){
    function showPopup(whichpopup){
     var docHeight = $(document).height();
     var scrollTop = $(window).scrollTop();
     $('.overlay-bg').show().css({'height' : docHeight});
     $('.popup'+whichpopup).show().css({'top': scrollTop+20+'px'});
    }
    // function to close our popups

    function closePopup(){
        $('.overlay-bg, .overlay-content').hide();
    }
    $('.show-popup').click(function(event){
        event.preventDefault();
        var selectedPopup = $(this).data('showpopup');
        showPopup(selectedPopup);
    });
    $('.close-btn, .fa-window-close, .overlay-bg').click(function(){
        closePopup();
    });
    $(document).keyup(function(e) {
        if (e.keyCode == 27) {
            closePopup();
        }
    });
});