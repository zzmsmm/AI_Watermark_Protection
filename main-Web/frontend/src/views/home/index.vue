<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">

        <el-col :span="7" :xs="24">
          <user-card :user="user" />
        </el-col>

        <el-col :span="17" :xs="24">
          <el-card>
            <el-tabs v-model="activeTab" :stretch=true>
              <el-tab-pane name="activity">
                <span slot="label" class="fontClass">注册记录</span>
                <activity />
              </el-tab-pane>
              <el-tab-pane name="timeline">
                <span slot="label" class="fontClass">裁决记录</span>
                <timeline />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>

      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import UserCard from './components/UserCard'
import Activity from './components/Activity'
import Timeline from './components/Timeline'

export default {
  name: 'Profile',
  components: { UserCard, Activity, Timeline },
  data() {
    return {
      user: {},
      activeTab: 'activity'
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'email'
    ])
  },
  created() {
    this.getUser()
  },
  methods: {
    getUser() {
      this.activeTab = this.$route.params.list != ':list' ? this.$route.params.list : 'activity'
      this.user = {
        name: this.name,
        email: this.email,
        avatar: this.avatar
      }
    }
  }
}
</script>

<style>
.fontClass{
  font-size:15px;
  font-weight: bold;
  color: #606266;
}
.fontClass:hover{
  font-size:15px;
  font-weight: bold;
  color: #409eff;
}
</style>
