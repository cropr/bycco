<template>
<div>
  <div class="mt-2" v-show="linkavailable">
   Live Games available <a :href="link">here</a>
  </div>
  <div class="mt-2" v-show="!linkavailable">
   Live Games not yet available
  </div>
</div>
</template>

<script>

const links = {
  U8: "http://bycco.livechesscloud.com/view#/2274b3a0-a577-4c72-a077-8c1a31301402",
  B10: "http://bycco.livechesscloud.com/view/#/8fc3e207-b149-4171-ab59-2ae8c882425c",
  G10: "http://bycco.livechesscloud.com/view#/09f7f5f0-a01c-43f5-83b5-c29e1bab1712",
  B12: "http://bycco.livechesscloud.com/view/#/000b3fbc-f53f-4588-89b3-41c962084347",
  G12: "http://bycco.livechesscloud.com/view#/0d3478bc-124b-436b-a986-abadaef82ac5",
  B14: "http://bycco.livechesscloud.com/view/#/dd2b79f6-8afc-472e-a479-cf62f2e87beb",
  G14: "http://bycco.livechesscloud.com/view/#/cd5596ad-9ac2-448c-8b20-4c6313ba4389",
  B16: "http://bycco.livechesscloud.com/view/#/11109f96-40f8-45cb-9293-78c2288d776d",
  G16: "http://bycco.livechesscloud.com/view/#/b7c7d269-10a4-4ee1-8b4f-2ad4eaad5e84",
  B18: "http://bycco.livechesscloud.com/view#/7bb06bdd-4a09-4e77-9980-e358b4611b15",
  G18: "http://bycco.livechesscloud.com/view#/7bb06bdd-4a09-4e77-9980-e358b4611b15",
  U20: "http://bycco.livechesscloud.com/view#/db5eea45-4bcf-47a8-8ca5-693de60dd396",
  IMT: "http://bycco.livechesscloud.com/view#/7bb06bdd-4a09-4e77-9980-e358b4611b15",
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
