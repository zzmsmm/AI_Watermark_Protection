<template>
  <div class="user-activity">
    <Post v-for="(item,index) in List" :key="index" :hash="item.hash" :time="item.time"
    :algorithm_name="item.algorithm_name" :model_type="item.model_type"
    :watermark_type="item.watermark_type" :algorithm_detail="item.algorithm_detail"></Post>
  </div>
</template>

<script>
import Post from './Post.vue'
export default {
  components: {
    Post
  },
  data() {
    return {
      List_Num: 2,
      List: [
        {
          model_type: 'NLP',
          watermark_type: '黑盒',
          hash: '111111',
          time: '2022-4-25 22:30',
          algorithm_name: '穿透水印',
          algorithm_detail: '这里是水印算法的详细介绍...',
        },
        {
          model_type: '图像识别',
          watermark_type: '白盒',
          hash: '222222',
          time: '2022-4-25 22:40',
          algorithm_name: 'MTL-Sign',
          algorithm_detail: '这里是水印算法的详细介绍...',
        },
      ],
    }
  }
}
</script>

<style>
</style>
