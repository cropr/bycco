<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row wrap>
    <v-flex>
        <h1>New Participant </h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="save()" slot="activator">
          <v-icon>save</v-icon>
        </v-btn>
        <span>Save changes</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoPhoto()" slot="activator">
          <v-icon>face</v-icon>
        </v-btn>
        <span>Edit photo</span>
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
      <v-text-field label="ID FIDE" v-model="p.idfide" /> 
      <v-text-field label="ID BEL" v-model="p.idbel" /> 
      <v-text-field label="Rating FIDE" v-model="p.ratingfide" />
      <v-text-field label="Rating Bel" v-model="p.ratingbel" />
      <v-text-field label="Rating used" v-model="p.rating" />
    </v-flex>
    <v-flex sm6 xs12>
      <v-select label="Locale" v-model="p.locale" :items="locales"/>
      <v-select label="Category" v-model="p.category" :items="categories"/>
      <v-select label="Gender" v-model="p.gender" :items="genders" />
      <v-text-field label="Nationality FIDE" v-model="p.nationalityfide" />
      <v-text-field label="Club number" v-model="p.idclub" /> 
      <v-text-field label="Email address" v-model="p.emailplayer" />
      <v-text-field label="Mobile number" v-model="p.mobileplayer" />
      <v-select label="Meals" v-model="p.meals" :items="meals" />
      <v-textarea label="Remarks" v-model="p.remarks" />
    </v-flex>
  </v-layout>

</v-container>
</template>

<script>

import api from '../util/api'
import DateFormatted from "./DateFormatted";

export default {
  name: "MgmtPartAdd",

  components: {
    DateFormatted,
  },

  data () {return {
    participant: {},
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
      api('addAttendee', {
        attendee: this.p,
      }).then(
        function(data){
          console.log('id received', data.id)
          this.$emit('update', {
            section: 'edit', 
            params:{id: data.id}, 
            reload: true,
            text: 'Attendee saved.'})
          console.log('data', data)
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );
    },
  },


}
</script>

<style scoped>

</style>