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
            })

        onWillStart(async ()=>{

        })
        onMounted(()=> {

        })
        onWillUnmount(function(){

        })
    }
}

SdMomDataDashboard.template = "sd_mom_data_dashboard_template"
SdMomDataDashboard.components = { SdMomDataCards }
//DataDashboard.components = { DataCards, DataPlans }
registry.category("actions").add("sd_mom_data_dashboard_tag", SdMomDataDashboard)
