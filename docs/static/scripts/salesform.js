const searchBox = document.getElementById("searchGoods");
const searchListDropdown = document.createElement("div");
let allStock = [];
let choiceProduct;
let userchoice;
let productSelected;


searchListDropdown.classList.add("dropdown-menu");

function appendFilteredList(input) {

    const fileterdList = allStock.filter(suggest => {
        return suggest.name.toLowerCase().startsWith(input.toLowerCase());
    })

    searchListDropdown.innerHTML = "";

    fileterdList.forEach(result => {
        const listElement = document.createElement("div");
        listElement.classList.add('dropdown-item');
        listElement.innerText = result.name;
        listElement.setAttribute("data-id", result.id);

        searchListDropdown.appendChild(listElement);

    })

    searchListDropdown.style.position = "absolute";
    searchListDropdown.style.top = `${Number(searchBox.getBoundingClientRect().top) + Number(searchBox.offsetHeight)}px`
    searchListDropdown.style.left = searchBox.offsetLeft + 'px';
    searchListDropdown.style.width = searchBox.offsetWidth + 'px';
    searchListDropdown.classList.add("show");
    document.body.appendChild(searchListDropdown);

    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener("click", (event) => {
            document.getElementById("productName").value = item.innerText;
            searchBox.value = "";
            searchListDropdown.classList.remove("show");
            extractChoice(item.getAttribute("data-id"));
        })
    })
}

function extractChoice (choice) {
    allStock.forEach(item => {
        if (item.id === choice) {
            userchoice = item;
		    console.log(userchoice);
            document.getElementById('goodsLeft').innerText = userchoice.stock_qty;
            document.getElementById('productTypeBtn').innerText = "Cost Price: " + userchoice.cost_price;
            return
        }
    })
}

//searchBox.addEventListener("blur", () => {
//   searchListDropdown.classList.remove('show');
//})

searchBox.addEventListener("focus", () => {
   searchListDropdown.classList.add("show");
})

searchBox.addEventListener("input", () => {
    appendFilteredList(searchBox.value);
});

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

document.addEventListener('DOMContentLoaded', function () {

    fetch("http://127.0.0.1:5000/api/stock", options )
    .then(resp => resp.json())
    .then(data => {
//        console.log(data);
        allStock = data;
    })

    // Update price on input change
    document.getElementById('unitsSold').addEventListener('input', updatePrice);
    document.getElementById('packsSold').addEventListener('input', updatePrice);
    document.getElementById('cartonsSold').addEventListener('input', updatePrice);

    async function updatePrice() {
        var units = parseInt(document.getElementById('unitsSold').value) || 0;
        var packs = parseInt(document.getElementById('packsSold').value) || 0;
        var cartons = parseInt(document.getElementById('cartonsSold').value) || 0;

        var totalPrice = await calculateTotalPrice(units, packs, cartons);
	    console.log(totalPrice);
        document.getElementById('displayPrice').innerText = totalPrice;
    }

    let totalProd;

    async function calculateTotalPrice(units, packs, cartons) {
        // Replace with your pricing logic based on the product type
        const pricePerUnit = userchoice.selling_price
        let pricePerPack;
        let pricePerCarton;

        await fetch("http://127.0.0.1:5000/api/product/" + userchoice.product_id, options)
        .then(resp => resp.json())
        .then(data => {
            productSelected = data;
            pricePerPack = userchoice.selling_price * data.pack;
            pricePerCarton = userchoice.selling_price * data.carton;
        })

        totalProd = units + packs * data.pack + cartons * data.carton;

        if (totalProd < userchoice.stock_qty) {
            document.getElementById('goodsLeft').style.backgroundColor = "green";
        } else document.getElementById('goodsLeft').style.backgroundColor = "red";

        var total = units * pricePerUnit + packs * pricePerPack + cartons * pricePerCarton;
	    console.log(total)
        return total;

    }
});

const soldPrice = document.getElementById("soldPrice");

soldPrice.addEventListener("change", () => {
    if (soldPrice.value > Number(document.getElementById("displayPrice").innerText)) {
        soldPrice.style.border = "green solid";
    } else soldPrice.style.border = "red solid";
})

document.getElementById("submitSale").addEventListener("click", (event) => {
    event.preventDefault();

    const salesJson = {
        "sell": soldPrice.value,
        "qty": totalProd,
    }

    const header = {
        "Authorization": `Bearer ${getCookie('x-token')}`,
        'Content-Type': 'application/json',
    }

    fetch("http://127.0.0.1/api/sales/" + userchoice.id, {
    method: "POST",
    headers: header,
    body: JSON.stringify(salesJson),
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

})
