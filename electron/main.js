const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    title: "Workflow Launcher",
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // 目前先加载一个简单的页面，后面再改成 offline.html
  mainWindow.loadFile(path.join(__dirname, 'public/offline.html'));
  
  // 如果 public/offline.html 还没创建，会先显示空白，我们后面再补
  mainWindow.setMenu(null);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});