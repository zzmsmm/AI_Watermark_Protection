<template>
  <div class="app-container">
    <div style="margin: 20px;"></div>
    <el-form ref="form" :model="form" :rules="formRules" label-width="80px">
      <el-form-item label="注册记录" prop="hash">
        <el-input v-model="form.hash" placeholder="请输入注册记录哈希" style="width: 50%;"></el-input>
      </el-form-item>
      <el-form-item label="水印类型">
        <el-radio-group v-model="type" size="small">
          <el-radio-button label=0 value=0>黑盒</el-radio-button>
          <el-radio-button label=1 value=1>白盒</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-show="type==1" label="模型文件" prop='file'>
        <div style="font-size: 14px;color: #606266;"><svg-icon icon-class="tip" style="margin-right: 10px;"/>
        上传可疑模型的参数，具体规范可参考算法指导</div>
        <el-upload
          class="upload-demo"
          action="#"
          :on-change="handleChange"
          multiple
          :limit="1"
          :before-upload="beforeUpload"
          :on-remove="handleRemove"
          :on-exceed="handleExceed"
          :file-list="form.fileList"
          style="width: 50%;">
          <el-button size="small" type="primary">点击上传</el-button>
        </el-upload>
        <p v-if="form.file != ''"  style="font-size: 14px;color: #606266;">
          <svg-icon icon-class="zip" style="margin-right: 10px;"/>
          {{form.file}}
        </p>
      </el-form-item>
      <el-form-item v-show="type==0" label="API" prop='api'>
        <el-input v-model="form.api" placeholder="请输入可疑 API" style="width: 50%;"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button :loading="loading" type="success" @click="judge_apply"
        style="margin-left: 10%; width: 20%;">
          提交裁决
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { judge_apply, judge_upload } from '@/api/judge'
export default {
  data(){
    const validatefileList = (rule, value, callback) => {
      if(value == '' && this.type == 1){
        callback(new Error('请先上传可疑模型参数'))
      }else{
        callback()
      }
    }
    const validateAPI = (rule, value, callback) => {
      if(value == '' && this.type == 0){
        callback(new Error('请输入可疑模型偷窃者的API'))
      }else{
        callback()
      }
    }
    return {
      type: 0,
      loading: false,
      form:{
        token:this.$store.getters.token,
        hash: '',
        api: '',
        file: ''
      },
      formRules: {
        hash: [{required: true, message:'请输入注册记录哈希值',trigger:'blur'}],
        api: [{required: true, validator:validateAPI, trigger:'blur'}],
        file: [{required: true, validator:validatefileList, trigger:'blur'}],
      }
    }
  },
  created(){
  	this.getfill()
  },
  methods:{
    getfill() {
      if(this.$route.params.hash !== ':hash') {
        this.form.hash = this.$route.params.hash
        this.type = this.$route.params.type === '黑盒' ? 0 : 1
      }
    },
    judge_apply(){
      this.$refs.form.validate(valid => {
        if(valid){
          this.loading = true
          judge_apply(this.form).then(response => {
            console.log(response.message)
            if(response.message == 'success') {
              this.$message({
                message: '裁决提交成功',
              	type: 'success',
              	showClose: true,
              	duration: 2 * 1000
              })
              this.loading = false
              this.$router.push({ path:'/home/timeline' })
            }
          }).catch(() => {
              this.loading = false
            })
        }else{
          return false
        }
      })
    },
    beforeUpload(file){
      var fd = new FormData();
      fd.append('file', file);
      fd.append('hash', this.form.hash);
      judge_upload(fd).then(response => {
        console.log("success")
        if(response.message == 'success') {
          console.log(file.name)
          this.form.file = file.name
          this.$message({
            message: '文件上传成功',
          	type: 'success',
          	showClose: true,
          	duration: 2 * 1000
          })
        }
      }).catch(() => {
              console.log("error")
              this.activestep = 2
            })
       return false  //屏蔽了action的默认上传
    },
    handleChange(file, fileList) {
      this.form.fileList = fileList.slice(-3)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
      this.form.fileList = fileList.slice(-3)
    }
  }
}
</script>

<style>
</style>
