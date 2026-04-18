// 安全暴露API
// 为了安全，Electron 提供了 contextBridge 和 ipcRenderer 模块来在主进程和渲染进程之间进行通信。通过 contextBridge，我们可以安全地暴露特定的 API 给渲染进程，而不会暴露整个 Node.js 环境，从而减少安全风险。
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('wifiAPI', {
  scan: () => ipcRenderer.invoke('wifi:scan'),
  connect: (ssid, password) => ipcRenderer.invoke('wifi:connect', ssid, password),
  getStatus: () => ipcRenderer.invoke('wifi:status')
});