/** @odoo-module */
    import { registry } from "@web/core/registry"
    const { Component, useRef, useState } = owl
    const { useEnv, onWillStart, onMounted, onWillUnmount } = owl.hooks;
    import { session } from "@web/session";
    import { useService } from "@web/core/utils/hooks"
    import { SdMomDataCards } from "./data_cards/data_cards"
//    import { DataPlans } from "./data_plans/data_plans"
    import Bus from 'web.Bus';
    const { DateTime, Settings } = luxon;
    import core from 'web.core';
    const _t = core._t;
    const SERVER_DATE_FORMAT = "yyyy-MM-dd";

export class SdMomDataDashboard extends Component {
    setup(){
        let self = this;
        let loadingEvent;
        let loadingPlanCard;
        this.legacyEnv = Component.env;
        this.orm = useService("orm")
        this.actionService = useService("action")
        console.log('Dashboard:',session.name)
        this.state = useState({
            title: {
                name: _t('Minutes Of Meeting'),
            },
            username: {
                value: '',
                status: session.name
            },
            open_mom: {
                value: 0
            }
        })

        onWillStart(async ()=>{
            await this._openMom()
                .then(data => {
                    this.state.open_mom.value = data.value
                })

        })
        onMounted(()=> {

        })
        onWillUnmount(function(){

        })
        this._openMom = this._openMom.bind(this);

    }
    async _openMom(){
//        let dateFormat = session.user_context.lang == 'fa_IR' ? "jYYYY/jMM/jDD" : "YYYY-MM-DD"
        const moms = await this.orm.searchRead("sd_mom.moms", [['active', '=', 'True']],['name',])
        console.log('moms:', moms)
//        this.state.spgr.status = moment(spgr[0].spgr_date).format(dateFormat);
//        this.state.spgr.value = spgr[0].spgr;
        let results = {'value': moms.length, 'status': 'open'}
        return results
    }
}

SdMomDataDashboard.template = "sd_mom_data_dashboard_template"
SdMomDataDashboard.components = { SdMomDataCards }
//DataDashboard.components = { DataCards, DataPlans }
registry.category("actions").add("sd_mom_data_dashboard_tag", SdMomDataDashboard)
