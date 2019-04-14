<template>
<div>
  <div class="mt-2 pa-2" v-show="linkavailable">
   Live Games available <a :href="link">here</a>
  </div>
  <div class="mt-2 pa-2" v-show="!linkavailable">
   Live Games not yet available
  </div>
</div>
</template>

<script>

const links = {
  U8: "http://view.livechesscloud.com/deabfe5d-5d82-481f-9b27-544ba50fdba9",
  B10: "http://view.livechesscloud.com/d58a240d-1eb6-4dea-8905-2df513b4a9d3",
  G10: "http://view.livechesscloud.com/5a79b739-7492-4e8b-81bf-3ebf6b5d24ab",
  B12: "http://view.livechesscloud.com/d99d423d-95d2-449f-ad21-933c8e6b15e8",
  G12: "http://view.livechesscloud.com/17f49146-bcf9-4bfd-8e53-3751e7ebeefd",
  B14: "http://view.livechesscloud.com/5acc14c9-a27a-4493-880f-65b820dd3fc2",
  G14: "http://view.livechesscloud.com/df3a9452-747e-476f-b4ac-c284cfafa9eb",
  B16: "http://view.livechesscloud.com/b2bc5d4e-5574-43b9-b8f8-cfb77e30c5ef",
  G16: "http://view.livechesscloud.com/003b14f4-73c8-4b8f-bb7d-1911a6a31e2b",
  B18: "http://view.livechesscloud.com/01024da8-854d-4214-9b42-85d2e42bf020",
  G18: "http://view.livechesscloud.com/76f4ce70-1c77-4445-b0e4-643c0db85667",
  U20: "http://view.livechesscloud.com/dd0059b6-3039-4527-a7de-75e8573276b0",
  IMT: "http://view.livechesscloud.com/4a968f54-e793-402b-ace6-6b56d8415f35",
};

export default {
  props: ['trn'],
  data () {
    return {}
  },
  computed: {

    linkavailable () {
      return this.trn.shortname && this.trn.shortname in links;
    },
    link () {
      if (this.trn.shortname && this.trn.shortname in links) {
        return links[this.trn.shortname];
      }
      return '';
    },
  }
}
</script>

<style>
</style>
