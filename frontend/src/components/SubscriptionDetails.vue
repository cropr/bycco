<template>
<div>
  <h2>{{$t('Details player')}}</h2>

  <v-layout row wrap>
    <v-flex xs12 sm6 >
      <div class="mt-2">
        <span>{{$t('Full name')}}</span>:
        {{ subscription.first_name }} {{subscription.last_name}}
      </div>
      <div class="mt-2">
        <span>{{$t('Birthdate')}}</span>:
        {{ birthdate }}
      </div>
      <div class="mt-2">
        <span>{{$t('ID Club')}}</span>:
        {{ subscription.idclub }}
      </div>
      <div class="mt-2">
        <span>{{$t('Nationality')}}</span>:
        {{ subscription.nationalitybel }}
      </div>
      <div class="mt-2">
        <span>{{$t('FIDE Nationality')}}</span>:
        {{ subscription.nationalityfide }}
      </div>
    </v-flex>
    <v-flex xs12 sm6>
      <div class="mt-2">
        <span>{{$t('National rating')}}</span>:
        {{ subscription.currentratingbel }}
      </div>
      <div class="mt-2">
        <span>{{$t('FIDE rating')}}</span>:
        {{ subscription.currentratingfide }}
      </div>
      <div class="mt-2">
        <span>{{$t('Gender')}}</span>:
        {{ subscription.gender }}
      </div>

      <div class="mt-2">
        <v-select v-model='flow.category' :label="$t('Category')" :items="cats"></v-select>
      </div>

    </v-flex>
  </v-layout>

  <div v-show="adult" class="mt-3">

      <h3 class="mt-3">{{$t('Required information')}}</h3>
      <div > {{ p1() }}</div>

      <v-layout row wrap>
        <v-flex xs12 sm6>
          <v-text-field :label="$t('Email address player')" v-model="flow.emailplayer" required>
          </v-text-field>
          <v-text-field :label="$t('GSM number player')" v-model="flow.mobileplayer" required>
          </v-text-field>
        </v-flex>
      </v-layout>

      <h3 class="mt-3">{{$t('Optional information')}}</h3>
      <v-layout row wrap>
        <v-flex xs12 sm6>
          <div>{{$t('SubDetail2')}}</div>
          <v-text-field :label="$t('Full name respresentative')" v-model="flow.fullnameattendant">
          </v-text-field>
          <v-text-field :label="$t('GSM number representative')" v-model="flow.mobileattendant">
          </v-text-field>
        </v-flex>
      </v-layout>
  </div>

  <div v-show="!adult">

    <h3 class="mt-3">{{$t('Required information')}}</h3>
    <div > {{ p3() }}</div>

    <v-layout row wrap>
      <v-flex xs12 sm6>
        <h4>{{$t('Info about parent')}}</h4>
        <v-text-field :label="$t('Full name')" v-model="flow.fullnameparent" required>
        </v-text-field>
        <v-text-field :label="$t('Email address')" v-model="flow.emailparent" required>
        </v-text-field>
        <v-text-field :label="$t('GSM number')" v-model="flow.mobileparent" required>
        </v-text-field>
      </v-flex>
      <v-flex xs12 sm6>
        <h4>{{$t('Info about presence on site')}}</h4>
        <v-checkbox :label="$t('A parent is present at site')"  v-model="flow.isParentPresent">
        </v-checkbox>
        <div v-show="!flow.isParentPresent">
          <h4>{{$t('Info about adult representative at site')}}</h4>
          <v-text-field :label="$t('Full name')" v-model="flow.fullnameattendant" required>
          </v-text-field>
          <v-text-field :label="$t('GSM number')" v-model="flow.mobileattendant" required>
          </v-text-field>
        </div>
      </v-flex>
    </v-layout>

    <h4 class="mt-3">{{$t('Optional information')}}</h4>
    <v-layout row wrap>
      <v-flex xs12 sm6>
        <div>{{$t('SubDetail4')}}</div>
        <v-text-field :label="$t('Email address player')" v-model="flow.emailplayer" required>
        </v-text-field>
        <v-text-field :label="$t('GSM number player')" v-model="flow.mobileplayer" required>
        </v-text-field>
      </v-flex>
    </v-layout>

  </div>

  <v-alert type="error" class="mt-2" dismissible :value="errorcode">
    <div v-show="errorcode == 'invalidfield'">{{$t('SubDetail5')}}</div>
    <div v-show="errorcode == 'firewall'">{{$t('SubDetail6')}}</div>
    <div v-show="errorcode == 'unknown'">{{$t('UnknownError')}}</div>
  </v-alert>

  <div class="mt-2">
    <v-btn @click="createSubscription()" color="primary">{{$t('Continue')}}
    </v-btn>
    <v-btn @click="prev" v-t="'Back'">
    </v-btn>
  </div>

