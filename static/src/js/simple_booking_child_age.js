/** @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';

'use strict';

publicWidget.registry.SimpleBookingChildAge = publicWidget.Widget.extend({
    selector: '#simple_booking_form',
    start: function () {
        this._super(...arguments);
        this.$childCount = this.$el.find('#child_count');
        if (!this.$childCount.length) {
            return Promise.resolve();
        }
        this.$childCount.attr('max', 5);
        this._updateChildAgeVisibility();
        this.$childCount.on('input change', this._updateChildAgeVisibility.bind(this));
        return Promise.resolve();
    },
    _updateChildAgeVisibility: function () {
        var cnt = parseInt(this.$childCount.val(), 10) || 0;
        for (var i = 1; i <= 5; i++){
            var $row = this.$el.find('#child_age_' + i + '_row');
            if (!$row.length) { continue; }
            if (i <= cnt) {
                $row.show();
            } else {
                $row.hide();
                // clear value when hidden
                this.$el.find('#child_age_' + i).val('');
            }
        }
    },
});

