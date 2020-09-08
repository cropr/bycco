<template>
<v-container class="elevation-2">
  <v-row>
    <v-col cols=12 sm=6>
        <h1>Edit board role: {{role.name}} </h1>
    </v-col>
    <v-col col=12 sm=6>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="back()" 
              slot="activator">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="save()" 
              slot="activator">
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
        </template>
        <span>Save BRole</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="remove()" 
              slot="activator">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete BRole</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="name" v-model="name" />
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="nl" v-model="i18n.nl" />
      <v-text-field label="fr" v-model="i18n.fr" />
    </v-col>
    <v-col cols=12 sm=6>
      <v-text-field label="de" v-model="i18n.de" />
      <v-text-field label="en" v-model="i18n.en" />
    </v-col>
  </v-row>
</v-container>
</template>

<script>

import { mapState } from 'vuex'

export default {

  name: "BRoleEdit",

  computed: {
    ...mapState(['token', 'api'])
  },

  data () {return {
    name: '',
    i18n: {
      nl: '',
      fr: '',
      de: '',
      en: ''
    },
    role: {},
  }},

  methods: {

    back () {
      this.$router.back();
    },

    fetchRole() {
      let self=this;
      this.api.get_board_role({
        id: this.$route.params.id
      }).then(
        function(rc) {
          self.readBRole(rc.obj.role)
        },
        function(rc){
          console.error('failed get brole', rc)
          // TODO snackbar
        }
      )
    },

    readBRole (role) {
      this.role = role;
      this.name = role.name + '';
      this.i18n = {
        nl: role.i18n.nl || '',
        fr: role.i18n.fr || '',
        de: role.i18n.de || '',
        en: role.i18n.en || '',
      }
    },

    remove () {
      let self=this;
      if (window.confirm('Are you sure to delete ' + this.name)) {
        this.api.delete_board_role({
          id: this.role.id
        }).then(
          function(){
            self.$router.push('/mgmt/brole/list')
            self.$root.$emit('snackbar', {text: 'Boardrole deleted'})
          }, 
          function(rc){
            console.error('failed to delete', rc);
            // TODO snackbar
          })
      }
    },

    save () {
      let self = this;
      this.api.update_board_role({id: this.role.id}, {
        requestBody: {
          name: this.name,
          i18n: this.i18n,
        }
      }).then(
        function(){
          self.$router.push('/mgmt/brole/list')
          self.$root.$emit('snackbar', {text: 'Boardrole saved'})
        },
        function(data){
          console.error('failed to save', data);
          // TODO snackbar
        }
      );
    },

  },

  mounted () {
    // make sure the api is loaded
    if (this.api) this.fetchRole()
  },
  
  watch: {
    api: function() {
      this.fetchRole()
    }
  },

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>