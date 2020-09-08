<template>

<v-container class="elevation-2">
  <h1>Management of board roles</h1>
  <v-data-table :headers="headers" :items="roles" :footer-props="footerprops"
       sort-by="name" :items-per-page="30">
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>
          Roles
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="addRole()" fab outlined color="deep-purple">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <span>Add Role</span>
         </v-tooltip>
      </v-toolbar>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editRole(item)">
        mdi-pencil
      </v-icon>
    </template>
    <template v-slot:no-data>
      No roles yet.
    </template>            
  </v-data-table>
</v-container>

</template>

<script>

import { mapState } from 'vuex'

export default {

  name: 'BRoleList',

  data () {return {
    headers: [
      {
        text: "Name", value: 'name'
      },
      {
        text: 'Actions', value: 'action', sortable: false
      }
    ],
    footerprops: {
      "items-per-page-options": [15,30,50,-1],
    },
    roles: [],
  }},

  computed: {
    ...mapState(['token', 'api'])
  },


  methods: {

    addRole () {
      this.$router.push('/mgmt/brole/add')
    },
    
    editRole (item) {
      this.$router.push('/mgmt/brole/edit/'  + item.id)
    },
    
    fetchRoles () {
      let self = this;
      this.api.get_board_roles().then(
        function(rc) {
          self.roles = rc.obj.roles;
        },
        function(rc){
          console.log('failed', rc)
          if (rc.status == 401) {
            self.$router.push('/mgmt/login')
          }
          else {
            // TODO snackbar
            console.error('get board roles', rc);
          }
        }
      );
    }

  },

  mounted () {
    // make sure the api is loaded
    if (this.api) this.fetchRoles()
  },
  
  watch: {
    api: function() {
      this.fetchRoles()
    }
  },

}
</script>
