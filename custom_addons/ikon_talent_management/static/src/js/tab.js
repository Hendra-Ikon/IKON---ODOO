$(document).ready(function() {
  const tabs = $('#pills-tab');
  const tabContent = $('#pills-tabContent');

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

  // Activate tab based on URL
  const urlParams = new URLSearchParams(window.location.href);
  const id = urlParams.get('id');
  console.log(urlParams)
  
  if (id) {
      const tabElement = $(`.nav-link[href="#${id}"]`);
      if (tabElement.length) {
          tabElement.tab('show'); // Activate the tab
      }
  }
});
