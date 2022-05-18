<template>
  <div class="post">
    <div class="user-block">
      <el-tooltip content="点击前往裁决" placement="top">
        <a href="javascript:;" @click="tojudge()">
          <img class="img-circle" :src="avatar+avatarPrefix">
        </a>
      </el-tooltip>
      <span class="typename text-muted">{{model_type}} 模型 - {{watermark_type}}</span>
      <span class="description">Hash: {{hash}}</span>
    </div>
    <p>水印算法：{{algorithm_name}}</p>
    <el-link :href="algorithm_detail" target="_blank">算法详情：{{algorithm_detail}}</el-link>
    <ul class="list-inline">
      <li>
        <span class="link-black text-sm">
          <svg-icon icon-class="time" />
          Time: {{timestamp}}
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
const avatarPrefix = '?imageView2/1/w/80/h/80'
import { mapGetters } from 'vuex'
export default {
  name: 'Post',
  props: {
    hash: '',
    timestamp: '',
    model_type: '',
    watermark_type: '',
    algorithm_name: '',
    algorithm_detail: '',
  },
  data() {
    return {
      avatarPrefix,
      avatar: require('@/assets/Certification.png'),
    }
  },
  computed: {
    ...mapGetters([
      'name',
    ])
  },
  methods: {
    tojudge() {
      this.$router.push({ path:'/judge/apply/'+ this.hash + '/' + this.watermark_type})
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
