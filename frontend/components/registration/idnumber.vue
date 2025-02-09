<script setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
import { categories } from "~/utils/constants"

// communication
const emit = defineEmits(["changeStep", "updateRegistration"])
defineExpose({ setup })
const { $backend } = useNuxtApp()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// i18n
const { t } = useI18n()

// datamodel member
const birthyear = ref(null)
const first_name = ref("")
const gender = ref(null)
const idbel = ref("")
const idclub = ref("")
const idfide = ref("")
const last_name = ref("")
const nationalitybel = ref("")
const nationalityfide = ref("")
const natstatus = ref("Unknown")
const ratingbel = ref(0)
const ratingfide = ref(0)

// datamodel the rest
const isBelPlayerFound = ref(false)
const isFidePlayerFound = ref(false)
const errorcode = ref(null)
const step = 2

async function lookup_bel() {
  let member
  errorcode.value = null
  showLoading(true)
  try {
    const reply = await $backend("registration", "lookup_idbel", {
      idbel: idbel.value.trim(),
    })
    console.log("bel member", reply.data)
    member = reply.data
  } catch (error) {
    console.error("lookup_bel failed", error)
    errorcode.value = "notfound"
    return
  } finally {
    showLoading(false)
  }
  isBelPlayerFound.value = member.belfound
  isFidePlayerFound.value = true
  birthyear.value = member.birthyear
  first_name.value = member.first_name
  gender.value = member.gender
  idclub.value = member.idclub
  idfide.value = member.idfide + ""
  last_name.value = member.last_name
  nationalitybel.value = member.nationalitybel
  nationalityfide.value = member.nationalityfide
  ratingbel.value = member.ratingbel
  ratingfide.value = member.ratingfide
  if (!isBelPlayerFound.value) {
    errorcode.value = "notfound"
  }
  if (birthyear.value < categories[0].year) {
    errorcode.value = "noyouth"
  }
}

function next() {
  updateRegistration()
  emit("changeStep", step + 1)
}

function prev() {
  updateRegistration()
  emit("changeStep", step - 1)
}

function restart() {
  isBelPlayerFound.value = false
  isFidePlayerFound.value = false
  errorcode.value = null
  idbel.value = ""
  idfide.value = ""
}

function setup(e) {
  idbel.value = e.idbel
  idfide.value = e.idfide
  first_name.value = e.first_name + ""
  last_name.value = e.last_name + ""
  ratingbel.value = e.ratingbel + 0
  ratingfide.value = e.ratingfide + 0
}

function updateRegistration() {
  emit("updateRegistration", {
    birthyear: birthyear.value,
    first_name: first_name.value,
    gender: gender.value,
    idbel: idbel.value.trim(),
    idclub: idclub.value,
    idfide: idfide.value,
    last_name: last_name.value,
    nationalitybel: nationalitybel.value,
    nationalityfide: nationalityfide.value,
    ratingbel: ratingbel.value,
    ratingfide: ratingfide.value,
  })
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
})
</script>
<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <v-row class="my-2">
      <h2>{{ t("enroll.idn_title") }}</h2>
    </v-row>
    <v-row class="mt-2">
      <div>{{ t("enroll.idn_enter") }}</div>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="idbel" :label="t('enroll.idn_title')" required />
      </v-col>
      <v-col cols="12" md="6">
        <v-btn color="primary" @click="lookup_bel()">
          {{ t("Lookup") }}
        </v-btn>
      </v-col>
    </v-row>
    <v-alert v-show="errorcode" type="error" class="mt-2" closable>
      <div v-show="errorcode == 'notfound'">
        <div>{{ t("enroll.idn_notfound") }}</div>
      </div>
      <div v-show="errorcode == 'alreadyregistered'">
        {{ t("enroll.idn_alreadyregistered") }}
      </div>
      <div v-show="errorcode == 'noyouth'">
        {{ t("enroll.idn_noyouth") }}
      </div>
      <div v-show="errorcode == 'unknown'">
        {{ t("UnknownError") }}
      </div>
    </v-alert>
    <div class="mt-4">
      <div v-show="isBelPlayerFound">
        {{ t("enroll.idn_playerfound") }} {{ first_name }} {{ last_name }}
      </div>
      <div class="mt-2">
        <v-btn class="ml-2" @click="prev" color="primary">
          {{ t("Back") }}
        </v-btn>
        <v-btn :disabled="!isBelPlayerFound" class="ml-2" color="primary" @click="next">
          {{ t("Continue") }}
        </v-btn>
        <v-btn class="ml-2" @click="restart">
          {{ t("Other player") }}
        </v-btn>
      </div>
    </div>
  </v-container>
</template>
