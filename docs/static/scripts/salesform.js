document.addEventListener('DOMContentLoaded', function () {
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
