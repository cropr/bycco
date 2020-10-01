<template>
<v-container>
  <h1>Management enrollments</h1>
  <v-data-table :items="filteredEnrollments" class="elevation-1" 
      :headers="headers" :footer-props="footerprops"  :items-per-page="-1">
    <template v-slot:top>
      <v-card color="grey lighten-4">
        <v-card-title>
          <v-row class="px-2">
            <v-checkbox v-model="isNotConfirmed" label="Not confirmed" hide-details 
              class="check"/>
            <v-spacer />
            <v-tooltip bottom >
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" @click="addEnrollment" fab outlined 
                      color="deep-purple">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              <span>Add enrollment</span>
            </v-tooltip>
            <v-tooltip bottom >
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" @click="getEnrollments" fab outlined 
                      color="deep-purple">
                  <v-icon>mdi-reload</v-icon>
                </v-btn>
              </template>
              <span>Reload</span>
            </v-tooltip>
            <v-tooltip bottom >
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" @click="csvDownload" fab outlined 
                      color="deep-purple">
                  <v-icon>cloud_download</v-icon>
                </v-btn>
              </template>
              <span>CSV Download</span>
            </v-tooltip>
          </v-row>
        </v-card-title>
      </v-card>
    </template>    
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editEnrollment(item)" >
        edit
      </v-icon>
    </template>          
  </v-data-table>

</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"

export default {

  name: "EnrollmentList",

  computed: {
    ...mapState(['token', 'api']),
    filteredEnrollments() {
      return this.enrollments.filter(
        i => this.isNotConfirmed ? !i.confirmed : 1)
    },
  },

  data () {return {
    enrollments: [],
    footerprops: {
      "items-per-page-options": [15,60,150,-1],
    },
    headers :[
      {
        text: 'Number',
        align: 'left',
        sortable: true,
        value: 'subscriptionnumber'
      },
      {
        text: 'First name',
        align: 'left',
        sortable: true,
        value: 'first_name'
      },
      {
        text: 'Last name',
        align: 'left',
        sortable: true,
        value: 'last_name'
      },
      {
        text: 'Category',
        align: 'center',
        value: 'category'
      },
      {
        text: 'Actions', value: 'action', sortable: false
      }      
    ],    
    isNotConfirmed: false,
  }},

  methods: {

    addEnrollment() {
      // toDO
    },

    editEnrollment(p) {
      this.$router.push('/mgmt/enrollment/edit/' + p.id)
    },

    csvDownload() {
      let self=this;
      this.api.csv_subscriptions({},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          console.log('csv subscriptions', data.obj);
          let link = document.createElement("a");
          link.download = 'enrollments.csv';
          link.href = 'data:text/csv;base64,' + btoa(data.obj);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        },
        function(data) {
          console.error('error gettting csv', data);
          self.$root.$emit('snackbar', { 
            text: 'Failed to download csv file: ' + data.statusText,
            reason: (data.data ? data.data.message : null)
          })
        }
      );
    },

    getEnrollments() {
      let self=this;
      this.api.get_subscriptions({},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.enrollments = data.obj.subscriptions;
        },
        function(data){
          if (data.status == 401) {
            self.$router.push('/mgmt/login')
          }
          else {
            console.error('getting getPages', data);
            self.$root.$emit('snackbar', {text: 'Getting pages failed', reason: data})            
          }          
        }
      );
    },

    gotoAdd () {
      this.$router.push('/mgmt/enrollment/add')
    },

    gotoNamecard () {
      this.$router.push('/mgmt/enrollment/namecard')
    },

  },

  mounted () {
    this.getEnrollments();
  },


}
</script>
