import http from 'node:http'; import { 创建LIS } from './app.js';
const lis = 创建LIS();
const 返回 = (res, code, body) => { res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' }); res.end(JSON.stringify(body)); };
http.createServer(async (req, res) => { try { if (req.method === 'GET' && req.url === '/健康') return 返回(res, 200, { 状态: '正常', 系统: '多医院互联LIS精简版' }); if (req.method === 'GET' && req.url === '/数据概览') return 返回(res, 200, lis.数据库); 返回(res, 404, { 错误: '接口不存在' }); } catch (e) { 返回(res, 400, { 错误: e.message }); } }).listen(3000, () => console.log('LIS服务已启动：http://localhost:3000'));
