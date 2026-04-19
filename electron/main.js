const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;

function getPythonPath(){
  const packedBinPath = path.join(process.resourcesPath, 'bin', 'wifi.exe');
  if (fs.existsSync(packedBinPath)) {
    return packedBinPath;
  }

  const devBinPath = path.join(__dirname, 'bin', 'wifi.exe');
  if (fs.existsSync(devBinPath)) {
    return devBinPath;
  }

  const venvPath = path.join(__dirname, '..', 'src', 'desktop', 'venv', 'Scripts','python.exe')
  if (fs.existsSync(venvPath)) {
    return venvPath;
  }

  return 'python';
}

function isExeMode(pythonExe) {
  return pythonExe.endsWith('.exe') && !pythonExe.includes('python.exe');
}

function executePython(scriptPath, args, workingDir) {
  return new Promise((resolve, reject) => {
    const pythonExe = getPythonPath();
    let spawnArgs;
    let cwd;

    if (isExeMode(pythonExe)) {
      spawnArgs = args;
      cwd = path.dirname(pythonExe);
    } else {
      spawnArgs = [scriptPath, ...args];
      cwd = workingDir || path.dirname(scriptPath);
    }

    const pythonProcess = spawn(pythonExe, spawnArgs, {
      encoding: 'utf-8',
      shell: false,
      cwd: cwd,
      windowsHide: true
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('[Python Error]', data.toString());
    });

    pythonProcess.on('close', (code) => {
      console.log('[Python stdout]', stdout);
      if (code !== 0) {
        console.error('[Python stderr]', stderr);
        reject(new Error(`Python进程退出码: ${code}`));
      } else {
        try {
          const lines = stdout.trim().split('\n');
          const jsonLine = lines[lines.length - 1];
          const result = jsonLine ? JSON.parse(jsonLine) : {};
          resolve(result);
        } catch (e) {
          reject(new Error('解析Python输出失败: ' + stdout));
        }
      }
    });

    pythonProcess.on('error', (err) => {
      reject(err);
    });
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    title: "Workflow Launcher",
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webviewTag: true
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'public/offline.html'));
  mainWindow.setMenu(null);

  mainWindow.webContents.on('did-attach-webview', (event, webContents) => {
    webContents.setWindowOpenHandler(({ url }) => {
      mainWindow.webContents.send('open-new-tab', url);
      return { action: 'deny' };
    });

    webContents.on('will-navigate', (event, url) => {
      if (url.startsWith('http://') || url.startsWith('https://')) {
        event.preventDefault();
        mainWindow.webContents.send('open-new-tab', url);
      }
    });
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

const wifiScriptPath = path.join(__dirname, '..', 'src', 'desktop', 'wifi.py');
const wifiScriptDir = path.dirname(wifiScriptPath);

ipcMain.handle('wifi:scan', async () => {
  try {
    const result = await executePython(wifiScriptPath, ['scan'], wifiScriptDir);
    return result;
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('wifi:connect', async (event, ssid, password) => {
  try {
    const result = await executePython(wifiScriptPath, ['connect', ssid, password], wifiScriptDir);
    return result;
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('wifi:status', async () => {
  try {
    const result = await executePython(wifiScriptPath, ['status'], wifiScriptDir);
    return result;
  } catch (err) {
    return { success: false, error: err.message };
  }
});
