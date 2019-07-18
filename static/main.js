$(window).on('load', function () {
    $('#detailModal').modal('show');
    $('#privateModal').modal('show');
    $('#404Modal').modal('show');
});

function onHover() {
    $(".addNoteImg").attr('src', '../static/compose2.png');
}

$("#search_icon").click(function (e) {
    e.preventDefault();
    searchbox = $('#search_input').val();
    if (searchbox != "") {
        searchbox = searchbox.trim().split(" ").join("-")
        window.location.replace("simplenote.ml/search/" + searchbox);
    } else {
        alert("blank input")
    }
})

function offHover() {
    $(".addNoteImg").attr('src', '../static/compose.png');
}

function cardOver(element) {
    element.classList.add("cardHover")
}

function cardOut(element) {
    element.classList.remove("cardHover")
}

document.getElementById("passwordEye").addEventListener("click", function () {
    showHide = document.getElementById("showHideIn");
    icon = document.getElementById("passwordEye").classList;

    var x = showHide.getAttribute("type");
    console.log(x);
    if (x === "password") {
        showHide.setAttribute("type", "text");
        icon.remove("fa-eye");
        icon.add("fa-eye-slash");
    } else if (x == "text") {
        showHide.setAttribute("type", "password");
        icon.remove("fa-eye-slash");
        icon.add("fa-eye");
    }

});

document.getElementById("formSwitch").addEventListener("click", function () {
    showHide = document.getElementById("showHideIn");
    icon = document.getElementById("passwordEye").classList;
    let isPrivate = document.getElementById("formSwitch").getAttribute("placeholder");
    if (isPrivate === "yes") {

        document.getElementById("formSwitch").setAttribute("placeholder", "no");
        showHide.value = "";
        showHide.disabled = true;
        showHide.disabled = true;
    } else if (isPrivate === "no") {
        document.getElementById("formSwitch").setAttribute("placeholder", "yes");
        showHide.disabled = false;
    }
});

$(document).ready(() => {

    //Add Note Control
    $("#kapgit").click(function (event) {
        event.preventDefault();
        inputData = {
            header: $('#formHeader').val(),
            note: $('#formText').val(),
            isPrivate: $('#formSwitch').attr('placeholder'),
            password: $('#showHideIn').val()

        };
        if (inputData.header == "") {
            $("#n1").css("display", "inline-block");
        } else if (inputData.note == "") {
            $("#n1").css("display", "none");
            $("#n2").css("display", "inline-block");
        } else if (inputData.isPrivate === "yes" && inputData.password == "") {
            $("#n1").css("display", "none");
            $("#n2").css("display", "none");
            $("#n3").css("display", "inline-block");
        } else {
            $("#n1,#n2,#n3").css("display", "none");
            $("#addNoteForm").submit();
        }
        console.log(inputData)
    });

    // Password Control
    $('#show').on('click', (e) => {
        $.ajax({
            data: {
                sPassword: $('#privateInputPassword').val(),
                sId: $('#sId').attr("placeholder")
            },
            type: 'POST',
            url: '/passwordcontrol'
        })
            .done((data) => {
                if (data.error) {
                    console.log(data.error);
                    $('.wrongPassword').css("display", "block");
                } else {
                    $('#privateHeader').text(data.header);
                    $('#privateContent').text(data.note);
                    $('#privateModal').modal('hide');
                    $('#privateDetailModal').modal('show');
                    console.log(data.sPassword)
                }
            })
    });


});


