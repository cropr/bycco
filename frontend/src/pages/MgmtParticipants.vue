<template>
<v-container fluid>

  <mgmt-part-list @update="update($event)" v-show="section == 'list'" :ts="ts" />
  <mgmt-part-edit @update="update($event)" v-if="section == 'edit'"
                  :participant="params" :ts="ts"/>
  <mgmt-part-invoice @update="update($event)" v-if="section == 'invoice'"
                  :participant="params"  :ts="ts" />
  <v-snackbar v-model="snackbar" bottom>
    {{ snacktext }}
    <v-btn flat @click="snackbar = false">
      <v-icon>cancel</v-icon>
    </v-btn>
  </v-snackbar>
</v-container>
</template>

<script>

import MgmtPartList from '../components/MgmtPartList'
import MgmtPartEdit from '../components/MgmtPartEdit'
import MgmtPartInvoice from '../components/MgmtPartInvoice'

export default {
  name: "MgmtParticipants",

  data () {return {
    section: 'list',
    snackbar: false,
    snacktext: '',
    params: {},
    ts: new Date(),
  }},

  components: {
    MgmtPartInvoice,
    MgmtPartList,
    MgmtPartEdit,
  },

  methods: {
    update (ev) {
      console.log('update', ev);
      this.section = ev.section;
      this.params = ev.params;
      if (ev.reload) {
        this.ts = new Date();
      }
      if (ev.text) {
        this.snacktext = ev.text;
        this.snackbar = true;
      }

    }
  }
}
</script>

<style scoped>

</style>