</div>
</template>

<script>
import { mapState } from 'vuex'
import _ from 'lodash'

import api from '../util/api'
import {categories, formatDate} from "../util/utils";
import * as moment from 'moment'


function invalidField(field) {
  if (!field) return true;
  return field.length < 2;
}

let mustache = /{{(.*?)}}/g;

export default {

  name: "SubscriptionDetails",
  data () {return {
    adultdate: moment('2001-04-14'),
    errorcode: null,
  }},

  computed: {
    adult () {
      return this.subscription.birthdate < this.adultdate
    },
    cats () {
      let bdate = this.subscription.birthdate;
      if (!bdate) {
        return categories
      }
      let c =  _.filter(categories, function(o){
        return o.year <= bdate.getFullYear()
      });
      return c;
    },
    birthdate () {
      return formatDate(this.subscription.birthdate)
    },
    ...mapState(['subscription', 'flow'])
  },

  watch: {
    cats (nc) {
      console.log('updating category', nc[nc.length-1].value);
      this.$store.commit('updateFlow', {category: nc[nc.length-1].value});
    }
  },

  methods: {

    createSubscription () {
      let rm = false;
      if (!this.adult) {
        rm = rm || invalidField(this.flow.fullnameparent);
        rm = rm || invalidField(this.flow.emailparent);
        rm = rm || invalidField(this.flow.mobileparent);
        if (!this.flow.isParentPresent) {
          rm = rm || invalidField(this.flow.fullnameattendant);
          rm = rm || invalidField(this.flow.mobileattendant);
        }
      }
      else {
        rm = rm || invalidField(this.flow.emailplayer);
        rm = rm || invalidField(this.flow.mobileplayer);
      }
      if (rm) {
        this.errorcode = 'invalidfield';
        return;
      }
      let subparam =  {
        category: (this.subscription.gender == 'M' ? 'B' : 'G') + this.flow.category,
        emailparent: this.flow.emailparent || '',
        emailplayer: this.flow.emailplayer || '',
        fullnameattendant: this.flow.fullnameattendant || '',
        fullnameparent: this.flow.fullnameparent || '',
        idbel: this.subscription.idbel,
        mobileattendant: this.flow.mobileattendant || '',
        mobileparent: this.flow.mobileparent || '',
      };
      api('createSubscription', {subscription: subparam}).then(
        function(data) {
          this.$store.commit('updateSubscription', {
            paymessage: data.paymessage,
            idsub: data.id,
            category: this.flow.category,
          });
          this.$store.commit('updateFlow', {step: this.flow.step + 1});
        }.bind(this),
        function(data) {
            console.error('subscription failed', data);
            this.errorcode = (data == 403) ? 'firewall' : 'unknown';
        }.bind(this)
      );
    },

    prev () {
      this.$store.commit('updateFlow', {step: this.flow.step-1})
    },

    p1 () {
      return this.subsub(this.$t('SubDetail1'))
    },

    p3 () {
      return this.subsub(this.$t('SubDetail3'))
    },

    subsub (str) {
      return str.replace(mustache, function(dummy, param) {
        return this.subscription[param] || '***'
      }.bind(this));
    }
  }

}

</script>

<style scoped>

</style>