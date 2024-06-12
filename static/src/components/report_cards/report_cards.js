/** @odoo-module */
    const { Component, useState } = owl
const { onMounted, useRef } = owl.hooks
import core from 'web.core';
const _t = core._t;
import { useBus } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks"
import { SdMomDataDashboard } from "../data_dashboard";

export class SdMomReportCards extends Component {
    setup(){
    super.setup();
        console.log('ReportCards',this)

    }
}

SdMomReportCards.template = "sd_mom_report_cards"
SdMomDataDashboard.components = { ...SdMomDataDashboard.components, SdMomReportCards }

patch(SdMomDataDashboard.prototype, 'data_dashboard_report',{
    setup(){
        this._super()
//        console.log('InputCards patch',this)
        this.state = useState({
            ...this.state,
            openInputInfo: {
                name: _t('Search'),
                view: _t('View'),
                value: 0,
                status: "",
            },
        })
        this.inputRef = useRef('report_ref');
//        this.toOpenInputInfo = this.toOpenInputInfo.bind(this);
//        this.onChange = this.onChange.bind(this);

//        console.log('data_dashboard_input', this.inputRef.el)
    },


})


