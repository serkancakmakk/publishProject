document.addEventListener('DOMContentLoaded', function() {
    var editButtons = document.querySelectorAll('.kat-edit-btn');
    
    editButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var katAd = button.dataset.katAd;
            var katDurum = button.dataset.katDurum;
            var katID = button.dataset.katId;
            var modal = new bootstrap.Modal(document.getElementById('katDüzenleModal'));
            
            // Hedeflenen inputları doğru şekilde almak için id'leri kontrol edelim
            var katAdInput = document.getElementById('katAdInput');
            var katDurumInput = document.getElementById('katDurumInput');
            var katIdInput = document.getElementById('katIdInput')
            // Modal başlığını güncelleyin
            var modalTitle = document.getElementById('katTitle');
            modalTitle.textContent = 'Şuanda Düzenlenen Kategori: ' + katAd;
            // Inputlara değerleri atayın
            katAdInput.value = katAd;
            katIdInput.value = katID;
           // katDurumInput.value = katDurum;
            katDurumInput.checked = katDurum === 'True';
            
            // Modalı gösterin
            modal.show();
        });
    });
});