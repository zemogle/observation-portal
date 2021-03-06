import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import $ from 'jquery';
import './request_row';
import App from './request_detail.vue';

import { cancelRequestGroup } from './requestgroup_header';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import '../css/main.css';

Vue.use(BootstrapVue)

$('#cancelrg').click(function(){
  cancelRequestGroup($(this).data('id'));
});

new Vue({
  el: '#app',
  render: function(h){
    return h(App);
  }
});
