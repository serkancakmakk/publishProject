
document.addEventListener('DOMContentLoaded', function() {
  var editButtons = document.querySelectorAll('.masa-edit-btn');
  editButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var masaId = button.dataset.masaId;
      var masaNum = button.dataset.masaNum;
      var masaKat = button.dataset.masaKat;
      var selectedKatAd = button.dataset.masaKat;
      var masaKatId = button.dataset.masaKatId;
      var masaDurum = button.dataset.masaDurum;
      console.log('Seçilen KAt adı',selectedKatAd);
      var modal = new bootstrap.Modal(document.getElementById('masaDüzenleModal'));
      var masaDurumInput = document.getElementById('masaDurumInput');
      var masaNumInput = document.getElementById('masaNumInput');
      var masaIdInput = document.getElementById('masaIdInput');
      var selectedKatOption = document.getElementById('selectedKatOption');
      var selectedKat = document.getElementById('selectedKat');
      var modalTitle = document.getElementById('table_info');
      modalTitle.textContent = 'Düzenlenen Masa: ' + masaNum + ' (' + selectedKatAd + ')';
      masaDurumInput.checked = masaDurum === 'True'; // Boolean değer checkbox'a atanır
      masaNumInput.value = masaNum;
      masaIdInput.value = masaId;
      selectedKat.textContent = selectedKatAd;
      selectedKat.value = masaKatId;
      masaDurumInput
      modal.show();

// Modal dışındaki bir yere tıklandığında da modalı kapat
document.addEventListener('click', function(event) {
if (event.target === document.querySelector('.modal.fade.show')) {
modal.hide();
}
});
    });
  });
});