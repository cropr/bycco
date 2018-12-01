<template>
<v-layout row class="mt-2 mb-1">
  <v-flex xs4>
    <span v-text="ix+1"></span>&nbsp;&nbsp;
    <input type="checkbox" @change="changePresence" v-model="attendee.present">&nbsp;&nbsp;
    <span xs4 v-text="fullname"></span>
  </v-flex>
  <v-flex xs3 v-text="formatPresence"></v-flex>
</v-layout>
</template>

<script>
import _ from 'lodash';
import moment from 'moment';
import api from '../api/api';

export default {
  props: ['attendee', 'ix'],
  computed: {
    fullname () {
      return this.attendee.first_name + ' ' + this.attendee.last_name
    },
    formatPresence () {
      if (this.attendee.present) {
        return moment(this.attendee.present).format('DD/MM/YY HH:mm')
      }
      return 'Not checked in'
    }
  },
  methods: {
    changePresence () {
      var self=this;
      if (this.attendee.present) {
        this.attendee.present = (new Date()).toISOString();
      }
      api('updateAttendee', {
        id: this.attendee.id,
        attendee: this.attendee
      }).then(
        function(data){
          console.log('emitting sort');
          self.$emit('doUpdate')
        },
        function(data) {
          console.error('updating went wrong', data)
        }
      )
    }
  }
}
</script>

<style>
</style>
