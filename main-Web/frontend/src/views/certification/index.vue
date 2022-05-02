<template>
  <div class="app-container">
    <el-form ref="form" :model="form":rules="formRules" label-width="80px">
      <el-form-item label="模型名称">
        <el-input v-model="form.model_name"></el-input>
      </el-form-item>
      <el-form-item label="模型类型">
        <el-select v-model="form.watermark_type" placeholder="请选择模型类型">
          <el-option label="分类模型" value="classification"></el-option>
          <el-option label="回归模型" value="regression"></el-option>
          <el-option label="生成模型" value="generate"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="水印类型">
        <el-select v-model="form.model_type" placeholder="请选择水印类型">
          <el-option label="Alg1" value="classification"></el-option>
          <el-option label="Alg2" value="regression"></el-option>
          <el-option label="Alg3" value="generate"></el-option>
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
      if(value.length == 0){
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
      form: {
        model_name: '',
        watermark_type:'',
        model_type:''
      },
      formRules:{
        model_name:[{required: true, message:'请输入模型名字',trigger:'blur'},
                    {validator:validateName, trigger:'blur'}],
        watermark_type:[{required: false, message:'请选择水印类型',trigger:'blur'},
                        {validator:validateWater, trigger:'blur'}],
        model_type:[{required: false, message:'请选择模型类型',trigger:'blur'},
                    {validator:validateModel, trigger:'blur'}]
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('try submit')
      console.log(this.form.model_name)
      console.log(this.form.model_type)
      console.log(this.form.watermark_type)
      this.$refs.form.validate(valid => {
        if(valid){
          console.log("sumit!")
          certification_apply(this.form).then(response => {
            console.log("get response")
            console.log(response)
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
