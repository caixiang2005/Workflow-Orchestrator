import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import apiClient from '../api/client';
import Input from '../components/Input';

export default function RegisterPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [email, setEmail] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // 新增状态：演示输入框的值
  const [demoValue, setDemoValue] = useState('');

  useEffect(() => {
    if (!token) {
      setError('注册链接无效：缺少 token');
      setLoading(false);
      return;
    }

    apiClient.get('/auth/register', { params: { token } })
      .then((response) => {
        setEmail(response.data.email);
        setLoading(false);
      })
      .catch((err) => {
        const msg = err.response?.data?.detail || '请求失败，请稍后重试';
        setError(msg);
        setLoading(false);
      });
  }, [token]);

  if (loading) return <div className="p-4">加载中，请稍后...</div>;
  if (error) return <div className="p-4 text-red-500">错误：{error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">注册账号</h1>
      <p>邮箱：{email}</p>

      {/* 正确使用 Input 组件，没有 style 属性 */}
      <Input
        label="演示输入框"
        value={demoValue}
        onChange={(e) => setDemoValue(e.target.value)}
        placeholder="输入一些文字..."
      />
    </div>
  );
}