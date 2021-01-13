

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

addEventToCard()

$('#save').click( () => {

    const tname = $('#team-name').val();

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
                window.location = '/teams' 
            }
            else
            {
                alert("Couldn't save")
            }
        }
    
    })
})

$('#delete').click( () => {

    let tname = $('#team-name').val();
    if(tname === undefined)
        tname = window.location.href.split("/").pop().replace('_',' ');
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
                window.location = '/teams' 
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

let actualPage = 1;


$('.previus').click( () => {

    actualPage--;

    pageChange(actualPage);

})


$('.next').click( () => {

    actualPage++;

    pageChange(actualPage);

})


function pageChange(nowPage){

    $.ajax({
        type: "GET",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            page : nowPage,
        },
        success: function(data){

            if(data['has_previous'])
                $('.previus').css({
                    "pointer-events": "auto",
                    "visibility": "visible",
                })
            else
                $('.previus').css({
                    "pointer-events": "none",
                    "visibility": "hidden",
                })
            if(!data['has_next'])
                $('.next').css({
                    "pointer-events": "none",
                    "visibility": "hidden",
                })
            else
                $('.next').css({
                    "pointer-events": "auto",
                    "visibility": "visible",
                })

            const pokeList = data['poke_li'];

            const pokeListHtml = $(".pok_list").empty()

            pokeList.forEach(
                value => {
                    pokeListHtml.append(
                        `
                        <div class="card" data-id="${value[0]}" data-name="${value[1]}" data-pic="${value[2]}">
                        <div class="imgbox">
                            <img src="${value[2]}" alt=""></img>
                        </div>
                        <h3>${value[0]} - ${value[1]}</h3>
                        </div>
                        `
                    )
            })

            addEventToCard();
        },
    })


}

function openDetails(tableData){

    const pokemons = $('.card', $('.pokemons')).toArray();

    const table = $(".table-section")

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

function addEventToCard() {
    $(".card").on("click",function() {

        console.log($(this))

        if (list.length < 6 )
        {
            $( this ).clone().appendTo($(".pokemons"))
            const id = $(this).data('id')
            list.push(id)     
        }
    })
}


