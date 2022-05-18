<template>
  <div class="user-activity">
    <Post v-for="(item,index) in List" :key="index" :hash="item.hash" :timestamp="item.timestamp"
    :algorithm_name="item.algorithm_name" :model_type="item.model_type"
    :watermark_type="item.watermark_type" :algorithm_detail="item.algorithm_detail"></Post>
  </div>
</template>

<script>
import { certification_list } from '@/api/certification'
import Post from './Post.vue'
export default {
  components: {
    Post
  },
  data() {
    return {
      List_Num: '',
      List: [],
    }
  },
  created(){
    this.getlist()
  },
  methods: {
    getlist() {
      certification_list(this.$store.getters.token).then(response => {
        console.log(response)
        const { data } = response
        console.log()
        var count = 0
        for(var i in data){
          count ++
        }
        console.log(count)
        this.List_Num = count
        for(var i = 0;i<count;i++){
          this.$set(this.List,i,data[i])
          console.log(data[i].timestamp)
        }
      })
    }
  }
}
</script>

<style>
</style>
