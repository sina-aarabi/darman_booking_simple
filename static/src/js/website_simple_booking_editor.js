/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import FormEditorRegistry from "@website/js/form_editor_registry";

FormEditorRegistry.add('simple_booking', {
    formFields: [
        {
            type: 'char',
            required: true,
            name: 'name',
            string: _t('Full Name'),
        }, {
            type: 'tel',
            required: true,
            name: 'mobile',
            string: _t('Mobile Number'),
        }, 
        {
            type: 'date',
            required: true,
            fillWith: 'start_date',
            name: 'start_date',
            string: _t('Start Date'),
        }, {
            type: 'date',
            required: true,
            fillWith: 'end_date',
            name: 'end_date',
            string: _t('End Date'),
        }, {
            type: 'selection',
            required: true,
            name: 'partner_type',
            string: _t('نوع همکار'),
            selection: [
                ['fanap', 'گروه فناپ'],
                ['pasargad_financial', 'گروه مالی بانک پاسارگاد'],
                ['pasargad_club', 'باشگاه مشتریان بانک پاسارگاد']
            ]
        }, {
            type: 'integer',
            required: true,
            name: 'adult_count',
            string: _t('Adults (12+ years)'),
            defaultValue: 1,
            min: 1,
            max: 10
        }, {
            type: 'integer',
            name: 'child_count',
            string: _t('Children (2-11 years)'),
            defaultValue: 0,
            min: 0,
            max: 9
        }, {
            type: 'integer',
            name: 'infant_count',
            string: _t('Infants (0-2 years)'),
            defaultValue: 0,
            min: 0,
            max: 9
        }, {
            type: 'text',
            name: 'description',
            string: _t('Description'),
        }
    ],
    successPage: '/contactus-thank-you',
});
