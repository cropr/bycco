<template>
<v-container fluid grid-list-md class="elevation-1">
 
  <v-layout row wrap>
    <v-flex>
      <h1>Badges</h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="print()" slot="activator">
          <v-icon>print</v-icon>
        </v-btn>
        <span>Print selection</span>
      </v-tooltip>      
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="clear()" slot="activator">
          <v-icon>delete</v-icon>
        </v-btn>
        <span>Clear custom</span>
      </v-tooltip>
    </v-flex>
  </v-layout>
 
  <div>
    <h4>Make selection</h4>
    <v-layout row wrap>
        <v-flex md1 sm2 xs3 v-for="c in boys" :key="c">
          <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                      @change="recalc" />
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex md1 sm2 xs3 v-for="c in girls" :key="c">
          <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                      @change="recalc" />
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex md1 sm2 xs3 v-for="c in rest" :key="c">
          <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                      @change="recalc" />
        </v-flex>
      </v-layout>

  </div>


</v-container>
</template>

<script>

import api from '../util/api'


export default {

  name: "MgmtPartBadge",


  props: ['participant'],

  data () {return {
    selection: [],
    boys: ['B8', 'B10', 'B12', 'B14', 'B16', 'B18', 'B20'],
    catsSelected: {'custom'},
    girls:  ['G8', 'G10', 'G12', 'G14', 'G16', 'G18', 'G20'],
    rest: ['ORG', 'ARB', 'IMT', 'RES', 'SPO'],
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list', params:{}})
    },

    clear () {
        this.selection = []
    },

    print() {
        var ids=[];
        this.selection.forEach(p => {
            ids.push(p.id);
        });
        var qstr = id.join('&')
        window.open('/cd_subscription/printbadges?' + qstr, "_print");
    },

    getAttendee () {
      api('getAttendee', {
        id: this.participant.id
      }).then(
      function(data) {
          this.p = data.attendee;
          this.photosrc =  this.p.id ? '/api/subscriptions/' + this.p.id + 
            '/photo?time=' + (new Date()).getTime() : 
        '/static/img/nobody.png';
          this.photo = '';
        }.bind(this)
      )
    },

  },

  mounted () {
    this.getAttendee()
  }

}
</script>

<style>
.dropbox {
  width: 100%;
  height: 100px;
}
.photosrc{
  overflow: hidden;
  width: 100%;
  height: 400px;
  border: 1px dashed #808080;
  background-color: #d3d3d3;
}
.photoresult {
  overflow: hidden;
  position: relative;
  text-align: center;
  width: 160px;
  height: 200px;
}
</style>