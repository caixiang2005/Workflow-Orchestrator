import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {                     // 匹配前端请求中以 /api 开头的路径
        target: 'http://localhost:8000',   // 后端服务器地址
        changeOrigin: true,        // 修改请求头中的 origin 为目标 URL
        // rewrite: (path) => path.replace(/^\/api/, '') // 如果需要去掉 /api 前缀，取消注释
      }
    }
  }
})