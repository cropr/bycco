<template>
<div>
  <h2>{{$t('Details player')}}</h2>

  <v-row>
    <v-col cols=12 sm=6>
      <div class="mt-2">
        <span>{{$t('Full name')}}</span>:
        {{ subscription.first_name }} {{subscription.last_name}}
      </div>
      <div class="mt-2">
        <span>{{$t('Birthdate')}}</span>:
        {{ subscription.birthdate }}
      </div>
      <div class="mt-2">
        <span>{{$t('ID Club')}}</span>:
        {{ subscription.idclub }}
      </div>
      <div class="mt-2">
        <span>{{$t('Nationality')}}</span>:
        {{ subscription.nationality }}
      </div>
   </v-col>
    <v-col cols=12 sm=6>
      <div class="mt-2">
        <span>{{$t('National rating')}}</span>:
        {{ subscription.ratingbel }}
      </div>
      <div class="mt-2">
        <span>{{$t('FIDE rating')}}</span>:
        {{ subscription.ratingfide }}
      </div>
      <div class="mt-2">
        <span>{{$t('Gender')}}</span>:
        {{ subscription.gender }}
      </div>

      <div class="mt-2">
        <v-select v-model='age' :label="$t('Category')" 
          :items="catselect" />
      </div>

    </v-col>
  </v-row>

  <div v-show="adult" class="mt-3">

      <h3 class="mt-3">{{$t('Required information')}}</h3>
      <div > {{ p1() }}</div>

      <v-row >
        <v-col cols=12 sm=6>
          <v-text-field :label="$t('Email address player')" v-model="emailplayer" required>
          </v-text-field>
          <v-text-field :label="$t('GSM number player')" v-model="mobileplayer" required>
          </v-text-field>
        </v-col>
      </v-row>

      <h3 class="mt-3">{{$t('Optional information')}}</h3>
      <v-row>
        <v-col cols=12 sm=6>
          <div>
            {{ $t('Although optional it is recommended to provide the details of a club or league representative that is at site during the tournament') }}
          </div>
          <v-text-field :label="$t('Full name respresentative')" v-model="fullnameattendant">
          </v-text-field>
          <v-text-field :label="$t('Email respresentative')" v-model="emailattendant">
          </v-text-field>
          <v-text-field :label="$t('GSM number representative')" v-model="mobileattendant">
          </v-text-field>
        </v-col>
      </v-row>
  </div>

  <div v-show="!adult">

    <h3 class="mt-3">{{$t('Required information')}}</h3>
    <div > {{ p3() }}</div>

    <v-row>
      <v-col cols=12 sm=6>
        <h4>{{$t('Info about parent')}}</h4>
        <v-text-field :label="$t('Full name')" v-model="fullnameparent" required>
        </v-text-field>
        <v-text-field :label="$t('Email address')" v-model="emailparent" required>
        </v-text-field>
        <v-text-field :label="$t('GSM number')" v-model="mobileparent" required>
        </v-text-field>
      </v-col>
      <v-col cols=12 sm=6>
        <h4>{{$t('Person picking up the player after the game')}}</h4>
        <v-checkbox :label="$t('The parent is picking up the player')"  v-model="isParentPresent">
        </v-checkbox>
        <div v-show="!isParentPresent">
          <v-text-field :label="$t('Full name')" v-model="fullnameattendant" required>
          </v-text-field>
          <v-text-field :label="$t('Email')" v-model="emailattendant" required>
          </v-text-field>
          <v-text-field :label="$t('GSM number')" v-model="mobileattendant" required>
          </v-text-field>
        </div>
      </v-col>
    </v-row>

    <h4 class="mt-3">{{$t('Optional information')}}</h4>
    <v-row>
      <v-col cols=12 sm=6>
        <div>
          {{$t('The information requested below, is optional but it is highly recommended to provide it') }}
        </div>
        <v-text-field :label="$t('Email address player')" v-model="emailplayer" required>
        </v-text-field>
        <v-text-field :label="$t('GSM number player')" v-model="mobileplayer" required>
        </v-text-field>
      </v-col>
    </v-row>

  </div>

  <v-alert type="error" class="mt-2" dismissible :value="!!errorcode">
    <div v-show="errorcode == 'invalidfield'">
      {{ $t('One of the required fields is invalid.') }}
    </div>
    <div v-show="errorcode == 'unknown'">{{$t('UnknownError')}}</div>
  </v-alert>

  <div class="mt-2">
    <v-btn @click="updateSubscription()" color="primary">{{$t('Continue')}}
    </v-btn>
    <v-btn @click="prev" v-t="'Back'">
    </v-btn>
  </div>

