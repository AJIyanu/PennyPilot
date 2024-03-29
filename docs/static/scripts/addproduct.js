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

        const header = {
            "Authorization": `Bearer ${getCookie('x-token')}`,
            'Content-Type': 'application/json',
        }

        console.log(formData, header);

        fetch("http://127.0.0.1:5000/api/newproduct", {
        method: 'POST',
        headers: header,
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alertify.alert("Name already exist", data.error, () => {
            location.reload();
            return;
          })
        }
        alertify.alert("Sucess", data.status, function(){
            location.reload();
          });
      console.log(data);
    })
    .catch(error => {

      console.error(error);
      alertify.error('Some Error has occured. Product is not saved');

    });
  });
});
