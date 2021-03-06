function addCard(baseLien, linkGetDetail, companyId, linkDeleteCard, linkFounder, username, linkCard){
    //DATA of the form
    var phase = document.getElementById("phase").value;
    var title = document.getElementById("title").value;
    var comment = document.getElementById("comment").value;
    var deadline = document.getElementById("deadline").value;
    var assigned = document.getElementById("assigned").value;
    var state = document.getElementById("state").checked;
    var update = document.getElementById("update").value;

    //Prepare the link
    baseLien = baseLien.replace(/([0-9]+)/, companyId);

    var newUl = document.getElementById('phase-'+ phase);
    order = newUl.getElementsByTagName('li').length + 1;

    //Link to add a card
    lien = baseLien + "add/";
    $.ajax({
        type: 'POST',
        url: lien,
        data: '&title=' + title
            + '&comment=' + comment
            + '&deadline=' + deadline
            + '&assigned=' + assigned
            + '&order=' + order
            + '&phase=' + phase
            + '&state=' + state
            + '&update=' + update,

        success: function(data, status) {
            //It's a new card
            if(!data.updated){
                if(data.title){
                    createCard(data.id, linkGetDetail, linkDeleteCard, linkFounder, username, linkCard);
                }
            }

            //It's an update of a card
            else{
                //Init the form
                document.getElementById('update').value = "False";
                refreshCard(data.id, linkGetDetail, linkDeleteCard, linkFounder, username, linkCard);

                //Init the title of the form
                var titleForm = document.getElementById('ui-id-1');
                titleForm.innerHTML = "Create new task";
            }
        },

        error: function(resultat, status, erreur) {
            //Init the form
            document.getElementById('update').value = "False";
        }
    });
}