</div>
</template>

<script>
import { mapState } from 'vuex'
import { catselect } from "@/util/subscription"
import * as moment from 'moment'

let mustache = /{{(.*?)}}/g;

function invalidField(field) {
  if (!field) return true;
  return field.length < 2;
}

export default {

  name: "SubscriptionDetails",

  computed: {
    catselect (){ 
      if (!this.subscription.birthdate) return []
      return catselect(parseInt(this.subscription.birthdate.substr(0,4)));
    },
    adult () {
      return this.subscription.birthdate < this.adultdate
    },
    age: {
      get() {
        return this.$store.state.age;
      },
      set(value) {
        this.$store.commit('updateSubscription', {
          category: this.subscription.category.substr(0,1) + value
        });
      },
    },
    ...mapState(['subscription', 'flow', 'api', 'locale', 'age'])
  },

  data () {return {
    adultdate: moment('2002-11-05'),
    errorcode: null,
    emailattendant: '',
    emailparent: '',
    emailplayer: '',
    fullnameattendant : '',
    fullnameparent: '',
    isParentPresent: false,
    mobileattendant: '',
    mobileparent: '',
    mobileplayer: '',
  }},

  methods: {

    prev () {
      this.$store.commit('updateFlow', {step: this.flow.step-1})
    },

    p1 () {
      return this.subsub(
        this.$t('')
      )
    },

    p3 () {
      return this.subsub(
        this.$t('{{first_name}} is a minor at the start of a tournament. For minors we need following information.')
      )
    },

    subsub (str) {
      let self=this;
      return str.replace(mustache, function(dummy, param) {
        return self.subscription[param] || '***'
      });
    },

    updateSubscription() {
      let rm = false, self = this, update;
      if (!this.adult) {
        rm = rm || invalidField(this.fullnameparent);
        rm = rm || invalidField(this.emailparent);
        rm = rm || invalidField(this.mobileparent);
        if (!this.isParentPresent) {
          rm = rm || invalidField(this.fullnameattendant);
          rm = rm || invalidField(this.mobileattendant);
        }
      }
      else {
        rm = rm || invalidField(this.emailplayer);
        rm = rm || invalidField(this.mobileplayer);
      }
      if (rm) {
        this.errorcode = 'invalidfield';
        return;
      }        
      update ={category: this.category, isParentPresent: this.isParentPresent};
      if (this.emailattendant.length) update.emailattendant = this.emailattendant;
      if (this.emailparent.length) update.emailparent = this.emailparent;
      if (this.emailplayer.length) update.emailplayer = this.emailplayer;
      if (this.fullnameattendant.length) update.fullnameattendant = this.fullnameattendant;
      if (this.fullnameparent.length) update.fullnameparent = this.fullnameparent;
      if (this.mobileattendant.length) update.mobileattendant = this.mobileattendant;
      if (this.mobileparent.length) update.mobileparent = this.mobileparent;
      if (this.mobileparent.length) update.mobileparent = this.mobileparent;      
      this.api.anon_update_subscription({id: this.subscription.id}, 
          {requestBody: update}).then(
        function(data){
          self.$store.commit('updateSubscription', data.obj)
          self.$store.commit('updateFlow', {step: self.flow.step + 1})
        },
        function(data){
          console.error('cannot update subscription', data);
          self.errorcode = 'unknown'
        })
    },

    mounted(){
      let self=this;
      this.$root.$on('updateCategory', function(cat) {
        self.category = cat;
      })
    }


  },

}

</script>

<style scoped>

</style>