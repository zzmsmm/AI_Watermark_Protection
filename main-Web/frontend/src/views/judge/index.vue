<template>
  <div class="app-container">
    <div style="margin: 20px;"></div>
    <el-form ref="form" :model="form" :rules="formRules" label-width="80px">
      <el-form-item label="注册记录" prop="hash">
        <el-input v-model="form.hash" placeholder="请输入注册记录哈希"></el-input>
      </el-form-item>
      <el-form-item label="水印类型">
        <el-radio-group v-model="type" size="small">
          <el-radio-button label=0 value=0>黑盒</el-radio-button>
          <el-radio-button label=1 value=1>白盒</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-show="type==1" label="模型文件" prop='fileList'>
        <el-upload
          class="upload-demo"
          action="http://127.0.0.1:8000/upload_test/"
          :on-change="handleChange"
          multiple
          :limit="1"
          :on-exceed="handleExceed"
          :before-remove="beforeRemove"
          :file-list="form.fileList">
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">上传材料...</div>
        </el-upload>
      </el-form-item>
      <el-form-item v-show="type==0" label="API" prop='api'>
        <el-input v-model="form.api"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交裁决</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { request } from '@/api/judge'
export default {
  data(){
    const validatefileList = (rule, value, callback) => {
      if(value == '' && this.type == 1){
        callback(new Error('上传文件'))
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
      type:0,
      form:{
        hash: '',
        api: '',
        fileList: []
      },
      formRules: {
        hash: [{required: true, message:'请输入注册记录哈希值',trigger:'blur'}],
        api: [{required: true, validator:validateAPI, trigger:'blur'}],
        fileList: [{required: true, validator:validatefileList, trigger:'blur'}],
      }
    }
  },
  methods:{
    onSubmit(){
      this.$refs.form.validate(valid => {
        if(valid){
          console.log('good')
          // request(this.$refs.black_data)
        }else{
          console.log('bad')
          return false
        }
      })
    },
    handleChange(file, fileList) {
      this.form.fileList = fileList.slice(-3)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    }
  }
}
</script>

<style>
</style>
