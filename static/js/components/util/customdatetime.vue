<template>
  <span>
    <b-form-group
      :id="field + '-datetimegroup-' + $parent.id"
      v-show="$parent.show"
      label-size="sm"
      label-align-sm="right"
      label-cols-sm="4"
      :label-for="field"
    >
      <template 
        slot="label"
      >
        {{ label }}
        <sup 
          v-if="desc"
          class="text-primary" 
          v-b-tooltip=tooltipConfig 
          :title="desc"
        >
          ?
        </sup>
      </template>
      <VueCtkDateTimePicker 
        v-model="value"
        label=""
        :format="datetimeFormat"
        :formatted="datetimeFormat"
        :id="field + '-datetimefield-' + $parent.id" 
        :error="hasErrors"
        :no-header="true"
        :no-button-now="true"
        :no-button="true"
        @input="update($event)"
      />
      <span 
        class="errors text-danger" 
        v-for="error in errors" 
        :key="error"
      >
        {{ error }}
      </span>    
    </b-form-group>
    <span 
      class="mr-4" 
      v-show="!$parent.show"
    >
      {{ label }}: <strong>{{ value || '...' }}</strong>
    </span>
  </span>
</template>
<script>
  import _ from 'lodash';
  import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';

  import { datetimeFormat, tooltipConfig } from '../../utils';
  
  export default {
    props: [
      'value',
      'label', 
      'field', 
      'errors', 
      'type', 
      'desc',
    ],
    components: {
      VueCtkDateTimePicker
    },
    data: function() {
      return {
        tooltipConfig: tooltipConfig,
        datetimeFormat: datetimeFormat
      }
    },
    computed: {
      hasErrors: function() {
        return !_.isEmpty(this.errors);
      }
    },
    methods: {
      update: function(value) {
        this.$emit('input', value);
      }
    }
  };
</script>
<style scoped>
  @import '~vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
</style>
<style>
  /* 
   * Override the default ctk datetime picker styles to look like other
   * bootstrap 4 input fields, using scoped style does not work 
   */
  .date-time-picker .field .field-input {
    color: inherit !important;
    font-size: 0.875rem !important;
    padding-top: 0rem !important;
    font-family: inherit !important;
    height: 38px !important;
    min-height: 38px !important;
  }
  .date-time-picker span.errors {
    font-size: 90%;
  }
</style>
