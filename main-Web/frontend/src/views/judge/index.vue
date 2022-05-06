<template>
  <div class="app-container">
    <el-radio-group v-model="type" size="small">
      <el-radio-button label=0 value=0>黑盒</el-radio-button>
      <el-radio-button label=1 value=1>白盒</el-radio-button>
    </el-radio-group>
    <div style="margin: 20px;"></div>
    <el-form ref="form":model="form":rules="formRules" label-width="120px">
      <el-form-item label="模型hash" prop="hash">
        <el-input v-model="all_hash" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item v-show="type==0" label="模型文件" prop='white'>
        <el-upload
          class="upload-demo"
          action="https://jsonplaceholder.typicode.com/posts/">
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
        </el-upload>
      </el-form-item>

      <el-form-item v-show="type==1" label="模型说明" prop='black'>
        <el-input type="textarea" v-model="form.black_data.file"></el-input>
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
    const validateWhite = (rule, value, callback) => {
      if(value == '' && type==0){
        callback(new Error('上传文件'))
      }else{
        callback()
      }
    }
    const validateBlack = (rule, value, callback) => {
      if(value == '' && type==1){
        callback(new Error('输入说明'))
      }else{
        callback()
      }
    }
    return {
      type:0,
      all_hash:'',
      form:{
        white_data:{
          hash:this.$refs.all_hash,
          file:''
        },
        black_data:{
          hash:this.$refs.all_hash,
          file:''
        }
      },
      formRules: {
        hash:[{required: true, message:'请输入模型哈希',trigger:'blur'}],
        black:[{required: true, message:'requeire black', trigger: 'blur'}, 
               {validator:validateBlack, messaage:'black!', trigger:'blur'}],
        white:[{required: true, message:'requeire black', trigger: 'blur'}, 
               {validator:validateWhite, message:'red', trigger:'blur'}]
      }
    }
  },
  methods:{
    onSubmit(){
      console.log("a:", this.type)
      console.log("b:",this.all_hash)
      console.log("c:",this.form.white_data)
      this.$refs.form.validate(valid => {
        if(valid){
          console.log('good')
          request(this.$refs.black_data)
        }else{
          console.log('bad')
          return false
        }
      })
    }
  }
}
</script>

<style>
</style>
