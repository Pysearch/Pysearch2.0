$(document).ready(function(){
    $('#search-button').on("click", function(e){
        
        $('#search-box').hide()
        $('#search-button').hide()
        $('.infinity').show();
        console.log('before show');
        console.log('after show');
        
        e.preventDefault();
        $.ajax({
            url: "/",
            method: "POST",
            data: {
                "url": $('#search-box').val(),
            },
            success: function(){
                console.log("clicked");
                window.location.href = "/loading?url=" + $('#search-box').val();
            }
        });
    });
});