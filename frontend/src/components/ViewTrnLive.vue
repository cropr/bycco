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
  B10: "http://bycco.livechesscloud.com/view/#/8fc3e207-b149-4171-ab59-2ae8c882425c",
  B14: "http://bycco.livechesscloud.com/view/#/dd2b79f6-8afc-472e-a479-cf62f2e87beb",
  G16: "http://bycco.livechesscloud.com/view/#/b7c7d269-10a4-4ee1-8b4f-2ad4eaad5e84",
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
  },
}
</script>

<style>
</style>
