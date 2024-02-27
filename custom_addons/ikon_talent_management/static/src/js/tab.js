$(document).ready(function() {
  const tabs = $('#pills-tab');
  const tabContent = $('#pills-tabContent');
  var hash = window.location.hash;
  var button =  document.getElementById('buttonclick')

  // Next Button
  $('.nextBtn').on('click', function() {
      console.log("next1")
      const activeTab = tabs.find('.nav-link.active');
      const nextTab = activeTab.parent().next().find('.nav-link');

      if (nextTab.length) {
          activeTab.removeClass('active');
          nextTab.tab('show');
      }
  });

  // Back Button
  $('.backBtn').on('click', function() {
      console.log("back")
      const activeTab = tabs.find('.nav-link.active');
      const prevTab = activeTab.parent().prev().find('.nav-link');

      if (prevTab.length) {
          activeTab.removeClass('active');
          prevTab.tab('show');
      }
  });


  switch (hash) {
    case "#education":
        showTab('#pills-family');
        activateButton('#pills-family-tab');
        resetUrl('/pds/data');
        break;
    case "#work":
        showTab('#pills-work');
        activateButton('#pills-work-tab');
        resetUrl('/pds/data');
        break;
    case "#language":
        showTab('#pills-education');
        activateButton('#pills-education-tab');
        resetUrl('/pds/data');
        break;
    case "#medical":
        showTab('#pills-language');
        activateButton('#pills-language-tab');
        resetUrl('/pds/data');
        break;
    case "#financial":
        showTab('#pills-financial');
        activateButton('#pills-financial-tab');
        resetUrl('/pds/data');
        break;
    case "#confirm":
        console.log("confirm")
        button.click()
        setTimeout(function() {
            window.location.href = '/my/profile';
        }, 2000); // 2000 milliseconds = 2 seconds
        break;
}

function activateButton(buttonId) {
    // Hapus kelas 'active' dari semua tombol
    document.querySelectorAll('.nav-link').forEach(function(button) {
        button.classList.remove('active');
    });
    // Tambahkan kelas 'active' ke tombol yang sesuai
    document.querySelector(buttonId).classList.add('active');
}


    function showTab(tabId) {
        $('#pills-tabContent .tab-pane').removeClass('show active');
        $(tabId).addClass('show active');
    }
    function showModal(){
        
        setInterval(function(){
            buttonclick.click()
        },10)
    }
      

    function resetUrl(url) {
        history.replaceState(null, null, url);
    }
});




