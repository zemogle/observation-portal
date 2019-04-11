import Vue from 'vue';
import $ from 'jquery';
import './request_row';
import App from './request_detail.vue';

import {cancelRequestGroup} from './requestgroup_header';

$('#cancelrg').click(function(){
  cancelRequestGroup($(this).data('id'));
});

new Vue({
  el: '#app',
  render: function(h){
    return h(App);
  }
});
