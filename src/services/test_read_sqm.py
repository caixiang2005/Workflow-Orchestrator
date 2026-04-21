auth_file = r'C:/Users\ASUS\Desktop\Workflow-Orchestrator\data\sqm.txt'
with open(auth_file, 'r', encoding='utf-8') as f:
    PASSWORD = f.read().strip()
print(PASSWORD)