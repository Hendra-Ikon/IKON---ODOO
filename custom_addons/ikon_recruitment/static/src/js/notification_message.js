// odoo.define('portal_offer_notification.website_notification', function (require) {
//     'use strict';
//     var session = require('web.session');
//     var publicWidget = require('web.public.widget');
//     publicWidget.registry.WebsiteNotification = publicWidget.Widget.extend({
//         selector: '#wrapwrap',
//         start: function () {
//             var self = this;
//             var message = "";
//             if (session.user_id) {
//                 console.log("******* HELLO *******")
//                 self._rpc({
//                     model: 'website.notification',
//                     method: 'get_notifications',
//                     args: [{}, session.user_id],
//                 }).then(function (data) {
//                     for (var notification of data) {
//                         message = notification;
//                         Push.create(message, {
//                             body: "Offers and discounts",
//                         });
//                     }
//                 });
//             }
//         },
//     })
// });