<template>
  <el-card style="margin-bottom:20px;">
    <div slot="header" class="clearfix">
      <div style="font-weight: bold; font-size: 15px; color: #606266;">个人信息</div>
    </div>

    <div class="user-profile">
      <div class="box-center">
        <pan-thumb :image="user.avatar" :height="'120px'" :width="'120px'" :hoverable="false">
          <div style="font-weight: bold; font-size: 15px; margin-top: 20px; color: #606266;">
            更改头像
          </div>
          <el-upload
            class="avatar-uploader"
            action="https://jsonplaceholder.typicode.com/posts/"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </pan-thumb>
      </div>

      <div class="box-center">
        <div class="user-name text-center">{{ user.name }}</div>
      </div>
    </div>

    <div class="user-bio">
      <div class="user-education user-bio-section">
        <div class="user-bio-section-header"><svg-icon icon-class="email" /><span>邮箱</span></div>
        <div class="user-bio-section-body">
          <div class="text-muted">
            {{ user.email }}
          </div>
        </div>
      </div>

      <div class="user-skills user-bio-section">
        <div class="user-bio-section-header"><svg-icon icon-class="process" /><span>进度</span></div>
        <div class="user-bio-section-body">
          <div class="progress-item">
            <span>认证1</span>
            <el-progress :percentage="70" />
          </div>
          <div class="progress-item">
            <span>认证2</span>
            <el-progress :percentage="100" status="success" />
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import PanThumb from '@/components/PanThumb'
import {changeAvatar} from '@/api/user.js'
export default {
  components: { PanThumb },
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          email: '',
          avatar: '',
        }
      }
    }
  },
  data() {
    return {
      imageUrl: ''
    }
  },
  methods: {
    handleAvatarSuccess(res, file) {
            // this.imageUrl = URL.createObjectURL(file.raw);
            // console.log(file)
          },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message({
          message: '上传头像图片只能是 PNG 格式!',
          type: 'error',
          showClose: true,
          duration: 1 * 1000
        })
      }
      if (!isLt2M) {
        this.$message({
          message: '上传头像图片大小不能超过 2MB!',
          type: 'error',
          showClose: true,
          duration: 1 * 1000
        })
      }
      if(isJPG && isLt2M) {
        var formdata = new FormData();
        formdata.append('avatar_name', this.user.name);
        formdata.append('avatar_file', file);
        changeAvatar(formdata).then(response => {
          console.log(response)
          this.$router.go(0)
        })
      }
      return isJPG && isLt2M;
    }
  }
}
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.user-profile {
  .user-name {
    font-weight: bold;
    font-size: 20px;
    color: #606266;
  }

  .box-center {
    padding-top: 10px;
  }

  .user-role {
    padding-top: 10px;
    font-weight: 400;
    font-size: 14px;
  }

  .box-social {
    padding-top: 30px;

    .el-table {
      border-top: 1px solid #dfe6ec;
    }
  }

  .user-follow {
    padding-top: 20px;
  }
}

.user-bio {
  margin-top: 20px;
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}

.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    //position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    margin-top: 15px;
    margin-right: 10px;
    font-size: 20px;
    color: #8c939d;
    width: 10px;
    height: 10px;
    line-height: 10px;
  }
  .avatar {
    width: 10px;
    height: 10px;
    display: block;
  }
</style>
