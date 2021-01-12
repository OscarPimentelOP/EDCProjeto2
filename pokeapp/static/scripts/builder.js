function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

var total = 0;
const list = [];

$(".card").each((key, card) => {
    $(card).click(() => {
        if (total < 6 )
        {
            $(card).clone().appendTo($(".pokemons"))
            const id = $(card).data('id')
            list.push(id)
            total++;       
        }
    })
})

$('#save').click( () => {

    const name = $('#team-name').val();
    console.log(name)

    $.ajax({
        type: "POST",
        url: "/teams/create",
        dataType: "json",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "team-pokemons" : JSON.stringify(list),
            name: name,
        },
        success: (data) => {
            if(data['status'])
            {
                confirm(` Team ${name} saved with success`)
                // window.location = '/teams' 
            }
            else
            {
                alert("Couldn't save")
            }
        }
    
    })
})

$('#delete').click( () => {

    const tname = $('#team-name').val();
    console.log(tname)

    $.ajax({
        type: "POST",
        url: "/teams/delete",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            name : tname,
        },
        success: function(data){
            if(data['status'])
            {
                confirm(` Team ${tname} deleted success`)
                // window.location = '/teams' 
            }
            else
            {
                alert("Couldn't delete")
            }
        },
    })
})

$('#details').click( () => {

    const data_to_send = JSON.stringify(list)

     $.ajax({
        type: "GET",
        url: "details",
        dataType: "json",
        contentType: "application/json",
        data: {"team-pokemons" : data_to_send} ,
        success: function(data){
            console.log(data)
            openDetails(data)
        },
        failure: () => {
            alert("Couldn't get details")
    }
    })
})

function openDetails(tableData){

    const ids = Object.keys(tableData)

    console.log(ids)

    var pokemons = $('.card', $('.pokemons'))

    console.log(pokemons)

}