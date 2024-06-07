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
                name: session.name,
                status: moment().locale('fa').format('jYYYY/jMM/jDD'),
            },
            ongoing_mom: {
                value: 0,
            },
            all_mom: {
                value: 0,
            },
        })

        onWillStart(async ()=>{
            await this._getUpdateMom()
                .then(data => {
                    console.log('_ongoingMom', data)
                    this.state.all_mom.value = data.all.value
                    this.state.ongoing_mom.value = data.ongoing.value
                })

        })
        onMounted(()=> {

        })
        onWillUnmount(function(){

        })
        this._getUpdateMom = this._getUpdateMom.bind(this);
        this.viewMoms = this.viewMoms.bind(this);

    }
    async _getUpdateMom(){
//        let dateFormat = session.user_context.lang == 'fa_IR' ? "jYYYY/jMM/jDD" : "YYYY-MM-DD"
//        const moms = await this.orm.searchRead("sd_mom.moms", [['state', 'in', ['ongoing', 'stopped']]],['name',])
        const moms = await this.orm.searchRead("sd_mom.moms", [],['state',])
//        console.log('_getUpdateMom', moms)
        let ongoing = moms.filter(r => ['ongoing', 'stopped'].includes(r.state))

        let results = {'all':{'value': moms.length,}, 'ongoing':{'value': ongoing.length,}, }
        return results
    }
        viewMoms(mom_state='all'){
//        console.log('viewMoms', mom_state )
        let domain = []
        let reportName = 'All MOMs'
        if(mom_state == 'ongoing'){
            domain = [['state',  'in', ['ongoing', 'stopped']]]
            reportName = 'Ongoing MOMs'
        }

        this.actionService.doAction({
            name: reportName,
            res_model: "sd_mom.moms",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
//            context: {'search_default_meter_no_group': 1},
            target: "current",
        });
    }




}

SdMomDataDashboard.template = "sd_mom_data_dashboard_template"
SdMomDataDashboard.components = { SdMomDataCards }
//DataDashboard.components = { DataCards, DataPlans }
registry.category("actions").add("sd_mom_data_dashboard_tag", SdMomDataDashboard)
