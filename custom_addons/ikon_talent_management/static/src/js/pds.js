console.log("Haloooo");

var ikon_talent_management = ikon_talent_management || {};

ikon_talent_management.pds = (function ($) {
    "use strict";

    function editCert(certId) {
        // Your existing edit logic here
    }

    function deleteCert(cert) {
        console.log("Before confirmation");
        if (confirm("Are you sure you want to delete this certification?")) {
            console.log("After confirmation");
            $(cert).remove();  // Remove the table row from the DOM
            console.log("Yoyoyo");
        }
    }


    return {
        editCert: editCert,
        deleteCert: deleteCert,
    };
})();
