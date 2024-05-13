
function decreaseQuantity(urunId, urunFiyat) {
    var quantityElement = document.getElementById('quantity_' + urunId);
    var currentQuantity = parseInt(quantityElement.innerText);
    if (currentQuantity > 0) {
        quantityElement.innerText = currentQuantity - 1;

        // Azaltma işlemi yapıldığında sipariş detaylarını güncelle
        updateOrderDetails(urunId, currentQuantity - 1);
        checkOrderButtonVisibility();
    }
}

function increaseQuantity(urunId) {
    var quantityElement = document.getElementById('quantity_' + urunId);
    var currentQuantity = parseInt(quantityElement.innerText);
    quantityElement.innerText = currentQuantity + 1;

    // Artırma işlemi yapıldığında sipariş detaylarını güncelle
    updateOrderDetails(urunId, currentQuantity + 1);
    checkOrderButtonVisibility();
}

function updateOrderDetails(urunId, quantity) {
    var listItem = document.getElementById("order_" + urunId);

    // Eğer listede ürün zaten varsa, miktarını güncelle
    if (listItem) {
        var spanElement = listItem.querySelector('span');
        spanElement.innerText = quantity + " adet";
    } else {
        listItem = document.createElement("li");
        listItem.id = "order_" + urunId;
        listItem.innerHTML = "<span>" + quantity + " adet</span>";

        var decreaseButton = document.createElement("button");
        decreaseButton.innerText = "-";
        decreaseButton.onclick = function() {
            decreaseQuantity(urunId);
        };
        listItem.appendChild(decreaseButton);

        var increaseButton = document.createElement("button");
        increaseButton.innerText = "+";
        increaseButton.onclick = function() {
            increaseQuantity(urunId);
        };
        listItem.appendChild(increaseButton);

        document.getElementById("orderList").appendChild(listItem);
    }
}

function showModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";

    var orderList = document.getElementById("orderList");
    orderList.innerHTML = ""; // Önceki içeriği temizle

    // Tüm kartlardaki ürünleri kontrol et
    var cards = document.getElementsByClassName("card");
    for (var i = 0; i < cards.length; i++) {
        var card = cards[i];
        var urunAdi = card.getElementsByTagName("h3")[0].innerText;
        var urunId = card.getElementsByTagName("span")[0].id.split("_")[1]; // ürün id'sini al
        var miktar = parseInt(card.getElementsByClassName("quantity")[0].getElementsByTagName("span")[0].innerText);

        // Miktar sıfırdan büyükse, listeye ekleyelim
        if (miktar > 0) {
            var listItem = document.createElement("li");
            listItem.id = "order_" + urunId;
            listItem.innerHTML = "<p>" + urunAdi + ": <span class='quantity-display'>" + miktar + " adet</span></p>";

            var buttonDiv = document.createElement("div");
            buttonDiv.className = "btn-group";

            var decreaseButton = document.createElement("button");
            decreaseButton.className = "btn btn-warning azalt";
            decreaseButton.innerText = "-";
            decreaseButton.onclick = (function(id) {
                return function() {
                    decreaseQuantity(id);
                };
            })(urunId);
            buttonDiv.appendChild(decreaseButton);

            var increaseButton = document.createElement("button");
            increaseButton.className = "btn btn-primary arttir";
            increaseButton.innerText = "+";
            increaseButton.onclick = (function(id) {
                return function() {
                    increaseQuantity(id);
                };
            })(urunId);
            buttonDiv.appendChild(increaseButton);

            listItem.appendChild(buttonDiv);

            orderList.appendChild(listItem);
        }
    }

}
function isCartEmpty() {
    var orderList = document.getElementById("orderList");
    return orderList.children.length === 0; // Eğer orderList'in içinde hiç çocuk yoksa, sepet boş demektir
}
// Sayfa yüklendiğinde çalışacak fonksiyon
window.onload = function() {
    // Butonun görünürlüğünü kontrol et
    checkOrderButtonVisibility();
}

// Siparişi tamamla butonunu kontrol eden fonksiyon
function checkOrderButtonVisibility() {
    var orderOkButton = document.getElementById("orderOk");
    if (isCartEmpty()) {
        orderOkButton.style.display = "none"; // Sepet boşsa butonu gizle
    } else {
        orderOkButton.style.display = "block"; // Sepet doluysa butonu göster
    }
}
function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

window.onclick = function(event) {
    var modal = document.getElementById("myModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Çerezin başlangıcını kontrol et
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function confirmOrder() {
    // CSRF token'ı alın
    var csrfToken = getCookie('csrftoken');
    var firmaKod = document.getElementById("firma-kod").value;
    // Modaldan seçilen ürünlerin bilgilerini al
    var selectedProducts = [];
    var orderListItems = document.getElementById("orderList").getElementsByTagName("li");
    for (var i = 0; i < orderListItems.length; i++) {
        var productId = orderListItems[i].id.split("_")[1];
        var quantity = parseInt(orderListItems[i].getElementsByClassName("quantity-display")[0].textContent);

        selectedProducts.push({urun_id: productId, miktar: quantity});
    }

    // Sipariş bilgilerini JSON formatına dönüştür
    var orderData = {
        urunler: selectedProducts
    };

    // AJAX ile sunucuya sipariş bilgilerini gönder
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/siparis_olustur/" + firmaKod, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    // CSRF token'ı başlığa ekleyin
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            Swal.fire({
                title: 'Sipariş Tamamlandı',
                text: response.message,
                icon: 'success',
                // showCancelButton: true,
                backdrop:false,
                confirmButtonText: 'Tamam',
                cancelButtonText: 'Kapat',
                allowOutsideClick: false,
            }).then((result) => {
                if (result.isConfirmed) {
                    closeModal(); // Modali kapat
                    location.reload(); // Sayfayı yenile
                    Swal.close(); // Swal modalını kapat
                }
            });
            
        }
    };
    xhr.send(JSON.stringify(orderData));
}