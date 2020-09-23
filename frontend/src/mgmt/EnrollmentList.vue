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
                <v-btn v-on="on" @click="addEnrollment()" fab outlined 
                      color="deep-purple">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              <span>Add Enrollment</span>
            </v-tooltip>
            <v-tooltip bottom >
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" @click="csvAttendees()" fab outlined 
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

    editEnrollment(p) {
      this.$router.push('/mgmt/enrollment/edit/' + p.id)
    },

    csvAttendees () {
      // api('getAttendees', {
      //   cat: this.catsearch,
      //   ss: this.ss.length ? this.ss : null,
      //   format: 'csv'
      // }).then(
      //   function(data) {
      //     console.log('csv attendees', data);
      //     let link = document.createElement("a");
      //     link.download = 'subscription.csv';
      //     link.href = 'data:text/csv;base64,' + btoa(data.attendees);
      //     document.body.appendChild(link);
      //     link.click();
      //     document.body.removeChild(link);
      //   }.bind(this)
      // );
    },


    getEnrollments () {
      let self=this;
      this.api.get_subscriptions({},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.enrollments = data.obj.subscriptions;
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
