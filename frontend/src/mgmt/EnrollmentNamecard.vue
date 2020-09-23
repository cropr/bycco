<template>

  <v-container fluid grid-list-md class="elevation-1">
 
    <v-layout row wrap>
      <v-flex>
        <h1>Name Cards</h1>
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
          <span>Clear custom selection</span>
        </v-tooltip>
      </v-flex>
    </v-layout>
  
    <div>
      <h4>Make selection</h4>
      <v-radio-group v-model="cat">
        <v-layout row wrap>
          <v-flex md1 sm2 xs3 v-for="c in cats" :key="c">
            <v-radio :label="c" :value='c' hide-details class="check"
                        @change="recalc" />
          </v-flex>
        </v-layout>
      </v-radio-group>  
    </div>

    <div>
      <h4>Selected particpants</h4>
      <table>
        <tr v-for="(p,ix) in namecards" :key="p.id">
          <td style="width: 3em;"> {{ ix + 1}}</td>  
          <td  style="width: 20em;"> {{ p.first_name}} {{p.last_name}}</td>  
          <td> {{ p.category}}</td>
        </tr>
      </table>  
    </div>

  </v-container>
</template>

<script>

import api from '../util/api'

export default {

  name: "ParticipantNamecard",

  props: ['selection'],

  data () {return {
    cats: ['U8', 'B10', 'G10', 'B12', 'G12', 'B14', 'G14', 'B16', 'G16',
      'B18', 'G18','U20', 'ORG', 'ARB', 'IMT', 'EAT', 'SPO', 'Custom'],
    cat: 'Custom',
    catsearch: '',
    ss: '',
    namecards: this.selection,
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list', params:{}})
    },

    clear () {
      this.cat = 'Custom'
      this.$emit('update', {
        section: 'list',
        selection: [],
        reload: true,
      });      
    },

    print() {
      var ids, qstr, cs;
      if (this.cat == 'Custom') {
        ids=[];
        this.selection.forEach(p => {
            ids.push(p.id);
        });
        qstr = "ids=" + ids.join(',');
      }
      else {
        cs = this.cat;
        if (cs == 'U8') cs = 'B8,G8';
        if (cs == 'U20') cs = 'B20,G20';        
        qstr = "cat=" + cs;
      }
      window.open('/trn/printnamecards?' + qstr, "_print");
    },

    recalc (c) {
      if (c == 'Custom') {
        this.namecards = this.sortAlphabetically(this.selection);
      }
      else {
        var cs = c;
        if (cs == 'U8') cs = 'B8,G8';
        if (cs == 'U20') cs = 'B20,G20';
        api('getAttendees', {
          cat: cs
        }).then(
          function(data){
            console.log('data.attendees', data.attendees)
            this.namecards = this.sortAlphabetically(data.attendees); 
          }.bind(this),
          function(data){
            console.log('error getAttendees', data)
          }
        );
      } 
    },

    search() {

    },

    sortAlphabetically(a) {
      var result = [...a];
      console.log('result', result);
      result.sort((a,b) => (a.last_name > b.last_name) ? 1 : (
        (b.last_name > a.last_name) ? -1 : 0));
      return result
    },

    mounted() {
      this.recalc('Custom')
    }
    
    
  },

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