<template>
<div>
  <h2>{{$t('ID number')}}</h2>
  <div>
    {{ $t('Please provide your id number of the RBCF') }}
  </div>
  <v-text-field :label="$t('ID number')" required v-model="flow.idnumber"></v-text-field>
  <v-btn @click="lookup()" color="primary">{{$t('Lookup ID number')}}</v-btn>
  <v-alert type="error" class="mt-2" v-show="errorcode">
    <div v-show="errorcode == 'notfound'">
      <div>{{ $t('The id number could not be found.') }}</div>
      <div>{{ $t('Please take into account that it takes a few days before a newly requested id number is available.') }}</div>
    </div>
    <div v-show="errorcode == 'playeradult'">
      {{ $t('The id number is not belonging to a youth player') }}
    </div>
    <div v-show="errorcode == 'alreadyregistered'">
      {{ $t('This player is already registered.') }}
    </div>
    <div v-show="errorcode == 'notaffiliated'">
      {{ $t('This player is not affiliated. Please contact your club to take the necessary action.') }}
    </div>
    <div v-show="errorcode == 'unknown'">
      {{ $t('UnknownError') }}
    </div>
  </v-alert>
  <div class="mt-4">
    <div v-show="flow.isPlayerFound">
      {{$t('Player found:')}} 
      {{first_name}} {{last_name}}
    </div>
    <div class="mt-2">
      <v-btn v-show="flow.isPlayerFound" @click="next" color="primary">
        {{$t('Continue')}}
      </v-btn>
      <v-btn class="ml-2" v-show="flow.isPlayerFound" @click="restart">
        {{ $t('Other player') }}
      </v-btn>
      <v-btn class="ml-2" @click="prev">{{$t('Back')}}</v-btn>
    </div>
  </div>
</div>
</template>

<script>
import { categories, normalcategory } from '@/util/subscription'
import { mapState } from 'vuex'

export default {

  name: "SubscriptionIDNumber",

  data () {return{
    errorcode: false,
    first_name: '',
    last_name: '',
    maxyear: categories[0].year,
    reply: {}
  }},

  computed: {
    ...mapState(['subscription', 'flow', 'api', 'locale'])
  },

  methods: {
    restart () {
      this.$store.commit('delSubscription');
      this.$store.commit('updateFlow', {
        idsubscription: null,
        idnumber: '',
      });
      this.errorcode = false;
    },

    lookup() {
      let self=this;
      this.errorcode = false;
      this.api.anon_check_id({idbel: this.flow.idnumber}).then(
        function(data){
          self.reply = data.obj
          if (self.reply.birthyear < 2000) {
            self.errorcode = 'playeradult';
            return
          }
          if (!self.reply.belfound) {
            self.errorcode = 'notfound';
            return
          }
          if (self.reply.subconfirmed) {
            self.errorcode = 'alreadyregistered';
            return
          }
          if (!self.reply.affiliated) {
            self.errorcode = 'notaffiliated';
            return
          }
          self.first_name = self.reply.first_name;
          self.last_name = self.reply.last_name;
          if (self.reply.subfound) {
            // we have a not confirmed subscription
            self.$store.commit('updateFlow', {
              idsubscription: data.obj.subid,
              isPlayerFound: true,
            })
            console.log('not confirmed subscription')
          }
          else {
            self.$store.commit('updateFlow', {
              isPlayerFound: true,
            })
          }

        },
        function(data){
          console.error('cannot check id', data)
          self.errorcode = 'unknown'
        }
      );
    },
    

    get_subscription(id) {
      console.log('getting subscription')
      let self = this;
      this.api.anon_get_subscription({id: id}).then(
        function(data) {
          self.$store.commit('updateSubscription', data.obj)
        },
        function(data) {
          console.error('cannot get subscription', data)
        }
      );
    },

    next () {
      let self=this;
      if (!this.flow.idsubscription) {
        this.api.anon_add_subscription({}, {requestBody: {
          locale: this.locale,
          category: normalcategory( this.reply.gender, this.reply.birthyear),
          idbel: this.flow.idnumber,
        }}).then(
          function(data){
            self.$store.commit('updateFlow', {
              idSubscription: data.obj,
              step: self.flow.step + 1
            })
            self.get_subscription(data.obj)
          },
          function(data) {
            console.error('cannot add subscription', data);
            self.errorcode = 'unknown'
          }
        )
      }
      else {
        self.$store.commit('updateFlow', { step: self.flow.step + 1 })        
        self.get_subscription(self.flow.idsubscription)
      }
    },

    prev () {
      this.$store.commit('updateFlow', {step: this.flow.step-1})
    },

  }
}
</script>

<style scoped>

</style>