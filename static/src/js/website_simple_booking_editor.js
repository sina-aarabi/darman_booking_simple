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
            string: _t('Children (0-12 years)'),
            defaultValue: 0,
            min: 0,
            max: 9
        }, {
            type: 'selection',
            name: 'child_age_1',
            string: _t('Child 1 Age Range'),
            selection: [
                ['1', _t('Under 1 year')],
                ['2', _t('1 to 2 years')],
                ['3', _t('2 to 3 years')],
                ['4', _t('3 to 4 years')],
                ['5', _t('4 to 5 years')],
                ['6', _t('5 to 6 years')],
                ['7', _t('6 to 7 years')],
                ['8', _t('7 to 8 years')],
                ['9', _t('8 to 9 years')],
                ['10', _t('9 to 10 years')],
                ['11', _t('10 to 11 years')],
                ['12', _t('11 to 12 years')],
            ]
        }, {
            type: 'selection',
            name: 'child_age_2',
            string: _t('Child 2 Age Range'),
            selection: [
                ['1', _t('Under 1 year')],
                ['2', _t('1 to 2 years')],
                ['3', _t('2 to 3 years')],
                ['4', _t('3 to 4 years')],
                ['5', _t('4 to 5 years')],
                ['6', _t('5 to 6 years')],
                ['7', _t('6 to 7 years')],
                ['8', _t('7 to 8 years')],
                ['9', _t('8 to 9 years')],
                ['10', _t('9 to 10 years')],
                ['11', _t('10 to 11 years')],
                ['12', _t('11 to 12 years')],
            ]
        }, {
            type: 'selection',
            name: 'child_age_3',
            string: _t('Child 3 Age Range'),
            selection: [
                ['1', _t('Under 1 year')],
                ['2', _t('1 to 2 years')],
                ['3', _t('2 to 3 years')],
                ['4', _t('3 to 4 years')],
                ['5', _t('4 to 5 years')],
                ['6', _t('5 to 6 years')],
                ['7', _t('6 to 7 years')],
                ['8', _t('7 to 8 years')],
                ['9', _t('8 to 9 years')],
                ['10', _t('9 to 10 years')],
                ['11', _t('10 to 11 years')],
                ['12', _t('11 to 12 years')],
            ]
        }, {
            type: 'selection',
            name: 'child_age_4',
            string: _t('Child 4 Age Range'),
            selection: [
                ['1', _t('Under 1 year')],
                ['2', _t('1 to 2 years')],
                ['3', _t('2 to 3 years')],
                ['4', _t('3 to 4 years')],
                ['5', _t('4 to 5 years')],
                ['6', _t('5 to 6 years')],
                ['7', _t('6 to 7 years')],
                ['8', _t('7 to 8 years')],
                ['9', _t('8 to 9 years')],
                ['10', _t('9 to 10 years')],
                ['11', _t('10 to 11 years')],
                ['12', _t('11 to 12 years')],
            ]
        }, {
            type: 'selection',
            name: 'child_age_5',
            string: _t('Child 5 Age Range'),
            selection: [
                ['1', _t('Under 1 year')],
                ['2', _t('1 to 2 years')],
                ['3', _t('2 to 3 years')],
                ['4', _t('3 to 4 years')],
                ['5', _t('4 to 5 years')],
                ['6', _t('5 to 6 years')],
                ['7', _t('6 to 7 years')],
                ['8', _t('7 to 8 years')],
                ['9', _t('8 to 9 years')],
                ['10', _t('9 to 10 years')],
                ['11', _t('10 to 11 years')],
                ['12', _t('11 to 12 years')],
            ]
        }, {
            type: 'text',
            name: 'description',
            string: _t('Description'),
        }
    ],
    successPage: '/contactus-thank-you',
});
