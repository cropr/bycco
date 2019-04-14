<template>
<v-flex xs12 lg6 xl4>
  <v-card class="ma-2" >
    <div class="person-container">
      <div class="person-left">
        <img src="{{ photourl }}" class="person-photo"></img>
      </div>
      <div class="person-right">
        <v-card-title  class="green lighten-2">{{name}}</v-card-title>
        <v-card-text>
          <div>tel: {{mobile}}</div>
          <div>email: {{email}}</div>
        </v-card-text>
        <v-card-actions>
          <v-btn flat icon class="green" href="tel:{{mobile}}">
            <v-icon color="white">phone</v-icon>
          </v-btn>
          <v-btn flat icon class="green" href="sms:{{mobile}}">
            <v-icon  color="white">textsms</v-icon>
          </v-btn>
          <v-btn flat icon  class="green" href="mailto:{{email}}">
            <v-icon color="white">email</v-icon>
          </v-btn>
        </v-card-actions>
      </div>
    </div>
  </v-card>
</v-flex>
</template>

<script>

import api from '../util/api';

export default {
  props: ['fullname', 'mobile', 'email', 'photourl'],

}
</script>

<style>
</style>
