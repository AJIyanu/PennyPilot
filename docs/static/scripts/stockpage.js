const productSelect = document.getElementById('productName');
let allProducts

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


const options = {
    headers: {
        "Authorization": `Bearer ${getCookie("x-token")}`
    },
}

fetch("http://127.0.0.1:5000/api/products/all", options )
.then(response => response.json())
.then(data => {
    allProducts = data;
    allProducts.array.forEach(productOption => {
        const option = document.createElement("option");
        option.value = productOption.id;
        option.text = productOption.name;
        productSelect.add(option);
    });
})
.catch(err => console.error(err));
