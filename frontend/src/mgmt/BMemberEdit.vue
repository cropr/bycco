<template>
<v-container class="elevation-2">
  <v-row>
    <v-col cols=12 sm=8>
        <h1>Edit board member: {{ member.first_name }} {{ member.last_name }} </h1>
    </v-col>
    <v-col col=12 sm=4>
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
        <span>Save BMember</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="remove()" 
              slot="activator">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete BMember</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="First name" v-model="first_name" />
      <v-text-field label="Last name" v-model="last_name" />
      <v-checkbox label="Account enabled" v-model="enabled" />
      <v-text-field label="Priority" v-model="priority" />
      <v-select v-model="membertype" :items="btypes" />
    </v-col>
    <v-col cols=12 sm=6>
      <v-text-field label="E-mail" v-model="email" />
      <v-checkbox label="Email publicly visible" v-model="showemail" />
      <v-text-field label="Mobile" v-model="mobile" />
      <v-checkbox label="Mobile publicly visible" v-model="showmobile" />
    </v-col>
  </v-row>
  <h4>Roles</h4>
  <v-row>
    <v-col cols=12 sm=6>
      <v-select v-model="role1" :items="roles" />
      <v-select v-model="role2" :items="roles" />
      <v-select v-model="role3" :items="roles" />
      <v-select v-model="role3" :items="roles" />
    </v-col>
    <v-col cols=12 sm=6>
      <h4>Picture</h4>
      <file-pond ref="pond" @addfile="handleFile" className="dropbox" /> 

    </v-col>
  </v-row>
</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"
import { boardmembertype } from '@/util/cms'

export default {

  name: "PageEdit",

  computed: {
    ...mapState(['token', 'api']),
  },

  data () {return {
    btypes: boardmembertype,
    first_name: '',
    last_name: '',
    enabled: true,
    email: '',
    mobile: '',
    member: {},
    membertype: 'board',
    picture: '',
    picturename: '',
    priority: 10,
    showemail: true,
    showmobile: true,
    roles: [ '' ],
    role1: '',
    role2: '',
    role3: '',
    role4: '',
  }},

  methods: {

    back () {
      this.$router.back();
    },

    fetchMember() {
      let self=this;
      this.api.get_board_member({
        id: this.$route.params.id
      }).then(
        function(rc) {
          self.readBMember(rc.obj.member)
        },
        function(rc){
          console.error('failed get bmember', rc)
          // TODO snackbar
        }
      )
    },

    fetchRoles() {
      let self=this;
      this.api.get_board_roles().then(
        function(rc) {
          self.readBRoles(rc.obj.roles)
        },
        function(rc){
          console.error('failed get bmember', rc)
          // TODO snackbar
        }
      )
    },

    handleFile(err, file){
      let self=this;
      const reader = new FileReader();
      console.log('file dropped', file);
      this.picturename = file.filename;
      reader.onload = function() {
        self.picture = reader.result.split(',')[1];
      };
      reader.readAsDataURL(file.file);
    },

    readBMember (member) {
      this.member = member;
      this.first_name = member.first_name + '';
      this.last_name = member.last_name + '';
      this.active = !!member.active;
      this.email = member.email + '';
      this.mobile = member.mobile + '';
      this.priority = member.priority + 0;
      this.membertype = member.membertype + '';
      this.showemail = !!member.showemail;
      this.showmobile = !!member.showmobile;
      if (member.boardroles.length > 0) this.role1 = member.boardroles[0];
      if (member.boardroles.length > 1) this.role2 = member.boardroles[1];
      if (member.boardroles.length > 2) this.role3 = member.boardroles[2];
      if (member.boardroles.length > 3) this.role4 = member.boardroles[3];
    },

    readBRoles(roles) {
      let self=this;
      this.roles = ['']
      roles.forEach(function(r){
        self.roles.push(r.name)
      })
    },

    remove () {
      let self=this;
      if (window.confirm('Are you sure to delete ' + this.fullname)) {
        this.api.delete_board_member({
          id: this.role.id
        }).then(
          function(){
            self.$router.push('/mgmt/bmember/list')
            self.$root.$emit('snackbar', {text: 'Boardmember deleted'})
          }, 
          function(rc){
            console.error('failed to delete', rc);
            // TODO snackbar
          })
      }

    },

    save () {
      let self=this, boardroles=[];
      if (this.role1) boardroles.push(this.role1)
      if (this.role2) boardroles.push(this.role2)
      if (this.role3) boardroles.push(this.role3)
      if (this.role4) boardroles.push(this.role4)
      this.api.update_board_member(
        {id: this.member.id}, 
        {
          requestBody: {
            boardroles: boardroles,
            first_name: this.first_name,
            last_name: this.last_name,
            enabled: this.enabled,
            email: this.email,
            membertype: this.membertype,
            mobile: this.mobile,
            picture: this.picture,
            picturename: this.picturename,
            priority: this.priority,
            showemail:  this.showemail,
            showmobile: this.showmobile
          },
        securities: bearertoken(this.token),
      }).then(
        function(){
          self.$router.push('/mgmt/bmember/list')
          self.$root.$emit('snackbar', {text: 'Boardmember saved'})
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
    if (this.api) {
      this.fetchMember();
      this.fetchRoles();
    }
  },
  
  watch: {
    api: function() {
      this.fetchMember();
      this.fetchRoles();
    }
  },

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
.dropbox {
  width: 100%;
  height: 100px;
}
</style>