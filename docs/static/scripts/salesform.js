const searchBox = document.getElementById("searchGoods");
const searchListDropdown = document.createElement("div");
let allStock = [];
let choiceProduct;
let userchoice;


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

    // Simulate API response for product details
    var productDetails = {
        name: "Sample Product",
        goodsLeft: 50,
        productType: "Unit" // Replace with actual API response
    };

    // Update UI with product details
    document.getElementById('productName').value = productDetails.name;
    document.getElementById('goodsLeft').innerText = productDetails.goodsLeft;
    document.getElementById('productTypeBtn').innerText = "Product Type: " + productDetails.productType;

    // Update price on input change
    document.getElementById('unitsSold').addEventListener('input', updatePrice);
    document.getElementById('packsSold').addEventListener('input', updatePrice);
    document.getElementById('cartonsSold').addEventListener('input', updatePrice);

    function updatePrice() {
        var units = parseInt(document.getElementById('unitsSold').value) || 0;
        var packs = parseInt(document.getElementById('packsSold').value) || 0;
        var cartons = parseInt(document.getElementById('cartonsSold').value) || 0;

        var totalPrice = calculateTotalPrice(units, packs, cartons);
        document.getElementById('displayPrice').innerText = totalPrice.toFixed(2);
    }

    function calculateTotalPrice(units, packs, cartons) {
        // Replace with your pricing logic based on the product type
        var pricePerUnit = 2.00; // Sample price per unit
        var pricePerPack = 5.00; // Sample price per pack
        var pricePerCarton = 20.00; // Sample price per carton

        var total = units * pricePerUnit + packs * pricePerPack + cartons * pricePerCarton;
        return total;
    }
});
