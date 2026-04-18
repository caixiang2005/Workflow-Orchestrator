const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function getPythonPath() {
  const venvPath = path.join(__dirname, '..', 'src', 'desktop', 'venv', 'Scripts', 'python.exe');
  const fs = require('fs');
  if (fs.existsSync(venvPath)) {
    return venvPath;
  }
  return process.platform === 'win32' ? 'python' : 'python3';
}

function executePython(scriptPath, args, workingDir) {
  return new Promise((resolve, reject) => {
    const pythonExe = getPythonPath();
    const spawnArgs = args.map(arg => String(arg));
    
    const pythonProcess = spawn(pythonExe, [scriptPath, ...spawnArgs], {
      encoding: 'utf-8',
      shell: false,
      cwd: workingDir || path.dirname(scriptPath),
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
      console.log('[Python stderr]', stderr);
      if (code !== 0 && !stdout) {
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
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    title: "Workflow Launcher",
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'public/offline.html'));
  mainWindow.setMenu(null);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
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