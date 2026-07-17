# Kubernetes 风格迷你调度器与容器编排模拟器

本地 Node.js CLI 模拟集群，不调用真实 Kubernetes API。

```bash
node src/cli/mini-k8s.js demo
```

演示包括 Deployment 创建、Service、资源 filter+score 调度、手工扩缩、失败滚动发布自动回滚、健康探针、HPA 与事件时间线。设置 `MINI_K8S_STATE=/绝对路径/state.json` 可启用文件式状态存储；未设置时为内存模式。
