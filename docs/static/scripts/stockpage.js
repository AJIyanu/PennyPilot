const formSubmit = document.getElementById("addStock");
const cost = document.getElementById('costPrice');
const productSelect = document.getElementById('productName');
const sellingPrice = document.getElementById("sellingPrice");
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
    console.log(allProducts);
    allProducts.forEach(productOption => {
        const option = document.createElement("option");
        option.value = productOption.id;
        option.text = productOption.name;
        productSelect.add(option);
    });
})
.catch(err => console.error(err));

productSelect.addEventListener("change", () => {
    let sel = productSelect.options[productSelect.selectedIndex].value;
    allProducts.forEach((check) => {
        if ( check.id === sel ) sel = check;
    })
    cost.value = sel.selling_price;
    // cost.disabled = true;
})

sellingPrice.addEventListener("change", () => {
    if ( sellingPrice.value < cost.value ) {
        sellingPrice.style.border = 'red solid 2px';
    } else {
        sellingPrice.style.border = 'green solid 2px'
    }
})

formSubmit.onsubmit = (event) => {
    event.preventDefault();

    let stockFrom = {
        cost: document.getElementById('costPrice').value,
        sell: document.getElementById("sellingPrice").value,
        name: productSelect.options[productSelect.selectedIndex].text,
        product: productSelect.options[productSelect.selectedIndex].value,
    }

    const multiplier = document.getElementById("productType").value;
    if (multiplier === "unit") {
        stockFrom.qty = document.getElementById("quantity").value;
    } else if ( multiplier === "pack" ) {
        let optionObj = productSelect.options[productSelect.selectedIndex].value;
        allProducts.forEach((check) => {
            if (check.id == optionObj) optionObj = check;
        })
        const newqty = optionObj.pack * document.getElementById("quantity").value;
        stockFrom.qty = newqty;
    } else if ( multiplier === "carton" ) {
        let optionObj = productSelect.options[productSelect.selectedIndex].value;
        allProducts.forEach((check) => {
            if (check.id === optionObj) optionObj = check;
        })
        const newqty = optionObj.pack * optionObj.carton * document.getElementById("quantity").value;
        stockFrom.qty = newqty;
    }

    console.log(stockFrom);

    const header = {
        "Authorization": `Bearer ${getCookie('x-token')}`,
        'Content-Type': 'application/json',
    }

    console.log(formData, header);

    fetch(`http://127.0.0.1:5000/api/newstock/${productSelect.options[productSelect.selectedIndex].value}`, {
    method: 'POST',
    headers: header,
    body: JSON.stringify(stockFrom)
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

}
