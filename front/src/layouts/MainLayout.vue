<template>
  <q-layout view="hHh lpR fFf">

    <q-header reveal elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title align="left">
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          校园随心贴
        </q-toolbar-title>

        <q-tabs
          v-model="tab"
          inline-label
          class="bg-primary text-white"
          align="right"
        >

          <q-btn round align="right">
            <q-avatar size="42px">
              <img src="https://cdn.quasar.dev/img/avatar2.jpg">
            </q-avatar>
          </q-btn>

          <q-btn-dropdown auto-close stretch flat label="热门">
            <q-list>
              <q-item clickable @click="tab = 'movies'">
                <q-item-section>Movies</q-item-section>
              </q-item>
              <q-item clickable @click="tab = 'photos'">
                <q-item-section>Photos</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>

          <q-btn-dropdown auto-close stretch flat label="消息">
            <q-list>
              <q-item clickable @click="tab = 'movies'">
                <q-item-section>Movies</q-item-section>
              </q-item>
              <q-item clickable @click="tab = 'photos'">
                <q-item-section>Photos</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>

        </q-tabs>

      </q-toolbar>

    </q-header>

    <q-page-container style="overflow: hidden">
      <router-view />
    </q-page-container>

    <q-footer reveal elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          页脚
        </q-toolbar-title>
        <q-btn round align="center" color="primary" @click="uploadPost">
          <i class="el-icon-plus"></i>
        </q-btn>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
export default {
  data () {
    return {
      tab: 'mails'
    }
  },
  methods:{
    uploadPost(){
      this.$router.push("./upload_picture?token="+this.$route.query.token);
    },
  }
}
</script>
