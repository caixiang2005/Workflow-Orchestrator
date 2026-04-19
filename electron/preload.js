const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('wifiAPI', {
  scan: () => ipcRenderer.invoke('wifi:scan'),
  connect: (ssid, password) => ipcRenderer.invoke('wifi:connect', ssid, password),
  getStatus: () => ipcRenderer.invoke('wifi:status')
});

contextBridge.exposeInMainWorld('electronAPI', {
  onOpenNewTab: null,
  onWindowLoaded: null
});

ipcRenderer.on('open-new-tab', (event, url) => {
  if (window.electronAPI && window.electronAPI.onOpenNewTab) {
    window.electronAPI.onOpenNewTab(url);
  }
});

ipcRenderer.on('window-loaded', () => {
  if (window.electronAPI && window.electronAPI.onWindowLoaded) {
    window.electronAPI.onWindowLoaded();
  }
});

window.addEventListener('message', (event) => {
  if (event.data && event.data.type === '__open-link' && event.data.url) {
    ipcRenderer.send('open-new-tab', event.data.url);
  }
});
