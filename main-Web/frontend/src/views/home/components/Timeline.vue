<template>
  <div class="block">
    <el-timeline :reverse="reverse">
      <el-timeline-item v-for="(item,index) of timeline" :key="index" :timestamp="item.timestamp" placement="top">
        <el-card>
          <div class="user-block">
            <el-tooltip content="点击查看详情" placement="top">
              <a href="javascript:;" @click="todetail()">
                <img class="img-circle" :src="item.avatar+avatarPrefix">
              </a>
            </el-tooltip>
            <span class="typename text-muted">{{item.model_type}} 模型 - {{item.watermark_type}}</span>
            <span class="description">Hash: {{item.hash}}</span>
          </div>
          <p style="color: #606266;font-size: 14px;"><b>水印算法：</b>{{ item.algorithm_name }}</p>
          <p style="color: #606266;font-size: 14px;"><b>对应注册记录哈希：</b>{{ item.authentication_hash }}</p>
          <p style="color: #606266;font-size: 14px;"><b>裁决对象 {{item.type}}：</b>{{ item.judge_info }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
const avatarPrefix = '?imageView2/1/w/80/h/80'
import { judge_list } from '@/api/judge'
export default {
  data() {
    return {
      reverse: true,
      avatarPrefix,
      timeline: [
        {
          timestamp: '2022-4-24',
          hash: '111',
          model_type: '111',
          watermark_type: '111',
          avatar: require('@/assets/judge_success.png'),
          algorithm_name: '111',
          authentication_hash: '111',
          judge_info: '111',
          type: '111',
        }
      ]
    }
  },
  created(){
    this.getlist()
  },
  methods: {
    getlist() {
      judge_list(this.$store.getters.token).then(response => {
        //console.log(response)
        const { data } = response
        var count = 0
        for(var i in data){
          count ++
        }
        //console.log(count)
        this.List_Num = count
        for(var i = 0;i<count;i++){
          this.$set(this.timeline,i,data[i])
          if (data[i].judge_result == 'success')
            this.timeline[i].avatar = require('@/assets/judge_success.png')
          else
            this.timeline[i].avatar = require('@/assets/judge_fail.png')
          this.timeline[i].type = this.timeline[i].watermark_type == '黑盒' ? 'API' : '模型信息'
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .user-block {

    .typename,
    .description {
      display: block;
      margin-left: 50px;
      padding: 2px 0;
      font-weight: bold;
      color: #409EFF;
    }

    .typename{
      font-size: 16px;
      color: #606266;
    }

    :after {
      clear: both;
    }

    .img-circle {
      border-radius: 50%;
      width: 40px;
      height: 40px;
      float: left;
    }

    span {
      font-weight: 500;
      font-size: 12px;
    }
  }

  .post {
    font-size: 14px;
    border-bottom: 1px solid #d2d6de;
    margin-bottom: 15px;
    padding-bottom: 15px;
    color: #666;

    .image {
      width: 100%;
      height: 100%;

    }

    .user-images {
      padding-top: 20px;
    }
  }

  .list-inline {
    padding-left: 0;
    margin-left: -5px;
    list-style: none;

    li {
      display: inline-block;
      padding-right: 5px;
      padding-left: 5px;
      font-size: 13px;
    }

    .link-black {
      font-weight: bold;
      font-size: 10px;
      color: #409EFF;
      &:hover,
      &:focus {
        color: #999;
      }
    }
  }

.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}
</style>
