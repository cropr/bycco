<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row wrap>
    <v-flex>
        <h1>Edit Participant: {{ fullname }} </h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="remove()" slot="activator">
          <v-icon>delete</v-icon>
        </v-btn>
        <span>Delete participant</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="save()" slot="activator">
          <v-icon>save</v-icon>
        </v-btn>
        <span>Save changes</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="sendConfirmationEmail()" slot="activator">
          <v-icon>email</v-icon>
        </v-btn>
        <span>Send confirmation email</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoPhoto()" slot="activator">
          <v-icon>face</v-icon>
        </v-btn>
        <span>Edit photo</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoInvoice()" slot="activator">
          <v-icon>euro_symbol</v-icon>
        </v-btn>
        <span>Invoice</span>
      </v-tooltip>
    </v-flex>
  </v-layout>
  <v-layout row wrap>
    <v-flex sm6 xs12>
      <v-text-field label="Last name" v-model="p.last_name" />
      <v-text-field label="First name" v-model="p.first_name" />
      <v-select label="Chess title" v-model="p.chesstitle"
                :items="['', 'GM', 'IM', 'FM', 'WGM', 'WIM', 'WFM', 'IA', 'FA']"
      />
      <v-menu :close-on-content-click="false" v-model="menu_birthdate"
        :nudge-right="40" lazy transition="scale-transition" offset-y
        full-width min-width="290px">
        <v-text-field slot="activator" v-model="p.birthdate"
          label="Birthdate" prepend-icon="event" readonly
        ></v-text-field>
        <v-date-picker v-model="p.birthdate" @input="menu_birthdate = false"
                       color="blue-grey" />
      </v-menu>
      <v-select label="Category" v-model="p.category" :items="categories"/>
      <v-select label="Gender" v-model="p.gender" :items="genders" />
      <p>ID club: {{p.idclub}}</p>
      <v-text-field label="ID Bel" v-model="p.idbel" />
      <v-text-field label="ID Fide" v-model="p.idfide" />
      <p>Nationality Bel: {{p.nationalitybel}}</p>
      <v-text-field label="Nationality FIDE" v-model="p.nationalityfide" />
      <v-text-field label="Rating FIDE" v-model="p.ratingfide" />
      <v-text-field label="Rating Bel" v-model="p.ratingbel" />
      <v-text-field label="Rating used" v-model="p.rating" />
      <v-select label="Confirmed" v-model="p.confirmed" :items="yesno" />
    </v-flex>
    <v-flex sm6 xs12>
      <v-text-field label="Email player" v-model="p.emailplayer" />
      <v-text-field label="Mobile player" v-model="p.mobileplayer" />
      <v-text-field label="Fullname parent" v-model="p.fullnameparent" />
      <v-text-field label="Mobile parent" v-model="p.mobileparent" />
      <v-text-field label="Email parent" v-model="p.emailparent" />
      <v-text-field label="Fullname local representative" v-model="p.fullnameattendant" />
      <v-text-field label="Mobile local representative" v-model="p.mobileattendant" />
      <v-select label="Meals" v-model="p.meals" :items="meals" />
      <v-select label="Locale" v-model="p.locale" :items="locales" />
      <v-text-field label="Payment amount" v-model="p.payamount" />
      <v-text-field label="Payment message" v-model="p.paymessage" />
      <p>Invoice created: <date-formatted :date="p.invoicecreated"/></p>
      <p>Invoice sent: <date-formatted :date="p.invoicesent" /></p>
      <v-text-field label="Custom1" v-model="p.custom1" />
      <v-textarea label="Remarks" v-model="p.remarks" />
    </v-flex>
  </v-layout>

</v-container>
</template>

<script>

import api from '../util/api'
import DateFormatted from "./DateFormatted";

export default {
  name: "MgmtPartEdit",

  components: {
    DateFormatted,
  },

  props: ['participant'],

  computed :  {
    fullname () {
      return this.p.first_name + ' ' + this.p.last_name;
    }
  },

  data () {return {
    categories: [
      {value: 'B8', text:'B8'},
      {value: 'G8', text:'G8'},
      {value: 'B10', text:'B10'},
      {value: 'G10', text:'G10'},
      {value: 'B12', text:'B12'},
      {value: 'G12', text:'G12'},
      {value: 'B14', text:'B14'},
      {value: 'G14', text:'G14'},
      {value: 'B16', text:'B16'},
      {value: 'G16', text:'G16'},
      {value: 'B18', text:'B18'},
      {value: 'G18', text:'G18'},
      {value: 'B20', text:'B20'},
      {value: 'G20', text:'G20'},
      {value: 'IMT', text:'IM tournament'},
      {value: 'ORG', text:'Organiser'},
      {value: 'ARB', text:'Arbiter'},
      {value: 'SPO', text:'Sponsor'},
      {value: 'EAT', text:'Resident with meals'},
    ],
    genders: [
      {value: 'M', text: 'Male'},
      {value:'F', text: 'Female'},
    ],
    locales: ['nl', 'fr', 'de', 'en'],
    meals: [
      {value: '', text:'No meals'},
      {value:'FB', text: 'Full Boarding'},
      {value:'HB', text: 'Half Boarding'},
      {value:'BO', text: 'Breakfast only'},
    ],
    menu_birthdate: false,
    p: {},
    snacktext: '',
    yesno: [
      {value:true, text: 'Yes'},
      {value:false ,text:'No'}
    ],
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list', params:{}})
    },

    gotoInvoice () {
      this.$emit('update', {section: 'invoice', params: this.participant})
    },

    gotoPhoto () {
      this.$emit('update', {section: 'photo', params: this.participant})
    },

    remove () {
      if (window.confirm('Are you sure to delete ' + this.fullname)) {
        api('deleteAttendee', {
          id: this.participant.id
        }).then(function(){
          this.$emit('update', {section: 'list', params:{}, reload: true,
            text: this.fullname + ' deleted.'})
        }.bind(this), function(data){
          console.error('failed to delete', data);
        })
      }
    },

    save () {
      api('updateAttendee', {
        id: this.participant.id,
        attendee: this.p,
      }).then(
        function(){
          this.$emit('update', {section: 'list', params:{}, reload: true,
            text: this.fullname + ' saved.'})
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );
    },

    sendConfirmationEmail () {
      api('resendConfirmation', {
        id: this.participant.id,
      }).then(
        function(){
          this.$emit('update', {section: 'edit', params:this.participant,
            reload: false, text: this.fullname + ' confirmation sent.'})
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );

    },
  },

  mounted () {
    console.log('received participant', this.participant.id)
    api('getAttendee', {
      id: this.participant.id
    }).then(
     function(data) {
        console.log('participant data', data);
        this.p = data.attendee;
      }.bind(this)
    )
  }

}
</script>

<style scoped>

</style>