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
            showTab('#pills-education');
            resetUrl('/pds/data');
            break;
        case "#language":
            showTab('#pills-language');
            resetUrl('/pds/data');
            break;
        case "#medical":
            showTab('#pills-medical_records');
            resetUrl('/pds/data');
            break;
        case "#confirm":
            console.log("confirm")
            button.click()
            resetUrl('/my/profile');
            break;

        // Add more cases for other tabs as needed
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




