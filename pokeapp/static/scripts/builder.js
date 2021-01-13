

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


const children = $(".pokemons").children().toArray()

const list = [];
if(children.length > 0) children.forEach((elem) => list.push($(elem).data('id')))

$(".card").each((key, card) => {
    $(card).click(() => {
        if (list.length < 6 )
        {
            $(card).clone().appendTo($(".pokemons"))
            const id = $(card).data('id')
            list.push(id)     
        }
    })
})

$('#save').click( () => {

    const tname = $('#team-name').val();
    console.log(tname)

    $.ajax({
        type: "POST",
        url: "/teams/create",
        dataType: "json",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "team-pokemons" : JSON.stringify(list),
            name: tname.toString(),
        },
        success: (data) => {
            if(data['status'])
            {
                confirm(` Team \"${tname}\" saved with success`)
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
            name : tname.toString(),
        },
        success: function(data){
            if(data['status'])
            {
                confirm(` Team \"${tname}\" deleted success`)
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

    if(list.length <= 0) {
        alert("Theres no pokemons in team")
        return
    }

    const data_to_send = JSON.stringify(list)

    console.log(list)

     $.ajax({
        type: "GET",
        url: "/builder/details",
        dataType: "json",
        contentType: "application/json",
        data: {"team-pokemons" : data_to_send} ,
        success: function(data){
            openDetails(data)
            $('#details').css({
                "display" : "none",
                "visibility" : "hidden",
            })
        },
        failure: () => {
            alert("Couldn't get details")
    }
    })
})

function openDetails(tableData){

    const pokemons = $('.card', $('.pokemons')).toArray();

    const table = $(".table-section")

    //display
    $(table).css({
        "visibility": "visible",
        "display": "block",
    })

    $('html, body').animate({
        scrollTop: $(table).offset().top + "px"
    }, 500);

    pokemons.forEach(poke => {
        const pokemon_data = {
            id: $(poke).data('id'),
            name: $(poke).data('name'),
            pic: $(poke).data('pic'),
        }

        $('#tableHead>tr').append(getTableHeadHtml(pokemon_data))
        const tbody = $("#tableBody").children().toArray();

        tbody.forEach(function(val,index){
            $(val).append(` <td>${tableData[pokemon_data["id"]][index]}</td> `)
        })
        
    });      
}

function getTableHeadHtml({id,name,pic}){

    return (
        `
        <th scope="col">
            <div class="table-pokemon">
                <div class="img-holder">
                    <img src=${pic} alt="">
                </div>
                <p>${id} - ${name}</p>
            </div>
        </th>
        `) 

}
