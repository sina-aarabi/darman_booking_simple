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
    },  {
        type: 'date',
        required: true,
        fillWith: 'end_date',
        name: 'end_date',
        string: _t('End Date'),
    }],
    successPage: '/contactus-thank-you',
});
