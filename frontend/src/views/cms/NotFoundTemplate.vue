<template>

<v-container>
    <h1>{{ $t("Page not found") }} </h1>
    <p>{{ $t("Page") }} '{{ path }}'  {{ $t("was not found") }}</p>
</v-container>

</template>

<script>

export default {

  name: 'RouteNotFound',

  data () {return {
    path: this.$route.params.pathMatch
  }},

}

</script>

