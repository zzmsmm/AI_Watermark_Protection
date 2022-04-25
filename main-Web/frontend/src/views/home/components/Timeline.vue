<template>
  <div class="block">
    <el-timeline :reverse="reverse">
      <el-timeline-item v-for="(item,index) of timeline" :key="index" :timestamp="item.timestamp" placement="top">
        <el-card>
          <p style="font-weight: bold; font-size: 16px; color: #606266;">
          <i :class="item.icon_type" style="color: #409EFF;"/> {{ item.title }}</p>
          <p>{{ item.content }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reverse: true,
      timeline: [
        {
          timestamp: '2022-4-22',
          title: '认证',
          icon_type: 'el-icon-s-claim',
          content: 'PanJiaChen committed 2022-4-22 20:46'
        },
        {
          timestamp: '2022-4-24',
          title: '裁决',
          icon_type: 'el-icon-s-check',
          content: 'PanJiaChen committed 2022-4-24 20:46'
        }
      ]
    }
  }
}
</script>
