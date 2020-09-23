<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row wrap>
    <v-flex>
        <h1>Edit Participant: {{ fullname }} </h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="blue-grey" @click="back()" 
            slot="activator">
            <v-icon>arrow_back</v-icon>
          </v-btn>
        </template>
        <span>Go back</span>        
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="blue-grey" 
            @click="deleteEnrollment()" slot="activator">
            <v-icon>delete</v-icon>
          </v-btn>
        </template>
        <span>Delete participant</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="blue-grey" 
            @click="saveEnrollment()" slot="activator">
            <v-icon>save</v-icon>
          </v-btn>
        </template>
        <span>Save changes</span>
      </v-tooltip>
    </v-flex>
  </v-layout>
  <v-layout row wrap>
    <v-flex sm6 xs12>
      <p>Enrollment number: {{p.subscriptionnumber}}</p>
      <v-text-field label="Last name" v-model="p.last_name" />
      <v-text-field label="First name" v-model="p.first_name" />
      <v-select label="Chess title" v-model="p.chesstitle"
                :items="['', 'GM', 'IM', 'FM', 'WGM', 'WIM', 'WFM', 'IA', 'FA']"
      />
      <v-menu :close-on-content-click="false" v-model="menu_birthdate"
        :nudge-right="40" transition="scale-transition" offset-y min-width="290px">
        <template v-slot:activator="{ on }">
          <v-text-field v-on="on" slot="activator" v-model="p.birthdate"
            label="Birthdate" prepend-icon="event" readonly />
        </template>
        <v-date-picker v-model="p.birthdate" @input="menu_birthdate = false"
                       color="blue-grey" />
      </v-menu>
      <v-select label="Category" v-model="p.category" :items="categories"/>
      <v-select label="Gender" v-model="p.gender" :items="genders" />
      <p>ID club: {{p.idclub}}</p>
      <v-text-field label="ID Bel" v-model="p.idbel" />
      <v-text-field label="ID Fide" v-model="p.idfide" />
      <v-text-field label="Nationality" v-model="p.nationality" />
      <v-text-field label="Rating FIDE" v-model.number="p.ratingfide" type="number" />
      <v-text-field label="Rating Bel" v-model.number="p.ratingbel" type="number" />
      <p>Enrollment confirmed: {{p.confirmed ? "Yes": 'No'}}</p>
    </v-flex>
    <v-flex sm6 xs12>
      <p>Invoice number: {{p.invoicenumber}}</p>
      <v-text-field label="Email player" v-model="p.emailplayer" />
      <v-text-field label="Mobile player" v-model="p.mobileplayer" />
      <v-text-field label="Fullname parent" v-model="p.fullnameparent" />
      <v-text-field label="Mobile parent" v-model="p.mobileparent" />
      <v-text-field label="Email parent" v-model="p.emailparent" />
      <v-text-field label="Fullname local representative" v-model="p.fullnameattendant" />
      <v-text-field label="Mobile local representative" v-model="p.mobileattendant" />
      <v-select label="Locale" v-model="p.locale" :items="locales" />
      <v-text-field label="Payment message" v-model="p.paymessage" />
      <v-text-field label="Custom1" v-model="p.custom1" />
      <v-textarea label="Remarks" v-model="p.remarks" />
    </v-flex>
  </v-layout>

</v-container>
</template>

<script>
import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"

export default {
  name: "EnrollmentEdit",

  computed :  {
    ...mapState(['token', 'api']),
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
    id: this.$route.params.id,
    p: {},
    snacktext: '',
    yesno: [
      {value:true, text: 'Yes'},
      {value:false ,text:'No'}
    ],
  }},

  methods: {

    back () {
      this.$router.back();
    },

    deleteEnrollment () {
      let self=this;
      if (window.confirm('Are you sure to delete ' + this.fullname)) {
        console.log('deleting')
        this.api.delete_subscription({ id: this.id }, {
          securities: bearertoken(this.token),
        }).then(
          function(){
            self.$root.$emit('snackbar', {text: self.fullname + ' deleted.'})
            self.$router.push('/mgmt/enrollment/list')
          }, 
          function(data){
            self.$root.$emit('snackbar', { 
              text: 'Failed to delete: ' + data.statusText,
              reason: (data.data ? data.data.message : null)
            })
          }
        );
      }
      else {
        console.log('not deleting')
      }
    },

    saveEnrollment () {
      let self=this;
      this.api.update_subscription({ id: this.p.id },{
        requestBody: this.p,
        securities: bearertoken(this.token),
      } ).then(
        function(){
          self.$root.$emit('snackbar', { text: self.fullname + ' saved.'})
        },
        function(data){
          self.$root.$emit('snackbar', { text: 'Failed to save: ' + data.statusText, 
            reason: (data.data ? data.data.message : null) })
        }
      );
    },

    confirmationEnrollment () {
      let self=this;
      this.api.confirm_subscription({id: this.id,},{
        securities: bearertoken(this.token),
      }).then(
        function(){
          self.$root.$emit('snackbar', {text: 'Confirmation mail for ' + self.fullname 
            + ' sent.'})
        },
        function(data){
          self.$root.$emit('snackbar', { 
            text: 'Failed to send confirmation: ' + data.statusText,
            reason: (data.data ? data.data.message : null)
          })
        }
      );

    },
  },

  mounted () {
    let self=this;
    this.api.get_subscription({ id: this.$route.params.id},
        {securities: bearertoken(this.token)},
    ).then(
      function(data) {
        self.p = data.obj;
      },
      function(data) {
          self.$root.$emit('snackbar', { 
            text: 'Failed to get participant: ' + data.statusText, 
            reason: (data.data ? data.data.message : null) 
          })
      }
    )
  }

}
</script>

<style scoped>

</style>