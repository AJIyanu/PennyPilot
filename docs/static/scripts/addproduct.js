$(document).ready(function() {

  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const  cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                        }
        }
    }
    return cookieValue;
    }

    $("#addnewproduct").submit(function(event) {
        event.preventDefault();

        let formData = {};

        $(this).serializeArray().map(function(x) {
          formData[x.name] = x.value;
        });

        console.log(formData);

      });
})
