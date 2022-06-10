<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            平台用户
          </div>
          <h1>{{user_num}}</h1>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="">
        <div class="card-panel-icon-wrapper icon-algorithm">
          <svg-icon icon-class="algorithm" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            水印算法
          </div>
          <h1>{{algorithm_num}}</h1>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="">
        <div class="card-panel-icon-wrapper icon-register">
          <svg-icon icon-class="register" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            注册模型
          </div>
          <h1>{{authentication_num}}</h1>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="">
        <div class="card-panel-icon-wrapper icon-judge">
          <svg-icon icon-class="judge" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            裁决记录
          </div>
          <h1>{{judge_num}}</h1>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import { getcount } from '@/api/admin'
export default {
  data() {
    return {
      user_num: '',
      algorithm_num: '',
      authentication_num: '',
      judge_num: ''
    }
  },
  created(){
    this.getcount()
  },
  methods: {
    getcount() {
      getcount(this.$store.getters.token).then(response => {
        const { data } = response
        this.user_num = data.user_num
        this.algorithm_num = data.algorithm_num
        this.authentication_num = data.authentication_num
        this.judge_num = data.judge_num
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 0px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-algorithm {
        background: #36a3f7;
      }

      .icon-register {
        background: #f4516c;
      }

      .icon-judge {
        background: #ffaa00
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-algorithm {
      color: #36a3f7;
    }

    .icon-register {
      color: #f4516c;
    }

    .icon-judge {
      color: #ffaa00
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
