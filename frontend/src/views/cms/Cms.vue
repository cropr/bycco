<template>
<div>
  <landing-template v-if="template=='landing'" :page="page" />
  <multi-locale-template v-if="template=='multilocale'" :page="page" />
  <not-found-template v-if="template=='notfound'" />
  <simple-template v-if="template=='simple'" :page="page" />
</div>
</template>
<script>
import { mapState } from "vuex"
import { available_templates } from '@/util/server_injected'

import LandingTemplate from './LandingTemplate'
import MultiLocaleTemplate from './MultiLocaleTemplate'
import NotFoundTemplate from './NotFoundTemplate'
import SimpleTemplate from './SimpleTemplate'

export default {

  name: 'Cms',

  data() {
    return {
      page: {},
      template: 'notfound',
    };
  },

  components: {
    LandingTemplate,
    MultiLocaleTemplate,
    NotFoundTemplate,
    SimpleTemplate,
  },

  computed: {
    ...mapState(['api', 'slug']),
  },

  methods: {

    getContent () {
      let self=this, 
          t;
      this.api.anon_slug_page({
        slug: this.slug,
      }).then(
        function(data){
          self.page =  data.obj;
          t = data.obj.component;
          self.template = available_templates.includes(t) ? t : 'notfound';
          console.log('t', data.obj.component, self.template)
        },
        function(data){
          console.error('could not fetch page', data)
        }
      )
    },

  },

  mounted() {
    this.getContent()
  }

}
</script>
