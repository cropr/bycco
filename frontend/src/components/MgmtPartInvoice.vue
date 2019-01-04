<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row wrap>
    <v-flex>
        <h1>Invoice Participant: {{ fullname }} </h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoEdit()" slot="activator">
          <v-icon>edit</v-icon>
        </v-btn>
        <span>Edit participant</span>
      </v-tooltip>
    </v-flex>
  </v-layout>
  <div v-show="noInvoiceYet">
    <h3>No invoice yet</h3>
    <p>No invoice was found for this partic[pant</p>
    <v-btn @click="createInvoice()" primary>Create invoice</v-btn>
  </div>
  <div v-show="!noInvoiceYet">
    <h3>Invoice details</h3>
    <div class="mt-2">Participant: {{invdet.first_name}} {{invdet.last_name}}</div>
    <div class="mt-2">Responsible: {{invdet.fullnameresponsible}}</div>
    <div class="mt-2">Locale: {{invdet.locale}}</div>
    <div class="mt-2">E-mail: {{invdet.emailresponsible}}</div>
    <div class="mt-2">Amount VAT included: {{invdet.pricewithvat}} &euro;</div>
    <div class="mt-2">Amount VAT excluded: {{invdet.pricewithoutvat}} &euro;</div>
    <div class="mt-2">Amount VAT : {{invdet.vat}} &euro;</div>
    <div class="mt-2">Invoice number: {{invdet.invoicenumber}}</div>
    <div class="mt-2">Invoice created: <date-formatted :date="invdet.creationdate"/></div>
    <div class="mt-2">Invoice send on: <date-formatted :date="invdet.sentdate"/></div>
    <v-btn primary @click="showPdf">
      Show PDF
    </v-btn>
    <v-btn @click="createInvoice()" primary>Recreate invoice</v-btn>
    <v-btn @click="sendInvoice()" primary>Send invoice</v-btn>
  </div>
</v-container>
</template>

<script>

import api from '../util/api'
import DateFormatted from "./DateFormatted";

export default {
  name: "MgmtPartInvoice",

  components: {
    DateFormatted,
  },

  props: ['participant', 'ts'],

  computed :  {
    dataUrlPdf () {
      return 'data:application/pdf;base64,' + this.invdet.pdf;
    },
    fullname () {
      return this.participant.first_name + ' ' + this.participant.last_name;
    },


  },

  data () {return {
    noInvoiceYet: true,
    invdet: {},
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list', params:{}})
    },

    createInvoice () {
      api('createInvoice', {
        id_participant: this.participant.id
      }).then(
        function(data) {
          this.invdet = data.invoice;
          this.noInvoiceYet = false;
        }.bind(this),
        function(data) {
          console.error('Something went wrong', data)
        }.bind(this)
      );
    },

    getInvoice () {
      api('getInvoice', {
        id_participant: this.participant.id
      }).then(
        function(data) {
          this.invdet = data.invoice;
          this.noInvoiceYet = false;
        }.bind(this),
        function(data) {
          this.noInvoiceYet = true;
          if (data.status != 404) {
            console.error('Something went wrong', data)
          }
        }.bind(this)
      )
    },

    gotoEdit () {
      this.$emit('update', {section: 'edit', params: this.participant})
    },

    sendInvoice () {
      api('sendInvoice', {
        id_participant: this.participant.id
      }).then(
        function() {
          this.$emit('update', {section: 'invoice', params: this.participant,
            text: 'Invoice sent', reload: true})
        }.bind(this),
        function(data) {
          console.error('Something went wrong', data)
        }.bind(this)
      );
    },

    showPdf () {
      let win = window.open('',"_blank");
      win.document.write('<iframe src="' + this.dataUrlPdf +
          '" frameborder="0" style="border:0; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%;" allowfullscreen></iframe>');
    }


  },

  mounted () {
    this.getInvoice()
  },


  watch: {
    ts: function(){
      this.getInvoice();
    }
  }
}
</script>

<style scoped>
a.downloadlink {
  text-decoration: none;
  color: black;
}

</style>