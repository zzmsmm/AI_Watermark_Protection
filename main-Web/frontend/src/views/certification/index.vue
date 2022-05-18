<template>
  <div class="app-container">
    <div style="margin: 20px;"></div>
    <el-form ref="form" :model="form" :rules="formRules" label-width="80px">
      <el-form-item label="模型名称" prop="model_name" style="width: 50%;">
        <el-input v-model="form.model_name" autocomplete="off" placeholder="请输入模型名称"></el-input>
      </el-form-item>
      <el-form-item label="模型类型" prop="model_type">
        <el-select v-model="form.model_type" placeholder="请选择模型类型">
          <el-option label="NLP" value="NLP"></el-option>
          <el-option label="图像分类" value="图像分类"></el-option>
          <el-option label="目标检测" value="目标检测"></el-option>
          <el-option label="人脸识别" value="人脸识别"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="水印类型" prop="watermark_type">
        <el-select v-model="form.watermark_type" placeholder="请选择水印类型">
          <el-option label="黑盒水印" value="黑盒" :disabled="black_disabled"></el-option>
          <el-option label="白盒水印" value="白盒" :disabled="white_disabled"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即申请</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { certification_apply } from '@/api/certification'
export default {
  data() {
    const validateName = (rule, value, callback) => {
      if(value == ''){
        callback(new Error('模型名字不能为空'))
      }else {
        callback()
      }
    }
    const validateWater = (rule, value, callback) => {
      if(value.length == 0){
        console.log("suuusd")
        callback(new Error('请选择水印类型'))
      }else {
        console.log('ggine')
        callback()
      }
    }
    const validateModel = (rule, value, callback) => {
      if(value.length == 0){
        callback(new Error('请选择模型类型'))
      }else {
        callback()
      }
    }
    return {
      black_disabled: false,
      white_disabled: false,
      form: {
        model_name:null,
        watermark_type:null,
        model_type:null,
        token:this.$store.getters.token,
      },
      formRules: {
        model_name:[{required: true, message:'请输入模型名称',trigger:'blur'}],
        model_type:[{required: true, message:'请选择模型类型',trigger:'blur'}],
        watermark_type:[{required: true, message:'请选择水印类型',trigger:'blur'}]
      }
    }
  },
  watch: {
   'form.model_type': function () {
      this.form.watermark_type = null;
      if(this.form.model_type === '目标检测') {
        this.black_disabled = true;
      }
      else if(this.form.model_type === '人脸识别') {
        this.black_disabled = true;
        this.white_disabled = true;
      }
      else {
        this.black_disabled = false;
        this.white_disabled = false;
      }
    }
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate(valid => {
        if(valid){
          console.log("sumit!")
          certification_apply(this.form).then(response => {
            this.$message({
              message: '申请创建成功！',
            	type: 'success',
            	showClose: true,
            	duration: 1 * 1000
            });
            this.$router.push({ path:'/certification/detail/'+ response.hash })
          })
        }else{
          console.log("error submit")
          return false
        }
      })
    },
  }
}
</script>

<style>
</style>
