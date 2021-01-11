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

    const name = $('team-name').val();

    $.ajax({
        type: "POST",
        url: "/teams",
        dataType: "json",
        data: {
            "team-pokemons" : list,
            "team-name" : name,
        },
        success: () => {
            confirm(` Team ${name} saved with success`)
            window.location = '/teams'                
        },
        failure: () => {
            alert("Couldn't save team. Name invalid or team already exist ")
        }
    
    })
})

$('#delete').click( () => {

    const name = $('team-name').val();

    $.ajax({
        type: "POST",
        url: "teams",
        dataType: "json",
        data: {
            "name" : name,
        },
        success: function(data){
            console.log(data)
            openDetails(data)
        },
        failure: () => {
            alert("Couldn't get details")
        }
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

function openDetails(table_data){
    //write details
}