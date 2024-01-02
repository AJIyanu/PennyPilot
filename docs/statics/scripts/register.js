const form = document.getElementById("register");


form.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(form);


    let myForm = {}

    for (const [key, value] of formData.entries()) {
        myForm[key] = value
    }

    console.log(JSON.stringify(myForm));
    if (myForm["password"] !== myForm["confirm-password"]) {
        alert("Password mismatch");
        return
    }


    // Send the POST request
    fetch("http://127.0.0.1:5000/api/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(myForm),
    })
    .then(response => response.json())
    .then(data => {
        alertify.alert("User Registered Successfully", "Please Sign in now", function(){
            location.reload();
          });
      console.log(data);
    })
    .catch(error => {

      console.error(error);
      alertify.error('Some Error has occured. Check if email has been registered or contact IT');
    });
  });
