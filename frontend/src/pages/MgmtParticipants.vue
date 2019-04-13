<template>
  <v-container fluid>

    <mgmt-part-list @update="update($event)" v-show="section == 'list'" 
      :selection="selection"  :ts="ts" />
    <mgmt-part-edit @update="update($event)" v-if="section == 'edit'"
      :participant="participant" :ts="ts"/>
    <mgmt-part-add @update="update($event)" v-if="section == 'add'"/>
    <mgmt-part-invoice @update="update($event)" v-if="section == 'invoice'"
      :participant="participant"  :ts="ts" />
    <mgmt-part-photo @update="update($event)" v-if="section == 'photo'"
      :participant="participant"  :ts="ts" />
    <mgmt-part-badge @update="update($event)" v-if="section == 'badge'"
      :selection="selection" />
    <mgmt-part-namecard @update="update($event)" v-if="section == 'namecard'"
      :selection="selection" :ts="ts" />
    <mgmt-part-presence @update="update($event)" v-if="section == 'presence'"/>
    <v-snackbar v-model="snackbar" :timeout="timeout" bottom>
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
import MgmtPartAdd from '../components/MgmtPartAdd'
import MgmtPartInvoice from '../components/MgmtPartInvoice'
import MgmtPartPhoto from '../components/MgmtPartPhoto'
import MgmtPartBadge from '../components/MgmtPartBadge'
import MgmtPartNamecard from '../components/MgmtPartNamecard'
import MgmtPartPresence from '../components/MgmtPartPresence'

export default {
  name: "MgmtParticipants",

  data () {return {
    section: 'list',
    selection: [],
    snackbar: false,
    snacktext: '',
    participant: {},
    ts: new Date(),
    timeout: 4000,
  }},

  components: {
    MgmtPartInvoice,
    MgmtPartList,
    MgmtPartEdit,
    MgmtPartAdd,
    MgmtPartPhoto,
    MgmtPartBadge,
    MgmtPartNamecard,
    MgmtPartPresence,
  },

  methods: {
    update (e) {
      console.log('update', e);
      if (e.section)
        this.section = e.section;
      if (e.participant)
        this.participant = e.participant;
      if (e.selection)
        this.selection = e.selection
      if (e.reload) 
        this.ts = new Date();
      if (e.text) {
        this.snacktext = e.text;
        this.snackbar = true;
      }
    }
  }
}
</script>

<style scoped>

</style>